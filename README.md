[![Run Pytest](https://github.com/Msnehulak/opymapper/actions/workflows/tests.yaml/badge.svg)](https://github.com/Msnehulak/opymapper/actions/workflows/tests.yaml)
<h1>
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! <br>
This project is still in development but usable <br>
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
</h1>

# OPYMAPPER (OSU python mapper)
opymapper is a tool in Python to create osu! beatmaps programmatically. Developed with Test Driven Development.

## Download
```bash
pip install opymapper
```

## Development
Clone repo
### Install Dev dependencies
```bash
uv pip install ".[dev]"
# or
pip install -e ".[dev]"
```

### Install normal dependencies
```bash
uv pip install .
# or
pip install -e .
```

### Run pytest 
```bash 
pytest
```

### First code
```python
import opymapper

diff.add_circle(x=256, y=192, time=1000)

diff = opymapper.new_diff()

mapset = opymapper.new_mapset()
mapset.append_diff(diff)
mapset.save_all("hello_map")
```
This create playable `hello_map.osz` map witch you can play in osu lazer, 
with one note in the center at 1000ms.

## Links
- [PyPi](https://pypi.org/project/opymapper/)
- [GitHub](https://github.com/Msnehulak/opymapper)

Documentation soon

