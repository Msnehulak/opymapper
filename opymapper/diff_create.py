import logging
from typing import List

from . import share_property as ShareP
from .hit_objects import BaseHitObject, HitCircle, Slider, Spinner

ADD_TO_BEAT_MAP = ["General", "Metadata", "Difficulty", "Colours", "HitObjects"]


class CreateDiff:
    ar = ShareP.StatProperty("Difficulty", "ApproachRate")
    cs = ShareP.StatProperty("Difficulty", "CircleSize")
    hp = ShareP.StatProperty("Difficulty", "HPDrainRate")
    od = ShareP.StatProperty("Difficulty", "OverallDifficulty")

    color_combo_1 = ShareP.ColorProperty("Colours", "Combo1")
    color_combo_2 = ShareP.ColorProperty("Colours", "Combo2")
    color_combo_3 = ShareP.ColorProperty("Colours", "Combo3")
    color_combo_4 = ShareP.ColorProperty("Colours", "Combo4")
    color_combo_5 = ShareP.ColorProperty("Colours", "Combo5")
    color_combo_6 = ShareP.ColorProperty("Colours", "Combo6")
    color_combo_7 = ShareP.ColorProperty("Colours", "Combo7")
    color_combo_8 = ShareP.ColorProperty("Colours", "Combo8")

    title = ShareP.UnicodeProperty("Metadata", "Title", is_ascii_target=True)
    title_unicode = ShareP.UnicodeProperty("Metadata", "Title", is_ascii_target=False)

    artist = ShareP.UnicodeProperty("Metadata", "Artist", is_ascii_target=True)
    artist_unicode = ShareP.UnicodeProperty("Metadata", "Artist", is_ascii_target=False)

    audio = ShareP.FileProperty("General", "AudioFilename")

    def __init__(self) -> None:
        self.beatmap = {
            "format": 14,
            "General": {},
            "Metadata": {},
            "Difficulty": {},
            "Colours": {},
            "HitObjects": {},
        }
        self.temp = {}
        self.hit_objects: List[BaseHitObject] = []
        self.files = []

    def add_hit_object(self, obj: BaseHitObject) -> BaseHitObject:
        if not isinstance(obj, BaseHitObject):
            raise TypeError("Object must inherit from BaseHitObject.")
        self.hit_objects.append(obj)
        return obj

    # Factory metody pro rychlý zápis (Fluent API)
    def add_circle(self, x: int, y: int, time: int, **kwargs) -> HitCircle:
        circle = HitCircle(x, y, time, **kwargs)
        self.hit_objects.append(circle)
        return circle

    def add_slider(
        self, x: int, y: int, time: int, curve_type: str, points: list, **kwargs
    ) -> Slider:
        slider = Slider(x, y, time, curve_type, points, **kwargs)
        self.hit_objects.append(slider)
        return slider

    def add_spinner(self, time: int, spin_time: int, **kwargs) -> Spinner:
        spinner = Spinner(time, spin_time, **kwargs)
        self.hit_objects.append(spinner)
        return spinner

    def get_beatmap_content(self) -> str:
        content = ["osu file format v14", ""]

        for category, data in self.beatmap.items():
            if category in ADD_TO_BEAT_MAP and category != "HitObjects":
                content.append(f"[{category}]")
                for key, value in data.items():
                    content.append(f"{key}:{value}")
                content.append("")

        content.append("[HitObjects]")
        for obj in self.hit_objects:
            content.append(obj.to_osu_string())
        content.append("")

        return "\n".join(content)
