# philiprehberger-str-case

[![Tests](https://github.com/philiprehberger/py-str-case/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-str-case/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-str-case.svg)](https://pypi.org/project/philiprehberger-str-case/)
[![License](https://img.shields.io/github/license/philiprehberger/py-str-case)](LICENSE)
[![Sponsor](https://img.shields.io/badge/sponsor-GitHub%20Sponsors-ec6cb9)](https://github.com/sponsors/philiprehberger)

Convert strings between camelCase, snake_case, PascalCase, kebab-case, and more.

## Installation

```bash
pip install philiprehberger-str-case
```

## Usage

```python
from philiprehberger_str_case import to_snake, to_camel, to_pascal, to_kebab

to_snake("HTMLParser")       # "html_parser"
to_camel("html_parser")      # "htmlParser"
to_pascal("get-https-url")   # "GetHttpsUrl"
to_kebab("getHTTPSUrl")      # "get-https-url"
```

### Acronym handling

Acronyms are split correctly:

```python
from philiprehberger_str_case import to_snake

to_snake("HTMLParser")    # "html_parser"
to_snake("getHTTPSUrl")  # "get_https_url"
to_snake("XMLToJSON")    # "xml_to_json"
```

### Number-aware splitting

Numbers at letter-digit boundaries are split into separate words:

```python
from philiprehberger_str_case import to_snake, to_kebab

to_snake("html2json")      # "html_2_json"
to_snake("item123Name")    # "item_123_name"
to_kebab("v2Api")          # "v2-api"  (single-letter prefix stays attached)
```

### More formats

```python
from philiprehberger_str_case import to_constant, to_title, to_dot, to_path

to_constant("htmlParser")  # "HTML_PARSER"
to_title("html_parser")    # "Html Parser"
to_dot("htmlParser")       # "html.parser"
to_path("htmlParser")      # "html/parser"
```

### Sentence case and Header-Case

```python
from philiprehberger_str_case import to_sentence, to_header

to_sentence("html_parser")    # "Html parser"
to_sentence("getHTTPSUrl")    # "Get https url"

to_header("content_type")     # "Content-Type"
to_header("xForwardedFor")    # "X-Forwarded-For"
```

### Convert dictionary keys

```python
from philiprehberger_str_case import convert_keys, to_snake

data = {
    "firstName": "John",
    "lastName": "Doe",
    "contactInfo": {
        "emailAddress": "john@example.com",
        "phoneNumber": "555-1234",
    },
}

convert_keys(data, to_snake)
# {
#     "first_name": "John",
#     "last_name": "Doe",
#     "contact_info": {
#         "email_address": "john@example.com",
#         "phone_number": "555-1234",
#     },
# }
```

Lists of dicts are also supported:

```python
records = [{"firstName": "Alice"}, {"firstName": "Bob"}]
convert_keys(records, to_snake)
# [{"first_name": "Alice"}, {"first_name": "Bob"}]
```

### Detect case

```python
from philiprehberger_str_case import detect_case, is_case

detect_case("my_variable")   # "snake_case"
detect_case("myVariable")    # "camelCase"
detect_case("MyVariable")    # "PascalCase"
detect_case("my-variable")   # "kebab-case"
detect_case("MY_VARIABLE")   # "CONSTANT_CASE"
detect_case("Content-Type")  # "Header-Case"
detect_case("Hello world")   # "Sentence case"

is_case("my_variable", "snake_case")  # True
is_case("my_variable", "camelCase")   # False
```

## API

| Function | Description |
|----------|-------------|
| `to_snake(s)` | Convert to snake_case |
| `to_camel(s)` | Convert to camelCase |
| `to_pascal(s)` | Convert to PascalCase |
| `to_kebab(s)` | Convert to kebab-case |
| `to_constant(s)` | Convert to CONSTANT_CASE |
| `to_title(s)` | Convert to Title Case |
| `to_dot(s)` | Convert to dot.case |
| `to_path(s)` | Convert to path/case |
| `to_sentence(s)` | Convert to Sentence case |
| `to_header(s)` | Convert to HTTP Header-Case |
| `convert_keys(data, converter)` | Recursively convert dict/list keys |
| `detect_case(s)` | Detect case convention of a string |
| `is_case(s, case)` | Check if string matches a case convention |


## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
