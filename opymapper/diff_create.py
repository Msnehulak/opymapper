import logging
import unicodedata

ADD_TO_BEAT_MAP = ["General", "Metadata", "Difficulty", "Colours", "HitObjects"]


class StatProperty:
    def __init__(self, category: str, key: str):
        self.category = category
        self.key = key

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.beatmap[self.category].get(self.key)

    def __set__(self, instance, value: float):
        if not (0.0 <= value <= 10.0):
            raise ValueError(f"{self.key} must be between 0.0 and 10.0, got {value}")

        if round(value, 1) != value:
            logging.warning(
                f"{value} has more than one decimal place, rounded to {round(value, 1)}"
            )
        instance.beatmap[self.category][self.key] = round(value, 1)


class UnicodeProperty:
    def __init__(self, category: str, key: str, is_ascii_target: bool = True):
        self.category = category
        self.key = key  # Základní klíč, např. "Title" nebo "Artist"
        self.unicode_key = f"{key}Unicode"  # "TitleUnicode" nebo "ArtistUnicode"
        self.is_ascii_target = (
            is_ascii_target  # True pro title, False pro title_unicode
        )

    def __get__(self, instance, owner):
        if instance is None:
            return self

        target_key = self.key if self.is_ascii_target else self.unicode_key
        return instance.beatmap[self.category].get(target_key)

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError("Value must str.")

        metadata = instance.beatmap[self.category]

        if self.is_ascii_target:
            # PŘÍPAD 1: Zápis přes ASCII vlastnost (např. diff.title = ...)
            if not value.isascii():
                # Pokud uživatel zadá Unicode do ASCII pole, převedeme ho na čisté ASCII
                ascii_val = self._to_ascii(value)
                logging.warning(f"'{value}' is non ASCII convert to '{ascii_val}'.")
                value = ascii_val

            metadata[self.key] = value
            instance.temp[f"{self.key}_defined"] = True

            # Pokud ještě nebyl definován Unicode název, doplníme ho stejnou hodnotou
            if not instance.temp.get(f"{self.unicode_key}_defined"):
                metadata[self.unicode_key] = value

        else:
            # PŘÍPAD 2: Zápis přes Unicode vlastnost (např. diff.title_unicode = ...)
            metadata[self.unicode_key] = value
            instance.temp[f"{self.unicode_key}_defined"] = True

            # Pokud ještě nebyl definován ASCII název, vytvoříme jeho ASCII verzi
            if not instance.temp.get(f"{self.key}_defined"):
                metadata[self.key] = self._to_ascii(value)

    @staticmethod
    def _to_ascii(text: str) -> str:
        normalized = unicodedata.normalize("NFKD", text)
        return normalized.encode("ASCII", "ignore").decode("utf-8")


class CreateDiff:
    ar = StatProperty("Difficulty", "ApproachRate")
    cs = StatProperty("Difficulty", "CircleSize")
    hp = StatProperty("Difficulty", "HPDrainRate")
    od = StatProperty("Difficulty", "OverallDifficulty")

    title = UnicodeProperty("Metadata", "Title", is_ascii_target=True)
    title_unicode = UnicodeProperty("Metadata", "Title", is_ascii_target=False)

    artist = UnicodeProperty("Metadata", "Artist", is_ascii_target=True)
    artist_unicode = UnicodeProperty("Metadata", "Artist", is_ascii_target=False)

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
