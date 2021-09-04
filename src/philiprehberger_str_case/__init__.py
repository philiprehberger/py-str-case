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
    "to_sentence",
    "to_header",
    "convert_keys",
    "detect_case",
    "is_case",
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

    # Split at letter-digit and digit-letter boundaries for number-aware splitting.
    # Split when 2+ letters precede digits: "html2json" -> "html 2json", "item123Name" -> "item 123Name"
    # Keep single-letter + digit together: "v2Api" stays "v2 Api"
    result = re.sub(r"([a-zA-Z]{2,})(\d)", r"\1 \2", result)
    # Split when digits precede letters: "html 2json" -> "html 2 json"
    result = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", result)

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


def to_sentence(s: str) -> str:
    """Convert to Sentence case -- first word capitalized, rest lowercase.

    >>> to_sentence("html_parser")
    'Html parser'
    >>> to_sentence("getHTTPSUrl")
    'Get https url'
    """
    words = _split_words(s)
    if not words:
        return s
    return " ".join([words[0].capitalize()] + [w.lower() for w in words[1:]])


def to_header(s: str) -> str:
    """Convert to HTTP Header-Case (e.g., Content-Type).

    >>> to_header("content_type")
    'Content-Type'
    >>> to_header("xForwardedFor")
    'X-Forwarded-For'
    """
    words = _split_words(s)
    if not words:
        return s
    return "-".join(w.capitalize() for w in words)


def convert_keys(data: dict | list, converter: Callable[[str], str]) -> dict | list:
    """Recursively convert all keys in a dictionary using the given converter.

    Nested dicts, lists of dicts, and top-level lists are handled recursively.

    >>> convert_keys({"firstName": "John", "lastName": "Doe"}, to_snake)
    {'first_name': 'John', 'last_name': 'Doe'}
    >>> convert_keys([{"firstName": "John"}], to_snake)
    [{'first_name': 'John'}]
    """
    if isinstance(data, list):
        return [
            convert_keys(item, converter) if isinstance(item, (dict, list)) else item
            for item in data
        ]
    result: dict = {}
    for key, value in data.items():
        new_key = converter(key) if isinstance(key, str) else key
        if isinstance(value, dict):
            result[new_key] = convert_keys(value, converter)
        elif isinstance(value, list):
            result[new_key] = [
                convert_keys(item, converter) if isinstance(item, (dict, list)) else item
                for item in value
            ]
        else:
            result[new_key] = value
    return result


def detect_case(s: str) -> str:
    """Detect the case convention of a string.

    Returns one of: "snake_case", "camelCase", "PascalCase", "kebab-case",
    "CONSTANT_CASE", "dot.case", "path/case", "Title Case", "Sentence case",
    "Header-Case", or "unknown".

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
    >>> detect_case("Content-Type")
    'Header-Case'
    >>> detect_case("Hello world")
    'Sentence case'
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
        # Check for Header-Case: all dash-separated words are capitalized
        parts = stripped.split("-")
        if all(p and p[0].isupper() and (len(p) == 1 or p[1:] == p[1:].lower()) for p in parts):
            return "Header-Case"
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
        # Check for Sentence case: first word capitalized, rest lowercase
        if (
            len(words) >= 2
            and words[0][0].isupper()
            and all(w == w.lower() for w in words[1:])
        ):
            return "Sentence case"
        return "unknown"
    # No separators — check casing
    if stripped[0].islower() and any(c.isupper() for c in stripped[1:]):
        return "camelCase"
    if stripped[0].isupper() and any(c.islower() for c in stripped):
        return "PascalCase"
    return "unknown"


def is_case(s: str, case: str) -> bool:
    """Check if a string matches a specific case convention.

    >>> is_case("my_variable", "snake_case")
    True
    >>> is_case("my_variable", "camelCase")
    False
    """
    return detect_case(s) == case
