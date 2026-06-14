"""English strings and translation helpers for Forum 2024 sessions page."""
from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

try:
    from i18n_person_names_en import latin_display_name
    from i18n_scientists_maps_en import COUNTRY_EN, FIELD_EN
except ImportError:
    from helpers.i18n_person_names_en import latin_display_name  # type: ignore
    from helpers.i18n_scientists_maps_en import COUNTRY_EN, FIELD_EN  # type: ignore

COUNTRY_EN_EXT = {
    **COUNTRY_EN,
    "İsveçrə": "Switzerland",
}

META_DESCRIPTION_EN = (
    "Forum 2024 — organization of 10 September strategic sessions in mixed and "
    "discipline-specific groups, moderators, and table participants."
)

SUMMARY_TITLE_EN = "Day summary"
SUMMARY_EN = (
    "This page provides detailed information on sessions organized on 10 September "
    "within the Forum programme: mixed groups in the morning and discipline-specific groups "
    "after lunch, conducted on a brainstorming basis. It also explains how "
    "participants were seated at tables, the principles governing session "
    "organization, and the role and duties of moderators."
)

PHOTO_HEADER_EN = "Photo"

TABLE_HEADER_EN = {
    "№": "No.",
    "Foto": "Photo",
    "Moderator": "Moderator",
    "Moderatorlar": "Moderators",
    "İxtisas": "Specialty",
    "Ölkə": "Country",
    "Masalar": "Tables",
    "Ad, soyad": "Name",
    "Elm sahəsi": "Field",
}

FIELD_GROUP_EN = {
    "ƏDƏBİYYAT / SOCİAL ELMLƏR / İLAHİYYAT": "LITERATURE / SOCIAL SCIENCES / THEOLOGY",
    "HUMANİTAR / TƏHSİL / İNCƏSƏNƏT / TARİX": "HUMANITIES / EDUCATION / ARTS / HISTORY",
    "HÜQUQŞÜNASLIQ": "LAW",
    "İQTİSADİYYAT VƏ İDARƏÇİLİK": "ECONOMICS AND MANAGEMENT",
    "MÜHƏNDİSLİK VƏ ƏLAQƏLİ SAHƏLƏR": "ENGINEERING AND RELATED FIELDS",
    "TƏBABƏT VƏ ƏLAQƏLİ SAHƏLƏR": "MEDICINE AND RELATED FIELDS",
    "TƏBİƏT ELMLƏRİ": "NATURAL SCIENCES",
}

MODERATOR_SPECIALTY_EN = {
    "bəxtiyar siracov": "Computer Science / Dr.",
    "səadət kərimi": "Mathematics and mechanics / Prof. Dr.",
    "teymur rzayev": "Artist / Prof. Dr.",
}

SPECIALTY_EN: dict[str, str] = {
    "Avtomatika və İnformatika/ Prof. Dr.": "Automation and Informatics / Prof. Dr.",
    "Beynəlxalq hüquq / Prof. Dr.": "International law / Prof. Dr.",
    "Biofizika, biokimya/ Dr.": "Biophysics, biochemistry / Dr.",
    "Bioinformatika / Dr.": "Bioinformatics / Dr.",
    "Biologiya elmləri / Dr.": "Biological sciences / Dr.",
    "Biologiya və həyat elmləri / Dr.": "Biology and life sciences / Dr.",
    "Dərman çatdırılması və Biomühəndislik / Dr.": "Drug delivery and bioengineering / Dr.",
    "Enerji sistemlərinin təhlili və optimallaşdırılması / Dr.": "Energy systems analysis and optimisation / Dr.",
    "Ermənişünas / Prof. Dr.": "Armenian studies / Prof. Dr.",
    "Ermənişünas / Prof. Dr..": "Armenian studies / Prof. Dr.",
    "Farmakoloq / Dr.": "Pharmacologist / Dr.",
    "Filoloq / Dr.": "Philologist / Dr.",
    "Filosof, Hüquq / Prof. Dr.": "Philosophy, Law / Prof. Dr.",
    "Fizik  / Prof. Dr.": "Physicist / Prof. Dr.",
    "Fizik / Prof. Dr.": "Physicist / Prof. Dr.",
    "Fizika / Dr.": "Physics / Dr.",
    "Fizika / Prof. Dr.": "Physics / Prof. Dr.",
    "Fizika-Riyaziyyat / Prof. Dr.": "Physics and mathematics / Prof. Dr.",
    "Fizika-riyaziyyat / Dr.": "Mathematical physics / Dr.",
    "Fizika-riyaziyyat / Prof. Dr.": "Mathematical physics / Prof. Dr.",
    "Fizika/ Dr.": "Physics / Dr.",
    "Geofizik / Prof. Dr.": "Geophysicist / Prof. Dr.",
    "Humanitar Elmlər, Təhsil, İncəsənət, Tarix": "Humanities, Education, Arts, History",
    "Hüquq / Dr.": "Law / Dr.",
    "Hüquq-Sosial idarəetmə və hüquq / Dr.": "Law — social administration and law / Dr.",
    "Hüquqşünaslıq": "Law",
    "Həkim (hüceyrə biologiyası) / Dr.": "Physician (cell biology) / Dr.",
    "Həkim (stomatoloq) / Dr.": "Physician (dentist) / Dr.",
    "Həkim /  Dr.": "Physician / Dr.",
    "Həkim / Dr.": "Physician / Dr.",
    "Həkim / Prof. Dr.": "Physician / Prof. Dr.",
    "Həkim/ Prof. Dr.": "Physician / Prof. Dr.",
    "IT- Databank, Proqram təminatı və Sistem Administratoru": "IT — databank, software and systems administrator",
    "Iqtisadçı / Dr.": "Economist / Dr.",
    "Kimya / Dr.": "Chemistry / Dr.",
    "Kompüter elmləri / Dr.": "Computer Science / Dr.",
    "Molekulyar biologiya / Dr.": "Molecular biology / Dr.",
    "Musiqi Sənəti / Dr.": "Music art / Dr.",
    "Musiqiçi / Dr.": "Musician / Dr.",
    "Musiqiçi, bəstəkar / Dr.": "Musician, composer / Dr.",
    "Mühəndis / Prof. Dr.": "Engineer / Prof. Dr.",
    "Mühəndislik / Dr.": "Engineering / Dr.",
    "Mühəndislik / Prof. Dr.": "Engineering / Prof. Dr.",
    "Mühəndislik və Əlaqəli Sahələr": "Engineering and related fields",
    "Optika TexNlogiyası / Dr.": "Optical technology / Dr.",
    "Proqram Sistemləri / Dr.": "Programme systems / Dr.",
    "Proqram təminatı və Sistem Administratoru": "Software and systems administrator",
    "Qeyri-üzvü kimya / Prof. Dr.": "Inorganic chemistry / Prof. Dr.",
    "Riyaziyyat / Dr.": "Mathematics / Dr.",
    "Riyaziyyat / Prof. Dr.": "Mathematics / Prof. Dr.",
    "Riyaziyyat və mexanika / Prof. Dr.": "Mathematics and mechanics / Prof. Dr.",
    "Riyaziyyat və statistika / Prof. Dr.": "Mathematics and statistics / Prof. Dr.",
    "Rəhbərlik və Psixoloji Məsləhət/ Prof. Dr.": "Leadership and psychological counselling / Prof. Dr.",
    "Rəssam / Prof. Dr.": "Artist / Prof. Dr.",
    "Siyasi tarix , iqtisadiyyat sosialogiyası  / Prof. Dr.": "Political history, economic sociology / Prof. Dr.",
    "Sosial elmlər / Dr.": "Social sciences / Dr.",
    "Sosial İqtisadi və Siyasi Münasibətlər / Prof. Dr.": "Socio-economic and political relations / Prof. Dr.",
    "Sosiologiya / Dr.": "Sociology / Dr.",
    "Tarix (İslam Məzhəpləri Tarixi) / Prof. Dr.": "History (history of Islamic schools of thought) / Prof. Dr.",
    "Tarix / Prof. Dr.": "History / Prof. Dr.",
    "Texnika / Prof. Dr.": "Engineering technology / Prof. Dr.",
    "Tibb (Həkim onkoloq) / Dr.": "Medicine (oncologist) / Dr.",
    "Tibb / Dr.": "Medicine / Dr.",
    "Türk Dili ve Edebiyatı / Dr.": "Turkish language and literature / Dr.",
    "Türk Lehçeleri ve Edebiyatları / Dr.": "Turkic dialects and literatures / Dr.",
    "Türk Lehçeleri ve Edebiyyatları /  Dr.": "Turkic dialects and literatures / Dr.",
    "Təbabət və Əlaqəli Sahələr": "Medicine and related fields",
    "Təbiət Elmləri, Riyaziyyat və Məntiq": "Natural sciences, mathematics and logic",
    "Tədbiqi riyaziyyat  / Dr.": "Applied mathematics / Dr.",
    "Tədbiqi riyaziyyat / Dr.": "Applied mathematics / Dr.",
    "Təhsil / Dr.": "Education / Dr.",
    "Tətbiqi riyaziyyat / Dr.": "Applied mathematics / Dr.",
    "Yazıçı, tərcüməçi, ədəbiyyatşünas / Dr.": "Writer, translator, literary scholar / Dr.",
    "Yazıçı, şair, ədəbiyyatşünas": "Writer, poet, literary scholar",
    "Yuksək enerjilər kimyasi, nuvə kimyası / Dr.": "High-energy and nuclear chemistry / Dr.",
    "Yuksək enerjilər kimyasi, nuvə kimyası/ Dr.": "High-energy and nuclear chemistry / Dr.",
    "İnnovasiya və dəyişikliklərin idarə edilməsi / Dr.": "Innovation and change management / Dr.",
    "İnnovasiya və dəyişikliklərin idarə edilməsi/ Dr.": "Innovation and change management / Dr.",
    "İqtisadiyyat / Dr.": "Economics / Dr.",
    "İqtisadiyyat və İdarəcilik": "Economics and management",
    "İqtisadçı / Dr.": "Economist / Dr.",
    "İqtisadçı / Prof. Dr.": "Economist / Prof. Dr.",
    "İqtisadçı-mühəndis / Dr.": "Economist-engineer / Dr.",
    "Ədəbiyyat / Dr.": "Literature / Dr.",
    "Ədəbiyyat / Prof. Dr.": "Literature / Prof. Dr.",
    "Ədəbiyyat, Sosial Elmlər, İlahiyyat": "Literature, Social Sciences, Theology",
    "Ərəb dili və ədəbiyyatı / Dr.": "Arabic language and literature / Dr.",
}

INTRO_SECTIONS_EN: dict[str, dict[str, Any]] = {
    "teskil-prinsipleri": {
        "title": "Organization principles",
        "paragraphs": [
            "The purpose of the Forum is to develop short-, medium-, and long-term strategies "
            "that will guide WAAS's future activities. In other words, if one may put it this way, "
            "the Forum's 'output' should be several strategic plans.",
            "Within the events planned for 10 September, a series of morning and post-lunch "
            "sessions has been scheduled with the participation of international guests:",
            "In the morning sessions, groups are formed as MIXED groups — that is, participants "
            "are divided into groups regardless of their field of science, specialty, or country "
            "of residence.",
        ],
        "bullets": [
            "In the post-lunch sessions, participants work in groups aligned with their fields of "
            "science (these may be called Discipline-Specific Groups).",
            "Organizing groups in these two ways will contribute to participant networking. For "
            "example, participants who joined MIXED groups may later find themselves in one of the "
            "Discipline-Specific Groups. This, in turn, will enable participants to connect with more "
            "colleagues and broaden their networks.",
            "Before discussions begin, moderators must introduce participants to the audience, "
            "providing very brief (10-second) information on each person's name, field of science, "
            "workplace, and scientific achievements.",
            "Sessions are conducted using the brainstorming method.",
            "Each table will display a sign indicating its number. Name plates showing each "
            "participant's name and country of representation will be placed on the tables.",
            "During Discipline-Specific group discussions, additional signs indicating the relevant fields "
            "of science will also be placed on the tables.",
            "Sessions will be moderated by members of the WAAS Executive Board and other "
            "designated (selected) participants. Moderators will guide discussions and overall "
            "management in both MIXED and Discipline-Specific Groups. To record ideas and proposals voiced by "
            "participants, one scribe will be selected at each table. While moderators remain "
            "responsible for their groups as a whole, scribes will be responsible for capturing "
            "table discussions on paper. The number of moderators will remain the same, while the "
            "number of scribes will equal the number of tables. At the end of the sessions, "
            "moderators will collect the scribes' notes, synthesize them, and present them to the "
            "audience on behalf of their groups.",
        ],
    },
    "qarisiq-muzakire": {
        "title": "MIXED groups — discussion topics",
        "lead": "MIXED groups",
        "bullets": [
            "They discuss the short-, medium-, and long-term strategies shown as examples in the "
            '"STRATEGIC PLANNING DIRECTIONS" section and select those most suitable for '
            "implementation;",
            "Taking into account issues raised in the presentations of state officials and "
            "university leaders;",
            "They produce a draft containing provisions reflecting the group's preferred strategic "
            "directions and explaining why they are appropriate.",
        ],
        "caption": "Figure 1. MIXED group activity",
    },
    "ixtisas-muzakire": {
        "title": "Discipline-Specific Groups — discussion topics",
        "lead": "Discipline-Specific Groups",
        "bullets": [
            "The priority strategic directions identified by the MIXED groups;",
            "Issues raised in the presentations of state officials and university leaders; and",
            'By reviewing topics listed in the "RECOMMENDED DISCUSSION TOPICS BY FIELD OF SCIENCE" '
            "section, they prepare and produce WAAS's short-, medium-, and long-term strategic "
            "plans.",
        ],
        "caption": "Figure 2. Discipline-Specific group activity",
    },
    "strategi-planlasdirma": {
        "title": "STRATEGIC PLANNING DIRECTIONS",
    },
    "elm-saheleri-tovsiyeler": {
        "title": "RECOMMENDED DISCUSSION TOPICS BY FIELD OF SCIENCE",
    },
}

UI_EN = {
    "qarisiq_tables_title": "MIXED group tables",
    "ixtisas_tables_title": "Discipline-Specific group tables",
    "moderators_lead": "Session facilitators and moderators",
    "toc_principles": "Organization principles",
    "toc_mixed": "MIXED groups",
    "toc_specialty": "Discipline-Specific Groups",
    "toc_strategic": "Strategic directions",
    "toc_topics": "Topics by field",
    "toc_mixed_label": "MIXED groups",
    "toc_specialty_label": "Discipline-Specific Groups",
}

DEGREE_SUFFIX_RE = re.compile(
    r"\s*/\s*(Prof\.\s*Dr\.{1,2}|Dr\.)\s*$",
    re.IGNORECASE,
)

NAME_HEADERS = {"Ad, soyad", "Moderator", "Moderatorlar"}
SPECIALTY_HEADERS = {"İxtisas", "Elm sahəsi"}
COUNTRY_HEADERS = {"Ölkə"}


class SessionsTranslator:
    """Translate sessions page content from Azerbaijani source strings."""

    def __init__(
        self,
        profiles_by_key: dict[str, dict],
        person_key_fn: Callable[[str], str],
    ) -> None:
        self.profiles_by_key = profiles_by_key
        self.person_key_fn = person_key_fn

    def header(self, label: str) -> str:
        return TABLE_HEADER_EN.get(label, label)

    def photo_header(self) -> str:
        return PHOTO_HEADER_EN

    def cell(self, header: str, value: str, person_name: str = "") -> str:
        clean_header = header.strip().rstrip(",")
        if clean_header in NAME_HEADERS:
            return self.name(value)
        if clean_header in COUNTRY_HEADERS:
            return self.country(value)
        if clean_header == "Elm sahəsi":
            return self.field_area(value)
        if clean_header in SPECIALTY_HEADERS:
            return self.specialty(value, person_name or value)
        return value

    def field_area(self, raw: str) -> str:
        text = raw.strip()
        if text in SPECIALTY_EN:
            return SPECIALTY_EN[text]
        return text

    def name(self, raw: str) -> str:
        clean = raw.strip().rstrip(",").strip()
        if not clean:
            return clean
        profile = self._profile(clean)
        if profile and profile.get("name_en"):
            return profile["name_en"]
        return latin_display_name(clean)

    def country(self, raw: str) -> str:
        text = raw.strip()
        return COUNTRY_EN_EXT.get(text, text)

    def field_group(self, raw: str) -> str:
        return FIELD_GROUP_EN.get(raw.strip(), raw.strip())

    def table_title(self, masa_title: str) -> str:
        match = re.fullmatch(r"MASA\s+(\d+)", masa_title.strip(), re.I)
        if match:
            return f"TABLE {match.group(1)}"
        return masa_title

    def specialty(self, raw: str, person_name: str = "") -> str:
        text = raw.strip()
        if not text:
            return text
        person_key = self.person_key_fn(person_name.strip().rstrip(",").strip())
        fixed = MODERATOR_SPECIALTY_EN.get(person_key)
        if fixed:
            return fixed
        if text in SPECIALTY_EN:
            return SPECIALTY_EN[text]
        profile = self._profile(person_name)
        if profile:
            field_en = (profile.get("field_en") or "").strip()
            degree = extract_degree_suffix(text)
            if field_en and degree:
                return f"{field_en} / {degree}"
            if field_en and not degree:
                return field_en
        mapped = FIELD_EN.get(text, "")
        if mapped:
            return mapped
        degree_match = DEGREE_SUFFIX_RE.search(text)
        if degree_match:
            field_part = text[: degree_match.start()].strip(" /")
            translated_field = SPECIALTY_EN.get(field_part) or FIELD_EN.get(field_part, field_part)
            return f"{translated_field} / {degree_match.group(1).strip()}"
        return text

    def localize_intro(self, sections: list[dict]) -> list[dict]:
        localized: list[dict] = []
        for section in sections:
            sid = section.get("id", "")
            en = INTRO_SECTIONS_EN.get(sid)
            if not en:
                localized.append(section)
                continue
            copy = dict(section)
            copy.update(en)
            localized.append(copy)
        return localized

    def _profile(self, name: str) -> dict | None:
        key = self.person_key_fn(name.strip().rstrip(",").strip())
        return self.profiles_by_key.get(key)


def extract_degree_suffix(text: str) -> str:
    match = DEGREE_SUFFIX_RE.search(text.strip())
    if match:
        return match.group(1).strip()
    return ""
