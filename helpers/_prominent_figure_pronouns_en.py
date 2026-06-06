"""Replace plural pronouns that refer to a single profile subject with neutral singular phrasing."""
from __future__ import annotations

# Longest-first phrase replacements (subject = one prominent figure).
_SINGULAR_PHRASES: tuple[tuple[str, str], ...] = (
    (
        "Notable aspects of their life and work",
        "Notable aspects of the life and work",
    ),
    (
        "Interesting facts from their life",
        "Notable aspects of the life and work",
    ),
    (
        "a guiding principle from their legacy",
        "a guiding principle drawn from this legacy",
    ),
    (
        "Like many distinguished scholars, their contributions were not limited to the needs of their own era; they shaped",
        "Like many distinguished scholars, this contribution was not limited to the needs of a single era; it shaped",
    ),
    (
        "Among the principal areas of their work, particular note is given to their activities in",
        "Among the principal areas of this work, particular note is given to activities in",
    ),
    (
        "; contributions to Enlightenment thought, culture, and scholarly heritage; and their role in",
        "; contributions to Enlightenment thought, culture, and scholarly heritage; and to the role in",
    ),
    (
        "These examples are the primary indicators of the scholarly, literary, or cultural influence they generated in their field.",
        "These examples are the primary indicators of the scholarly, literary, or cultural influence generated in this field.",
    ),
    (
        "strengthened new directions of thought and scholarly inquiry in their field.",
        "strengthened new directions of thought and scholarly inquiry in this field.",
    ),
    (
        "strengthened new directions of thought and research in their field.",
        "strengthened new directions of thought and research in this field.",
    ),
    (
        "Their life and work occupy an important place",
        "This figure's life and work occupy an important place",
    ),
    (
        "Their work was primarily associated with",
        "This work was primarily associated with",
    ),
    (
        "the scientific questions of their era.",
        "the scientific questions of the period.",
    ),
    (
        "The ideas they developed in",
        "The ideas developed in",
    ),
    (
        "Their principal contribution is associated with",
        "The principal contribution is associated with",
    ),
    (
        "Their work left a lasting mark in the history of universal human progress.",
        "This work left a lasting mark in the history of universal human progress.",
    ),
    (
        "Their legacy continues to be recalled in diverse scholarly and cultural settings.",
        "This legacy continues to be recalled in diverse scholarly and cultural settings.",
    ),
    (
        "Their scholarly legacy has influenced research and educational environments in many countries.",
        "This scholarly legacy has influenced research and educational environments in many countries.",
    ),
    (
        "This figure's legacy was not confined to their own era;",
        "This figure's legacy was not confined to that era;",
    ),
    (
        "Their name occupies an important place in the shared cultural memory of the Turkic world.",
        "This figure's name occupies an important place in the shared cultural memory of the Turkic world.",
    ),
    (
        "is presented as a figure who contributed to the established traditions of their field",
        "is presented as a figure who contributed to the established traditions of this field",
    ),
    (
        "profoundly influenced the intellectual climate of their era",
        "profoundly influenced the intellectual climate of the era",
    ),
    (
        "influenced the intellectual climate of their time",
        "influenced the intellectual climate of the period",
    ),
    (
        "influenced the intellectual climate of their era",
        "influenced the intellectual climate of the era",
    ),
    (
        "The profile highlights their work, their contribution to public and cultural life, and their place in",
        "The profile highlights this work, the contribution to public and cultural life, and the place in",
    ),
    (
        "helped shape the cultural and intellectual environment of their period.",
        "helped shape the cultural and intellectual environment of the period.",
    ),
    (
        "associated with their field",
        "associated with this field",
    ),
    (
        "traditions associated with their field",
        "traditions associated with this field",
    ),
    (
        "is recognized as a major figure in their field",
        "is recognized as a major figure in this field",
    ),
    (
        "is among the prominent figures who shaped their field",
        "is among the prominent figures who shaped this field",
    ),
    (
        "Contributions in their region",
        "Contributions in the region",
    ),
    (
        "Made an important contribution in their field",
        "Made an important contribution in this field",
    ),
    (
        "Their life and work are presented as part of",
        "This figure's life and work are presented as part of",
    ),
    (
        "Their legacy influenced research and education in many countries.",
        "This legacy influenced research and education in many countries.",
    ),
    (
        "Their legacy is recalled across many scientific and cultural settings.",
        "This legacy is recalled across many scientific and cultural settings.",
    ),
    (
        "Their work is closely connected with",
        "This work is closely connected with",
    ),
)


def apply_singular_pronouns(text: str) -> str:
    """Rewrite person-referring plural pronouns for single-subject profile text."""
    for old, new in _SINGULAR_PHRASES:
        if old in text:
            text = text.replace(old, new)
    return text
