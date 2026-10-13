# -*- coding: utf-8 -*-
"""Shared EN→AZ terminology for scientist Word CVs."""
from __future__ import annotations

import re

# Exact phrase replacements (longer first). Applied after structural header mapping.
PHRASES: list[tuple[str, str]] = [
    ("Academic and professional positions", "Elmi və peşəkar vəzifələr"),
    ("Awards, honors and fellowships", "Mükafatlar, fəxri adlar və təqaüdlər"),
    ("Grants and research projects", "Qrantlar və tədqiqat layihələri"),
    ("Research metrics", "Elmi göstəricilər"),
    ("Participation in DAAB", "DAAB-da iştirak"),
    ("Profile summary", "Profil xülasəsi"),
    ("Contact and identifiers", "Əlaqə məlumatları və identifikatorlar"),
    ("CURRICULUM VITAE", "ELMİ CV"),
    ("Field / thesis title", "Sahə / dissertasiya mövzusu"),
    ("Institution, city, country", "Təhsil müəssisəsi, şəhər, ölkə"),
    ("Department / unit", "Kafedra / bölmə"),
    ("Award / honor", "Mükafat / fəxri ad"),
    ("Awarding body", "Təltif edən qurum"),
    ("Project title", "Layihənin adı"),
    ("Funding body", "Maliyyələşdirən qurum"),
    ("Your role", "Rolunuz"),
    ("Date checked", "Yoxlanma tarixi"),
    ("associate professor", "dosent"),
    ("Associate Professor", "Dosent"),
    ("Assistant Professor", "Baş müəllim"),
    ("assistant professor", "baş müəllim"),
    ("full professor", "professor"),
    ("Professor", "Professor"),
    ("professor", "professor"),
    ("Postdoctoral", "Postdoktorantura"),
    ("postdoctoral fellow", "postdoktorant"),
    ("Postdoctoral fellow", "Postdoktorant"),
    ("postdoctoral research associate", "postdoktorant tədqiqatçı"),
    ("Staff Scientist", "Elmi işçi"),
    ("staff scientist", "elmi işçi"),
    ("Visiting Professor", "Qonaq professor"),
    ("visiting professor", "qonaq professor"),
    ("Research Professor", "Tədqiqat professoru"),
    ("research professor", "tədqiqat professoru"),
    ("Team Leader", "Komanda rəhbəri"),
    ("Section Head", "Bölmə rəhbəri"),
    ("Vice-Rector", "Prorektor"),
    ("vice-rector", "prorektor"),
    ("dean", "dekan"),
    ("Dean", "Dekan"),
    ("chair of the Department", "kafedra müdiri"),
    ("head of the Department", "kafedra müdiri"),
    ("Head of Department", "Kafedra müdiri"),
    ("Member of the WAAS Executive Board", "DAAB İcraiyyə Şurasının üzvü"),
    ("Co-Chair of the WAAS Executive Board", "DAAB İcraiyyə Şurasının həmsədri"),
    ("Chair of the WAAS Executive Board", "DAAB İcraiyyə Şurasının sədri"),
    ("Honored Artist of the Republic of Azerbaijan", "Azərbaycan Respublikasının əməkdar artisti"),
    ("Honored Scientist of the Republic of Azerbaijan", "Azərbaycan Respublikasının əməkdar elm xadimi"),
    ("United States", "Amerika Birləşmiş Ştatları"),
    ("United Kingdom", "Birləşmiş Krallıq"),
    ("Russian Federation", "Rusiya Federasiyası"),
    ("Germany", "Almaniya"),
    ("France", "Fransa"),
    ("Turkey", "Türkiyə"),
    ("Austria", "Avstriya"),
    ("Israel", "İsrail"),
    ("Ukraine", "Ukrayna"),
    ("Poland", "Polşa"),
    ("Sweden", "İsveç"),
    ("Canada", "Kanada"),
    ("Italy", "İtaliya"),
    ("Spain", "İspaniya"),
    ("Japan", "Yaponiya"),
    ("China", "Çin"),
    ("Georgia", "Gürcüstan"),
    ("Estonia", "Estoniya"),
    ("Finland", "Finlandiya"),
    ("Netherlands", "Niderland"),
    ("Belgium", "Belçika"),
    ("Switzerland", "İsveçrə"),
    ("Hungary", "Macarıstan"),
    ("Czech Republic", "Çexiya"),
    ("Saudi Arabia", "Səudiyyə Ərəbistanı"),
    ("Azerbaijan", "Azərbaycan"),
    ("Moscow", "Moskva"),
    ("Baku", "Bakı"),
    ("Vienna", "Vyana"),
    ("Istanbul", "İstanbul"),
    ("Ankara", "Ankara"),
    ("present", "hazırda"),
    ("Native", "Ana dili"),
    ("Fluent", "Səlis"),
    ("Advanced", "İrəliləmiş"),
    ("Intermediate", "Orta"),
    ("Beginner", "Başlanğıc"),
    ("Years", "İllər"),
    ("Year", "İl"),
    ("Degree", "Dərəcə"),
    ("Position", "Vəzifə"),
    ("Institution", "Təşkilat"),
    ("Indicator", "Göstərici"),
    ("Value", "Dəyər"),
    ("Source", "Mənbə"),
    ("Level", "Səviyyə"),
    ("Number", "Say"),
    ("Notes", "Qeydlər"),
    ("Course", "Kurs"),
    ("Language", "Dil"),
    ("Supervision", "Elmi rəhbərlik"),
    ("Teaching", "Tədris fəaliyyəti"),
    ("Education", "Təhsil"),
    ("Languages", "Dillər"),
    ("bachelor’s degree", "bakalavr dərəcəsi"),
    ("Bachelor’s degree", "Bakalavr dərəcəsi"),
    ("master’s degree", "magistr dərəcəsi"),
    ("Master’s degree", "Magistr dərəcəsi"),
    ("doctoral dissertation", "doktorluq dissertasiyası"),
    ("doctorate", "doktorluq"),
]

# Section name for AZ awards table
AWARDS_SECTION_AZ = "Mükafatlar, fəxri adlar və təqaüdlər"
AWARDS_HEADER_AZ = ["İl", "Mükafat / fəxri ad", "Təltif edən qurum"]

SECTION_MAP = {
    "education": "Təhsil",
    "academic and professional positions": "Elmi və peşəkar vəzifələr",
    "awards, honors and fellowships": AWARDS_SECTION_AZ,
    "awards": AWARDS_SECTION_AZ,
    "grants and research projects": "Qrantlar və tədqiqat layihələri",
    "research metrics": "Elmi göstəricilər",
    "teaching": "Tədris fəaliyyəti",
    "supervision": "Elmi rəhbərlik",
    "languages": "Dillər",
    "participation in daab": "DAAB-da iştirak",
}


def map_section(en_section: str) -> str:
    key = (en_section or "").strip().lower()
    for en, az in SECTION_MAP.items():
        if key.startswith(en):
            return az
    return en_section


def translate_labels(text: str) -> str:
    """Apply glossary phrases to structural / short labels. Not for full prose."""
    if not text:
        return text
    out = text
    # present in date ranges
    out = re.sub(r"(?i)\bpresent\b", "hazırda", out)
    for en, az in sorted(PHRASES, key=lambda x: -len(x[0])):
        if en in out:
            out = out.replace(en, az)
    return out
