from __future__ import annotations

import argparse
from pathlib import Path

import tomli

import cargparse


def parse_config(filename: Path | str) -> cargparse.Namespace:
    def project_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--urls", type=url_namespace, required=True)
        return cargparse.Cargparse(parser).parse_dict(args)

    def url_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--homepage", type=str)
        parser.add_argument("--bug_tracker", type=str)
        return cargparse.Cargparse(parser).parse_dict(args)

    def tool_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--pytest", type=pytest_namespace, required=True)
        parser.add_argument("--black", type=black_namespace, required=True)
        parser.add_argument("--isort", type=isort_namespace, required=True)
        return cargparse.Cargparse(parser).parse_dict(args)

    def pytest_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--ini_options", type=ini_options_namespace)
        return cargparse.Cargparse(parser).parse_dict(args)

    def ini_options_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--testpaths", type=cargparse.list_str)
        parser.add_argument("--markers", type=cargparse.list_str)
        parser.add_argument("--log_level", type=str)
        parser.add_argument("--log_format", type=str)
        return cargparse.Cargparse(parser).parse_dict(args)

    def black_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--line_length", type=int)
        return cargparse.Cargparse(parser).parse_dict(args)

    def isort_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--profile", type=str)
        return cargparse.Cargparse(parser).parse_dict(args)

    with open(filename, "rb") as f:
        toml = tomli.load(f)

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=project_namespace)
    parser.add_argument("--tool", type=tool_namespace)
    return cargparse.Cargparse(parser).parse_dict(toml)


if __name__ == "__main__":

    config = parse_config("config.toml")

    try:
        assert config.tool.pytest.ini_options.log_level == "INFO"
        print("All good!")
    except AssertionError as e:
        print(e.__class__.__name__)
        exit(1)
