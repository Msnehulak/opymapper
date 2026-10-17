import os
import shutil
import zipfile
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


class CreateMap:
    _md_help = {"min": 0.0, "max": 10.0, "round_to": 1}
    ar = ShareP.NumberProperty("Difficulty", "ApproachRate", **_md_help)
    cs = ShareP.NumberProperty("Difficulty", "CircleSize", **_md_help)
    hp = ShareP.NumberProperty("Difficulty", "HPDrainRate", **_md_help)
    od = ShareP.NumberProperty("Difficulty", "OverallDifficulty", **_md_help)

    title = ShareP.UnicodeProperty("Metadata", "Title", is_ascii_target=True)
    title_unicode = ShareP.UnicodeProperty("Metadata", "Title", is_ascii_target=False)

    artist = ShareP.UnicodeProperty("Metadata", "Artist", is_ascii_target=True)
    artist_unicode = ShareP.UnicodeProperty("Metadata", "Artist", is_ascii_target=False)

    version = ShareP.TextProperty("Metadata", "Version")
    creator = ShareP.TextProperty("Metadata", "Creator")
    source = ShareP.TextProperty("Metadata", "Source")

    audio = ShareP.FileProperty("General", "AudioFilename")
    stack_leniency = ShareP.NumberProperty(
        "General", "StackLeniency", min=0.0, max=1.0, round_to=2
    )

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

    def save_all(self, file_name: str, save_path: Path = Path.cwd()) -> None:
        fs = fsspec.filesystem("memory")
        external_files = []

        for diff in self.diffs:
            self.validate_diff(diff)
            diff_content = diff.get_beatmap_content().replace("\n", "\r\n")
            diff_name = (
                f"{diff.title} - {diff.artist} ({diff.creator}) [{diff.version}].osu"
            )
            with fs.open(f"/osu_map/{diff_name}", "w") as f:
                f.write(diff_content)

            external_files.extend(diff.files)
        external_files.extend(self.files)

        target_zip = save_path / f"{file_name}.zip"
        target_osz = save_path / f"{file_name}.osz"

        with zipfile.ZipFile(
            target_zip, "w", compression=zipfile.ZIP_STORED
        ) as zip_out:
            # From fsspec
            for path in fs.find(""):
                with fs.open(path, "rb") as f_in:
                    arcname = os.path.basename(path)
                    if arcname:
                        zip_out.writestr(arcname, f_in.read())

            # External Files
            for file in external_files:
                with (
                    zip_out.open(file["name"], "w") as target_file,
                    open(str(file["path"]), "rb") as source_file,
                ):
                    while chunk := source_file.read(1024 * 1024):
                        target_file.write(chunk)

        os.rename(target_zip, target_osz)

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

        self.title = "Auto Created map"
        self.artist = "opymapper"
        self.version = "Auto created"
        self.creator = "Osu Python Maper"
