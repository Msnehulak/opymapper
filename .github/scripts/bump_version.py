import re
import sys
import tomllib
from pathlib import Path


def calculate_new_version(current_version: str, publish_type: str) -> str:
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:b(\d+))?$", current_version)
    if not match:
        raise ValueError(f"Neplatný formát verze v pyproject.toml: '{current_version}'")

    major, minor, patch, beta = match.groups()
    major, minor, patch = int(major), int(minor), int(patch)

    if publish_type == "small":
        if beta is not None:
            return f"{major}.{minor}.{patch}b{int(beta) + 1}"
        return f"{major}.{minor}.{patch + 1}"

    elif publish_type == "medium":
        return f"{major}.{minor + 1}.0"

    elif publish_type == "major":
        return f"{major + 1}.0.0"

    else:
        raise ValueError(
            f"Neznámý typ publikace: '{publish_type}'. Použij 'small', 'medium' nebo 'major'."
        )


def main():
    publish_type = sys.argv[1] if len(sys.argv) > 1 else "small"
    pyproject_path = Path("pyproject.toml")

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    current_version = data["project"]["version"]

    new_version = calculate_new_version(current_version, publish_type)
    print(f"Zvyšuji verzi ({publish_type}): {current_version} -> {new_version}")

    content = pyproject_path.read_text(encoding="utf-8")
    old_line = f'version = "{current_version}"'
    new_line = f'version = "{new_version}"'

    if old_line not in content:
        raise ValueError(f"Řádek '{old_line}' nebyl v souboru pyproject.toml nalezen.")

    updated_content = content.replace(old_line, new_line, 1)
    pyproject_path.write_text(updated_content, encoding="utf-8")


if __name__ == "__main__":
    main()
