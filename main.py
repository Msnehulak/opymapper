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

diff.version = "my version"

mapset = opymapper.new_mapset()

mapset.append_diff(diff)

mapset.save_all("test_map")
