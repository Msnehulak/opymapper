import logging

import pytest

import opymapper


def test():
    mapset = opymapper.new_mapset()
    diff = opymapper.new_diff()
    diff.title = "Song Title"
    diff.ar = 9.0

    mapset.append_diff(diff)


def test_alternative_class():
    mapset = opymapper.new_mapset()

    class OtherClass:
        pass

    other_class = OtherClass()
    with pytest.raises(TypeError):
        mapset.append_diff(other_class)


@pytest.mark.parametrize(
    "stat",
    [
        {"key": "ar", "val": 10.0},
        {"key": "hp", "val": 5.0},
        {"key": "title", "val": "Pepa"},
        {"key": "artist", "val": "Adam"},
    ],
)
def test_corect_diff_validate(stat):
    mapset = opymapper.new_mapset()
    diff = opymapper.new_diff()

    setattr(mapset, stat["key"], stat["val"])
    mapset.validate_diff(diff, _ignore_mising_trait=True)

    assert getattr(diff, stat["key"]) == stat["val"]
