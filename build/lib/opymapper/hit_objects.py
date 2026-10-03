from abc import ABC, abstractmethod
from typing import List, Literal, Optional, Tuple

from pydantic import Field, validate_call


class BaseHitObject(ABC):
    def __init__(
        self,
        x: int,
        y: int,
        time: int,
        new_combo: bool = False,
        combo_skip: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8] = 0,
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
    def __init__(
        self,
        x: int,
        y: int,
        time: int,
        curve_type: str,  # 'L', 'B', 'P', 'C'
        points: List[Tuple[int, int]],
        repeats: int = 1,
        length: float = 0.0,
        **kwargs,
    ):
        super().__init__(x, y, time, **kwargs)
        self.curve_type = curve_type.upper()
        self.points = points
        self.repeats = repeats
        self.length = length

    def to_osu_string(self) -> str:
        type_val = self._get_type_bitmask(2)
        points_str = "|".join(f"{p[0]}:{p[1]}" for p in self.points)
        curve_str = f"{self.curve_type}|{points_str}"
        return f"{self.x},{self.y},{self.time},{type_val},{self.hit_sound},{curve_str},{self.repeats},{self.length:.2f}"


class Spinner(BaseHitObject):
    def __init__(
        self,
        time: int,
        end_time: int,
        x: int = 256,
        y: int = 192,
        **kwargs,
    ):
        super().__init__(x, y, time, **kwargs)
        self.end_time = int(end_time)

    def to_osu_string(self) -> str:
        type_val = self._get_type_bitmask(8)
        return f"{self.x},{self.y},{self.time},{type_val},{self.hit_sound},{self.end_time},0:0:0:0:"
