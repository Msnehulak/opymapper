import logging

from . import share_property as ShareP

ADD_TO_BEAT_MAP = ["General", "Metadata", "Difficulty", "Colours", "HitObjects"]


class CreateDiff:
    ar = ShareP.StatProperty("Difficulty", "ApproachRate")
    cs = ShareP.StatProperty("Difficulty", "CircleSize")
    hp = ShareP.StatProperty("Difficulty", "HPDrainRate")
    od = ShareP.StatProperty("Difficulty", "OverallDifficulty")

    title = ShareP.UnicodeProperty("Metadata", "Title", is_ascii_target=True)
    title_unicode = ShareP.UnicodeProperty("Metadata", "Title", is_ascii_target=False)

    artist = ShareP.UnicodeProperty("Metadata", "Artist", is_ascii_target=True)
    artist_unicode = ShareP.UnicodeProperty("Metadata", "Artist", is_ascii_target=False)

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

    def get_beatmap_content(self) -> str:
        content = ["osu file format v14", ""]

        for category, data in self.beatmap.items():
            if category in ADD_TO_BEAT_MAP:
                content.append(f"[{category}]")
                for key, value in data.items():
                    content.append(f"{key}:{value}")
                content.append("")

        return "\n".join(content)
