import argparse
import tomli
import tomli_w

with open("mosamatic/pyproject.toml", "rb") as f:
    data = tomli.load(f)

data["tool"]["poetry"]["version"] = "2.0.0"

with open("pyproject.toml", "wb") as f:
    tomli_w.dump(data, f)

print("Version updated!")
