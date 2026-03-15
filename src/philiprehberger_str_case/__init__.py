"""Convert strings between camelCase, snake_case, PascalCase, kebab-case, and more."""

from __future__ import annotations

import re
from typing import Callable

__all__ = [
    "to_snake",
    "to_camel",
    "to_pascal",
    "to_kebab",
    "to_constant",
    "to_title",
    "to_dot",
    "to_path",
    "convert_keys",
    "detect_case",
]


def _split_words(s: str) -> list[str]:
    """Split a string into its component words, handling acronyms and separators."""
    # Strip and preserve leading/trailing underscores
    stripped = s.strip("_")
    if not stripped:
        return []

    # Replace common separators with a single space
    result = re.sub(r"[-_./\\]+", " ", stripped)

    # Insert space before transitions:
    # - Between a lowercase/digit and an uppercase letter: getHTTPSUrl -> get HTTPSUrl
    result = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", result)

    # - Between consecutive uppercase letters followed by a lowercase letter:
    #   HTTPSUrl -> HTTPS Url, HTMLParser -> HTML Parser
    result = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", result)

    words = result.split()
    return [w.lower() for w in words if w]


def _preserve_underscores(s: str) -> tuple[str, str]:
    """Return the leading and trailing underscores from a string."""
    leading = ""
    trailing = ""
    for ch in s:
        if ch == "_":
            leading += "_"
        else:
            break
    for ch in reversed(s):
        if ch == "_":
            trailing += "_"
        else:
            break
    return leading, trailing


def to_snake(s: str) -> str:
    """Convert a string to snake_case.

    >>> to_snake("HTMLParser")
    'html_parser'
    >>> to_snake("getHTTPSUrl")
    'get_https_url'
    """
    leading, trailing = _preserve_underscores(s)
    words = _split_words(s)
    if not words:
        return s
    return leading + "_".join(words) + trailing


def to_camel(s: str) -> str:
    """Convert a string to camelCase.

    >>> to_camel("html_parser")
    'htmlParser'
    >>> to_camel("get_https_url")
    'getHttpsUrl'
    """
    leading, trailing = _preserve_underscores(s)
    words = _split_words(s)
    if not words:
        return s
    first = words[0]
    rest = [w.capitalize() for w in words[1:]]
    return leading + first + "".join(rest) + trailing


def to_pascal(s: str) -> str:
    """Convert a string to PascalCase.

    >>> to_pascal("html_parser")
    'HtmlParser'
    >>> to_pascal("get-https-url")
    'GetHttpsUrl'
    """
    leading, trailing = _preserve_underscores(s)
    words = _split_words(s)
    if not words:
        return s
    return leading + "".join(w.capitalize() for w in words) + trailing


def to_kebab(s: str) -> str:
    """Convert a string to kebab-case.

    >>> to_kebab("HTMLParser")
    'html-parser'
    """
    leading, trailing = _preserve_underscores(s)
    words = _split_words(s)
    if not words:
        return s
    return leading + "-".join(words) + trailing


def to_constant(s: str) -> str:
    """Convert a string to CONSTANT_CASE.

    >>> to_constant("htmlParser")
    'HTML_PARSER'
    """
    leading, trailing = _preserve_underscores(s)
    words = _split_words(s)
    if not words:
        return s
    return leading + "_".join(w.upper() for w in words) + trailing


def to_title(s: str) -> str:
    """Convert a string to Title Case.

    >>> to_title("html_parser")
    'Html Parser'
    """
    leading, trailing = _preserve_underscores(s)
    words = _split_words(s)
    if not words:
        return s
    return leading + " ".join(w.capitalize() for w in words) + trailing


def to_dot(s: str) -> str:
    """Convert a string to dot.case.

    >>> to_dot("htmlParser")
    'html.parser'
    """
    leading, trailing = _preserve_underscores(s)
    words = _split_words(s)
    if not words:
        return s
    return leading + ".".join(words) + trailing


def to_path(s: str) -> str:
    """Convert a string to path/case.

    >>> to_path("htmlParser")
    'html/parser'
    """
    leading, trailing = _preserve_underscores(s)
    words = _split_words(s)
    if not words:
        return s
    return leading + "/".join(words) + trailing


def convert_keys(d: dict, converter: Callable[[str], str]) -> dict:
    """Recursively convert all keys in a dictionary using the given converter.

    Nested dicts and lists of dicts are handled recursively.

    >>> convert_keys({"firstName": "John", "lastName": "Doe"}, to_snake)
    {'first_name': 'John', 'last_name': 'Doe'}
    """
    result: dict = {}
    for key, value in d.items():
        new_key = converter(key) if isinstance(key, str) else key
        if isinstance(value, dict):
            result[new_key] = convert_keys(value, converter)
        elif isinstance(value, list):
            result[new_key] = [
                convert_keys(item, converter) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[new_key] = value
    return result


def detect_case(s: str) -> str:
    """Detect the case convention of a string.

    Returns one of: "snake_case", "camelCase", "PascalCase", "kebab-case",
    "CONSTANT_CASE", "dot.case", "path/case", "Title Case", or "unknown".

    >>> detect_case("my_variable")
    'snake_case'
    >>> detect_case("myVariable")
    'camelCase'
    >>> detect_case("MyVariable")
    'PascalCase'
    >>> detect_case("my-variable")
    'kebab-case'
    >>> detect_case("MY_VARIABLE")
    'CONSTANT_CASE'
    """
    stripped = s.strip("_")
    if not stripped:
        return "unknown"

    if "/" in stripped and " " not in stripped:
        return "path/case"
    if "." in stripped and " " not in stripped:
        return "dot.case"
    if "-" in stripped and " " not in stripped:
        if stripped == stripped.lower():
            return "kebab-case"
        return "unknown"
    if "_" in stripped and " " not in stripped:
        if stripped == stripped.upper():
            return "CONSTANT_CASE"
        if stripped == stripped.lower():
            return "snake_case"
        return "unknown"
    if " " in stripped:
        words = stripped.split()
        if all(w[0].isupper() for w in words if w):
            return "Title Case"
        return "unknown"
    # No separators — check casing
    if stripped[0].islower() and any(c.isupper() for c in stripped[1:]):
        return "camelCase"
    if stripped[0].isupper() and any(c.islower() for c in stripped):
        return "PascalCase"
    return "unknown"
