import random
import string

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
    assert diff.beatmap_content == DIFF_TEST_FORMAT
