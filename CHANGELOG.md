# Changelog
## 0.2.1- Add pytest and mypy tool configuration to pyproject.toml

## 0.2.0 (2026-03-16)

- Improve word splitting to handle number-letter boundaries (`"html2json"` -> `["html", "2", "json"]`)
- Add `to_sentence()` -- Sentence case conversion
- Add `to_header()` -- HTTP Header-Case conversion
- Add `is_case()` -- check if string matches a case convention
- Support lists of dicts in `convert_keys()`

## 0.1.5

- Add basic import test

## 0.1.4

- Add Development section to README

## 0.1.1

- Re-release for PyPI publishing

## 0.1.0 (2026-03-15)

- Initial release
- Convert strings between 8 case formats: snake_case, camelCase, PascalCase, kebab-case, CONSTANT_CASE, Title Case, dot.case, path/case
- Acronym-aware splitting (HTMLParser -> html_parser, getHTTPSUrl -> get_https_url)
- Preserve leading and trailing underscores
- Recursive dictionary key conversion with `convert_keys`
- Case detection with `detect_case`
