from abc import ABC, abstractmethod
from typing import Annotated, List, Literal, Optional, Tuple

from pydantic import Field, validate_call

from .slider_lenght import calculate_slider_length

XLimit = Annotated[int, Field(ge=0, le=512)]
YLimit = Annotated[int, Field(ge=0, le=384)]


class BaseHitObject(ABC):
    @validate_call
    def __init__(
        self,
        x: XLimit,
        y: YLimit,
        time: int,
        new_combo: bool = False,
        combo_skip: Annotated[int, Field(ge=0, le=8)] = 0,
        hit_sound: int = 0,
    ):
        self.x = int(x)
        self.y = int(y)
        self.time = int(time)
        self.new_combo = new_combo
        self.combo_skip = combo_skip
        self.hit_sound = hit_sound

    def _get_type_bitmask(self, base_type_flag: int) -> int:
        """
        1 = Circle, 2 = Slider, 8 = Spinner, 4 = New Combo
        """
        bitmask = base_type_flag
        if self.new_combo:
            bitmask |= 4
        if self.combo_skip > 0:
            bitmask |= (self.combo_skip & 7) << 4
        return bitmask

    @abstractmethod
    def to_osu_string(self) -> str:
        """Převede objekt do odpovídajícího řádku pro sekci [HitObjects]."""
        pass


class HitCircle(BaseHitObject):
    def to_osu_string(self) -> str:
        type_val = self._get_type_bitmask(1)
        return f"{self.x},{self.y},{self.time},{type_val},{self.hit_sound},0:0:0:0:"


class Slider(BaseHitObject):
    @validate_call
    def __init__(
        self,
        x: XLimit,
        y: YLimit,
        time: int,
        curve_type: str,  # 'L', 'B', 'P', 'C'
        points: List[Tuple[XLimit, YLimit]],
        repeats: int = 1,
        length: float | None = None,
        **kwargs,
    ):
        super().__init__(x, y, time, **kwargs)
        self.curve_type = curve_type.upper()
        self.points = points
        self.repeats = repeats
        if length is None:
            _length = calculate_slider_length(self.curve_type, (x, y), points)
        else:
            _length = length
        self.length = _length * repeats

    def to_osu_string(self) -> str:
        type_val = self._get_type_bitmask(2)
        points_str = "|".join(f"{p[0]}:{p[1]}" for p in self.points)
        curve_str = f"{self.curve_type}|{points_str}"
        return f"{self.x},{self.y},{self.time},{type_val},{self.hit_sound},{curve_str},{self.repeats},{self.length:.2f}"


class Spinner(BaseHitObject):
    @validate_call
    def __init__(
        self,
        time: int,
        spin_time: int,
        x: XLimit = 256,
        y: YLimit = 192,
        **kwargs,
    ):
        super().__init__(x, y, time, **kwargs)
        self.end_time = int(time + spin_time)

    def to_osu_string(self) -> str:
        type_val = self._get_type_bitmask(8)
        return f"{self.x},{self.y},{self.time},{type_val},{self.hit_sound},{self.end_time},0:0:0:0:"
