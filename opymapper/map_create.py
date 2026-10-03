import os
import shutil
from pathlib import Path
from typing import List

import fsspec

from . import share_property as ShareP
from .diff_create import CreateDiff

NEED_DIFF_CONTENT = {
    "General": [""],
    "Metadata": ["Title", "TitleUnicode", "Artist", "ArtistUnicode"],
    "Difficulty": ["HPDrainRate", "CircleSize", "OverallDifficulty", "ApproachRate"],
}


def memory_to_disk(fs, src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    for path in fs.find(src_dir):
        rel = os.path.relpath(path, src_dir)
        target = os.path.join(dst_dir, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with fs.open(path, "rb") as fsrc, open(target, "wb") as fdst:
            fdst.write(fsrc.read())


class CreateMap:
    ar = ShareP.StatProperty("Difficulty", "ApproachRate")
    cs = ShareP.StatProperty("Difficulty", "CircleSize")
    hp = ShareP.StatProperty("Difficulty", "HPDrainRate")
    od = ShareP.StatProperty("Difficulty", "OverallDifficulty")

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
        self.diffs: List[CreateDiff] = []
        self.files = []

        self.set_defoult_values()

    def append_diff(self, diff: CreateDiff) -> None:
        if not isinstance(diff, CreateDiff):
            raise TypeError("Appedet objects must be create by CreateDiff.")

        self.diffs.append(diff)

    def save_all(self, output_dir: str) -> None:
        fs = fsspec.filesystem("memory")

        for diff in self.diffs:
            self.validate_diff(diff)
            diff_content = diff.get_beatmap_content().replace("\n", "\r\n")
            diff_name = f"{diff.title} - {diff.artist} (akjsh) [shhsj].osu"
            with fs.open(f"/osu_map/{diff_name}", "w") as f:
                f.write(diff_content)

            for ex_file in diff.files:
                fs.put(str(ex_file["path"]), f"/osu_map/{ex_file['name']}")

        for ex_file in self.files:
            fs.put(str(ex_file["path"]), f"/osu_map/{ex_file['name']}")

        output_path = Path(output_dir).resolve()
        if output_path.exists():
            shutil.rmtree(output_path)
        output_path.mkdir(parents=True)

        memory_to_disk(fs, "/osu_map", output_path)

        shutil.make_archive(str(output_path), "zip", output_path)
        os.replace(f"{output_path}.zip", f"{output_path}.osz")

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

                    if fallback_value is not None:
                        diff.beatmap[category][key] = fallback_value
                    elif _ignore_mising_trait:
                        pass
                    else:
                        raise ValueError(
                            f"Missing required metadata '{key}' in category '{category}'"
                        )

    def set_defoult_values(self):
        self.ar = 5
        self.hp = 5
        self.od = 5
        self.cs = 5

        self.title = "Auto create map"
        self.artist = "opymapper"
