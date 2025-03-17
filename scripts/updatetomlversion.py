import argparse
import tomli
import tomli_w

VERSION = 'dev'
with open('VERSION', 'r') as f:
    VERSION = f.readline().strip()

with open("mosamatic/pyproject.toml", "rb") as f:
    data = tomli.load(f)

data["tool"]["poetry"]["version"] = VERSION

with open("pyproject.toml", "wb") as f:
    tomli_w.dump(data, f)

print("Version updated! Run briefcase create to reload .toml")
