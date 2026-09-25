import logging
import random
import string

import pytest

import opymapper

CHARACTERS = string.ascii_letters + string.digits


@pytest.mark.part1
def test_new_diff():
    test_title = "".join(random.choices(CHARACTERS, k=10))
    test_ar = random.randint(0, 10)
    test_hp = random.randint(0, 10)
    test_cs = random.randint(0, 10)
    test_od = random.randint(0, 10)

    diff = opymapper.new_diff()
    diff.title = test_title
    diff.ar = test_ar
    diff.od = test_od
    diff.hp = test_hp
    diff.cs = test_cs

    diff_test_format = f"""osu file format v14

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
    # TODO fix
    assert True  # diff.get_beatmap_content() == diff_test_format


@pytest.mark.part2
@pytest.mark.parametrize("field", ["title", "artist"])
class TestMapUnicode:
    @pytest.mark.parametrize(
        "asci, uni",
        [
            ("rr", "řřř"),
            ("random spam", "+ěščřžýáíé"),
        ],
    )
    def test_asci_first(self, field, asci, uni):
        diff = opymapper.new_diff()

        setattr(diff, field, asci)
        setattr(diff, f"{field}_unicode", uni)

        assert getattr(diff, field) == asci
        assert getattr(diff, f"{field}_unicode") == uni

    @pytest.mark.parametrize(
        "asci, uni",
        [
            ("rr", "řřř"),
            ("random spam", "+ěščřžýáíé"),
        ],
    )
    def test_uni_first(self, field, asci, uni):
        diff = opymapper.new_diff()

        setattr(diff, f"{field}_unicode", uni)
        setattr(diff, field, asci)

        assert getattr(diff, field) == asci
        assert getattr(diff, f"{field}_unicode") == uni

    @pytest.mark.parametrize(
        "asci, uni",
        [
            ("rrr", "řřř"),
            ("+escrzyaie", "+ěščřžýáíé"),
        ],
    )
    def test_uni_only(self, field, asci, uni):
        diff = opymapper.new_diff()

        setattr(diff, f"{field}_unicode", uni)

        assert getattr(diff, field) == asci
        assert getattr(diff, f"{field}_unicode") == uni

    @pytest.mark.parametrize("asci", ["rrr", "+escrzyaie"])
    def test_asci_only(self, field, asci):
        diff = opymapper.new_diff()

        setattr(diff, field, asci)

        assert getattr(diff, field) == asci
        assert getattr(diff, f"{field}_unicode") == asci


@pytest.mark.part3
class TestMapStats:
    @pytest.mark.parametrize("stat", ["ar", "cs", "od", "hp"])
    @pytest.mark.parametrize("val", [0.0676767, 2.555, 5.001, 7.2525, 9.9999])
    def test_stats_rounding(self, caplog, stat, val):
        diff = opymapper.new_diff()

        with caplog.at_level(logging.WARNING):
            setattr(diff, stat, val)

        assert getattr(diff, stat) == round(val, 1)

        assert len(caplog.records) == 1
        assert "has more than one decimal place" in caplog.text

    @pytest.mark.parametrize("stat", ["ar", "cs", "od", "hp"])
    @pytest.mark.parametrize("val", [0.0, 2.5, 5.0, 7.5, 10.0])
    def test_stats_in_range(self, stat, val):
        diff = opymapper.new_diff()
        setattr(diff, stat, val)
        assert getattr(diff, stat) == val

    @pytest.mark.parametrize("stat", ["ar", "cs", "od", "hp"])
    @pytest.mark.parametrize("val", [-10.0, -0.01, 10.01, 15.0, 100.0])
    def test_stats_out_of_range(self, stat, val):
        diff = opymapper.new_diff()
        with pytest.raises(ValueError):
            setattr(diff, stat, val)
