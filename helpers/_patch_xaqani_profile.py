#!/usr/bin/env python3
"""Update Xaqani Qayıblı profile bio and card heading in scientists-profiles.json."""
from __future__ import annotations

import json

try:
    from _paths import ROOT
    from scientists_profiles_core import PROFILES_JSON, load_profiles, save_profiles
except ImportError:
    from helpers._paths import ROOT  # type: ignore
    from helpers.scientists_profiles_core import (  # type: ignore
        PROFILES_JSON,
        load_profiles,
        save_profiles,
    )

BIO_HTML_AZ = (
    '<p class="bio">Xaqani Qayıblı şair, tərcüməçi, alim və ictimai xadimdir. O, Azərbaycan ədəbiyyatı, '
    "dilçiliyi və jurnalistikası sahəsində geniş tədqiqatları ilə yanaşı, beynəlxalq arenada diaspor "
    "fəaliyyəti və akademik əməkdaşlıqları ilə də tanınır. &quot;Eston və türk dillərində feil "
    "quruluşlarının müqayisəsi&quot; adlı elmi işi ilə dünya dilçiliyində Fin-Uqor və Türk-Tatar "
    "dilləri arasındakı qohumluq əlaqələrini araşdıran ilk azərbaycanlı alimdir.</p>"
    '<p class="bio-section-title">Əsas Elmi Araşdırmaları və Tədqiqat Sahələri</p>'
    '<p class="bio-section-title">Türkologiya və dilçilik:</p>'
    '<ul class="awards-list"><li>&quot;Eston və türk dillərində feil quruluşlarının müqayisəsi&quot;</li>'
    '<li>&quot;Türkcə və estonca arasında dil əlaqələri və struktural fərqlər&quot;</li></ul>'
    '<p class="bio-section-title">Siyasi və mədəni əlaqələr:</p>'
    '<ul class="awards-list"><li>&quot;Estoniya ilə Türk Dünyası arasında siyasi və mədəni əlaqələr&quot;</li></ul>'
    '<p class="bio-section-title">Jurnalistika və vizual media:</p>'
    '<ul class="awards-list"><li>&quot;Yazılı mətbuatda fotoqrafiyanın əhəmiyyəti&quot;</li></ul>'
    '<p class="bio-section-title">Mükafatlar və Fəxri Adlar:</p>'
    '<ul class="awards-list">'
    '<li>&quot;Tərəqqi&quot; medalı (2022) – Azərbaycan diasporunun inkişafına verdiyi töhfəyə görə '
    "Azərbaycan Prezidenti tərəfindən təltif edilib.</li>"
    '<li>&quot;Altın Yıldız Madalyası&quot; (2024) – Türkiyə Respublikası Türk Dünyası Araşdırmaları '
    "Beynəlxalq Elmlər Akademiyası tərəfindən verilib.</li>"
    '<li>&quot;Diaspor fəaliyyətində xidmətə görə&quot; medalı (2024) – Azərbaycan Respublikası '
    "Diasporla İş üzrə Dövlət Komitəsi tərəfindən təqdim edilib.</li></ul>"
    '<p class="bio-section-title">Nəşrlər və Ədəbi Fəaliyyət:</p>'
    '<p class="bio">Xaqani Qayıblı həm elmi-publisistik məqalələrin, həm də şeir və nəsr əsərlərinin '
    "müəllifidir. Əsərləri eston, gürcü, rus, latış, alman, ingilis və digər türk dillərinə tərcümə olunub.</p>"
    '<ul class="awards-list">'
    "<li>40-dan çox ictimai-siyasi, tarixi və elmi-mədəni məqalənin,</li>"
    "<li>6 kitab və 1 monoqrafiyanın,</li>"
    "<li>2 elmi jurnalda dərc olunmuş 4 elmi məqalənin müəllifidir.</li>"
    "<li>20-dən çox beynəlxalq simpozium və konfransın məruzəçisi və iştirakçısıdır.</li></ul>"
    '<p class="bio-section-title">Peşəkar və Akademik Fəaliyyət:</p>'
    '<ul class="awards-list">'
    "<li>Fin-Uqor və Türk Xalqları Araşdırma Mərkəzi – sədr</li>"
    "<li>Tartu Universiteti (Estoniya) – Türk Dili Mərkəzinin müdiri</li>"
    "<li>Dünya Azərbaycanlıları Konqresi – İdarə Heyətinin üzvü, sədr müavini</li>"
    "<li>Estoniya-Azərbaycan Cəmiyyəti – sədr</li>"
    "<li>Dünya Azərbaycanlı Alimlər Dərnəyi – Təşkilat Komitəsinin üzvü</li>"
    "<li>Azərbaycan Yazıçılar Birliyi – üzv</li>"
    "<li>Estoniya Akademik Şərqşünaslar Cəmiyyəti – üzv</li>"
    "<li>Türk Ədəbiyyatı Vakfı – fəxri üzv</li></ul>"
    '<p class="bio-section-title">Diplomatik və Tərcüməçilik Fəaliyyəti:</p>'
    '<p class="bio">Xaqani Qayıblı Estoniyada və Türkiyədə yüksək səviyyəli rəsmi görüşlərdə tərcüməçi '
    "kimi iştirak edib. O, Azərbaycan, Türkiyə və Estoniya prezidentlərinin, parlament sədrlərinin və "
    "nazirlərinin rəsmi səfərlərində xüsusi tərcüməçi olub.</p>"
)


def main() -> None:
    profiles = load_profiles()
    n = 0
    for p in profiles:
        if (p.get("email") or "").strip().lower() != "hakan@ut.ee":
            continue
        p["bio_html_az"] = BIO_HTML_AZ
        p["name_heading_az"] = "XAQANİ QAYIBLI"
        p["name_heading_en"] = "KHAGANI GAYIBLI"
        n += 1
    if not n:
        raise SystemExit("Xaqani profile (hakan@ut.ee) not found")
    save_profiles(profiles)
    print(f"Updated {n} profile in {PROFILES_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
