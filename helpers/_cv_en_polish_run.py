# -*- coding: utf-8 -*-
"""Deterministic + rule-based English CV polish, then apply to Word files."""
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

from _cv_en_polish_profile_fixes import PROFILE_FIXES
from _cv_en_polish_lib import EN_CV_DIR, META_PHRASE_RE, apply_cv, extract_all

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "helpers" / "_cv_en_polish_extract.json"
EDITS = ROOT / "helpers" / "_cv_en_polish_edits.json"


def clean_spaces(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def polish_cell(text: str) -> str:
    if not text:
        return text
    t = text
    # Remove meta hedges in table cells
    t = re.sub(r"\s*Year not stated\.?", "", t, flags=re.I)
    t = re.sub(r"\s*Years? not (stated|given)\.?", "", t, flags=re.I)
    t = re.sub(
        r"\s*The CV (states|lists|gives|reports|mentions|does not[^.]*|notes|spells|title is)[^.]*\.?",
        "",
        t,
        flags=re.I,
    )
    t = re.sub(
        r"\s*The employment record (states|says|lists)[^.]*\.?",
        "",
        t,
        flags=re.I,
    )
    t = re.sub(
        r"\s*The CV gives both labels for \d{4}\.?",
        "",
        t,
        flags=re.I,
    )
    t = re.sub(
        r"Seven published papers and conference participation are mentioned, without titles\.?",
        "Seven published papers and conference presentations.",
        t,
        flags=re.I,
    )
    t = re.sub(
        r"The employment record states that the dissertation was submitted in (\d{4})\.?",
        r"Dissertation submitted in \1.",
        t,
        flags=re.I,
    )
    t = re.sub(r"\bAssociated Professor\b", "Associate Professor", t)
    t = re.sub(r"\bProf\. Dr\.\b", "Professor", t)
    t = clean_spaces(t)
    t = re.sub(r"\s*;\s*$", "", t)
    t = re.sub(r"\s*,\s*$", "", t)
    return t


def polish_header_line(text: str, index: int) -> str:
    if index == 0:
        return text  # CURRICULUM VITAE
    t = text
    t = re.sub(r"\bAssociated Professor\b", "Associate Professor", t)
    t = re.sub(r"\bProf\. Dr\.\b", "Professor", t)
    # Soften parenthetical meta
    t = re.sub(
        r"\s*\(head of the sociology department until August 2024\)",
        "",
        t,
        flags=re.I,
    )
    return clean_spaces(t)


def polish_profile(profile: str, header: list[str], file: str) -> str:
    if not profile:
        return profile
    t = profile

    # Specific known awkward openings / meta patches by file
    specific = SPECIFIC_PROFILES.get(file)
    if specific:
        return clean_spaces(specific)

    # Generic meta removals / rewrites
    replacements = [
        (
            r"\ba rank the CV spells Associated Professor and dates from (\d{4})\b",
            r"an associate professor since \1",
        ),
        (
            r"\ba rank the CV spells Associated Professor\b",
            "an associate professor",
        ),
        (r"\bThe professor title is dated ([^.]+)\.", r"He was appointed professor on \1."),
        (r"\bThe associate-professor title is dated ([^.]+)\.", r"She was appointed associate professor on \1."),
        (r"\bThe CV gives her specialty as ([^.]+)\.", r"Her specialty is \1."),
        (r"\bThe CV gives his title as Prof\. Dr\. and does not name a doctorate\.", ""),
        (r"\bThe CV heading gives the degree PhD\.", "He holds a PhD."),
        (r"\bThe CV does not give the years\.", ""),
        (r"\bYear not stated\.?", ""),
        (r"\bis described as a professor and doctor\.", "is a professor."),
        (r"\bThe CV lists him as ([^.]+)\.", r"He has served as \1."),
        (r"\bThe CV lists ([^.]+)\.", r"His record includes \1."),
        (r"\bThe CV states ([^.]+)\.", r"\1."),
        (r"\bThe CV reports ([^.]+)\.", r"His record includes \1."),
        (r"\bThe CV describes him as ([^.]+)\.", r"He is \1."),
        (r"\bThe CV mentions ([^.]+)\.", r"\1."),
        (r"\bThe CV notes ([^.]+)\.", r"\1."),
        (r"\bPostgraduate study is recorded as ([^.]+)\.", r"He completed postgraduate study in \1."),
        (
            r"\bThe employment record states that the dissertation was submitted in (\d{4})\.",
            r"He submitted his dissertation in \1.",
        ),
        (
            r"\bSeven published papers and conference participation are mentioned, without titles\.",
            "He has seven published papers and has presented at conferences.",
        ),
        (r"\bPublications also use the spelling ([^.]+)\.", r"His publications also appear under the spelling \1."),
        (r"\bGoogle Scholar figures in the CV are ([^.]+)\.", r"Google Scholar metrics are \1."),
        (r"\bIt states ([^.]+)\.", r"His record includes \1."),
        (r"\ba post dated from ([^.]+)\.", r"a post he has held since \1."),
        (r"\ba post dated ([^.]+)\.", r"a post held since \1."),
        (r"\bThe work[^.]*title[^.]*\.", ""),
        (r"\bThe thesis[^.]*\.", lambda m: m.group(0)),  # keep unless meta - placeholder
    ]

    for pat, repl in replacements:
        if callable(repl):
            continue
        t = re.sub(pat, repl, t, flags=re.I)

    # Remove leftover empty sentences / double spaces
    t = re.sub(r"\s{2,}", " ", t)
    t = re.sub(r"\.\s*\.", ".", t)
    t = re.sub(r"\s+,", ",", t)
    t = clean_spaces(t)

    # If still contains meta phrases, strip sentences containing them
    if META_PHRASE_RE.search(t) or re.search(
        r"\b(the cv|employment record|year not stated|is described as)\b", t, re.I
    ):
        sentences = re.split(r"(?<=[.!?])\s+", t)
        kept = []
        for s in sentences:
            if re.search(
                r"\b(the cv\b|employment record|year not stated|is described as|"
                r"does not (give|name|state)|without titles)\b",
                s,
                re.I,
            ):
                continue
            kept.append(s)
        t = clean_spaces(" ".join(kept))

    return t


# Hand-crafted rewrites for profiles that need more than regex cleanup.
# Facts taken only from existing CV content.
SPECIFIC_PROFILES: dict[str, str] = {}


def load_specific_from_module() -> None:
    """Populate SPECIFIC_PROFILES with carefully rewritten summaries."""
    # Filled below in build_specific_profiles()
    SPECIFIC_PROFILES.update(build_specific_profiles())


def build_specific_profiles() -> dict[str, str]:
    d = {
        "Abdullayev_Shuay_CV_EN.docx": (
            "Shuay Abdullayev is a postdoctoral research associate at the Complex Carbohydrate Research Center "
            "of the University of Georgia in Athens, Georgia, in the group of Prof. David Crich. He received a PhD "
            "in organic chemistry from the Université du Québec à Montréal in 2021 for a thesis on the synthesis of "
            "therapeutic glyconanomaterials, supervised by Prof. René Roy. He previously studied chemistry at Baku "
            "State University and at the Université Claude Bernard Lyon 1. His publications focus on galectin ligands, "
            "sialylated oligosaccharides, neoglycolipids, and related carbohydrate chemistry. His Google Scholar h-index is 4."
        ),
        "Applebaum_Mark_CV_EN.docx": (
            "Mark Applebaum is an associate professor in the Department of Mathematics and Teaching Mathematics at "
            "Kaye Academic College of Education, a post he has held since 2018. He received an MSc from Azerbaijan "
            "State University named after Kirov in Baku (1981–1986) and a PhD from Azerbaijan State Pedagogical "
            "University (1996–2001) for a dissertation on teaching mathematics through inquiry-based problems, "
            "supervised by Peter Samovol. He completed postdoctoral studies with Roza Leikin at the University of "
            "Haifa Faculty of Education in 2006–2007."
        ),
        "Allahverdiyev_Aladdin_CV_EN.docx": (
            "Aladdin Allahverdiyev is a professor at National Research University MIET. He has served as a department "
            "head at the Fonon Research Institute of the USSR Ministry of the Electronics Industry; as professor, "
            "department head, dean, vice-rector, and first vice-rector at the Moscow State Academy of Business "
            "Administration; and as professor, head of education quality, and deputy vice-rector at MIET. He is a "
            "graduate of the Faculty of Mechanics and Mathematics of Lomonosov Moscow State University and of its "
            "postgraduate program. His record includes more than 450 works, inventions, monographs, and textbooks; "
            "supervision of seven candidates of sciences; and more than 60 talks, including 12 invited plenary lectures."
        ),
        "Ismayil_Togrul_CV_EN.docx": (
            "Togrul Ismayil is a professor at Kahramanmaraş Sütçü İmam University. He holds a doctorate in history from "
            "Lomonosov Moscow State University and a doctorate in economics from Istanbul University. He earned a "
            "bachelor’s degree in history from Lomonosov Moscow State University and a master’s degree in social "
            "structure and social change from Istanbul University. He has supervised master’s theses at Kahramanmaraş "
            "Sütçü İmam University and at TOBB University of Economics and Technology. His Russian score on the YDS "
            "examination is 93.75 (advanced)."
        ),
        "Suleymanov_Ebulfez_CV_EN.docx": (
            "Ebulfez Suleymanov was head of the Department of Sociology at Üsküdar University in Istanbul from January "
            "2012 to August 2024. From November 2022 to August 2024 he also worked at the International Turkic Academy "
            "in Astana. He is a professor with more than 150 scholarly works, including five monographs, twelve articles "
            "in Web of Science or Scopus journals, and more than 100 conference papers. His Google Scholar h-index is 10 "
            "and his i10-index is 11."
        ),
        "Sirajov_Bakhtiyar_CV_EN.docx": (
            "Bakhtiyar Sirajov worked at the International Atomic Energy Agency (IAEA) in Vienna from July 1995 until "
            "his retirement in November 2021. He was Team Leader of the Application Development Team from 2006 to 2021 "
            "and Section Head of the Application Development Section in 2020–2021, both at P5 grade. He holds a PhD in "
            "physics and mathematics. He completed postgraduate study from 1979 to 1986 at the Computer Center of the "
            "USSR Academy of Sciences in Moscow and submitted his dissertation in 1990. He also worked at I-NET GmbH in "
            "Vienna and at the Institute of Cybernetics of the Azerbaijan Academy of Sciences."
        ),
        "Bayramov_Ismikhan_CV_EN.docx": (
            "Ismihan Bayramoglu is a professor at Izmir University of Economics, where he has worked since 2001. He was "
            "dean of the Faculty of Arts and Sciences from 2001 to 2022 and chair of the Department of Mathematics from "
            "2001 to 2015. He received a PhD from Kiev State University in 1988 for a dissertation on invariant "
            "confidence intervals and statistical criteria based on training samples. He earned master’s and bachelor’s "
            "degrees in applied mathematics from Azerbaijan State University in 1981. From 1993 to 2001 he was a "
            "professor in the Department of Statistics at Ankara University. His publications also appear under the "
            "spelling Bairamov."
        ),
        "Eppelbaum_Lev_CV_EN.docx": (
            "Lev Eppelbaum works in the Department of Geosciences at Tel Aviv University. He received an MSc in "
            "geophysics from Azerbaijan State University of Oil and Industry in 1982 and a PhD in geophysics in 1989 "
            "through the All-Union Geophysical Institute in Baku, the Institute of Geophysics of the Georgian Academy "
            "of Sciences in Tbilisi, and the Moscow Mining Academy. He completed postdoctoral studies at Tel Aviv "
            "University in 1991–1993 on interpretation and modeling of potential geophysical fields in the Dead Sea "
            "Rift. Since October 2020 he has been an honorary professor at Azerbaijan State Oil and Industry University. "
            "He has 7,192 Google Scholar citations and an h-index of 46. In 2018–2019 he received the Christian Huygens "
            "Medal of the European Geosciences Union."
        ),
        "Karimi_Saadat_CV_EN.docx": (
            "Saadat Karimi is a senior lecturer and course manager at the University of Borås, with a permanent "
            "appointment since January 2021, and a university lecturer at the University of Gothenburg since January "
            "2016. He holds a PhD. From 1993 to 1999 he was a doctoral student, and from 1996 to 1999 a senior researcher "
            "and lecturer, at the Institute of Mathematics and Mechanics of the Azerbaijan National Academy of Sciences. "
            "He has also taught at the Royal Institute of Technology in Stockholm and at Umeå University, where he was "
            "responsible for national mathematics tests. His publications include books, chapters, and symposium papers, "
            "mostly on Azerbaijani history, literature, and education."
        ),
        "Asgerova_Sevinj_CV_EN.docx": (
            "Sevinj Asgerova is a professor and chief researcher at the N. I. Pirogov Russian National Research Medical "
            "University in Moscow. She is a physician and ophthalmologist-surgeon. She earned a Doctor of Sciences degree "
            "in medicine from the S. N. Fyodorov Eye Microsurgery complex in Moscow in 2005."
        ),
        "Kalantar_Khalil_CV_EN.docx": (
            "Khalil Kalantar is a senior researcher and developer at Global Optical Solutions & Kepler. He earned a "
            "bachelor’s degree in electronics engineering in 1980, a master’s degree in 1984 at Toyohashi University of "
            "Technology, a doctorate in 1987 at Nagoya University, and a further doctorate in 2003 at Tohoku University. "
            "Since 1995 his work has focused on optical devices for liquid-crystal displays, including light-guide "
            "plates. He has more than 96 articles, nearly 100 patents, three books in Japanese, and more than 15 book "
            "chapters."
        ),
        "Rustamov_Kamran_CV_EN.docx": (
            "Kamran Rustamov is scientific director of the Center for Modeling Political Communications in Moscow. He is "
            "a doctor of technical sciences, a professor, and an Honored Science Worker of the Republic of Azerbaijan. "
            "He undertook scientific training in the United Kingdom in 1977–1978 and advanced from assistant to head of "
            "department while completing candidate and doctoral dissertations. From 1991 to 1992 he was a state "
            "counselor to the President of Azerbaijan. He has more than 300 scientific works, including monographs, "
            "textbooks, and articles."
        ),
        "Ahmadov_Emil_CV_EN.docx": (
            "Emil Ahmadov is head of the Landau Department of Theoretical Physics at the Moscow Institute of Physics and "
            "Technology and a leading researcher in that institute’s High Energy Physics Laboratory and at the Institute "
            "for Theoretical and Experimental Physics in Moscow. He defended his PhD on 11 April 1998 and his "
            "habilitation on 3 June 2009. From 2005 to 2020 he was a visiting professor or researcher at the Albert "
            "Einstein Institute in Golm, and in 2002 at KEK in Tsukuba. His work has been supported by state "
            "assignments and by grants from the Basis foundation, the Dynasty foundation, and the President of the "
            "Russian Federation."
        ),
        "Aliyev_Ismayil_CV_EN.docx": (
            "Ismayil Aliyev is a professor at St. Petersburg State University of Economics in the Department of Economics "
            "and Management of Enterprises and Industrial Complexes."
        ),
        "Atakishiyev_Natig_CV_EN.docx": (
            "Natig Atakishiyev is a researcher, holding the rank of Investigador Nacional Emérito, at the Institute of "
            "Mathematics of the National Autonomous University of Mexico (UNAM)."
        ),
        "Badalov_Elchin_CV_EN.docx": (
            "Elchin Badalov is an associate professor in the Department of Oral and Maxillofacial Surgery at Istanbul "
            "Aydın University, where he has been a faculty member since 2014 and received the associate-professor title "
            "in 2023. He graduated from the Faculty of Dentistry of Istanbul University in 2007 and completed a "
            "doctorate there in oral implantology in 2014. His thesis is a histological and histomorphometric study of "
            "vascular endothelial growth factor and early bone growth in a mouse model. He has published more than 20 "
            "articles and book chapters in maxillofacial surgery and implantology, and has developed two surgical "
            "techniques and a suture method that carry his surname."
        ),
        "Efendiyev_Messoud_CV_EN.docx": (
            "Messoud Efendiyev is rector’s distinguished visiting professor at Marmara University in Istanbul and head of "
            "the Department of Dynamical Systems at Helmholtz Zentrum München."
        ),
        "Gadimov_Vahid_CV_EN.docx": (
            "Vahid Gadimov is a professor in the Department of Higher Mathematics and Programming at MIREA – Russian "
            "Technological University, and an acting professor at the Russian University of Transport. He earned a "
            "Dr. rer. nat. (Promotion A) in 1981 on contact problems of plastic flow in a thin metal layer, and a "
            "habilitation / Doctor of Science (Promotion B) in 2000 on nonstationary contact problems of flow in a thin "
            "plastic layer. He was a senior researcher and professor at the Institute of Mathematics and Mechanics in "
            "Baku from 1980 to 1997. He has more than 200 research publications and more than 45 textbooks, including "
            "16 key works."
        ),
        "Gayibli_Khagani_CV_EN.docx": (
            "Khagani Gayibli is director of the Turkish Language Center at the University of Tartu, a post he has held "
            "since 1998. He received a PhD in history from the University of Tartu."
        ),
        "Gojayev_Zahid_CV_EN.docx": (
            "Zahid Gojayev is deputy director for innovation and implementation at the Federal Scientific Agroengineering "
            "Center VIM and a professor at Moscow Polytechnic University."
        ),
        "Guliyev_Arif_CV_EN.docx": (
            "Arif Guliyev is a professor in the Department of Constitutional Law, International Law and Public-Law "
            "Subjects at the Kyiv University of Intellectual Property and Law."
        ),
        "Guliyeva_Aynur_CV_EN.docx": (
            "Aynur Guliyeva is an associate professor at the University of Technology Tarbes Occitanie Pyrénées, where "
            "she has worked since January 2024. She received a PhD in chemistry of materials."
        ),
        "Heyet_Mehmet_Riza_CV_EN.docx": (
            "Mehmet Riza Heyet teaches in the Department of Contemporary Turkic Dialects and Literatures at Ankara "
            "University, a post he has held since 2013. He has been concession holder and editor-in-chief of the journal "
            "Varliq since 2015 and head of the Tabriz Research Institute (TEBAREN) since 2016. He received a doctorate "
            "from Ankara University in 2021 on Mirza Mehdi Khan Astarabadi’s Sanglakh, and a master’s degree there in "
            "2005. He studied Azerbaijani language and literature at N. Tusi Pedagogical University (1993–1995) and "
            "Baku State University (1995–1998). His publications and talks address Iranian Turkic press, language, and "
            "identity."
        ),
        "Jannataliyev_Rasim_CV_EN.docx": (
            "Rasim Jannataliyev is a project manager for intelligent energy systems at EnBW AG in Stuttgart, where he "
            "has worked since June 2013. He holds a PhD (Dr.-Ing.) from Azerbaijan Technical University (2004–2007). His "
            "thesis examined the thermal properties of heat-transfer fluids for absorption refrigeration machines and "
            "heat pumps. Earlier he was a research assistant at the University of Rostock and at Azerbaijan Technical "
            "University, and a guest scientist at the Stuttgart University of Applied Sciences. He works in German, "
            "Azerbaijani, Turkish, and Russian."
        ),
        "Khalilova_Saida_CV_EN.docx": (
            "Saida Khalilova is founder and director of the Royal Conservatory of Music and Art in Muscat, a post she "
            "has held since November 2023, and an associate professor at the Baku Music Academy since October 2011. She "
            "received a PhD in music pedagogy from the Baku Music Academy in 2014 and a Master of Arts in music there "
            "in 1996. She taught piano at Sultan Qaboos University from 2011 to 2018 and at music colleges in Baku and "
            "Shusha. Her publications include a 2016 book and several papers on Elmira Aliyeva and piano education in "
            "Azerbaijan."
        ),
        "Mammadov_Agamali_CV_EN.docx": (
            "Agamali Mammadov is professor and head of the Department of Sociology of Communication Systems at the "
            "Faculty of Sociology of Lomonosov Moscow State University."
        ),
        "Mammadov_Nizami_CV_EN.docx": (
            "Nizami Mammadov is a professor at the Russian Presidential Academy of National Economy and Public "
            "Administration in Moscow, where he has worked since 1995."
        ),
        "Masumova_Nigar_CV_EN.docx": (
            "Nigar Masumova is an associate professor in the Department of World Economy at MGIMO University in Moscow "
            "and head of the Department of Advertising and Public Relations."
        ),
        "Mehdiyev_Gafar_CV_EN.docx": (
            "Gafar Mehdiyev is a professor at Erciyes University in Kayseri in the Department of Armenian Language and "
            "Culture, a title he has held since 2016."
        ),
        "Mehmedov_Emirullah_CV_EN.docx": (
            "Emirullah Mehmedov is an emeritus professor and leading researcher at the Nanotechnology Research Center "
            "of Bilkent University, where he has worked since 2011."
        ),
        "Najafoglu_Hajali_CV_EN.docx": (
            "Hajali Najafoglu is professor of inorganic chemistry at Kafkas University. He earned a doctorate in "
            "inorganic chemistry from the Azerbaijan Academy of Sciences and a master’s degree in organic chemistry."
        ),
        "Rahimov_Aliheydar_CV_EN.docx": (
            "Aliheydar Rahimov is a professor in the Department of Anesthesiology and Intensive Care at I. M. Sechenov "
            "First Moscow State Medical University, a post he has held since 2021. He has also headed the Department of "
            "Transfusiology at the Russian Scientific Center of Surgery named after B. V. Petrovsky since 1992. He "
            "graduated from the N. Narimanov Azerbaijan State Medical Institute in 1976, received the Candidate of "
            "Medical Sciences degree in 1980, the Doctor of Medical Sciences degree in 1988, and the title of professor "
            "in hematology and blood transfusion in 1993. He has more than 390 scientific works, including 18 "
            "monographs and 13 textbooks; has supervised 15 candidate and six doctoral dissertations; and holds four "
            "inventions."
        ),
        "Sultansoy_Saleh_CV_EN.docx": (
            "Saleh Sultansoy is a professor at TOBB University of Economics and Technology in Ankara, where he has "
            "worked since 2007, and a leading researcher at the Institute of Physics of the Azerbaijan National Academy "
            "of Sciences."
        ),
        "Zeynalova_Khadija_CV_EN.docx": (
            "Khadija Zeynalova is an associate professor at the Detmold University of Music and artistic director of "
            "the Bridge of Sound orchestra and of the Harmony of Sounds ensemble."
        ),
        "Ahmedoglu_Shahin_CV_EN.docx": (
            "Shahin Ahmedoglu is a professor in the history of Islamic sects at the Faculty of Islamic Sciences of "
            "Kırıkkale University. He was appointed professor on 7 March 2022 and received the associate-professor title "
            "from the Interuniversity Council on 19 October 2015. He earned a doctorate in the history of Islamic sects "
            "from Ankara University (2001–2005), a master’s degree in the same field (1998–2001), and a bachelor’s "
            "degree in theology (1993–1998), all at Ankara University. Since 2023 he has chaired the department of "
            "basic Islamic sciences and the program in the history of Islamic sects."
        ),
        "Aliyev_Ramin_CV_EN.docx": (
            "Ramin Aliyev is a professor of guidance and psychological counseling at Hasan Kalyoncu University in "
            "Gaziantep. He was appointed professor on 27 March 2024."
        ),
        "Genceli_Mehdi_CV_EN.docx": (
            "Mehdi Genceli is an associate professor in the Department of Turkish Language and Literature at the "
            "Institute of Turkic Studies of Marmara University in Istanbul. He has held a faculty appointment there "
            "since 4 January 2012 and has been deputy director of the institute since 1 January 2018. He received a "
            "doctorate at the same institute (2002–2008) on the life, art, and works of the Azerbaijani poet Muhammad "
            "Hadi, supervised by Muhammet Gür, after a master’s degree there (1999–2002) and a bachelor’s degree in "
            "Turkish language and literature at Marmara University (1993–1999)."
        ),
        "Mammadli_Barmanbay_Afina_CV_EN.docx": (
            "Afina Barmanbay is an associate professor of Azerbaijani Turkish and literature at Kafkas University in "
            "Kars. She was appointed associate professor on 20 January 2021. She completed an integrated doctorate at "
            "the Azerbaijan National Academy of Sciences in literature; her thesis, Ehmed Cavad ve Türkiye, was "
            "defended in 2010 with advisor Bekir Nebiyev, and the degree was awarded on 12 January 2011. She earned a "
            "bachelor’s degree in Azerbaijani language and literature from Azerbaijan State Pedagogical University "
            "(1989–1994). She was head of the department in 2017–2018."
        ),
        "Musayev_Yashar_CV_EN.docx": (
            "Yashar Musayev is head of development for new energy business at Siemens Energy AG in Erlangen and Munich, "
            "an executive post he has held since May 2020. His work covers green hydrogen, electrolysis, fuel technology, "
            "and renewable energy, with about 32 direct reports. He holds a Dr.-Ing. from Friedrich-Alexander University "
            "Erlangen-Nuremberg (doctoral research, 1998–2001) and a Dipl.-Ing. in mechanical engineering technology "
            "from the Technical University of Azerbaijan (1984–1991), with distinction. From 2005 to 2020 he worked at "
            "Schaeffler AG, including as senior vice president and head of the Competency Center for Surface Technology "
            "from 2015 to 2020."
        ),
        "Rzayev_Teymur_CV_EN.docx": (
            "Teymur Rzayev is a professor in the Department of Plastic Arts at Yeditepe University. He earned his "
            "doctorate from Azerbaijan State University of Fine Arts."
        ),
    }
    d.update(PROFILE_FIXES)
    return d


def polish_item(item: dict) -> dict:
    out = deepcopy(item)
    out["header"] = [
        polish_header_line(h, i) for i, h in enumerate(item.get("header") or [])
    ]
    out["profile"] = polish_profile(
        item.get("profile") or "", item.get("header") or [], item["file"]
    )
    new_tables = []
    for table in item.get("tables") or []:
        rows = []
        for row in table.get("rows") or []:
            rows.append([polish_cell(c) for c in row])
        new_tables.append({"section": table["section"], "rows": rows})
    out["tables"] = new_tables
    out["needs_meta_cleanup"] = bool(META_PHRASE_RE.search(out["profile"]))
    return out


def main() -> None:
    load_specific_from_module()
    if not EXTRACT.is_file():
        extract_all(EXTRACT)
    items = json.loads(EXTRACT.read_text(encoding="utf-8"))
    polished = [polish_item(x) for x in items]
    EDITS.write_text(json.dumps(polished, ensure_ascii=False, indent=2), encoding="utf-8")

    still_meta = [x["file"] for x in polished if META_PHRASE_RE.search(x["profile"])]
    print(f"polished {len(polished)} profiles; still_meta={len(still_meta)}")
    for f in still_meta:
        print(" META", f)

    # Apply
    changed = 0
    for edit in polished:
        path = EN_CV_DIR / edit["file"]
        changes = apply_cv(path, edit)
        if changes:
            changed += 1
            print(f"UPDATED {edit['file']}: {len(changes)} edits")
    print(f"files_changed={changed}")


if __name__ == "__main__":
    main()
