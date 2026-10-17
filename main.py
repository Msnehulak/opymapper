import opymapper

diff = opymapper.new_diff()

diff.ar = 9

CX = 512 / 2
CY = 384 / 2

SX = 60
SY = 120

# Star
for i in range(10):
    diff.add_circle(x=int(CX + (SX * 0)), y=int(CY + (SY * -1)), time=i * 1000)
    diff.add_circle(x=int(CX + (SX * -1)), y=int(CY + (SY * 1)), time=200 + i * 1000)
    diff.add_circle(x=int(CX + (SX * 2)), y=int(CY + (SY * 0)), time=400 + i * 1000)
    diff.add_circle(x=int(CX + (SX * -2)), y=int(CY + (SY * 0)), time=600 + i * 1000)
    diff.add_circle(
        x=int(CX + (SX * 1)), y=int(CY + (SY * 1)), time=800 + i * 1000, new_combo=True
    )

diff.audio = "other/audio.ogg"
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

diff.version = "my version"
diff.creator = "pepa"


mapset = opymapper.new_mapset()

mapset.append_diff(diff)

mapset.save_all("test_map")
