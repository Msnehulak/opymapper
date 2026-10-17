import logging
import random
import string

import pytest

import opymapper

CHARACTERS = string.ascii_letters + string.digits


@pytest.mark.part1
@pytest.mark.parametrize("metadata", ["source", "version", "creator"])
@pytest.mark.parametrize("value", ["my fav version", "2077 music", "Sortax"])
def test_meta_data(metadata, value):
    diff = opymapper.new_diff()

    setattr(diff, metadata, value)

    assert getattr(diff, metadata) == value


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


@pytest.mark.part4
@pytest.mark.parametrize("combo_num", range(1, 9))
class TestMapColors:
    @pytest.mark.parametrize(
        "colors",
        [(22, 70, 165), (19, 253, 248), (131, 51, 163), (223, 9, 97), (204, 60, 236)],
    )
    def test_combo_color_rgb(self, colors, combo_num):
        diff = opymapper.new_diff()
        attr_name = f"color_combo_{combo_num}"
        setattr(diff, attr_name, colors)
        assert getattr(diff, attr_name) == colors

    @pytest.mark.parametrize(
        "colors",
        [
            (473, 348, -44),
            (489, 487, 465),
            (-69, -42, 495),
            (-107, -184, 382),
            (453, -206, 279),
        ],
    )
    def test_combo_color_rgb_out_of_range(self, colors, combo_num):
        diff = opymapper.new_diff()
        with pytest.raises(ValueError):
            setattr(diff, f"color_combo_{combo_num}", colors)

    @pytest.mark.parametrize(
        "hex_code, expected_rgb",
        [
            ("#1646A5", (22, 70, 165)),
            ("13FDF8", (19, 253, 248)),
            ("#8333A3", (131, 51, 163)),
            ("DF0961", (223, 9, 97)),
            ("#CC3CEC", (204, 60, 236)),
        ],
    )
    def test_combo_color_hex(self, combo_num, hex_code, expected_rgb):
        diff = opymapper.new_diff()
        attr_name = f"color_combo_{combo_num}"
        setattr(diff, attr_name, hex_code)
        assert getattr(diff, attr_name) == expected_rgb

    @pytest.mark.parametrize(
        "invalid_hex",
        [
            "#FFF",
            "12345",
            "1234567",
            "#GGGGGG",
            "12345Z",
            "",
        ],
    )
    def test_combo_color_hex_out_of_range(self, combo_num, invalid_hex):
        diff = opymapper.new_diff()
        with pytest.raises(ValueError):
            setattr(diff, f"color_combo_{combo_num}", invalid_hex)
