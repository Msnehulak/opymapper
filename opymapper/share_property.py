import logging
import unicodedata
from pathlib import Path


class FileProperty:
    def __init__(self, category: str, key: str):
        self.category = category
        self.key = key

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.beatmap[self.category].get(self.key)

    def __set__(self, instance, value: str):
        file = Path(value).resolve()
        file_name = file.name

        instance.files.append(
            {
                "name": file_name,
                "path": file,
            }
        )

        instance.beatmap[self.category][self.key] = file_name


class TextProperty:
    def __init__(self, category: str, key: str):
        self.category = category
        self.key = key

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.beatmap[self.category].get(self.key)

    def __set__(self, instance, value: str):
        instance.beatmap[self.category][self.key] = value


class NumberProperty:
    def __init__(
        self,
        category: str,
        key: str,
        max: float = 10.0,
        min: float = 10.0,
        round_to: int = 1,
    ):
        self.category = category
        self.key = key
        self.max = max
        self.min = min
        self.round_to = round_to

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.beatmap[self.category].get(self.key)

    def __set__(self, instance, value: float):
        if not (self.min <= value <= self.max):
            raise ValueError(
                f"{self.key} must be between {self.min} and {self.max}, got {value}"
            )

        if round(value, self.round_to) != value:
            logging.warning(
                f"[{self.category}:{self.key}] {value} has more than {self.round_to} decimal place(s), rounded to {round(value, self.round_to)}"
            )
        instance.beatmap[self.category][self.key] = round(value, self.round_to)


class ColorProperty:
    def __init__(self, category: str, key: str):
        self.category = category
        self.key = key

    def __get__(self, instance, owner):
        if instance is None:
            return self

        raw_val = instance.beatmap[self.category].get(self.key)
        if raw_val is None:
            return None

        r, g, b = map(int, raw_val.split(","))
        return (r, g, b)

    def __set__(self, instance, value: tuple[int, int, int] | str):
        rgb = self._parse_color(value)

        instance.beatmap[self.category][self.key] = f"{rgb[0]},{rgb[1]},{rgb[2]}"

    @staticmethod
    def _parse_color(value) -> tuple[int, int, int]:
        if isinstance(value, str):
            hex_str = value.lstrip("#")
            if len(hex_str) == 6:
                try:
                    return tuple(int(hex_str[i : i + 2], 16) for i in (0, 2, 4))
                except ValueError:
                    pass
            raise ValueError(f"Invalid HEX color format: '{value}'")

        elif isinstance(value, (tuple, list)) and len(value) == 3:
            if all(isinstance(c, int) and 0 <= c <= 255 for c in value):
                return (int(value[0]), int(value[1]), int(value[2]))

        raise ValueError(
            f"Color must be tuple[int, int, int] with values 0-255 or HEX string, got {value}"
        )


class UnicodeProperty:
    def __init__(self, category: str, key: str, is_ascii_target: bool = True):
        self.category = category
        self.key = key
        self.unicode_key = f"{key}Unicode"
        self.is_ascii_target = is_ascii_target

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
