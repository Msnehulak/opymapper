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
