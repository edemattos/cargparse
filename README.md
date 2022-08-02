<p align="center">
    <br/><img src="https://demattos.io/img/cargparse.svg" alt="cargparse"><br/><br/>
    Parse and validate configuration files with <code>argparse</code>.<br/><br/>
    <a href="https://pypi.org/project/cargparse/" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/cargparse?color=lightgrey" alt="Python version">
    </a>
    <a href="https://pypi.org/project/cargparse/" target="_blank">
        <img src="https://img.shields.io/pypi/v/cargparse?color=lightgrey" alt="PyPI version">
    </a>
    <a href="https://github.com/psf/black" target="_blank">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="code style: black">
    </a>
</p>

## Installation

```
pip install cargparse
```

## Basic usage

Given  `config.yaml`:

```yaml
text: hello world
number: 42
```

Load the file as a string and use `argparse` as you normally would for command line arguments!

```python
import argparse
import cargparse
import ruamel.yaml # alternatively: pyyaml, strictyaml, etc.

with open("config.yaml") as f:
    yaml = ruamel.yaml.safe_load(f)

parser = argparse.ArgumentParser()
parser.add_argument("--text", type=str, required=True)
parser.add_argument("--number", type=int, required=True)
parser.add_argument("--decimal", type=float)
config = cargparse.Cargparse(parser).parse_dict(yaml)
```

```
>> config
{"text": "hello world", "number": 42)
>> config.text
"hello world"
>> type(config.number)
<class "int">
```

⚠️ Read the [documentation]() for more information about type validation.

## Advanced usage

You are not restricted to a flat hierarchy.

```yaml
model:
  lstm:
    input_size: 100
    hidden_size:
      - 128
      - 64
  summary: True
```

Define a helper function to parse each nested section `args`, which is interpreted as a dictionary `str`.

```python
from __future__ import annotations

def parse_config(filename: Path | str) -> cargparse.Namespace:

    def model_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--cnn", type=cnn_namespace)
        parser.add_argument("--lstm", type=lstm_namespace)
        parser.add_argument("--summary", type=cargparse.boolean)
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
        return cargparse.Cargparse(parser).parse_dict(args)

    with open(filename) as f:
        yaml = ruamel.yaml.safe_load(f)

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=model_namespace, required=True)
    return cargparse.Cargparse(parser).parse_dict(yaml)
```

```
>> config.model.cnn
>> config.model.lstm.hidden_units
*** AttributeError: hidden_units not in namespace: ["hidden_size", "input_size"]
>> config.model.lstm.hidden_size
[128, 64]
```

⚠️ Read the [documentation]() for more information about type validation.
