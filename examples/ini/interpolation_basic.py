from __future__ import annotations

import argparse
import configparser
from ast import Assert
from pathlib import Path

import cargparse


def parse_config(filename: Path | str) -> cargparse.Namespace:
    def percent_str_to_float(arg: str) -> float:
        return float(arg.replace("%", "e-2"))

    def paths_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--home_dir", type=Path)
        parser.add_argument("--my_dir", type=Path)
        parser.add_argument("--my_pictures", type=Path)
        return cargparse.Cargparse(parser).parse_dict(args)

    def escape_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--gain", type=percent_str_to_float)
        return cargparse.Cargparse(parser).parse_dict(args)

    cparser = configparser.ConfigParser()

    # preserve case-sensitivity
    cparser.optionxform = str  # type: ignore

    cparser.read(filename)

    cfg = {section: dict(cparser.items(section)) for section in cparser.sections()}

    parser = argparse.ArgumentParser()
    parser.add_argument("--Paths", type=paths_namespace)
    parser.add_argument("--Escape", type=escape_namespace)
    return cargparse.Cargparse(parser).parse_dict(cfg)


if __name__ == "__main__":

    config = parse_config("interpolation_basic.ini")

    try:
        assert config.Paths.my_pictures.parent.name == "lumberjack"
        assert config.Escape.gain == 0.8
        print("All good!")
    except AssertionError as e:
        print(e.__class__.__name__)
        exit(1)
