from __future__ import annotations

import argparse
import configparser
from pathlib import Path

import cargparse


def parse_config(filename: Path | str) -> cargparse.Namespace:
    def common_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--home_dir", type=Path)
        parser.add_argument("--library_dir", type=Path)
        parser.add_argument("--system_dir", type=Path)
        parser.add_argument("--macports_dir", type=Path)
        return cargparse.Cargparse(parser).parse_dict(args)

    def frameworks_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--Python", type=str)
        parser.add_argument("--path", type=Path)
        return cargparse.Cargparse(parser).parse_dict(args)

    def arthur_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--nickname", type=str)
        parser.add_argument("--last_name", type=str)
        parser.add_argument("--my_dir", type=Path)
        parser.add_argument("--my_pictures", type=Path)
        parser.add_argument("--python_dir", type=Path)
        return cargparse.Cargparse(parser).parse_dict(args)

    cparser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

    # preserve case-sensitivity
    cparser.optionxform = str  # type: ignore

    cparser.read(filename)

    cfg = {section: dict(cparser.items(section)) for section in cparser.sections()}

    parser = argparse.ArgumentParser()
    parser.add_argument("--Common", type=common_namespace)
    parser.add_argument("--Frameworks", type=frameworks_namespace)
    parser.add_argument("--Arthur", type=arthur_namespace)
    return cargparse.Cargparse(parser).parse_dict(cfg)


if __name__ == "__main__":

    config = parse_config("interpolation_extended.ini")

    try:
        assert config.Frameworks.path.parent.parent.name == "System"
        print("All good!")
    except AssertionError as e:
        print(e.__class__.__name__)
        exit(1)
