"""English display names for prominent-figure profiles (slug → accepted Latin form)."""
from __future__ import annotations

import re

# Canonical English names keyed by profile slug (filename without .html).
PROMINENT_FIGURE_NAME_EN: dict[str, str] = {
    # — Azerbaijani & Turkic heritage —
    "abay_qunanbayev": "Abay Kunanbayev",
    "abdulla_qodiriy": "Abdulla Qadiri",
    "abdulla_shaiq": "Abdulla Shaig",
    "abdurehim_otkur": "Abdurrahim Otkur",
    "alp_arslan": "Alp Arslan",
    "asiq_veysel": "Ashiq Veysel",
    "azad_mirzecanzade": "Azad Mirzajanzade",
    "aziz_sancar": "Aziz Sancar",
    "behruz_kengerli": "Behruz Kangarli",
    "bekir_chobanzade": "Bekir Chobanzade",
    "berdax": "Berdakh",
    "bilge_xaqan": "Bilge Khagan",
    "biruni": "Al-Biruni",
    "bulbul": "Bulbul Murtuza Mammadov",
    "cahit_arf": "Cahit Arf",
    "cefer_cabbarli": "Jafar Jabbarli",
    "celil_memmedquluzade": "Jalil Mammadguluzade",
    "chingiz_aytmatov": "Chingiz Aytmatov",
    "ebu_bekr_tehrani": "Abu Bakr Tehrani",
    "ebulfez_elchibey": "Abulfaz Elchibey",
    "ehmed_bey_agaoglu": "Ahmed bey Agaoglu",
    "ehmed_cavad": "Ahmad Javad",
    "ehmed_yesevi": "Ahmad Yasawi",
    "el_ferabi": "Al-Farabi",
    "eli_bey_huseynzade": "Ali bey Huseynzade",
    "eli_quscu": "Ali Qushji",
    "eliaga_vahid": "Aliaga Vahid",
    "elishir_nevai": "Ali-Shir Nava'i",
    "elkey_margulan": "Alkey Margulan",
    "evliya_celebi": "Evliya Celebi",
    "fikret_emirov": "Fikret Amirov",
    "fuat_koprulu": "Mehmet Fuat Koprulu",
    "fuzuli": "Muhammad Fuzuli",
    "gabdulla_tukay": "Gabdulla Tukay",
    "haci_bektas_veli": "Haji Bektash Veli",
    "halime_edib_adivar": "Halide Edib Adivar",
    "hemze_hekimzade_niyazi": "Hamza Hakimzade Niyazi",
    "hesen_bey_zerdabi": "Hasan bey Zardabi",
    "heyder_eliyev": "Heydar Aliyev",
    "huseyn_bayqara": "Husayn Bayqara",
    "huseyn_cavid": "Husayn Javid",
    "ibn_sina": "Ibn Sina",
    "ismail_qaspirali": "Ismail Gasprinski",
    "kadizade_rumi": "Qadi Zada al-Rumi",
    "katib_celebi": "Katib Celebi",
    "kul_tigin": "Kul Tigin",
    "lutfi_zade": "Lotfi Zadeh",
    "mahmud_kasqari": "Mahmud al-Kashgari",
    "mahmud_qeznevi": "Mahmud al-Ghaznavi",
    "maqtimqulu_feraqi": "Mahtumkuli Firaqi",
    "matrakci_nasuh": "Matrakci Nasuh",
    "mehemmed_emin_resulzade": "Mammad Amin Rasulzade",
    "memmed_seid_ordubadi": "Muhammad Said Ordubadi",
    "mikayil_musfiq": "Mikayil Mushfiq",
    "mimar_sinan": "Mimar Sinan",
    "mireli_qashqay": "Mirali Ghashghai",
    "mirze_elekber_sabir": "Mirza Alekber Sabir",
    "mirze_feteli_axundzade": "Mirza Fatali Akhundov",
    "molla_penah_vaqif": "Molla Panah Vagif",
    "musa_celil": "Musa Jalil",
    "mustafa_kamal_ataturk": "Mustafa Kemal Ataturk",
    "muxtar_euezov": "Mukhtar Auezov",
    "namiq_kamal": "Namik Kemal",
    "nazim_hikmet": "Nazim Hikmet",
    "nehqsbend": "Baha ud-Din Naqshband",
    "neriman_nerimanov": "Nariman Narimanov",
    "nesimi": "Imadaddin Nasimi",
    "nesireddin_tusi": "Nasir al-Din al-Tusi",
    "nizami_gencevi": "Nizami Ganjavi",
    "oljas_suleymenov": "Olzhas Suleimenov",
    "omer_xeyyam": "Omar Khayyam",
    "orhan_pamuk": "Orhan Pamuk",
    "piri_reis": "Piri Reis",
    "qanish_setbayev": "Ganiash Satbayev",
    "qara_qarayev": "Gara Garayev",
    "qasim_bey_zakir": "Gasim bey Zakir",
    "qasim_tinistanov": "Gasim Tinishstanov",
    "qayum_nasiri": "Qayyum Nasiri",
    "qazi_burhaneddin": "Qazi Burhan al-Din",
    "qorqud_ata": "Dede Korkut",
    "reshid_behbudov": "Rashid Behbudov",
    "sabahattin_ali": "Sabahattin Ali",
    "sedri_meqsudi_arsal": "Sadri Maksud Arbey",
    "semed_vurgun": "Samad Vurgun",
    "seydi_eli_reis": "Seydi Ali Reis",
    "seyid_ezim_sirvani": "Sayyid Azim Shirvani",
    "shah_ismayil_xetai": "Shah Ismail Khatai",
    "sihabeddin_mercani": "Shihab ad-Din al-Marjani",
    "taqieddin_resedci": "Taqi al-Din al-Rasid",
    "tofiq_quliyev": "Tofig Guliyev",
    "tonyukuk": "Tonyukuk",
    "ulubey": "Ulugbek Mirza Muhammad",
    "uzeyir_hacibeyov": "Uzeyir Hajibeyov",
    "xudu_memmedov": "Khudu Mammadov",
    "yunus_emre": "Yunus Emre",
    "yusif_balasaqunlu": "Yusuf Balasaguni",
    "yusif_memmedeliyev": "Yusif Mammadaliyev",
    "yusif_vezir_chemenzeminli": "Yusif Vazir Chamanzaminli",
    "zahireddin_mehemmed_babur": "Zahir ud-Din Muhammad Babur",
    "zeki_velidi_togan": "Zeki Velidi Togan",
    "ziya_gokalp": "Ziya Gokalp",
    # — World scientists (standard English forms; ASCII where needed for consistency) —
    "erwin_schrodinger": "Erwin Schrodinger",
}

# Alternate Azerbaijani forms seen in profile body text → English display name.
_AZ_NAME_ALIASES: dict[str, str] = {
    "Abdulla Şaiq": "Abdulla Shaig",
    "Şaiq": "Shaig",
    "Bilgə Xaqan": "Bilge Khagan",
    "Kül Tigin": "Kul Tigin",
    "Əl-Biruni Əbu Reyhan": "Al-Biruni",
    "Əl-Biruni": "Al-Biruni",
    "Bəkir Çobanzadə": "Bekir Chobanzade",
    "Lütfi Zadə": "Lotfi Zadeh",
    "Zadə": "Zadeh",
    "Zadənin": "Zadeh's",
    "Nəvai": "Navoi",
    "Nəsimi": "Nasimi",
    "Çobanzadə": "Chobanzade",
    "Bəhruz Kəngərli": "Behruz Kangarli",
    "Kəngərli": "Kangarli",
    "Məhəmməd Əmin Rəsulzadə": "Mammad Amin Rasulzade",
    "Rəsulzadə": "Rasulzade",
    "Mirzə Fətəli Axundzadə": "Mirza Fatali Akhundov",
    "Axundzadə": "Akhundov",
    "Üzeyir Hacıbəyov": "Uzeyir Hajibeyov",
    "Hacıbəyov": "Hajibeyov",
    "İbn Sina Əbu Əli": "Ibn Sina",
    "İbn Sina": "Ibn Sina",
    "Nizami Gəncəvi": "Nizami Ganjavi",
    "Mahmud Kaşğari": "Mahmud al-Kashgari",
    "Kaşğari": "al-Kashgari",
    "Bəhaəddin Nəqşbənd": "Baha ud-Din Naqshband",
    "Nəsirəddin Tusi": "Nasir al-Din al-Tusi",
    "Ömər Xəyyam": "Omar Khayyam",
    "Xəyyam": "Khayyam",
    "Əhməd Yəsəvi": "Ahmad Yasawi",
    "Yəsəvi": "Yasawi",
    "Heydər Əliyev": "Heydar Aliyev",
    "Əbülfəz Elçibəy": "Abulfaz Elchibey",
    "Elçibəy": "Elchibey",
    "Musa Cəlil": "Musa Jalil",
    "Səməd Vurğun": "Samad Vurgun",
    "Rəşid Behbudov": "Rashid Behbudov",
    "Fikrət Əmirov": "Fikret Amirov",
    "Qara Qarayev": "Gara Garayev",
    "Molla Pənah Vaqif": "Molla Panah Vagif",
    "Mirzə Ələkbər Sabir": "Mirza Alekber Sabir",
    "Cəfər Cabbarlı": "Jafar Jabbarli",
    "Hüseyn Cavid": "Husayn Javid",
    "Əhməd Cavad": "Ahmad Javad",
    "Nəriman Nərimanov": "Nariman Narimanov",
    "Muxtar Əuezov": "Mukhtar Auezov",
    "Əuezov": "Auezov",
    "Çingiz Aytmatov": "Chingiz Aytmatov",
    "Mustafa Kamal Atatürk": "Mustafa Kemal Ataturk",
    "Bülbül Murtuza Məmmədov": "Bulbul Murtuza Mammadov",
    "Bülbül": "Bulbul",
    "Abay Qunanbayev": "Abay Kunanbayev",
    "Abdulla Qodiriy": "Abdulla Qadiri",
    "Mehmet Fuat Köprülü": "Mehmet Fuat Koprulu",
    "Oljas Süleymenov": "Olzhas Suleimenov",
    "Nizaminin": "Nizami's",
}

AZ_CHAR = re.compile(r"[əğıöüşçƏĞİÖÜŞÇ]")


def english_name(slug: str, fallback: str = "") -> str:
    """Return the English display name for a profile slug."""
    if slug in PROMINENT_FIGURE_NAME_EN:
        return PROMINENT_FIGURE_NAME_EN[slug]
    return fallback or slug.replace("_", " ").title()


def az_to_en_name_map() -> dict[str, str]:
    """Build AZ display name → EN display name from slug table + aliases."""
    mapping: dict[str, str] = dict(_AZ_NAME_ALIASES)
    try:
        from _build_prominent_figures_catalog import parse_profile
        from _paths import ROOT

        for group in ("azturk", "world"):
            folder = ROOT / "az" / "prominent_figures" / group
            if not folder.is_dir():
                continue
            for path in folder.glob("*.html"):
                if path.name == "hazirlanir.html":
                    continue
                row = parse_profile(path, group)
                if not row:
                    continue
                az = row["name"]
                en = english_name(row["id"], az)
                if az and en and az != en:
                    mapping[az] = en
    except ImportError:
        pass
    return mapping


def name_replacement_pairs() -> list[tuple[str, str]]:
    """Longest-first (AZ, EN) pairs for HTML/text replacement."""
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    for az, en in az_to_en_name_map().items():
        if not az or az == en or az in seen:
            continue
        if not AZ_CHAR.search(az) and az == en:
            continue
        seen.add(az)
        pairs.append((az, en))
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    return pairs


def apply_english_names(text: str, slug: str = "") -> str:
    """Replace Azerbaijani name forms with English display names."""
    if slug:
        row_name = None
        for az, en in az_to_en_name_map().items():
            if english_name(slug, "") == en:
                row_name = (az, en)
                break
    for az, en in name_replacement_pairs():
        if az in text:
            text = text.replace(az, en)
    return text
