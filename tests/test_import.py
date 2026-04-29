"""Tests for philiprehberger_str_case."""

from __future__ import annotations

from philiprehberger_str_case import (
    convert_keys,
    detect_case,
    is_case,
    to_camel,
    to_constant,
    to_dot,
    to_header,
    to_kebab,
    to_pascal,
    to_path,
    to_sentence,
    to_snake,
    to_title,
    to_words,
)


def test_import():
    import philiprehberger_str_case
    assert hasattr(philiprehberger_str_case, "__name__")


def test_to_snake_basic():
    assert to_snake("HTMLParser") == "html_parser"
    assert to_snake("getHTTPSUrl") == "get_https_url"


def test_to_camel_basic():
    assert to_camel("html_parser") == "htmlParser"


def test_to_pascal_basic():
    assert to_pascal("get-https-url") == "GetHttpsUrl"


def test_to_kebab_basic():
    assert to_kebab("HTMLParser") == "html-parser"


def test_to_constant_basic():
    assert to_constant("htmlParser") == "HTML_PARSER"


def test_to_title_basic():
    assert to_title("html_parser") == "Html Parser"


def test_to_dot_path():
    assert to_dot("htmlParser") == "html.parser"
    assert to_path("htmlParser") == "html/parser"


def test_to_sentence_and_header():
    assert to_sentence("html_parser") == "Html parser"
    assert to_header("content_type") == "Content-Type"


def test_detect_and_is_case():
    assert detect_case("my_variable") == "snake_case"
    assert is_case("my_variable", "snake_case") is True
    assert is_case("my_variable", "camelCase") is False


def test_convert_keys_basic():
    assert convert_keys({"firstName": "x"}, to_snake) == {"first_name": "x"}


def test_to_words_basic():
    assert to_words("html_parser") == ["html", "parser"]


def test_to_words_acronym_handling():
    assert to_words("getHTTPSUrl") == ["get", "https", "url"]
    assert to_words("HTMLParser") == ["html", "parser"]


def test_to_words_number_boundaries():
    assert to_words("html2json") == ["html", "2", "json"]
    assert to_words("item123Name") == ["item", "123", "name"]


def test_to_words_separators():
    assert to_words("a-b_c.d/e") == ["a", "b", "c", "d", "e"]


def test_to_words_empty_or_only_underscores():
    assert to_words("") == []
    assert to_words("___") == []
