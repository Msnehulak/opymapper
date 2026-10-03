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
diff.audio = "/home/snehulak/Music/audio.ogg"


for i in range(0, 10000, 100):
    diff.add_circle(x=0, y=0, time=1000 + i, new_combo=True)
    diff.add_circle(x=512, y=384, time=1050 + i, new_combo=True)

mapset = opymapper.new_mapset()

mapset.append_diff(diff)

mapset.save_all("./test_ma/")
