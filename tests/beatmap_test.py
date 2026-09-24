import logging
import random
import string

import pytest

import opmaper

CHARACTERS = string.ascii_letters + string.digits


def test_new_diff():
    test_title = "".join(random.choices(CHARACTERS, k=10))
    test_ar = random.randint(0, 10)
    test_hp = random.randint(0, 10)
    test_cs = random.randint(0, 10)
    test_od = random.randint(0, 10)

    diff = opmaper.new_diff()
    diff.title = test_title
    diff.ar = test_ar
    diff.od = test_od
    diff.hp = test_hp
    diff.cs = test_cs

    DIFF_TEST_FORMAT = f"""osu file format v14

[General]

[Metadata]
Title:{test_title}

[Difficulty]
ApproachRate:{test_ar}
OverallDifficulty:{test_od}
HPDrainRate:{test_hp}
CircleSize:{test_cs}

[Colours]

[HitObjects]
"""
    assert diff.get_beatmap_content() == DIFF_TEST_FORMAT


@pytest.mark.parametrize("stat", ["ar", "cs", "od", "hp"])
@pytest.mark.parametrize("val", [0.0676767, 2.555, 5.001, 7.2525, 9.9999])
def test_stats_rounding(caplog, stat, val):
    diff = opmaper.new_diff()

    with caplog.at_level(logging.WARNING):
        setattr(diff, stat, val)

    assert getattr(diff, stat) == round(val, 1)

    assert len(caplog.records) == 1
    assert "is more then one decimal" in caplog.text


@pytest.mark.parametrize("stat", ["ar", "cs", "od", "hp"])
@pytest.mark.parametrize("val", [0.0, 2.5, 5.0, 7.5, 10.0])
def test_stats_in_range(stat, val):
    diff = opmaper.new_diff()
    setattr(diff, stat, val)
    assert getattr(diff, stat) == val


@pytest.mark.parametrize("stat", ["ar", "cs", "od", "hp"])
@pytest.mark.parametrize("val", [-10.0, -0.01, 10.01, 15.0, 100.0])
def test_stats_out_of_range(stat, val):
    diff = opmaper.new_diff()
    with pytest.raises(ValueError):
        setattr(diff, stat, val)
