from __future__ import annotations

import argparse
from typing import Any


class Namespace:
    def __init__(self, args: argparse.Namespace) -> None:
        # update object namespace so arguments can be accessed as attributes
        self.__dict__.update(**vars(args))

    def __getattr__(self, name: str) -> Any:
        if name not in dir(self):
            raise AttributeError(f"{name} not in namespace: {sorted(vars(self).keys())}")
        return super().__getattribute__(name)

    def __getitem__(self, name: str) -> Any:
        return getattr(self, name)

    def __repr__(self) -> str:
        return str({key: getattr(self, key) for key in dir(self) if not key.startswith("_")})

    def __key(self):
        attrs = []
        for _, value in vars(self).items():
            attrs.append(value)
        return tuple(attrs)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other: object) -> bool:
        for attribute, value in vars(self).items():
            if isinstance(value, Namespace):
                value.__eq__(vars(other)[attribute])
            if value != vars(other)[attribute]:
                return False
        return True


class Cargparse:
    def __init__(self, parser: argparse.ArgumentParser) -> None:
        """
        ArgumentParser wrapper. The parser object must define the arguments for your project using
        --flagged arguments. Positional arguments will not work. If you want to make an argument
        required, use `parser.add_argument('--flag', required=True)`
        """
        self.parser = parser

    def parse_dict(self, args: dict | str) -> Namespace:
        """
        Parse a nested dictionary in your configuration file.
        """
        if not isinstance(eval(str(args)), dict):
            raise argparse.ArgumentTypeError(f"`args` must be a valid (stringified) dictionary. args={args}")
        return Namespace(self.parser.parse_args(self._dict_str_to_list_flagged(args)))

    # def parse_file(
    #     self,
    #     filename: Path | str,
    #     format: str | None = None,
    #     case_sensitive: bool = True,
    #     reader: configparser.ConfigParser | None = None,
    # ) -> Namespace:
    #     """
    #     Parse a configuration file.
    #     """

    #     if reader and not isinstance(reader, configparser.ConfigParser):
    #         raise ValueError(
    #             "Customs readers are only supported for cfg/ini files and must be of type configparser.ConfigParser"
    #         )

    #     return self._parse(_read_file(filename, format, case_sensitive, reader))

    def _dict_str_to_list_flagged(self, x: dict | str) -> list[str]:
        """
        Convert key-value pairs of (stringified) dict to a list of (--flagged) string arguments.
        """
        arg_dict = []
        for key, value in eval(str(x)).items():
            arg_dict.append(f"--{key}")
            arg_dict.append(str(value))
        return arg_dict

    def _parse(self, args: list[str]) -> Namespace:
        """
        Parse and validate types with ArgumentParser. Input is a list[str] in the form ['--flag', 'value', ...]
        just like the command line, except here `value` might be a stringified dictionary.
        """
        pass
