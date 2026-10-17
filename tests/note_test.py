import pytest
from pydantic import ValidationError

import opymapper


@pytest.mark.parametrize("time", [100, 50])
@pytest.mark.parametrize("new_combo", [True, False])
class TestNotes:
    @pytest.mark.parametrize("x", [100, 50])
    @pytest.mark.parametrize("y", [100, 50])
    def test_note(self, x, y, time, new_combo):
        diff = opymapper.new_diff()

        diff.add_circle(x=x, y=y, time=time, new_combo=new_combo)

        _test_type = 1 + (4 if new_combo else 0)
        assert (
            diff.hit_objects[-1].to_osu_string()
            == f"""{x},{y},{time},{_test_type},0,0:0:0:0:"""
        )

    @pytest.mark.parametrize("x", [999, -5])
    @pytest.mark.parametrize("y", [999, -5])
    def test_note_out_range(self, x, y, time, new_combo):
        diff = opymapper.new_diff()

        with pytest.raises(ValidationError):
            diff.add_circle(x=x, y=y, time=time, new_combo=new_combo)


@pytest.mark.parametrize("new_combo", [True, False])
class TestSpiner:
    @pytest.mark.parametrize("start_time", [100, 50])
    @pytest.mark.parametrize("spin_time", [100, 50])
    def test_spiner(self, start_time, spin_time, new_combo):
        diff = opymapper.new_diff()

        diff.add_spinner(
            time=start_time,
            spin_time=spin_time,
            new_combo=new_combo,
        )

        _test_type = 8 + (4 if new_combo else 0)
        assert (
            diff.hit_objects[-1].to_osu_string()
            == f"""256,192,{start_time},{_test_type},0,{start_time + spin_time},0:0:0:0:"""
        )


@pytest.mark.parametrize("new_combo", [True])
class TestSlider:
    def test_slider_length(self, new_combo):
        diff = opymapper.new_diff()

        diff.add_slider(
            x=56,
            y=32,
            time=6500,
            curve_type="L",
            points=[
                (76, 192),
                (56, 352, "P"),
                (256, 272),
                (456, 352, "B"),
                (356, 192),
                (456, 12),
            ],
        )

        assert (
            diff.hit_objects[0].to_osu_string()
            == "56,32,6500,2,0,L|76:192|P|56:352|256:272|B|456:352|356:192|456:12,1,1123"
        )
