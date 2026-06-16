#!/usr/bin/env python3
"""Bring az/charter.html into structural parity with en/charter.html.

Tasks performed by this helper (idempotent):
  1. Rebuild the 26 <section class="charter-card"> blocks:
       * sentence-case .article-separate-title and <h3> headings
       * single-line titles for sections 2 and 7
       * <ol> for numbered legal lists (sec 2/5/6/9/10/12/13)
       * remove stray inline lists (sec 7)
       * fill paragraphs missing in AZ but present in EN
         (sec 7 meeting-time lead, sec 11 audit-board request,
          sec 21 split, sec 22 delegate/HQ rules, sec 24 quorum rules,
          sec 25 liquidation paragraphs, sec 26 Provisional Article 1)
       * standardise vocabulary
         ("İdarə Heyəti" instead of "Direktorlar Şurası",
          "Ümumi Yığıncaq" instead of "Baş Assambleya",
          "Birlik" instead of "Dərnək", typo fixes)
  2. Repair the duplicate `lang="az"` attribute on <html>.
  3. Repair the footer ("<div class=footer-title>" -> "<h4 class=footer-title>";
     "© 2026 DAAB / WAAS" -> "© 2026 DAAB").

Run with:  python helpers/_normalize_az_charter.py
"""
from __future__ import annotations

import re
from html import escape as h
from pathlib import Path

from _paths import ROOT


def p(text: str) -> str:
    return "<p>" + h(text, quote=False) + "</p>"


def h3(text: str) -> str:
    return "<h3>" + h(text, quote=False) + "</h3>"


def ol(items: list[str]) -> str:
    return "<ol>" + "".join("<li>" + h(item, quote=False) + "</li>" for item in items) + "</ol>"


SECTIONS: list[tuple[str, str, str, list[str]]] = [
    (
        "section-01",
        "Birliyin adı və baş qərargahı",
        "Maddə 1.",
        [
            p('Birliyin adı: "DÜNYA AZƏRBAYCANLI ALİMLƏR BİRLİYİ".'),
            p("Birliyin baş qərargahı İSTANBULdadır."),
            p("Birlik xaricdə və ölkə daxilində filiallar aça bilər."),
        ],
    ),
    (
        "section-02",
        "Birliyin məqsədi, fəaliyyət subyektləri və fəaliyyət sahəsi",
        "Maddə 2.",
        [
            p(
                "DÜNYA AZƏRBAYCANLI ALİMLƏR BİRLİYİ dünyanın müxtəlif "
                "ölkələrində yaşayan Azərbaycanlı ziyalıların birliyi kimi, "
                "elm və texnologiya, enerji, təhsil, səhiyyə, sosial elmlər "
                "və mədəniyyət sahələrinə dair strateji planların "
                "hazırlanması və tətbiq olunması işində Azərbaycana dəstək "
                "vermək məqsədi ilə qurulmuşdur."
            ),
            h3("Birlik tərəfindən həyata keçiriləcək iş mövzuları və formaları"),
            ol([
                "Fəaliyyətlərini təmin etmək və inkişaf etdirmək üçün araşdırma aparmaq;",
                "Kurslar, seminarlar, konfranslar və panellər kimi təlim-təhsil fəaliyyətlərinin təşkili;",
                "Məqsədin həyata keçirilməsi üçün zəruri olan hər cür məlumat, sənəd və nəşrləri təqdim etmək, sənədləşmə mərkəzi yaratmaq, çalışmalarını tanıtmaq üçün öz məqsədinə müvafiq olaraq qəzet, jurnal, kitab və bülletin kimi nəşrləri dərc etmək;",
                "Məqsədin həyata keçirilməsi üçün sağlam iş mühitini təmin etmək, hər cür texniki alət, avadanlıq və dəftərxana ləvazimatı ilə təmin etmək;",
                "Lazımi icazələrin alınması şərti ilə xeyriyyə fəaliyyəti ilə məşğul olmaq və yerli və xaricdən ianə qəbul etmək;",
                "Nizamnamənin məqsədlərinə çatmaq üçün lazım olan gəlirləri təmin etmək məqsədi ilə təsərrüfat, ticarət və sənaye müəssisələri yaratmaq və fəaliyyət göstərmək;",
                "Üzvlərinin faydalanmaları və asudə vaxtlarını səmərəli keçirmələri üçün klublar açmaq, sosial-mədəni obyektlər yaratmaq və bunları təchiz etmək;",
                "Üzvləri arasında bəşəri münasibətləri inkişaf etdirmək və davam etdirmək üçün yeməkli görüşlər, konsertlər, ballar, teatrlar, sərgilər, səfərlər və əyləncəli tədbirlər və s. təşkil etmək və ya bu cür tədbirlərdən üzvlərinin faydalanmasına imkan yaratmaq;",
                "Birliyin fəaliyyəti üçün lazım olan daşınan və daşınmaz əmlakı almaq, satmaq, icarəyə almaq, icarəyə vermək və daşınmaz əmlak üzərində eyni hüquqlar yaratmaq;",
                "Məqsədə nail olmaq üçün zəruri görüldüyü təqdirdə daxildə və xaricdə bir vəqf qurmaq, federasiya yaratmaq və ya qurulmuş federasiyaya qoşulmaq, lazımi icazəni alaraq birliklərin qura biləcəyi obyektlər yaratmaq;",
                "Beynəlxalq fəaliyyətlə məşğul olmaq, xaricdə birlik və ya təşkilatlara üzv olmaq və bu təşkilatlarla əməkdaşlıq etmək və ya yardımlaşmaq;",
                "Məqsədinə çatmaq üçün zəruri görüldüyü təqdirdə, 5072 saylı “Birlik və Vəqflərin Dövlət Qurumları ilə Münasibətləri haqqında” Qanunun müddəalarına xələl gətirmədən vəzifə sahələrinə aid məsələlərdə dövlət qurumları və təşkilatları ilə ortaq layihələr həyata keçirmək;",
                "Birlik üzvlərinin qida, geyim kimi zəruri ehtiyac olan mallarını və digər mal və xidmətlərlə qısamüddətli kredit ehtiyaclarını qarşılamaq məqsədi ilə fond yaratmaq;",
                "Zəruri hesab edilən yerlərdə filial və nümayəndəliklərin açılması;",
                "Birliyin məqsədi ilə bağlı olan və qanunla qadağan olunmayan sahələrdə digər birliklər və ya fondlar, ittifaqlar və bu kimi qeyri-hökumət təşkilatları ilə ortaq məqsədə çatmaq üçün platformalar yaratmaq;",
                "Məqsədinə çatmaq üçün zəruri olan və qanunla qadağan olunmayan hər cür fəaliyyətlə məşğul olmaq.",
            ]),
            h3("Birliyin fəaliyyət sahəsi"),
            p(
                "Birlik dünyanın müxtəlif ölkələrində yaşayan Azərbaycanlı "
                "ziyalıların birliyi olaraq elm və texnologiya, enerji, "
                "təhsil, səhiyyə, sosial elmlər və mədəniyyət sahələrinə "
                "dair strateji planların hazırlanmasında və həyata "
                "keçirilməsi işində Azərbaycana dəstək məqsədi ilə daxildə "
                "və xaricdə fəaliyyət göstərir."
            ),
        ],
    ),
    (
        "section-03",
        "Üzv olmaq hüququ və üzvlük qaydaları",
        "Maddə 3.",
        [
            p(
                "Hüquq qabiliyyəti olan və Birliyin məqsəd və prinsiplərini "
                "mənimsəməklə bu istiqamətdə işləməyi qəbul edən, "
                "qanunvericilikdə nəzərdə tutulmuş şərtlərə cavab verən hər "
                "bir fiziki və hüquqi şəxsin bu Birliyə üzv olmaq hüququ vardır."
            ),
            p(
                "Birliyin sədrliyinə yazılı şəkildə edilən üzvlük müraciəti "
                "Birliyin İdarə Heyəti tərəfindən ən çox otuz gün ərzində "
                "müzakirə olunur; üzvlüyün qəbul edilməsi və ya tələbin "
                "rədd edilməsi barədə qərar verilir və nəticə ərizəçiyə "
                "yazılı şəkildə bildirilir. Ərizəsi qəbul edilən üzvün adı "
                "və digər zəruri məlumatları bu məqsədlə saxlanılan "
                "dəftərdə qeyd olunur."
            ),
            p(
                "Birliyin əsl üzvləri Birliyin təsisçiləri ilə onların "
                "müraciəti əsasında İdarə Heyəti tərəfindən üzvlüyə qəbul "
                "edilən şəxslərdir."
            ),
            p(
                "Birliyə əhəmiyyətli maddi və mənəvi cəhətdən dəstək olanlar "
                "İdarə Heyətinin qərarı ilə fəxri üzv qəbul edilə bilərlər."
            ),
            p(
                "Birliyin filiallarının sayı üçdən çox olduqda, Birliyin "
                "qərargahında qeydiyyatdan keçmiş şəxslərin üzvlük "
                "qeydiyyatı filiallara verilir. Yeni üzvlük müraciətləri "
                "filiallara edilir. Üzvlüyün qəbulu və üzvlükdən "
                "çıxarılması qaydaları filialın İdarə Heyəti tərəfindən "
                "həyata keçirilir və ən çox otuz gün müddətində Baş İdarəyə "
                "yazılı məlumat verilir."
            ),
        ],
    ),
    (
        "section-04",
        "Üzvlükdən çıxma",
        "Maddə 4.",
        [
            p(
                "Hər bir üzv yazılı şəkildə bildirməklə Birlikdən çıxmaq "
                "hüququna malikdir. Üzvün istefa ərizəsi İdarə Heyətinə "
                "çatdıqda çıxış qaydaları başa çatmış sayılır. Üzvlükdən "
                "çıxmaq, üzvün Birliyə yığılmış borclarını ləğv etmir."
            ),
        ],
    ),
    (
        "section-05",
        "Üzvlükdən çıxarılma",
        "Maddə 5.",
        [
            p("Birlik üzvlüyündən çıxarılmasını tələb edən hallar:"),
            ol([
                "Birliyin nizamnaməsinə zidd davranmaq;",
                "Mütəmadi olaraq təyin olunmuş vəzifələrdən yayınmaq;",
                "Yazılı xəbərdarlıqlara baxmayaraq altı ay ərzində üzvlük haqqını ödəməmək;",
                "Birlik orqanlarının qəbul etdiyi qərarlara əməl etməmək;",
                "Üzv olma şərtlərini itirmək.",
            ]),
            p(
                "Yuxarıda göstərilən hallardan biri aşkar edildikdə, üzv "
                "İdarə Heyətinin qərarı ilə üzvlükdən çıxarıla bilər."
            ),
            p(
                "Birlikdən çıxan və ya xaric edilənlər üzv reyestrindən "
                "silinir və Birliyin əmlakı üzərində hüquq tələb edə bilməzlər."
            ),
        ],
    ),
    (
        "section-06",
        "Birliyin orqanları",
        "Maddə 6.",
        [
            p("Birliyin orqanları aşağıdakılardır:"),
            ol([
                "Ümumi Yığıncaq;",
                "İdarə Heyəti;",
                "Təftiş Şurası.",
            ]),
        ],
    ),
    (
        "section-07",
        "Birliyin Ümumi Yığıncağının yaradılması, iclasın vaxtı, çağırış və iclas qaydası",
        "Maddə 7.",
        [
            p(
                "Ümumi Yığıncaq Birliyin ən səlahiyyətli qərar qəbul edən "
                "orqanı olub, Birlikdə qeydiyyatdan keçmiş üzvlərdən ibarətdir. "
                "Birliyin filialı açıldıqda, filialların sayı üçə qədər "
                "olduqda Ümumi Yığıncaq qərargah və filiallarda qeydiyyatda "
                "olan üzvlərdən ibarət olur; filialların sayı üçdən çox "
                "olduqda, qərargahda qeydə alınmış üzvlər filiallara "
                "keçirilir və Ümumi Yığıncaq filialların Ümumi "
                "Yığıncaqlarında seçilmiş nümayəndələrdən ibarət olur."
            ),
            h3("Yığıncağın vaxtı"),
            p(
                "Növbəti Ümumi Yığıncaq hər 3 ildən bir, yanvar ayında "
                "İdarə Heyəti tərəfindən müəyyən edilən gün, yer və vaxtda "
                "toplanır."
            ),
            p(
                "İdarə Heyəti və ya Təftiş Şurası tərəfindən zərurət "
                "yarandıqda, yaxud Birlik üzvlərinin beşdə birinin yazılı "
                "müraciəti əsasında İdarə Heyəti tərəfindən növbədənkənar "
                "yığıncaq çağırılır. İdarə Heyəti Ümumi Yığıncağı iclasa "
                "çağırmadıqda üzvlərdən birinin ərizəsi ilə sülh hakimi "
                "Ümumi Yığıncağı iclasa çağırmaq üçün üç üzvü təyin edir."
            ),
            h3("Dəvət üsulu"),
            p(
                "İdarə Heyəti Birliyin nizamnaməsinə uyğun olaraq Ümumi "
                "Yığıncaqda iştirak etmək hüququ olan üzvlərin siyahısını "
                "hazırlayır. Ümumi Yığıncaqda iştirak etmək hüququ olan "
                "üzvlər ən azı on beş gün əvvəl yığıncağın günü, vaxtı, "
                "yeri və gündəliyi ən azı bir qəzetdə və ya Birliyin "
                "internet saytında elan edilməklə, yazılı şəkildə "
                "bildirilməklə, üzv tərəfindən verilən e-poçt ünvanına və "
                "ya əlaqə nömrəsinə mesaj göndərməklə və ya yerli kütləvi "
                "informasiya vasitəsində dərc edilməklə yığıncağa "
                "çağırılır. Bu çağırışda səs çoxluğu olmadığı səbəbindən "
                "iclas keçirilə bilmədikdə ikinci iclasın günü, vaxtı və "
                "yeri də qeyd olunmalıdır. Birinci iclasla ikinci iclas "
                "arasındakı müddət yeddi gündən az, altmış gündən çox ola bilməz."
            ),
            p(
                "Yığıncaq yetərsay olmamasından başqa hər hansı səbəbdən "
                "təxirə salınarsa, bu vəziyyət təxirə salınma səbəbləri "
                "göstərilməklə ilk iclasa çağırış proseduruna uyğun olaraq "
                "üzvlərə elan edilir. İkinci iclas təxirə salınma "
                "tarixindən ən geci altı ay ərzində keçirilməlidir. Üzvlər "
                "birinci bənddə göstərilən prinsiplərə uyğun olaraq ikinci "
                "iclasa dəvət olunurlar."
            ),
            p("Ümumi Yığıncağın iclası bir dəfədən artıq təxirə salına bilməz."),
            h3("Yığıncaq qaydaları"),
            p(
                "Ümumi Yığıncaq iştirak etmək hüququ olan üzvlərin mütləq "
                "əksəriyyətinin, nizamnamədə dəyişiklik edildikdə və "
                "Birliyin ləğvi hallarında isə üçdə ikisinin iştirakı ilə "
                "çağırılır. Səs çoxluğu olmadığı səbəbindən iclas təxirə "
                "salınarsa, ikinci iclasda səs çoxluğu tələb olunmur. "
                "Lakin bu iclasda iştirak edən üzvlərin sayı İdarə Heyəti "
                "və Təftiş Şurası üzvlərinin ümumi sayından iki dəfədən "
                "az ola bilməz."
            ),
            p(
                "Ümumi Yığıncaqda iştirak etmək hüququ olan üzvlərin "
                "siyahısı iclas yerində hazır saxlanılır. İclas yerinə "
                "daxil olan üzvlərin rəsmi orqanlar tərəfindən verilmiş "
                "şəxsiyyət sənədləri İdarə Heyətinin üzvləri və ya İdarə "
                "Heyəti tərəfindən təyin edilmiş məsul şəxslər tərəfindən "
                "yoxlanılır. Üzvlər İdarə Heyəti tərəfindən hazırlanan "
                "siyahıda adlarını imzalayaraq iclas yerinə daxil olurlar."
            ),
            p(
                "İclasın kvorumu (yetərsay) təmin edildikdə, vəziyyət "
                "protokolda qeyd edilir və iclası İdarə Heyətinin sədri və "
                "ya onun təyin etdiyi İdarə Heyəti üzvlərindən biri açır. "
                "İclasın kvorumu təmin edilmədikdə, İdarə Heyəti tərəfindən "
                "protokol tərtib edilir."
            ),
            p(
                "Açılışdan sonra iclası idarə etmək üçün sədr, kifayət "
                "qədər sayda sədr müavinləri və katib seçilərək şura "
                "komitəsi yaradılır."
            ),
            p(
                "Birliyin orqanlarının seçilməsi üçün keçiriləcək "
                "səsvermədə səs verən üzvlərdən şura komitəsinə öz "
                "şəxsiyyət sənədlərini göstərmək və iştirak edənlər "
                "siyahısında adlarının qarşılarına imza atmaq tələb olunur."
            ),
            p("İclasın idarə edilməsi və təhlükəsizliyinə şura sədri cavabdehdir."),
            p(
                "Ümumi Yığıncaqda yalnız gündəlikdəki məsələlər müzakirə "
                "olunur. Bununla belə, iclasda iştirak edən üzvlərin onda "
                "biri tərəfindən yazılı şəkildə müzakirəsi tələb olunan "
                "məsələlər gündəliyə salınmalıdır."
            ),
            p(
                "Ümumi Yığıncaqda hər bir üzv bir səsə malikdir; üzv "
                "şəxsən səs verməlidir. Fəxri üzvlər ümumi yığıncaqlarda "
                "iştirak edə bilərlər, lakin səs verə bilməzlər. Hüquqi "
                "şəxs üzv olduqda, hüquqi şəxsin İdarə Heyətinin sədri və "
                "ya onu təmsil etməyi həvalə edilmiş şəxs səs verir."
            ),
            p(
                "İclasda müzakirə olunan məsələlər və qəbul edilmiş "
                "qərarlar protokola yazılır və şura sədri ilə katib "
                "tərəfindən birgə imzalanır. İclasın sonunda protokol və "
                "digər sənədlər İdarə Heyətinin sədrinə təhvil verilir. "
                "İdarə Heyətinin sədri bu sənədlərin qorunmasına və yeddi "
                "gün ərzində yeni seçilmiş İdarə Heyətinə çatdırılmasına "
                "cavabdehdir."
            ),
        ],
    ),
    (
        "section-08",
        "Ümumi Yığıncağın səsvermə və qərar qəbulu qaydaları",
        "Maddə 8.",
        [
            p(
                "Ümumi Yığıncaqda, əksinə qərar verilmədiyi təqdirdə "
                "səsvermə açıq şəkildə aparılır. Açıq səsvermədə Ümumi "
                "Yığıncağın sədrinin müəyyən etdiyi üsul tətbiq edilir."
            ),
            p(
                "Gizli səsvermə zamanı iclasın sədri tərəfindən möhürlənmiş "
                "sənədlər və ya bülletinlər üzvlər lazımi işləri gördükdən "
                "sonra boş bir qutuya atılır və səsvermə başa çatdıqdan "
                "sonra açıq sayım yolu ilə nəticə müəyyən edilir."
            ),
            p(
                "Ümumi Yığıncağın qərarları iclasda iştirak edən üzvlərin "
                "mütləq səs çoxluğu ilə qəbul edilir. Bununla belə, "
                "Birliyin nizamnaməsinə dəyişikliklər və ləğv edilməsi "
                "barədə qərarlar yalnız iclasda iştirak edən üzvlərin "
                "üçdə iki səs çoxluğu ilə qəbul edilə bilər."
            ),
            h3("İclas olmadan qəbul edilən qərarlar"),
            p(
                "Bütün üzvlərin bir araya gəlmədən yazılı iştirakı ilə "
                "qəbul edilən qərarlar və Birliyin bütün üzvlərinin bu "
                "nizamnamədə yazılmış çağırış qaydalarına əməl edilmədən "
                "qəbul etdiyi qərarlar etibarlıdır. Qərarların bu şəkildə "
                "qəbul edilməsi Ümumi Yığıncağın iclasını əvəz etmir."
            ),
        ],
    ),
    (
        "section-09",
        "Ümumi Yığıncağın vəzifələri və səlahiyyətləri",
        "Maddə 9.",
        [
            p("Aşağıdakı məsələlər Ümumi Yığıncaqda müzakirə edilir və qərara alınır:"),
            ol([
                "Birlik orqanlarının seçilməsi;",
                "Birliyin nizamnaməsində dəyişiklik edilməsi;",
                "İdarə Heyəti və Təftiş Şurasının hesabatlarının müzakirəsi və İdarə Heyətinə bəraət verilməsi;",
                "İdarə Heyəti tərəfindən hazırlanan büdcənin müzakirəsi və olduğu kimi və ya dəyişikliklərlə qəbul edilməsi;",
                "Birliyin digər orqanlarına nəzarət etmək və zəruri hallarda onları haqlı səbəblərdən vəzifələrindən azad etmək;",
                "İdarə Heyətinin üzvlükdən imtina və ya üzvlükdən xaric edilməsi ilə bağlı qərarlarına qarşı edilən etirazların araşdırılması və qərara bağlanması;",
                "İdarə Heyətinə Birlik üçün lazım olan daşınmaz əmlakı almaq və ya mövcud daşınmaz əmlakı satmaq səlahiyyətinin verilməsi;",
                "Birliyin fəaliyyəti ilə bağlı İdarə Heyəti tərəfindən hazırlanacaq əsasnamələrin olduğu kimi və ya dəyişikliklərlə nəzərdən keçirilməsi və təsdiq edilməsi;",
                "Birliyin sədri və dövlət məmuru olmayan İdarə Heyəti və Təftiş Şurası üzvlərinə ödəniləcək maaş və hər cür əlavə ödəniş, ezamiyyət pulu və kompensasiyaların, üzvlərinə veriləcək gündəlik və yol xərclərinin müəyyən edilməsi;",
                "Birliyin federasiyaya daxil olub-olmamasına qərar vermək;",
                "Birliyin filiallarının açılmasına qərar verilməsi və açılmasına qərar verilən filialla bağlı əməliyyatların aparılması üçün İdarə Heyətinə səlahiyyət verilməsi;",
                "Birliyin beynəlxalq fəaliyyət göstərməsi, xaricdə birlik və təşkilatlara qoşulması və ya onları tərk etməsi;",
                "Birliyin vəqf qurması;",
                "Birliyin ləğvi;",
                "İdarə Heyətinin digər təkliflərinin nəzərdən keçirilməsi və qərara alınması;",
                "Birliyin ən səlahiyyətli orqanı olaraq, Birliyin başqa orqanına verilməyən vəzifələri yerinə yetirmək və səlahiyyətləri həyata keçirmək;",
                "Ümumi Yığıncaq tərəfindən qanunvericiliklə müəyyən edilmiş digər vəzifələrin yerinə yetirilməsi.",
            ]),
        ],
    ),
    (
        "section-10",
        "İdarə Heyətinin təşkili, vəzifələri və səlahiyyətləri",
        "Maddə 10.",
        [
            p(
                "İdarə Heyəti Ümumi Yığıncaq tərəfindən beş əsas və beş "
                "əvəzedici üzvdən ibarət seçilir."
            ),
            p(
                "İdarə Heyəti seçkidən sonrakı ilk iclasında qərarla "
                "vəzifə bölgüsü apararaq sədr, həmsədr, sədr müavini, "
                "katib, xəzinədar və üzvləri müəyyən edir."
            ),
            p(
                "İdarə Heyətinin ilkin tərkibində istefa və ya digər "
                "səbəblərə görə vakant yer yaranarsa, Ümumi Yığıncaqda "
                "alınan səs çoxluğu sırasına uyğun olaraq əvəzedici "
                "üzvlərin vəzifəyə çağırılması məcburidir."
            ),
            h3("İdarə Heyətinin vəzifələri və səlahiyyətləri"),
            p("İdarə Heyəti aşağıdakı vəzifələri yerinə yetirir:"),
            ol([
                "Birliyi təmsil etmək və ya öz üzvlərindən birinə ya da bir üçüncü şəxsə bununla bağlı səlahiyyət vermək;",
                "Gəlir və xərc hesabatları ilə bağlı əməliyyatları həyata keçirmək və növbəti dövr üçün büdcəni hazırlayıb Ümumi Yığıncağa təqdim etmək;",
                "Birliyin fəaliyyəti ilə bağlı əsasnaməni hazırlayıb Ümumi Yığıncağın təsdiqinə təqdim etmək;",
                "Ümumi Yığıncağın verdiyi səlahiyyətlə daşınmaz əmlak almaq, Birliyə məxsus daşınan və daşınmaz əmlakı satmaq, bina və ya obyekt tikdirmək, kirayə müqaviləsi bağlamaq, Birliyin xeyrinə girov, ipoteka və ya daşınmaz hüquqlar yaratmaq;",
                "Şöbələrin açılması ilə bağlı əməliyyatların Ümumi Yığıncaq tərəfindən verilən səlahiyyətlə həyata keçirilməsini təmin etmək;",
                "Birliyin filiallarının yoxlanılmasını təmin etmək;",
                "Zəruri hesab edilən yerlərdə nümayəndəliklərin açılmasını təmin etmək;",
                "Ümumi Yığıncaqda qəbul edilən qərarları həyata keçirmək;",
                "Hər bir təqvim ilinin sonunda Birliyin əməliyyat hesabatını və ya balans, mənfəət və zərər hesabatı ilə İdarə Heyətinin fəaliyyətini izah edən hesabatı hazırlamaq və toplandığında Ümumi Yığıncağa təqdim etmək;",
                "Büdcənin icrasını təmin etmək;",
                "Üzvlərin Birliyə qəbulu və ya üzvlükdən çıxarılması ilə bağlı qərar qəbul etmək;",
                "Birliyin məqsədini həyata keçirmək üçün öz səlahiyyətləri daxilində hər cür qərarlar qəbul etmək və icra etmək;",
                "Qanunvericiliklə ona verilmiş digər vəzifələri yerinə yetirmək və səlahiyyətlərdən istifadə etmək.",
            ]),
        ],
    ),
    (
        "section-11",
        "Təftiş Şurasının yaradılması, vəzifələri və səlahiyyətləri",
        "Maddə 11.",
        [
            p(
                "Təftiş Şurası Ümumi Yığıncaq tərəfindən üç əsas və üç "
                "əvəzedici üzv olaraq seçilir."
            ),
            p(
                "Təftiş Şurasının ilkin tərkibində istefa və ya digər "
                "səbəblərə görə vakant yer yaranarsa, Ümumi Yığıncaqda "
                "alınan səs çoxluğu sırasına uyğun olaraq əvəzedici "
                "üzvlərin vəzifəyə çağırılması məcburidir."
            ),
            h3("Təftiş Şurasının vəzifələri və səlahiyyətləri"),
            p(
                "Təftiş Şurası, Birliyin nizamnaməsində nəzərdə tutulmuş "
                "məqsəd və vəzifələrə uyğun fəaliyyət göstərib-"
                "göstərmədiyini, kitab, hesab və qeydlərin qanunvericiliyə "
                "və Birliyin nizamnaməsinə uyğun aparılıb-aparılmadığını "
                "bir ildən çox olmayan aralıqlarla yoxlayır və yoxlamanın "
                "nəticələrini hesabatda əks etdirir. Təftiş Şurası "
                "hesabatını İdarə Heyətinə və iclas zamanı Ümumi "
                "Yığıncağa təqdim edir."
            ),
            p(
                "Təftiş Şurası zəruri hesab etdikdə Ümumi Yığıncağın "
                "iclasa çağırılmasını tələb edə bilər."
            ),
        ],
    ),
    (
        "section-12",
        "Birliyin gəlir mənbələri",
        "Maddə 12.",
        [
            p("Birliyin gəlir mənbələri aşağıda göstərilmişdir:"),
            ol([
                "Üzvlük haqları: üzvlərdən giriş haqqı olaraq 50 TL və aylıq 50 TL ödəniş alınır. Bu məbləğlər yalnız Ümumi Yığıncağın səlahiyyəti ilə artırıla və ya azaldıla bilər;",
                "Filial ödənişləri: filiallar tərəfindən toplanan üzvlük haqlarının 50%-i Birliyin ümumi xərclərini qarşılamaq üçün hər altı aydan bir baş qərargaha göndərilir;",
                "Birliyə fiziki və hüquqi şəxslər tərəfindən könüllü olaraq edilən ianələr və yardımlar;",
                "Birliyin təşkil etdiyi çay və yeməkli yığıncaqlar, səfərlər və əyləncələr, tamaşalar, konsertlər və konfranslar kimi fəaliyyətlərdən əldə edilən gəlirlər;",
                "Birliyin əmlakından əldə edilən gəlirlər;",
                "Yardımların toplanması ilə bağlı qanunvericilik müddəalarına uyğun olaraq toplanacaq ianələr və yardımlar;",
                "Birliyin məqsədini həyata keçirmək üçün ehtiyac duyduğu gəliri təmin etmək məqsədi ilə həyata keçirdiyi ticarət fəaliyyətlərindən əldə edilən mənfəət;",
                "Digər gəlirlər.",
            ]),
        ],
    ),
    (
        "section-13",
        "Birliyin mühasibat qeydiyyatı prinsipləri və saxlanılacaq kitablar",
        "Maddə 13.",
        [
            h3("Mühasibat uçotu prinsipləri"),
            p(
                "Birlik mühasibat kitablarını müəyyən edilmiş prinsiplərə "
                "uyğun aparmağa borcludur. Bununla belə, illik ümumi gəlir "
                "Birliklər Əsasnaməsinin 31-ci maddəsində göstərilən həddi "
                "aşarsa, mühasibat kitabları sonrakı hesabat dövründən "
                "başlayaraq balans əsasında aparılır."
            ),
            p(
                "Balans əsasına keçildikdə, yuxarıda qeyd olunan limit "
                "ardıcıl iki hesabat dövründə limitdən aşağı düşərsə, "
                "növbəti ildən təsərrüfat hesabı əsasına çevrilə bilər."
            ),
            p(
                "Yuxarıda qeyd olunan məhdudiyyətlərdən asılı olmayaraq, "
                "İdarə Heyətinin qərarı ilə mühasibat kitabları balans "
                "əsasında aparıla bilər."
            ),
            p(
                "Birlik kommersiya müəssisəsi açırsa, Vergi "
                "Qanunvericiliyinin müddəalarına uyğun olaraq bu "
                "kommersiya müəssisəsi üçün də mühasibat uçotu aparılır."
            ),
            h3("Qeydlərin aparılması qaydaları"),
            p(
                "Birliyin kitabları və qeydləri Birliklər Əsasnaməsində "
                "göstərilən qayda və prinsiplərə uyğun olaraq aparılır."
            ),
            h3("Saxlanılacaq kitablar"),
            p(
                "Birlikdə aşağıdakı kitablar saxlanılır. (a) Təsərrüfat "
                "hesabları əsasında aparılacaq kitablar və riayət olunacaq "
                "prinsiplər aşağıdakılardır:"
            ),
            ol([
                "Qərar kitabçası: İdarə Heyətinin qərarları bu kitabçada tarix və nömrə ardıcıllığı ilə yazılır; qərarlar iclasda iştirak edən üzvlər tərəfindən imzalanır.",
                "Üzvlük Qeydiyyat Kitabı: Birliyə üzv kimi daxil olanların şəxsiyyət məlumatları, giriş və çıxış tarixləri bu kitabda qeyd olunur; üzvlər tərəfindən ödənilən giriş və illik üzvlük haqları da burada qeyd edilir.",
                "Sənəd Qeydiyyatı Kitabı: qəbul edilən və göndərilən sənədlər tarix və sıra nömrəsi ilə bu kitabda qeyd olunur; daxil olan və göndərilən sənədlərin əsli saxlanılır; elektron poçt vasitəsilə qəbul edilən və ya göndərilən sənədlər çap olunmaqla saxlanılır.",
                "Təsərrüfat Hesabatı Kitabı: Birlik adından alınan gəlirlər və çəkilən xərclər bu kitabda aydın və müntəzəm şəkildə qeyd olunur.",
            ]),
            p("(b) Mühasibat balansı əsasında aparılacaq kitablar və riayət olunacaq prinsiplər:"),
            p(
                "(a) bəndinin 1, 2 və 3-cü yarımbəndlərində göstərilən "
                "kitablar mühasibat uçotu balansı əsasında aparıldığı halda "
                "da saxlanılır."
            ),
            p(
                "Jurnal Kitabı və Baş Mühasibat Kitabı: bu kitabların "
                "saxlanılması və uçotu Vergi Qanunvericiliyi ilə həmin "
                "Qanunun Maliyyə Nazirliyinə vermiş səlahiyyətə uyğun "
                "olaraq dərc edilən Mühasibat Uçotu Sisteminin Tətbiqinə "
                "dair Ümumi Təbliğlərin prinsiplərinə uyğun aparılır."
            ),
            h3("Kitabların təsdiqi"),
            p(
                "Birlikdə saxlanılması tələb olunan kitablar (Baş kitab "
                "istisna olmaqla) istifadəyə başlamazdan əvvəl Vətəndaş "
                "Cəmiyyəti ilə Əlaqələr Müdirliyi və ya notarius "
                "tərəfindən təsdiqlənir. Bu kitabların istifadəsi "
                "vərəqləri bitənə qədər davam edir və kitabların aralıq "
                "təsdiqi həyata keçirilmir. Bununla belə, balans əsasında "
                "saxlanılan Jurnal Kitabı hər il istifadə olunacağı ildən "
                "əvvəlki son ayda yenidən təsdiqlənməlidir."
            ),
            h3("Mənfəət hesabatının və mühasibat balansının tərtib edilməsi"),
            p(
                "Əgər uçot təsərrüfat hesabatı əsasında aparılırsa, ilin "
                "sonunda (31 dekabr) “Təsərrüfat hesabatı haqqında "
                "arayış” (Birliklər Əsasnaməsinin 16-cı Əlavəsində "
                "göstərilmişdir) hazırlanır. Kitablar balans əsasında "
                "aparılırsa, Maliyyə Nazirliyi tərəfindən dərc edilən "
                "Mühasibat Uçotu Sisteminin Tətbiqi Ümumi Təbliğləri "
                "əsasında ilin sonunda (31 dekabr) balans və mənfəət-zərər "
                "hesabatı hazırlanır."
            ),
        ],
    ),
    (
        "section-14",
        "Birliyin gəlir və xərc əməliyyatları",
        "Maddə 14.",
        [
            h3("Gəlir və xərc sənədləri"),
            p(
                "Birlik gəlirləri “Qəbz şəhadətnaməsi” ilə toplanır (bunun "
                "nümunəsi Birliklər Əsasnaməsinin 17-ci Əlavəsində "
                "verilmişdir). Birlik gəlirləri banklar vasitəsilə "
                "toplanarsa, bank tərəfindən verilən qəbz və ya hesabdan "
                "çıxarış kimi sənədlər qəbz kimi xidmət edir."
            ),
            p(
                "Birlik xərcləri hesab-faktura, pərakəndə satış qəbzləri "
                "və fərdi məşğulluq qəbzləri kimi xərc sənədləri ilə "
                "həyata keçirilir. Bununla birlikdə, Gəlir Vergisi "
                "Qanununun 94-cü maddəsinin əhatə dairəsinə daxil olan "
                "Birliyin ödənişləri üçün Vergi Qanunvericiliyinin "
                "müddəalarına uyğun olaraq xərc çeki, bu əhatə dairəsinə "
                "daxil olmayan ödənişlər üçün isə “Xərc qəbzi” və ya "
                "“Bank qəbzi” (nümunəsi Birliklər Əsasnaməsinin 13-cü "
                "Əlavəsindədir) xərc sənədi kimi istifadə olunur."
            ),
            p(
                "Birlik tərəfindən fiziki şəxslərə, qurumlara və ya "
                "təşkilatlara həyata keçiriləcək mal və xidmətlərin "
                "pulsuz çatdırılması “Natural yardımın çatdırılması "
                "sənədi” ilə (nümunəsi Birliklər Əsasnaməsinin 14-cü "
                "Əlavəsindədir) həyata keçirilir."
            ),
            p(
                "Fiziki şəxslər, qurumlar və ya təşkilatlar tərəfindən "
                "Birliyə ediləcək mal və xidmətlərin pulsuz çatdırılması "
                "“Natural ianə qəbzi şəhadətnaməsi” ilə (nümunəsi "
                "Birliklər Əsasnaməsinin 15-ci Əlavəsindədir) qəbul edilir."
            ),
            p(
                "Bu sənədlər Əlavə-13, Əlavə-14 və Əlavə-15-də göstərilən "
                "formada və ölçüdə, ardıcıl seriya və ardıcıl nömrələri "
                "daşıyan, əlli üzündən kopyalı orijinaldan və əlli üz "
                "vərəqindən ibarət cilddə və ya elektron sistemlər və "
                "yazı maşınları vasitəsilə davamlı forma kimi çap olunur."
            ),
            h3("Qəbzlər"),
            p(
                "Birliyin gəlirlərinin toplanmasında istifadə ediləcək "
                "“Qəbz sənədləri” (Birliklər Əsasnaməsinin 17-ci "
                "Əlavəsində göstərilən forma və ölçüdə) İdarə Heyətinin "
                "qərarı ilə mətbəədə çap olunur."
            ),
            p(
                "Qəbz sənədlərinin çapı və nəzarəti, mətbəədən qəbulu, "
                "uçot kitabçasında qeydiyyatı, köhnə və yeni xəzinədarlar "
                "arasında təhvil verilməsi və Birlik adından gəlir "
                "götürəcək şəxs və ya şəxslər tərəfindən istifadə "
                "edilməsinə dair məsələlərdə Birliklər Əsasnaməsinin "
                "müvafiq müddəalarına əməl olunur."
            ),
            h3("İcazə lisenziyası"),
            p(
                "İdarə Heyətinin əsas üzvləri istisna olmaqla, Birlik "
                "adından gəlir əldə edəcək şəxs və ya şəxslər səlahiyyət "
                "müddəti də göstərilməklə İdarə Heyətinin qərarı ilə "
                "müəyyən edilir. Gəlir toplayacaq şəxslərin şəxsiyyətini, "
                "imzasını və fotoşəkillərini özündə əks etdirən “İcazə "
                "şəhadətnaməsi” (Birliklər Əsasnaməsinin 19-cu Əlavəsinə "
                "daxildir) Birlik tərəfindən iki nüsxədə hazırlanır və "
                "Birlik İdarə Heyətinin sədri tərəfindən təsdiq edilir. "
                "İdarə Heyətinin əsas üzvləri səlahiyyət sertifikatı "
                "olmadan gəlir əldə edə bilərlər."
            ),
            h3("Gəlir və xərc sənədlərinin saxlanma müddəti"),
            p(
                "İcazə sertifikatlarının müddəti İdarə Heyəti tərəfindən "
                "ən çox bir il olaraq müəyyən edilir. Müddəti bitmiş "
                "icazə sənədləri birinci bəndə uyğun olaraq yenilənir. "
                "İcazə şəhadətnaməsinin müddəti başa çatdıqda və ya "
                "səlahiyyət verilmiş şəxs istefa verdikdə, vəfat etdikdə, "
                "vəzifədən və ya işdən azad edildikdə, verilmiş icazə "
                "sənədlərinin bir həftə müddətində Birliyin İdarə "
                "Heyətinə təqdim edilməsi məcburidir. Gəlir toplamaq "
                "səlahiyyəti istənilən vaxt İdarə Heyətinin qərarı ilə "
                "ləğv edilə bilər."
            ),
            p(
                "Kitablar istisna olmaqla, Birliyin istifadəsində olan "
                "qəbzlər, xərc sənədləri və digər sənədlər xüsusi "
                "qanunlarda müəyyən edilmiş müddətlərə xələl gətirmədən "
                "uçota alındıqları kitablardakı nömrə və tarix sırasına "
                "uyğun olaraq 5 il müddətində saxlanılır."
            ),
        ],
    ),
    (
        "section-15",
        "Bəyannamənin təqdimatı",
        "Maddə 15.",
        [
            p(
                "Birliyin əvvəlki il üzrə fəaliyyəti ilə gəlir və xərc "
                "əməliyyatları İdarə Heyəti tərəfindən təsdiq edildikdən "
                "sonra “Birlik Bəyannaməsi” (Birliklər Əsasnaməsinin "
                "21-ci əlavəsinə uyğun) Birlik sədri tərəfindən hər təqvim "
                "ilinin ilk dörd ayı ərzində müvafiq mülki idarə "
                "müdirliyinə təqdim edilir."
            ),
        ],
    ),
    (
        "section-16",
        "Bildiriş öhdəliyi",
        "Maddə 16.",
        [
            h3("Mülki orqana ediləcək bildirişlər"),
            p(
                "Ümumi Yığıncağın nəticə bildirişi: növbəti və ya "
                "növbədənkənar Ümumi Yığıncaqdan sonra otuz gün ərzində "
                "İdarə Heyəti, Təftiş Şurası və digər orqanlara seçilmiş "
                "əsas və əvəzedici üzvlərin daxil edildiyi “Ümumi "
                "Yığıncağın nəticə bildirişi” (Birliklər Əsasnaməsinin "
                "3-cü Əlavəsində göstərilmişdir) yerli hakimiyyət "
                "orqanına təqdim edilir. Ümumi Yığıncaqda nizamnamədə "
                "dəyişiklik edildikdə Ümumi Yığıncağın protokolu, "
                "dəyişdirilmiş maddələrin köhnə və yeni forması və hər "
                "səhifəsi İdarə Heyəti üzvlərinin mütləq səs çoxluğu ilə "
                "imzalanan Birliyin nizamnaməsinin yekun variantı bu "
                "bənddə göstərilən müddət ərzində yerli hakimiyyət "
                "orqanına təqdim edilir."
            ),
            h3("Daşınmaz əmlak haqqında bildiriş"),
            p(
                "Birliyin əldə etdiyi daşınmaz əmlak torpaq reyestrində "
                "qeydiyyata alındığı gündən otuz gün müddətində "
                "“Daşınmaz Əmlak Bəyannaməsi” (Birliklər Əsasnaməsinin "
                "26-cı əlavəsində təqdim olunur) doldurmaqla yerli "
                "inzibati orqana bildirilir."
            ),
            h3("Xaricdən yardım alınması haqqında bildiriş"),
            p(
                "Birlik xaricdən yardım alacaqsa, yardım almazdan əvvəl "
                "“Xaricdən yardım alınması haqqında bildiriş” (Birliklər "
                "Əsasnaməsinin 4-cü Əlavəsində göstərilmişdir) "
                "doldurularaq yerli inzibati orqana məlumat verilməlidir. "
                "Nağd yardım banklar vasitəsilə alınmalı və istifadə "
                "edilməzdən əvvəl bildiriş tələbi yerinə yetirilməlidir."
            ),
            h3("Dəyişikliklər haqqında bildiriş"),
            p(
                "Birliyin yerləşdiyi ünvanın dəyişdirilməsi (Birliklər "
                "Əsasnaməsinin 24-cü Əlavəsində göstərilmişdir) — "
                "“Yaşayış yerinin dəyişdirilməsi haqqında bildiriş”, və "
                "Ümumi Yığıncaqdan başqa Birlik orqanlarında baş verən "
                "dəyişikliklər, dəyişiklik edildikdən sonra otuz gün "
                "ərzində “Birlik orqanlarında dəyişikliklər haqqında "
                "bildiriş” (Birliklər Əsasnaməsinin 25-ci Əlavəsində "
                "göstərilmişdir) doldurularaq yerli hakimiyyət orqanına "
                "bildirilir."
            ),
            p(
                "Birliyin nizamnaməsinə edilən dəyişikliklər də nizamnamə "
                "dəyişikliyinin aparıldığı Ümumi Yığıncaqdan sonrakı otuz "
                "gün ərzində Ümumi Yığıncağın nəticə bildirişinə əlavə "
                "olaraq yerli icra hakimiyyəti orqanına məlumat verilir."
            ),
        ],
    ),
    (
        "section-17",
        "Birliyin daxili təftişi",
        "Maddə 17.",
        [
            p(
                "Daxili təftiş Birliyin Ümumi Yığıncağı, İdarə Heyəti və "
                "ya Təftiş Şurası, habelə müstəqil audit təşkilatları "
                "tərəfindən həyata keçirilə bilər. Təftişin Ümumi "
                "Yığıncaq, İdarə Heyəti və ya müstəqil audit firmaları "
                "tərəfindən həyata keçirilməsi Təftiş Şurasının "
                "məsuliyyətini aradan qaldırmır."
            ),
        ],
    ),
    (
        "section-18",
        "Birliyin borcalma qaydaları",
        "Maddə 18.",
        [
            p(
                "Birlik öz məqsədinə çatmaq və fəaliyyətini həyata "
                "keçirmək üçün zərurət yarandıqda, İdarə Heyətinin qərarı "
                "ilə borc pul götürə bilər. Bu borcalma mal və "
                "xidmətlərin kreditlə və ya nağd şəkildə alınması üçün ola "
                "bilər. Bununla belə, bu borcalma Birliyin gəlir mənbələri "
                "ilə əhatə olunmayan məbləğdə və ya Birliyin ödəməkdə "
                "çətinlik çəkməsinə səbəb olacaq şəkildə həyata keçirilə "
                "bilməz."
            ),
        ],
    ),
    (
        "section-19",
        "Birliyin filiallarının yaradılması",
        "Maddə 19.",
        [
            p(
                "Birlik Ümumi Yığıncağın qərarı ilə lazım bildiyi yerlərdə "
                "filiallar aça bilər. Bu məqsədlə Birliyin İdarə Heyəti "
                "tərəfindən səlahiyyət verilmiş ən azı üç nəfərdən ibarət "
                "təsisçilər şurası filialın yaradılması haqqında bildirişi "
                "və Birliyin Əsasnaməsində nəzərdə tutulmuş zəruri "
                "sənədləri filialın açılacağı yerin ali inzibati orqanına "
                "təqdim edir."
            ),
        ],
    ),
    (
        "section-20",
        "Filialların vəzifələri və səlahiyyətləri",
        "Maddə 20.",
        [
            p(
                "Filiallar hüquqi şəxs olmayan, Birliyin məqsədlərinə və "
                "xidmət subyektlərinə uyğun olaraq müstəqil fəaliyyət "
                "göstərmək tapşırığı və səlahiyyəti olan Birliyin daxili "
                "təşkilatlarıdır; bütün əməliyyatlardan yaranan debitor "
                "borcları və borclar üzrə məsuliyyət daşıyırlar."
            ),
        ],
    ),
    (
        "section-21",
        "Filialların orqanları və tətbiq olunan müddəalar",
        "Maddə 21.",
        [
            p(
                "Filialın orqanları onun Ümumi Yığıncağı, İdarə Heyəti və "
                "Təftiş Şurasıdır. Ümumi Yığıncaq filialın qeydiyyatdan "
                "keçmiş üzvlərindən ibarətdir. İdarə Heyəti filialın "
                "Ümumi Yığıncağı tərəfindən beş əsas və beş əvəzedici "
                "üzv, Təftiş Şurası isə üç əsas və üç əvəzedici üzv "
                "olaraq seçilir."
            ),
            p(
                "Bu orqanların vəzifə və səlahiyyətləri ilə bu "
                "nizamnaməyə daxil edilmiş Birliyə aid digər müddəalar da "
                "qanunvericiliklə müəyyən edilmiş çərçivədə filialda "
                "tətbiq edilir."
            ),
        ],
    ),
    (
        "section-22",
        "Filialların Ümumi Yığıncaqlarının vaxtı və qərargahda təmsil qaydaları",
        "Maddə 22.",
        [
            p(
                "Filiallar növbəti Ümumi Yığıncaqlarını qərargahın Ümumi "
                "Yığıncağına ən azı iki ay qalmış başa çatdırmalıdırlar. "
                "Filialların növbəti Ümumi Yığıncağı hər 3 ildən bir, "
                "yanvar ayında filialın İdarə Heyəti tərəfindən müəyyən "
                "edilən gün, yer və vaxtda toplanır. Filiallar Ümumi "
                "Yığıncağın nəticə bildirişinin surətini iclasın "
                "keçirildiyi tarixdən sonra otuz gün müddətində yerli "
                "inzibati orqana və Birliyin qərargahına təqdim etməyə "
                "borcludurlar."
            ),
            p(
                "Filialların sayı üçə qədər olduqda, onların bütün "
                "üzvləri Birliyin Ümumi Yığıncağında birbaşa iştirak "
                "etmək hüququna malikdir. Filialların sayı üçdən çox "
                "olduqda, filialda qeydiyyatdan keçmiş hər iyirmi (20) "
                "üzvdən bir (1) nümayəndə — qalan üzvlərin sayı 10-dan "
                "çox olarsa, həmin üzvlərdən bir nümayəndə də əlavə "
                "olunmaqla — filialın Ümumi Yığıncağında seçilərək "
                "Birliyin Ümumi Yığıncağında iştirak etmək hüququna "
                "malik olur."
            ),
            p(
                "Sonuncu filial Ümumi Yığıncağında seçilmiş nümayəndələr "
                "Birliyin Ümumi Yığıncağında iştirak edirlər. Qərargahın "
                "İdarə Heyəti və Təftiş Şurası üzvləri qərargahın Ümumi "
                "Yığıncağında iştirak edirlər, lakin filial adından "
                "nümayəndə seçilmədikləri halda səs verə bilməzlər."
            ),
            p(
                "Filialın İdarə Heyəti və ya Təftiş Şurası üzvləri "
                "qərargahın İdarə Heyətinə və ya Təftiş Şurasına "
                "seçildikdə filialdakı vəzifələrindən azad olurlar."
            ),
        ],
    ),
    (
        "section-23",
        "Nümayəndəliyin açılması",
        "Maddə 23.",
        [
            p(
                "Birlik lazım bildiyi yerlərdə öz fəaliyyətini həyata "
                "keçirmək üçün İdarə Heyətinin qərarı ilə nümayəndəliklər "
                "aça bilər. Nümayəndəliyin ünvanı İdarə Heyətinin qərarı "
                "ilə nümayəndə kimi təyin edilmiş şəxs və ya şəxslər "
                "tərəfindən həmin yerin yerli inzibati orqanına yazılı "
                "şəkildə bildirilir. Nümayəndəlik Birliyin Ümumi "
                "Yığıncağında təmsil oluna bilməz. Filiallar nümayəndəlik "
                "aça bilməzlər."
            ),
        ],
    ),
    (
        "section-24",
        "Nizamnamədə dəyişiklik edilməsinin qaydaları",
        "Maddə 24.",
        [
            p("Nizamnamədə dəyişiklik Ümumi Yığıncağın qərarı ilə edilə bilər."),
            p(
                "Ümumi Yığıncaqda nizamnamədə dəyişiklik etmək üçün Ümumi "
                "Yığıncaqda iştirak etmək və səs vermək hüququ olan "
                "üzvlərin 2/3 səs çoxluğu tələb olunur. Səs çoxluğu "
                "olmadığı səbəbindən iclas təxirə salınarsa, ikinci "
                "iclasda səs çoxluğu tələb olunmur. Lakin bu iclasda "
                "iştirak edən üzvlərin sayı İdarə Heyəti və Təftiş Şurası "
                "üzvlərinin ümumi sayından iki dəfədən az ola bilməz."
            ),
            p(
                "Nizamnamə dəyişikliyi üçün tələb olunan səs çoxluğu "
                "iclasda iştirak edən və səsvermə hüququna malik olan "
                "üzvlərin 2/3 səsidir. Ümumi Yığıncaqda nizamnamə "
                "dəyişikliyinə səsvermə açıq şəkildə keçirilir."
            ),
        ],
    ),
    (
        "section-25",
        "Birliyin ləğvi və aktivlərinin ləğvi qaydaları",
        "Maddə 25.",
        [
            p("Ümumi Yığıncaq istənilən vaxt Birliyin ləğvi barədə qərar verə bilər."),
            p(
                "Ləğv məsələsinin Ümumi Yığıncaqda müzakirə edilməsi üçün "
                "Ümumi Yığıncaqda iştirak etmək və səs vermək hüququ olan "
                "üzvlərin 2/3 səs çoxluğu tələb olunur. Səs çoxluğu "
                "olmadığı üçün iclas təxirə salınarsa, ikinci iclasda "
                "səs çoxluğu tələb olunmur. Lakin bu iclasda iştirak edən "
                "üzvlərin sayı İdarə Heyəti və Təftiş Şurası üzvlərinin "
                "ümumi sayından iki dəfədən az ola bilməz."
            ),
            p(
                "Ləğv qərarı üçün tələb olunan səs çoxluğu iclasda "
                "iştirak edən və səsvermə hüququna malik olan üzvlərin "
                "2/3 səsidir. Ləğv qərarının səsverməsi Ümumi Yığıncaqda "
                "açıq şəkildə keçirilir."
            ),
            h3("Ləğvetmə qaydaları"),
            p(
                "Ümumi Yığıncaq ləğv qərarı qəbul etdikdə, Birliyin "
                "maliyyə vəsaitləri, əmlakı və hüquqları İdarə Heyətinin "
                "sonuncu üzvlərindən ibarət ləğvetmə komissiyası "
                "tərəfindən ləğv edilir. Bu qaydalar Ümumi Yığıncağın "
                "ləğv haqqında qərarının qəbul edildiyi və ya birbaşa "
                "ləğvin baş verdiyi tarixdən başlayır. Ləğv dövründə "
                "bütün əməliyyatlarda Birliyin adında “Ləğv halında "
                "Dünya Azərbaycanlı Alimlər Birliyi” ifadəsi işlədilir."
            ),
            p(
                "Ləğvetmə komissiyası qanunvericiliklə müəyyən edilmiş "
                "qaydada Birliyin maliyyə vəsaitlərinin, əmlakının və "
                "hüquqlarının ləğvini əvvəldən axıra qədər başa "
                "çatdırmaq üçün məsuliyyət daşıyır və səlahiyyətlidir. "
                "Komissiya əvvəlcə Birliyin hesablarını yoxlayır; "
                "yoxlanış zamanı Birliyin kitabları, qəbzləri, xərc "
                "sənədləri, mülkiyyət sənədi, bank sənədləri və digər "
                "sənədlər müəyyən edilir və Birliyin aktiv və "
                "öhdəlikləri hesabatda əks etdirilir. Ləğvetmə "
                "prosesində Birliyin kreditorlarına müraciət edilir və "
                "Birliyin aktivləri, əgər varsa, nağd pula çevrilərək "
                "kreditorlara ödənilir."
            ),
            p(
                "Birlik kreditordursa, debitor borcları yığılır. Debitor "
                "borcları alındıqdan və borclar ödənildikdən sonra qalan "
                "bütün maliyyə vəsaitləri, əmlak və hüquqlar Ümumi "
                "Yığıncaqda müəyyən edilmiş yerə köçürülür. Köçürüləcək "
                "yer Ümumi Yığıncaqda müəyyən edilmədikdə, Birliyin "
                "yerləşdiyi vilayətdə məqsədinə ən yaxın olan və "
                "Birliyin ləğv edildiyi tarixdə üzvlərinin sayı ən çox "
                "olan birliyə verilir."
            ),
            p(
                "Yerli inzibati orqanlar tərəfindən üzrlü səbəbə görə "
                "verilən əlavə müddətlər istisna olmaqla, ləğvetmə ilə "
                "bağlı bütün əməliyyatlar ləğvetmə hesabatında "
                "göstərilir və ləğvetmə qaydaları üç ay ərzində başa "
                "çatdırılır."
            ),
            p(
                "Birliyin ləğvi və maliyyə vəsaitlərinin, əmlakının və "
                "hüquqlarının təhvil verilməsi başa çatdıqdan sonra "
                "ləğvetmə komissiyası yeddi gün müddətində Birliyin "
                "mərkəzi qərargahının yerləşdiyi yer üzrə yerli inzibati "
                "orqana məktubla məlumat verməlidir və bu məktuba "
                "ləğvetmə aktı əlavə edilməlidir."
            ),
            p(
                "İdarə Heyətinin sonuncu üzvləri ləğvetmə komissiyası "
                "olaraq Birliyin kitab və qeydlərinin saxlanmasına "
                "cavabdehdirlər. Bu vəzifə komissiya üzvlərindən birinə "
                "də həvalə edilə bilər. Bu kitablar və qeydlər beş il "
                "müddətində saxlanılmalıdır."
            ),
        ],
    ),
    (
        "section-26",
        "Hökm əksikliyi",
        "Maddə 26.",
        [
            p(
                "Bu nizamnamədə göstərilməyən məsələlərdə Birliklər "
                "Qanunu, Türkiyə Mülki Məcəlləsi, bu qanunlara istinadla "
                "çıxarılan Birliklər Nizamnaməsi və birliklərlə bağlı "
                "digər müvafiq qanunvericilik aktları tətbiq edilir."
            ),
            p(
                "Müvəqqəti maddə 1 — Birliyin orqanları ilk Ümumi "
                "Yığıncaqda formalaşana qədər aşağıda göstərilən "
                "müvəqqəti İdarə Heyəti üzvləri Birliyi təmsil edəcək və "
                "Birliyə aid işləri və əməliyyatları həyata keçirəcəklər."
            ),
        ],
    ),
]


def render_section(anchor_id: str, title: str, article_label: str, blocks: list[str]) -> str:
    parts = [
        f'<section class="charter-card" id="{anchor_id}">',
        f'<div class="article-separate-title">{h(title, quote=False)}</div>',
        '<div class="section-head">',
        '<span class="icon">📜</span>',
        f"<h2>{h(article_label, quote=False)}</h2>",
        "</div>",
        '<div class="charter-body">',
        *blocks,
        "</div>",
        "</section>",
    ]
    return "\n".join(parts)


def build_stack() -> str:
    return "\n".join(render_section(*section) for section in SECTIONS)


def fix_html_attrs(text: str) -> str:
    return text.replace(
        '<html lang="az" lang="az"',
        '<html lang="az"',
        1,
    )


def fix_footer(text: str) -> str:
    text = text.replace(
        '<div class="footer-col"><div class="footer-title">Əlaqə</div>',
        '<div class="footer-col"><h4 class="footer-title">Əlaqə</h4>',
        1,
    )
    text = text.replace(
        '<div class="footer-col"><div class="footer-title">Ünvan</div>',
        '<div class="footer-col"><h4 class="footer-title">Ünvan</h4>',
        1,
    )
    text = text.replace(
        '<div class="footer-col"><div class="footer-title">Rəhbərlik</div>',
        '<div class="footer-col"><h4 class="footer-title">Rəhbərlik</h4>',
        1,
    )
    text = text.replace(
        '<div class="footer-bottom">© 2026 DAAB / WAAS — All Rights Reserved</div>',
        '<div class="footer-bottom">© 2026 DAAB — Bütün hüquqlar qorunur</div>',
        1,
    )
    text = text.replace(
        '<div class="footer-bottom">© 2026 DAAB — All Rights Reserved</div>',
        '<div class="footer-bottom">© 2026 DAAB — Bütün hüquqlar qorunur</div>',
        1,
    )
    return text


def main() -> None:
    path = ROOT / "az" / "charter.html"
    text = path.read_text(encoding="utf-8")

    pattern = re.compile(
        r'(<div class="charter-stack">)(.*?)(</div>\s*</div>\s*</main>)',
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise SystemExit('Could not locate <div class="charter-stack"> block in az/charter.html')

    new_stack = "\n" + build_stack() + "\n"
    text = text[: match.start(2)] + new_stack + text[match.end(2):]

    text = fix_html_attrs(text)
    text = fix_footer(text)

    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"Updated az/charter.html — rebuilt {len(SECTIONS)} sections, repaired head + footer.")


if __name__ == "__main__":
    main()
