from __future__ import annotations

import argparse
import json
from pathlib import Path

import ruamel.yaml
import tomli

import cargparse


def parse_config(filename: Path | str) -> cargparse.Namespace:
    def model_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--cnn", type=cnn_namespace)
        parser.add_argument("--lstm", type=lstm_namespace)
        return cargparse.Cargparse(parser).parse_dict(args)

    def cnn_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--in_channels", type=int, required=True)
        parser.add_argument("--out_channels", type=int, required=True)
        parser.add_argument("--kernel_width", type=int, required=True)
        return cargparse.Cargparse(parser).parse_dict(args)

    def lstm_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input_size", type=int, required=True)
        parser.add_argument("--hidden_size", type=cargparse.list_int, required=True)
        parser.add_argument("--dropout", type=float)
        parser.add_argument("--bidirectional", type=cargparse.boolean)
        return cargparse.Cargparse(parser).parse_dict(args)

    def train_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input_dir", type=Path)
        parser.add_argument("--label_dir", type=Path)
        parser.add_argument("--learning_rate", type=float)
        parser.add_argument("--max_epochs", type=int)
        parser.add_argument("--optimizer", type=cargparse.list_str)
        parser.add_argument("--batch_size", type=cargparse.list_int)
        return cargparse.Cargparse(parser).parse_dict(args)

    def test_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input_dir", type=Path)
        parser.add_argument("--label_dir", type=Path)
        parser.add_argument("--confusion_matrix", type=cargparse.boolean)
        return cargparse.Cargparse(parser).parse_dict(args)

    mode = "rb" if filename.suffix == ".toml" else "r"
    with open(filename, mode) as f:
        if filename.suffix == ".yaml":
            config_str = ruamel.yaml.safe_load(f)
        elif filename.suffix == ".json":
            config_str = json.load(f)
        elif filename.suffix == ".toml":
            config_str = tomli.load(f)

    parser = argparse.ArgumentParser()
    parser.add_argument("--cuda", type=cargparse.boolean)
    parser.add_argument("--model", type=model_namespace, required=True)
    parser.add_argument("--train", type=train_namespace, required=True)
    parser.add_argument("--test", type=test_namespace, required=True)
    return cargparse.Cargparse(parser).parse_dict(config_str)


if __name__ == "__main__":

    extensions = ["json", "toml", "yaml"]
    configs = [parse_config(Path(__file__).parent / f"neural_network.{ext}") for ext in extensions]

    try:
        assert configs[0] == configs[1] == configs[2]
        print("All good!")
    except AssertionError as e:
        print(e.__class__.__name__)
        exit(1)
