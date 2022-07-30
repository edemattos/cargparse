<p align="center">
    <img src="https://raw.githubusercontent.com/edemattos/temp/main/cargparse.svg?token=GHSAT0AAAAAABWMSZSVUMA4KRHLOBEQTRU6YXFFHJA"></p>
<p align="center">
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

Parse configuration files with `argparse`. Built-in support for type validation and argument nesting.

[Contributions](/CONTRIBUTING.md) and [feedback](https://github.com/edemattos/cargparse/issues)
welcome! 🤝

## Supported file types

Files are safely loaded and validated with tried and tested libraries.

| type     | validator      | third-party | note                                   |
|----------|----------------|:-----------:|----------------------------------------|
|          | `argparse`     | no          |                                        |
| `cfg`    | `configparser` | no          |                                        |
| `ini`    | `configparser` | no          |                                        |
| `json`   | `json`         | no          |                                        |
| `toml`   | `toml`         | yes         | `tomllib` is built-in from Python 3.11 |
| `yaml`   | `pyyaml`       | yes         |                                        |

## Installation

```
pip install cargparse
```

## Basic usage

Given  `config.yaml`...

```yaml
text: hello world
decimal: 0.5
boolean: False
```

...just use `argparse` as you normally would...

```python
import argparse
import cargparse

parser = argparse.ArgumentParser()
parser.add_argument('--text', type=str)
parser.add_argument('--decimal', type=float)
parser.add_argument('--boolean', type=lambda x: eval(x))
config = cargparse.Parser(parser).parse_file('config.yaml')
```

...to get the familiar `Namespace` object!

```
>> config
Namespace(text='hello world', decimal=0.5, boolean=False)
>> config.text
'hello world'
>> type(config.decimal)
<class 'float'>
```

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

Define a helper function to parse each nested dictionary `args`, which is a valid dictionary `str`.

```python
def parse_config(filename: Path | str) -> cargparse.Namespace:

    def model_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument('--cnn', type=cnn_namespace)
        parser.add_argument('--lstm', type=lstm_namespace)
        parser.add_argument('--summary', type=lambda x: eval(x))
        return cargparse.Parser(parser).parse_args(args)

    def cnn_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument('--in_channels', type=int, required=True)
        parser.add_argument('--out_channels', type=int, required=True)
        parser.add_argument('--kernel_width', type=int, required=True)
        return cargparse.Parser(parser).parse_args(args)

    def lstm_namespace(args: str) -> cargparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument('--input_size', type=int, required=True)
        parser.add_argument('--hidden_size', type=lambda x: eval(x), required=True)
        return cargparse.Parser(parser).parse_args(args)

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=model_namespace, required=True)
    return cargparse.Parser(parser).parse_file(filename)

if __name__ == '__main__':
    config = parse_config(filename=sys.argv[1])
```

Nested dictionaries are `Namespace` objects, too! 🌈

```
>> config.model.cnn
>> config.model.lstm.hidden_units
*** AttributeError: hidden_units not in namespace: ['input_size', 'hidden_size']
>> config.model.lstm.hidden_size
[128, 64]
```
