import argparse
import tomli # type: ignore
import tomli_w


VERSION = 'dev'
with open('VERSION', 'r') as f:
    VERSION = f.readline().strip()


with open('mosamatic/pyproject.toml', 'rb') as f:
    data = tomli.load(f)

data['tool']['briefcase']['version'] = VERSION

with open('mosamatic/pyproject.toml', 'wb') as f:
    tomli_w.dump(data, f)

print('Version updated!')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('version', help='Version to use to update pyproject.toml')
    args = parser.parse_args()

    with open('mosamatic/pyproject.toml', 'rb') as f:
        data = tomli.load(f)
    data['tool']['briefcase']['version'] = args.version
    with open('mosamatic/pyproject.toml', 'wb') as f:
        tomli_w.dump(data, f)
    print(f'Updated pyproject.toml version to {args.version}')


if __name__ == '__main__':
    main()