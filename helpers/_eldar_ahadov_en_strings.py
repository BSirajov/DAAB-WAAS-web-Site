"""English strings for Eldar Ahadov literary pages."""
from __future__ import annotations

import json
from pathlib import Path

_TRANSLATIONS_PATH = Path(__file__).with_name("_eldar_ahadov_en_translations.json")
TRANSLATIONS: dict[str, str] = json.loads(
    _TRANSLATIONS_PATH.read_text(encoding="utf-8")
)

EN_OZUM_BIO_PARAS: list[str] = [
    "Eldar Ahadov",
    "Born in Baku on 19 July 1960, he graduated from the St Petersburg Mining University and worked as a chief specialist at the TNK-BP (Tyumen Oil Company–British Petroleum) joint venture and later at Rosneft.",
    "A traveller and researcher of the Arctic and Siberia, he is the author of 110 books—fiction, poetry, research and scholarly articles—published in Azerbaijani, English, Spanish, Italian, Chinese, Russian and Serbian. His books have appeared in Azerbaijan, Egypt, India, Canada, China, Mexico, Russia, Serbia, the United States and Türkiye. He is an honorary member of the Azerbaijan Writers’ Union (2021); an academician of the International Academy of Literature, Art, Culture and Social Sciences (2025, Uzbekistan); a member of the Russian Writers’ Union (since 2000) and of the board of its Krasnoyarsk branch; a member of the Russian National Geographic Society (2016) and PEN International; co-chair of the Literary Council of the Assembly of Peoples of the World (2020); head of the Coordination Council of the World Writers’ Organisation (2024); chair of the Toponymy Commission of the Krasnoyarsk branch of the Russian Geographical Society (2024); and executive editor of Reader’s Choice magazine (Mumbai, India, 2024–2026).",
]

EN_OZUM_AWARDS_TITLE: str = "Most important awards"

EN_OZUM_AWARDS_ITEMS: list[str] = [
    "Silver Medal of the World Writers’ Organisation “For Contribution to the Development of World Literature” (2024, Abuja, Nigeria);",
    "Laureate of the Naji Naaman International Prize (2024, Lebanon);",
    "Silver Medal of the Eurasian Literary Festival, in the category “Preserving National Identity in Works Created in a Foreign Language” (2019, Baku, Azerbaijan);",
    "Silver Medal of the All-Russian Literary Competition and Festival (2019, Tyumen, Russia);",
    "First Prize in Poetry in the international online competition “For Peace” — Charity in Art (2013, Moscow);",
    "Second Prize in Prose in the international online competition “For Peace” — Charity in Art (2012, Moscow);",
    "Individual grant of the Governor of Krasnoyarsk Krai for culture (2008, Krasnoyarsk);",
    "Literary cash prize of the Governor of the Yamalo-Nenets Autonomous Okrug, in the category “Fiction and Non-fiction” (2017, Salekhard, Yamalo-Nenets Autonomous Okrug);",
    "Letter of appreciation from the Legislative Assembly of the Yamalo-Nenets Autonomous Okrug “For Contribution to the Cultural Development of the Yamalo-Nenets Autonomous Okrug” (2022, Salekhard);",
    "Letter of appreciation from the Governor of Krasnoyarsk Krai “For Conscientious Work, High Professionalism, and Contribution to the Development of Culture in Krasnoyarsk Krai” (2025);",
    "Certificate of Merit from the Ministry of Culture of Krasnoyarsk Krai “For Conscientious Work and Personal Contribution to the Development of Culture in Krasnoyarsk Krai” (2020);",
    "Cash prize of the Russian Council of Muftis for second place in the competition “The Prophet Muhammad — Mercy to the Worlds” (2011, Moscow);",
    "Winner’s diploma in the Essay category of the ZA-ZA Verlag International Literary Competition (2018, Düsseldorf, Germany);",
    "Winner’s diploma of the Vincenzo Padula International Literary Competition in Italian (2022, Saracena, Calabria, Italy);",
    "Silver badge of the Russian Union of Mining Specialists “For Significant Contribution to the Development of Geodesy and to Ensuring the Rational Use and Protection of Mineral Resources” (Moscow, Order No. 07/08 of 4 May 2016);",
    "Medal “100 Years of the Geodetic and Cartographic Service in Russia” of the Tyumen Regional Geodetic Centre (19 March 2019, Tyumen);",
    "Medal of the International Elite Union of Public Diplomacy “Outstanding Writer of Russia and the Turkic World” (2020, Kazakhstan);",
    "Sultan Baybars Medal “For Outstanding Service to the International Literary Movement” (2024, Kazakhstan);",
    "Silver badge of the winner of the 2007 Russian Silver Pen Competition.",
]

EN_OZUM_BERENGARTEN: tuple[str, str, str] = (
    "Eldar Ahadov is an outstanding Azerbaijani poet writing in Russian. Ahadov embodies many identities: he is a scholar, geologist, Arctic explorer, driller, linguist, critic, educator and teacher. While celebrating the physical universe around and within us, he also explores the mysterious metaphysical questions posed by our world, at once infinite and microscopic. The poet’s spirit unites passionate intellectual inquiry, compassion and generosity. His poems evoke both suffering and joy, but above all they are distinguished by the hope they radiate. For these qualities, Ahadov is not only an exemplary person of our time, but also a model for our age and its future. He is not merely an internationalist; he is also an imaginationalist.",
    "Richard Berengarten",
    "Cambridge, June 2020",
)

EN_NAV_TITLES: dict[str, str] = {
    "eldar-ahadov": "About me",
    "eldar-ahadov-poeziya": "Poetry",
    "eldar-ahadov-poetik-dastanlar": "Poetic epics and legends",
    "eldar-ahadov-bedii-nesr": "Literary prose",
    "eldar-ahadov-esse": "Essay"
}

EN_CANONICAL_H2: dict[str, list[str]] = {
    "poeziya": [
        "Tree",
        "You will understand",
        "The call to prayer",
        "I will return to that place once more",
        "If one day everyone turns away from you",
        "Youth and old age",
        "Calling a doctor",
        "Let us be human",
        "Light has no shadow",
        "A father of paper",
        "Do not leave me",
        "My martyrs",
        "Miracle",
        "It is snowing",
        "Except for you",
        "A kind word",
    ],
    "poetik": [
        "The Azerbaijan epic — Khari Bulbul",
        "Index of names mentioned in the Khari Bulbul epic",
    ],
    "bedii": [
        "Feelings of the homeland",
        "Khadija",
        "Jidir Plain",
        "Light",
        "The pistachio tree",
        "Forbidden",
        "Whom am I greater than …",
        "Son",
        "I am not saying farewell",
        "My mother's dolma",
    ],
    "esse": [
        "Monument of Mercy",
    ],
}
