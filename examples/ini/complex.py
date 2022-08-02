from __future__ import annotations

import argparse
import configparser
from pathlib import Path

import cargparse


def parse_config(filename: Path | str) -> cargparse.Namespace:
    def simple_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--key", type=str)
        parser.add_argument("--spaces in keys", type=str)
        parser.add_argument("--spaces in values", type=str)
        parser.add_argument("--spaces around the delimiter", type=str)
        parser.add_argument("--you can also use", type=str)
        return cargparse.Cargparse(parser).parse_dict(args)

    def type_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--values like this", type=int)
        parser.add_argument("--or this", type=float)
        parser.add_argument("--integers, floats and booleans are held as", type=str)
        parser.add_argument("--but you can convert them using", type=str)
        return cargparse.Cargparse(parser).parse_dict(args)

    def multiline_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--chorus", type=str)
        return cargparse.Cargparse(parser).parse_dict(args)

    def no_values_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--empty string value here", type=str)
        return cargparse.Cargparse(parser).parse_dict(args)

    def comments_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--placeholder", type=str)
        return cargparse.Cargparse(parser).parse_dict(args)

    def indented_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--can_values_be_as_well", type=cargparse.boolean)
        parser.add_argument("--does_that_mean_anything_special", type=cargparse.boolean)
        parser.add_argument("--purpose", type=str)
        parser.add_argument("--multiline_values", type=str)
        return cargparse.Cargparse(parser).parse_dict(args)

    cparser = configparser.ConfigParser()

    # preserve case-sensitivity
    cparser.optionxform = str  # type: ignore

    cparser.read(filename)

    cfg = {section: dict(cparser.items(section)) for section in cparser.sections()}

    parser = argparse.ArgumentParser()
    parser.add_argument("--Simple Values", type=simple_namespace)
    parser.add_argument("--Type Validation", type=type_namespace)
    parser.add_argument("--Multiline Values", type=multiline_namespace)
    parser.add_argument("--No Values", type=no_values_namespace)
    parser.add_argument("--You can use comments", type=comments_namespace)
    parser.add_argument("--Sections Can Be Indented", type=indented_namespace)
    return cargparse.Cargparse(parser).parse_dict(cfg)


if __name__ == "__main__":

    config = parse_config("complex.ini")

    try:
        assert config["Multiline Values"].chorus.split("\n")[1] == "I sleep all night and I work all day"
        print("All good!")
    except AssertionError as e:
        print(e.__class__.__name__)
        exit(1)
