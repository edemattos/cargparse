from __future__ import annotations

import argparse
import configparser
from pathlib import Path

import cargparse


def parse_config(filename: Path | str) -> cargparse.Namespace:
    def default_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--ServerAliveInterval", type=int)
        parser.add_argument("--Compression", type=str)
        parser.add_argument("--CompressionLevel", type=int)
        parser.add_argument("--ForwardX11", type=str)
        return cargparse.Cargparse(parser).parse_dict(args)

    def bitbucket_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--ServerAliveInterval", type=int)
        parser.add_argument("--Compression", type=str)
        parser.add_argument("--CompressionLevel", type=int)
        parser.add_argument("--ForwardX11", type=str)
        parser.add_argument("--User", type=str)
        return cargparse.Cargparse(parser).parse_dict(args)

    def topsecret_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--ServerAliveInterval", type=int)
        parser.add_argument("--Compression", type=str)
        parser.add_argument("--CompressionLevel", type=int)
        parser.add_argument("--ForwardX11", type=str)
        parser.add_argument("--Port", type=int)
        return cargparse.Cargparse(parser).parse_dict(args)

    cparser = configparser.ConfigParser()

    # preserve case-sensitivity
    cparser.optionxform = str  # type: ignore

    cparser.read(filename)

    cfg = {section: dict(cparser.items(section)) for section in cparser.sections()}

    parser = argparse.ArgumentParser()
    parser.add_argument("--DEFAULT", type=default_namespace)
    parser.add_argument("--bitbucket.org", type=bitbucket_namespace)
    parser.add_argument("--topsecret.server.com", type=topsecret_namespace)
    return cargparse.Cargparse(parser).parse_dict(cfg)


if __name__ == "__main__":

    config = parse_config("basic.cfg")

    try:
        assert config["bitbucket.org"].CompressionLevel == 9
        assert config["bitbucket.org"]["User"] == "hg"
        assert config["topsecret.server.com"].ServerAliveInterval == 45
        print("All good!")
    except AssertionError as e:
        print(e.__class__.__name__)
        exit(1)
