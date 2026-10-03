from typing import List

from . import share_property as ShareP
from .diff_create import CreateDiff

NEED_DIFF_CONTENT = {
    "General": [""],
    "Metadata": ["Title", "TitleUnicode", "Artist", "ArtistUnicode"],
    "Difficulty": ["HPDrainRate", "CircleSize", "OverallDifficulty", "ApproachRate"],
}


class CreateMap:
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
        self.diffs: List[CreateDiff] = []

    def append_diff(self, diff: CreateDiff) -> None:
        if not isinstance(diff, CreateDiff):
            raise TypeError("Appedet objects must be create by CreateDiff.")

        self.diffs.append(diff)

    def save_all(self, output_dir: str) -> None:
        for diff in self.diffs:
            self.validate_diff(diff)
            content = diff.get_beatmap_content()

    def validate_diff(
        self, diff: CreateDiff, _ignore_mising_trait: bool = False
    ) -> None:
        for category, keys in NEED_DIFF_CONTENT.items():
            if category not in diff.beatmap:
                diff.beatmap[category] = {}

            for key in keys:
                if not key:
                    continue

                if (
                    key not in diff.beatmap[category]
                    or diff.beatmap[category][key] is None
                ):
                    fallback_value = self.beatmap.get(category, {}).get(key)

                    if fallback_value is not None or _ignore_mising_trait:
                        diff.beatmap[category][key] = fallback_value
                    else:
                        raise ValueError(
                            f"Missing required metadata '{key}' in category '{category}'"
                        )
