"""Build i18n/person-names-en.json from catalogue photos and transliteration rules."""
from __future__ import annotations

try:
    from i18n_person_names_en import write_cache
except ImportError:
    from helpers.i18n_person_names_en import write_cache  # type: ignore


def main() -> None:
    write_cache()
    print("Wrote i18n/person-names-en.json")


if __name__ == "__main__":
    main()
