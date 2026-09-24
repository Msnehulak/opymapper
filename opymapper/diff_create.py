import logging

ADD_TO_BEAT_MAP = ["General", "Metadata", "Difficulty", "Colours", "HitObjects"]


class CreateDiff:
    def __init__(self) -> None:
        self.beatmap = {
            "format": 14,
            "General": {},
            "Metadata": {},
            "Difficulty": {},
            "Colours": {},
            "HitObjects": {},
        }

    def get_beatmap_content(self) -> str:
        content = []
        content.append("osu file format v14")
        content.append("")

        for category, data in self.beatmap.items():
            if category in ADD_TO_BEAT_MAP:
                content.append(f"[{category}]")
                for key, value in data.items():
                    content.append(f"{key}:{value}")
                content.append("")

        return "\n".join(content)


PROPERTIES_MAP_STATS = {
    "hp": ("Difficulty", "HPDrainRate"),
    "cs": ("Difficulty", "CircleSize"),
    "od": ("Difficulty", "OverallDifficulty"),
    "ar": ("Difficulty", "ApproachRate"),
}

PROPERTIES_MAP = {
    "title": ("Metadata", "Title"),
}


def _make_property_stats(category: str, key: str):
    def getter(self):
        return self.beatmap[category].get(key)

    def setter(self, value: float):
        if 0.0 <= value <= 10.0:
            if round(value, 1) != value:
                logging.warning(
                    f"{value} has more than one decimal place, rounded to {round(value, 1)}"
                )
            self.beatmap[category][key] = round(value, 1)
        else:
            raise ValueError(f"{key} can only be between 0.0-10 {value}")

    return property(getter, setter)


def _make_property(category: str, key: str):
    def getter(self):
        return self.beatmap[category].get(key)

    def setter(self, value):
        self.beatmap[category][key] = value

    return property(getter, setter)


for prop_name, (category, key) in PROPERTIES_MAP.items():
    setattr(CreateDiff, prop_name, _make_property(category, key))

for prop_name, (category, key) in PROPERTIES_MAP_STATS.items():
    setattr(CreateDiff, prop_name, _make_property_stats(category, key))
