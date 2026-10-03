import opymapper

diff = opymapper.new_diff()

diff.add_circle(x=256, y=192, time=1000, new_combo=True)

diff.add_slider(
    x=100,
    y=100,
    time=2000,
    curve_type="B",
    points=[(200, 100), (200, 200), (200, 100), (200, 200)],
    repeats=2,
    length=150.0,
)

diff.add_spinner(time=5000, spin_time=8000, new_combo=True)

for i in diff.hit_objects:
    print(i.to_osu_string())
