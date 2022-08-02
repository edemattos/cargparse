"""
Good example of:
    - type validation for lists of dictionaries
    - type validation for complex types (datetime, timedelta)
    - error handling
    - spaces/characters in key names (dictionary['indexing'] and namespace.indexing)
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

import ruamel.yaml
import tomli

import cargparse


def parse_config(filename: Path | str) -> cargparse.Namespace:
    def min_sec(arg: str) -> timedelta:
        try:
            minutes, seconds = arg.split(":")
        except:
            # nicely formatted error message including the key (--duration; keys are otherwise inaccessible)
            raise argparse.ArgumentTypeError(f"{arg} failed to parse (expected MM:SS)")
        return timedelta(minutes=int(minutes), seconds=int(seconds))

    def year_month_day(arg: str) -> datetime:
        return datetime.strptime(arg, "%Y %m %d")

    def list_member_namespace(args: str) -> list[cargparse.Namespace]:
        args = eval(args)  # we expect args to be a list
        parser = argparse.ArgumentParser()
        parser.add_argument("--name", type=str)
        parser.add_argument("--dob", type=year_month_day)
        # use the same parser for each element in the list
        return [cargparse.Cargparse(parser).parse_dict(item) for item in args]

    mode = "rb" if filename.suffix == ".toml" else "r"
    with open(filename, mode) as f:
        if filename.suffix == ".yaml":
            config_str = ruamel.yaml.safe_load(f)
        elif filename.suffix == ".json":
            config_str = json.load(f)
        elif filename.suffix == ".toml":
            config_str = tomli.load(f)

    parser = argparse.ArgumentParser()
    parser.add_argument("--title", type=str)
    parser.add_argument("--artist", type=str)
    parser.add_argument("--label", type=str)
    parser.add_argument("--genre", type=cargparse.list_str)
    parser.add_argument("--duration", type=min_sec)
    parser.add_argument("--release date", type=year_month_day)
    parser.add_argument("--members", type=list_member_namespace)  # or cargparse.list_dict for list[dict[str, str]]
    return cargparse.Cargparse(parser).parse_dict(config_str)


if __name__ == "__main__":

    extensions = ["json", "toml", "yaml"]
    configs = [parse_config(Path(__file__).parent / f"twice_fancy.{ext}") for ext in extensions]

    try:
        assert configs[0] == configs[1] == configs[2]
        print("All good!\n")
    except AssertionError as e:
        print(e.__class__.__name__)
        exit(1)

    config = configs[2]

    print(f"{config['release date'].strftime('%Y %m %d')} - TWICE's smash hit 'Fancy' released")
    print(f"{datetime.now().strftime('%Y %m %d')} - Today's date")

    years = (datetime.now() - config["release date"]).days // 365
    days = (datetime.now() - config["release date"]).days % 365
    print(f"-> {years} years and {days} day{'s' if days != 1 else ''} have elapsed since then\n")

    print("How old is each TWICE member?")
    ages = {member: datetime.now().year - member.dob.year for member in config.members}
    for member, age in sorted(ages.items(), key=lambda x: x[1], reverse=True):
        msg = f"{age} - {member.name}"
        if datetime.now().month == member.dob.month and datetime.now().day == member.dob.day:
            msg += " (today is her birthday!)"
        print(msg)
