#!/usr/bin/env python3
"""Build az/en forum/2024/logistics.html from shared templates."""
from __future__ import annotations

from _paths import ROOT

import importlib.util

_spec = importlib.util.spec_from_file_location("_embed_static_nav", ROOT / "helpers" / "_embed_static_nav.py")
_embed = importlib.util.module_from_spec(_spec)
assert _spec.loader
_spec.loader.exec_module(_embed)

HEAD = """\
<link href="../../../css/daab-fonts.css?v=1" rel="stylesheet"/>
<link href="../../../css/daab-common.css?v=67" rel="stylesheet"/>
<link href="../../../css/daab-perf.css?v=1" rel="stylesheet"/>
<link href="../../../css/daab-mobile.css?v=13" rel="stylesheet"/>
<link href="../../../css/daab-sticky-chrome.css?v=1" rel="stylesheet"/>
<link href="../../../css/daab-search.css?v=4" rel="stylesheet"/>
<link href="../../../css/daab-back-to-top.css?v=2" rel="stylesheet"/>
<link href="../../../css/daab-lang.css?v=13" rel="stylesheet"/>
<link href="../../../css/daab-nav-mega.css?v=69" rel="stylesheet"/>
<link href="../../../css/daab-hero-summary.css?v=13" rel="stylesheet"/>
<link href="../../../css/daab-sidebar-widget.css?v=6" rel="stylesheet"/>
<link href="../../../css/daab-activities-layout.css?v=19" rel="stylesheet"/>
<link href="../../../css/daab-forum-content.css?v=43" rel="stylesheet"/>
<link href="../../../css/daab-forum-logistics.css?v=1" rel="stylesheet"/>
<script src="../../../js/daab-mobile.js?v=6" defer></script>
<script src="../../../js/daab-perf.js?v=1" defer></script>
<script src="../../../js/daab-sticky-chrome.js?v=3" defer></script>
<script src="../../../js/daab-back-to-top.js?v=3" defer></script>
<script src="../../../js/daab-i18n.js?v=32" defer></script>
<script src="../../../js/daab-lang-position.js?v=7" defer></script>
<script src="../../../js/daab-nav.js?v=31" defer></script>
<script src="../../../js/daab-primary-nav.js?v=52" defer></script>
<script src="../../../js/daab-shell.js?v=13" defer></script>
<script src="../../../js/daab-search.js?v=9" defer></script>"""

TOC_SCRIPT = """\
<script>
(function () {
  const links = Array.from(document.querySelectorAll('#logisticsTOC a[href^="#"]'));
  const ids = links.map(a => a.getAttribute('href').slice(1));
  const cards = ids.map(id => document.getElementById(id)).filter(Boolean);
  const eventsWidget = document.querySelector('.sidebar-widget');
  const eventsToggle = document.querySelector('.events-menu-toggle');
  const mobileQuery = window.matchMedia('(max-width: 1060px)');

  function activate(link) {
    links.forEach(a => a.classList.remove('tl-active'));
    if (link) link.classList.add('tl-active');
  }

  function closeEventsMenu() {
    if (!eventsWidget || !eventsToggle) return;
    eventsWidget.classList.remove('events-open');
    eventsToggle.setAttribute('aria-expanded', 'false');
  }

  function toggleEventsMenu() {
    if (!eventsWidget || !eventsToggle) return;
    const open = eventsWidget.classList.toggle('events-open');
    eventsToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  function jumpToTarget(event) {
    const link = event.currentTarget;
    const id = link.getAttribute('href').slice(1);
    const target = document.getElementById(id);
    if (!target) return;
    event.preventDefault();
    activate(link);
    const Pos = window.DAAB_LANG_POSITION;
    if (Pos && Pos.scrollToAnchor) {
      Pos.scrollToAnchor(id, false);
    } else {
      target.scrollIntoView({ block: 'start', behavior: 'auto' });
    }
    history.pushState(null, '', link.getAttribute('href'));
    if (mobileQuery.matches) closeEventsMenu();
  }

  function onScroll() {
    const mid = window.scrollY + window.innerHeight * 0.35;
    let active = null;
    for (let i = cards.length - 1; i >= 0; i--) {
      if (cards[i] && cards[i].offsetTop <= mid) {
        active = i;
        break;
      }
    }
    activate(active !== null ? links[active] : null);
  }

  links.forEach(link => link.addEventListener('click', jumpToTarget));
  if (eventsToggle) {
    eventsToggle.addEventListener('click', event => {
      event.stopPropagation();
      toggleEventsMenu();
    });
  }
  document.addEventListener('click', event => {
    if (!mobileQuery.matches || !eventsWidget || !eventsWidget.classList.contains('events-open')) return;
    if (eventsWidget.contains(event.target)) return;
    closeEventsMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeEventsMenu();
  });
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
</script>"""

AZ_MAIN = """
<article class="news-card logistics-card" id="umumi-melumat">
<div class="card-header"><h2 class="card-title">Ümumi məlumat</h2></div>
<div class="card-body">
<div class="logistics-callout">
<p><strong>Ödənişsiz:</strong> Xarici iştirakçıların təyyarə biletləri və 4 gecəlik (8–11 sentyabr) hotel xərcləri Azərbaycan Respublikası Diasporla İş üzrə Dövlət Komitəsi və Azərbaycan Respublikası Elm və Təhsil Nazirliyi tərəfindən qarşılanacaqdır.</p>
<p><strong>Məskunlaşma:</strong> Qonaqların Bakıdakı Badamdar Hotel &amp; Residences mehmanxanasında məskunlaşdırılması nəzərdə tutulur.</p>
<p><strong>Diqqət:</strong> Heydər Əliyev adına Bakı Beynəlxalq Hava Limanında qonaqların qarşılanması və ölkələrinə yola salınması planlaşdırılmamışdır.</p>
</div>
<p class="card-text">Hava limanını Bakı şəhəri ilə bağlayan müxtəlif nəqliyyat vasitələri mövcuddur. Eyni qaydada şəhərdən Heydər Əliyev Beynəlxalq Hava Limanına yetişmək mümkündür.</p>
</div>
</article>

<article class="news-card logistics-card" id="neqliyyat">
<div class="card-header"><h2 class="card-title">Hava limanından şəhərə</h2></div>
<div class="card-body">
<ol class="logistics-transport-list">
<li>
<strong>Taksi</strong>
Hava limanının çıxışında rəsmi taksilər mövcuddur. Onlar 7/24 fəaliyyət göstərir. Bolt və Uber mobil tətbiqlərinin vasitəsilə bu özəl taksi şirkətlərinin xidmətlərindən də yararlanmaq olar.
</li>
<li>
<strong>Hava limanı avtobusları (BakuBus)</strong>
Hər 25 dəqiqədən bir «H1–Airport Ekspres» avtobusları Hava Limanı → «Koroğlu» HUB → «28 May» metro stansiyası marşrutu üzrə hərəkət edirlər. Ödəniş hava limanında quraşdırılmış xüsusi aparatlar vasitəsilə əldə oluna bilən «BakıKart» kartları ilə həyata keçirilə bilər. Ətraflı məlumat üçün <a href="https://www.bakubus.az/" rel="noopener noreferrer" target="_blank">Baku Bus</a> saytına baxın.
</li>
<li>
<strong>Avtomobil kirayəsi</strong>
Hava limanında avtomobil kirayəsi təqdim edən müxtəlif şirkətlər mövcuddur.
</li>
</ol>
</div>
</article>

<article class="news-card logistics-card" id="hava-limani">
<div class="card-header"><h2 class="card-title">Heydər Əliyev adına Bakı Beynəlxalq Hava Limanı</h2></div>
<div class="card-body">
<p class="card-text">Heydər Əliyev Beynəlxalq Hava Limanı, Azərbaycanın əsas beynəlxalq qapısı və Cənubi Qafqaz regionunun ən işlək hava limanlarından biridir.</p>
<p class="logistics-fact-title">Məkan</p>
<p class="card-text">Hava limanı, Azərbaycanın paytaxtı Bakıdan təxminən 20 kilometr şimal-şərqdə yerləşir.</p>
<figure class="logistics-map">
<iframe title="Heydər Əliyev Beynəlxalq Hava Limanı — Google Xəritə" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen src="https://www.google.com/maps?q=Heydar+Aliyev+International+Airport,+Baku,+Azerbaijan&amp;hl=az&amp;z=13&amp;output=embed"></iframe>
<figcaption><a href="https://www.google.com/maps/search/?api=1&amp;query=Heydar+Aliyev+International+Airport,+Baku,+Azerbaijan" rel="noopener noreferrer" target="_blank">Google Xəritədə aç — Heydər Əliyev Beynəlxalq Hava Limanı</a></figcaption>
</figure>
<p class="logistics-fact-title">Tarix</p>
<p class="card-text">Əvvəlcə Bina Beynəlxalq Hava Limanı kimi tanınan bu hava limanı, 2004-cü ildə Azərbaycanın üçüncü prezidenti Heydər Əliyevin adını almışdır.</p>
<p class="logistics-fact-title">Təsisatlar</p>
<p class="card-text">Hava limanında iki sərnişin terminalı və iki yük terminalı var. 2014-cü ildə açılan Terminal 1, illik 6 milyon sərnişin qəbul etmək üçün nəzərdə tutulmuşdur və mağazalar, restoranlar, kafelər və duty-free mağazalar kimi müasir imkanlarla təchiz olunmuşdur.</p>
<p class="logistics-fact-title">Dizayn</p>
<p class="card-text">Terminal 1, Arup Group tərəfindən dizayn edilmiş üçbucaq forması və yarı şəffaf damı ilə diqqət çəkir; interyerlər isə Türkiyənin AUTOBAN şirkəti tərəfindən dizayn edilmiş palıd-şpon «kokonları» ilə təchiz olunmuşdur.</p>
<p class="logistics-fact-title">Hava yolları</p>
<p class="card-text">Bu hava limanı, Azərbaycan Hava Yolları, Buta Airways və bir neçə yük hava yolları üçün mərkəz rolunu oynayır.</p>
<p class="logistics-fact-title">Xidmətlər</p>
<p class="card-text">Hava limanı salonlar, spa və səmərəli baqaj idarəetmə sistemləri kimi müxtəlif xidmətlər təklif edir.</p>
</div>
</article>

<article class="news-card logistics-card" id="gulustan">
<div class="card-header"><h2 class="card-title">Gülüstan sarayı</h2></div>
<div class="card-body">
<p class="card-text">Gülüstan sarayı, Bakıda, Azərbaycan Respublikasının əhəmiyyətli dövlət konvensiya mərkəzidir. İstiqlaliyyət küçəsində yerləşir və şəhərin və Bakı körfəzinin möhtəşəm mənzərəsini təqdim edir.</p>
<figure class="logistics-map">
<iframe title="Gülüstan sarayı — Google Xəritə" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen src="https://www.google.com/maps?q=G%C3%BCl%C3%BCstan+Palace,+Istiqlaliyyat+Street,+Baku,+Azerbaijan&amp;hl=az&amp;z=16&amp;output=embed"></iframe>
<figcaption><a href="https://www.google.com/maps/search/?api=1&amp;query=G%C3%BCl%C3%BCstan+Palace,+Istiqlaliyyat+Street,+Baku,+Azerbaijan" rel="noopener noreferrer" target="_blank">Google Xəritədə aç — Gülüstan sarayı</a></figcaption>
</figure>
<p class="logistics-fact-title">Tarix</p>
<p class="card-text">1970–1980-ci illər arasında tikilmişdir və Sovet dövründə Gülüstan Toy Sarayı Kompleksi kimi tanınırdı. H. Əmirxanov və N. Hacıbəyov da daxil olmaqla bir qrup memar tərəfindən dizayn edilmişdir.</p>
<p class="logistics-fact-title">Memarlıq</p>
<p class="card-text">Saray, ənənəvi Azərbaycan memarlıq motivlərini əks etdirir, arxlarla çərçivələnmiş balkonlarla zərif və yüngül bir görünüş yaradır.</p>
<p class="logistics-fact-title">Təsisatlar</p>
<p class="card-text">1000-dən çox insan tutumuna malik əsas zal, kino, uşaq kafesi, barlar, diskoteka otaqları və suvenir mağazası var. Saray həmçinin lüks bir salon restoranı və banket otağına malikdir.</p>
<p class="logistics-fact-title">Tədbirlər</p>
<p class="card-text">Neft və qaz müqavilələrinin imzalanması, beynəlxalq konfranslar və milli bayramlar kimi müxtəlif rəsmi tədbirlərə ev sahibliyi edir.</p>
</div>
</article>

<article class="news-card logistics-card" id="badamdar">
<div class="card-header"><h2 class="card-title">Badamdar Hotel and Residences</h2></div>
<div class="card-body">
<p class="card-text">Badamdar Hotel and Residences, Bakıda yerləşən lüks 5 ulduzlu bir oteldir.</p>
<p class="logistics-fact-title">Məkan</p>
<p class="card-text">Mikayıl Müşfiq 1, Bakı ünvanında yerləşir və şəhərin müxtəlif cazibə mərkəzlərinə asan çıxış imkanı təklif edir.</p>
<figure class="logistics-map">
<iframe title="Badamdar Hotel and Residences — Google Xəritə" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen src="https://www.google.com/maps?q=Badamdar+Hotel+and+Residences,+Mikayil+Mushvig+1,+Baku,+Azerbaijan&amp;hl=az&amp;z=16&amp;output=embed"></iframe>
<figcaption><a href="https://www.google.com/maps/search/?api=1&amp;query=Badamdar+Hotel+and+Residences,+Mikayil+Mushvig+1,+Baku,+Azerbaijan" rel="noopener noreferrer" target="_blank">Google Xəritədə aç — Badamdar Hotel and Residences</a></figcaption>
</figure>
<p class="logistics-fact-title">Təsisatlar</p>
<p class="card-text">Oteldə ümumi salon, terras, restoran və bar var. Qonaqlar pulsuz WiFi, otaq xidməti, 24 saat fəaliyyət göstərən resepsiyon, spa və sağlamlıq mərkəzi, qapalı hovuz, fitness mərkəzi və sauna kimi imkanlardan istifadə edə bilərlər.</p>
<p class="logistics-fact-title">Otaqlar</p>
<p class="card-text">Otaqlar kondisioner, oturma sahəsi, peyk kanalları ilə düz ekran TV, təhlükəsizlik qutusu və bidet, pulsuz tualet ləvazimatları və fen ilə təchiz olunmuş xüsusi vanna otağı ilə təchiz olunmuşdur. Bəzi otaqlarda şəhər mənzərəsi olan balkonlar da var.</p>
<p class="logistics-fact-title">Yemək</p>
<p class="card-text">Oteldə müxtəlif yemək seçimləri təklif edən iki restoran var.</p>
<p class="logistics-fact-title">Tədbirlər</p>
<p class="card-text">Otel həm istirahət, həm də işgüzar səyahətçilər üçün çox yönlü bir seçim edərək, görüşlər və toylar üçün imkanlar təqdim edir.</p>
<p class="logistics-fact-title">Əlavə xidmətlər</p>
<p class="card-text">Otel hava limanı transfer xidməti, valyuta mübadiləsi və konsyerj xidmətləri təklif edir.</p>
</div>
</article>

<article class="news-card logistics-card" id="qidalanma">
<div class="card-header"><h2 class="card-title">Qidalanma</h2></div>
<div class="card-body">
<div class="program-table-wrap">
<table class="program-table logistics-meal-table">
<thead>
<tr><th>Tarix</th><th>Səhər yeməyi</th><th>Nahar</th><th>Şam yeməyi</th><th>Qeyd</th></tr>
</thead>
<tbody>
<tr>
<td>8 sentyabr 2024</td>
<td>—</td>
<td><span class="meal-tag meal-tag--self">Öz hesabına</span></td>
<td><span class="meal-tag meal-tag--self">Öz hesabına</span></td>
<td>—</td>
</tr>
<tr>
<td>9 sentyabr 2024</td>
<td><span class="meal-tag meal-tag--included">Hotel (ödənişsiz)</span></td>
<td><span class="meal-tag meal-tag--included">Gülüstan sarayında (ödənişsiz)</span></td>
<td><span class="meal-tag meal-tag--optional">İstəyə görə</span></td>
<td>Şam yeməyi iştirakçıların öz hesabına ödənilir; Bakını gəzmək imkanı verilir.</td>
</tr>
<tr>
<td>10 sentyabr 2024</td>
<td><span class="meal-tag meal-tag--included">Hotel (ödənişsiz)</span></td>
<td><span class="meal-tag meal-tag--included">Gülüstan sarayında (ödənişsiz)</span></td>
<td><span class="meal-tag meal-tag--included">Ziyafət — Gülüstan sarayında (ödənişsiz)</span></td>
<td>—</td>
</tr>
<tr>
<td>11 sentyabr 2024</td>
<td>—</td>
<td><span class="meal-tag meal-tag--included">Ödənişsiz</span></td>
<td><span class="meal-tag meal-tag--included">Ödənişsiz</span></td>
<td>Xankəndidə Qarabağ Universitetinin ziyarəti, Şuşaya səyahət.</td>
</tr>
</tbody>
</table>
</div>
<p class="card-text">9 sentyabr tarixində şam yeməyi iştirakçıların öz ixtiyarına verilir. Bu, istirakçılara istədikləri yerə gedərək, istədikləri menyunu seçmək və Bakını gəzmək üçün imkan yaradır.</p>
</div>
</article>
"""

EN_MAIN = """
<article class="news-card logistics-card" id="umumi-melumat">
<div class="card-header"><h2 class="card-title">General information</h2></div>
<div class="card-body">
<div class="logistics-callout">
<p><strong>At no charge:</strong> Flight tickets for international participants and four nights of hotel accommodation (8–11 September) will be covered by the State Committee on Diaspora Affairs of the Republic of Azerbaijan and the Ministry of Science and Education of the Republic of Azerbaijan.</p>
<p><strong>Accommodation:</strong> Guests are expected to stay at Badamdar Hotel &amp; Residences in Baku.</p>
<p><strong>Please note:</strong> Meet-and-greet at Heydar Aliyev International Airport and airport send-off upon departure are not planned.</p>
</div>
<p class="card-text">Various transport options connect the airport with the city of Baku. The same options can be used to reach Heydar Aliyev International Airport from the city.</p>
</div>
</article>

<article class="news-card logistics-card" id="neqliyyat">
<div class="card-header"><h2 class="card-title">From the airport to the city</h2></div>
<div class="card-body">
<ol class="logistics-transport-list">
<li>
<strong>Taxi</strong>
Official taxis are available at the airport exit and operate 24/7. Bolt and Uber mobile apps can also be used to book these private taxi services.
</li>
<li>
<strong>Airport buses (BakuBus)</strong>
Every 25 minutes, H1 Airport Express buses run on the route Airport → Koroglu HUB → 28 May metro station. Fares can be paid with BakiKart cards, available from machines at the airport. For details, see the <a href="https://www.bakubus.az/" rel="noopener noreferrer" target="_blank">Baku Bus</a> website.
</li>
<li>
<strong>Car rental</strong>
Several car rental companies operate at the airport.
</li>
</ol>
</div>
</article>

<article class="news-card logistics-card" id="hava-limani">
<div class="card-header"><h2 class="card-title">Heydar Aliyev International Airport</h2></div>
<div class="card-body">
<p class="card-text">Heydar Aliyev International Airport is Azerbaijan's main international gateway and one of the busiest airports in the South Caucasus region.</p>
<p class="logistics-fact-title">Location</p>
<p class="card-text">The airport is located approximately 20 kilometres north-east of Baku, the capital of Azerbaijan.</p>
<figure class="logistics-map">
<iframe title="Heydar Aliyev International Airport — Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen src="https://www.google.com/maps?q=Heydar+Aliyev+International+Airport,+Baku,+Azerbaijan&amp;hl=en&amp;z=13&amp;output=embed"></iframe>
<figcaption><a href="https://www.google.com/maps/search/?api=1&amp;query=Heydar+Aliyev+International+Airport,+Baku,+Azerbaijan" rel="noopener noreferrer" target="_blank">Open in Google Maps — Heydar Aliyev International Airport</a></figcaption>
</figure>
<p class="logistics-fact-title">History</p>
<p class="card-text">Originally known as Bina International Airport, it was renamed in 2004 after Heydar Aliyev, the third President of Azerbaijan.</p>
<p class="logistics-fact-title">Facilities</p>
<p class="card-text">The airport has two passenger terminals and two cargo terminals. Terminal 1, opened in 2014, is designed to handle six million passengers per year and offers modern amenities including shops, restaurants, cafés and duty-free outlets.</p>
<p class="logistics-fact-title">Design</p>
<p class="card-text">Terminal 1, designed by Arup Group, is noted for its triangular form and semi-transparent roof; interiors feature oak-veneer "cocoons" designed by Turkey's AUTOBAN studio.</p>
<p class="logistics-fact-title">Airlines</p>
<p class="card-text">The airport serves as a hub for Azerbaijan Airlines, Buta Airways and several cargo carriers.</p>
<p class="logistics-fact-title">Services</p>
<p class="card-text">The airport offers lounges, spa facilities and efficient baggage handling systems, among other services.</p>
</div>
</article>

<article class="news-card logistics-card" id="gulustan">
<div class="card-header"><h2 class="card-title">Gulustan Palace</h2></div>
<div class="card-body">
<p class="card-text">Gulustan Palace is a major state convention centre in Baku, Azerbaijan. It stands on Istiqlaliyyat Street and offers commanding views of the city and Baku Bay.</p>
<figure class="logistics-map">
<iframe title="Gulustan Palace — Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen src="https://www.google.com/maps?q=G%C3%BCl%C3%BCstan+Palace,+Istiqlaliyyat+Street,+Baku,+Azerbaijan&amp;hl=en&amp;z=16&amp;output=embed"></iframe>
<figcaption><a href="https://www.google.com/maps/search/?api=1&amp;query=G%C3%BCl%C3%BCstan+Palace,+Istiqlaliyyat+Street,+Baku,+Azerbaijan" rel="noopener noreferrer" target="_blank">Open in Google Maps — Gulustan Palace</a></figcaption>
</figure>
<p class="logistics-fact-title">History</p>
<p class="card-text">Built between the 1970s and 1980s, it was known in the Soviet era as the Gulustan Wedding Palace Complex. It was designed by a team of architects including H. Amirkhanov and N. Hajibeyov.</p>
<p class="logistics-fact-title">Architecture</p>
<p class="card-text">The palace reflects traditional Azerbaijani architectural motifs, with arched balconies that create an elegant, light appearance.</p>
<p class="logistics-fact-title">Facilities</p>
<p class="card-text">It includes a main hall seating more than 1,000 guests, a cinema, children's café, bars, discotheque rooms and a souvenir shop, as well as a luxury lounge restaurant and banquet hall.</p>
<p class="logistics-fact-title">Events</p>
<p class="card-text">The palace hosts official events including oil and gas contract signings, international conferences and national celebrations.</p>
</div>
</article>

<article class="news-card logistics-card" id="badamdar">
<div class="card-header"><h2 class="card-title">Badamdar Hotel &amp; Residences</h2></div>
<div class="card-body">
<p class="card-text">Badamdar Hotel &amp; Residences is a luxury five-star hotel in Baku.</p>
<p class="logistics-fact-title">Location</p>
<p class="card-text">It is located at Mikayil Mushvig 1, Baku, with convenient access to the city's main attractions.</p>
<figure class="logistics-map">
<iframe title="Badamdar Hotel and Residences — Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen src="https://www.google.com/maps?q=Badamdar+Hotel+and+Residences,+Mikayil+Mushvig+1,+Baku,+Azerbaijan&amp;hl=en&amp;z=16&amp;output=embed"></iframe>
<figcaption><a href="https://www.google.com/maps/search/?api=1&amp;query=Badamdar+Hotel+and+Residences,+Mikayil+Mushvig+1,+Baku,+Azerbaijan" rel="noopener noreferrer" target="_blank">Open in Google Maps — Badamdar Hotel &amp; Residences</a></figcaption>
</figure>
<p class="logistics-fact-title">Facilities</p>
<p class="card-text">The hotel offers a shared lounge, terrace, restaurant and bar. Guests can use free Wi‑Fi, room service, 24-hour reception, a spa and wellness centre, indoor pool, fitness centre and sauna.</p>
<p class="logistics-fact-title">Rooms</p>
<p class="card-text">Rooms are air-conditioned and equipped with a seating area, flat-screen TV with satellite channels, a safe, and a private bathroom with bidet, complimentary toiletries and a hairdryer. Some rooms have balconies with city views.</p>
<p class="logistics-fact-title">Dining</p>
<p class="card-text">Two on-site restaurants offer a range of dining options.</p>
<p class="logistics-fact-title">Events</p>
<p class="card-text">The hotel caters to both leisure and business travellers and provides facilities for meetings and celebrations.</p>
<p class="logistics-fact-title">Additional services</p>
<p class="card-text">Airport transfers, currency exchange and concierge services are available.</p>
</div>
</article>

<article class="news-card logistics-card" id="qidalanma">
<div class="card-header"><h2 class="card-title">Catering and meals</h2></div>
<div class="card-body">
<div class="program-table-wrap">
<table class="program-table logistics-meal-table">
<thead>
<tr><th>Date</th><th>Breakfast</th><th>Lunch</th><th>Dinner</th><th>Notes</th></tr>
</thead>
<tbody>
<tr>
<td>8 September 2024</td>
<td>—</td>
<td><span class="meal-tag meal-tag--self">At own expense</span></td>
<td><span class="meal-tag meal-tag--self">At own expense</span></td>
<td>—</td>
</tr>
<tr>
<td>9 September 2024</td>
<td><span class="meal-tag meal-tag--included">Hotel (included)</span></td>
<td><span class="meal-tag meal-tag--included">Gulustan Palace (included)</span></td>
<td><span class="meal-tag meal-tag--optional">Optional</span></td>
<td>Dinner at participants' own expense; time to explore Baku.</td>
</tr>
<tr>
<td>10 September 2024</td>
<td><span class="meal-tag meal-tag--included">Hotel (included)</span></td>
<td><span class="meal-tag meal-tag--included">Gulustan Palace (included)</span></td>
<td><span class="meal-tag meal-tag--included">Banquet — Gulustan Palace (included)</span></td>
<td>—</td>
</tr>
<tr>
<td>11 September 2024</td>
<td>—</td>
<td><span class="meal-tag meal-tag--included">Included</span></td>
<td><span class="meal-tag meal-tag--included">Included</span></td>
<td>Visit to Karabakh University in Khankendi; trip to Shusha.</td>
</tr>
</tbody>
</table>
</div>
<p class="card-text">On 9 September, dinner is at participants' discretion. This allows them to choose where to dine, select their preferred menu and explore Baku at leisure.</p>
</div>
</article>
"""

PAGES = {
    "az": {
        "path": ROOT / "az" / "forum" / "2024" / "logistics.html",
        "lang": "az",
        "title": "Logistika — DAAB",
        "description": "Forum 2024 — xarici iştirakçılar üçün nəqliyyat, Badamdar Hotel &amp; Residences, Gülüstan sarayı və qidalanma qaydaları.",
        "skip": "Məzmuna keç",
        "nav_label": "Əsas naviqasiya",
        "crumb_home": "Ana səhifə",
        "crumb_forum": "Forum 2024",
        "crumb_current": "Logistika",
        "h1": "Nəqliyyat, <span>hotel, qidalanma</span>",
        "subtitle": "Forum 2024 iştirakçıları üçün səyahət, məskunlaşma və yemək təşkili",
        "panel_label": "Logistika icmalı",
        "panel_title": "Logistika icmalı",
        "panel_lead": "Xarici iştirakçıların uçuş biletləri və 8–11 sentyabr tarixlərində dörd gecəlik hotel xərcləri dövlət tərəfindən qarşılanır. Forum tədbirləri Gülüstan sarayında, qonaqlar Badamdar Hotel &amp; Residences-də məskunlaşdırılır.",
        "toc_label": "📋 Mündəricat",
        "toc_toggle": "Mündəricat menyusunu aç",
        "toc_items": [
            ("umumi-melumat", "Ümumi məlumat"),
            ("neqliyyat", "Hava limanından şəhərə"),
            ("hava-limani", "Heydər Əliyev hava limanı"),
            ("gulustan", "Gülüstan sarayı"),
            ("badamdar", "Badamdar Hotel"),
            ("qidalanma", "Qidalanma"),
        ],
        "main": AZ_MAIN,
    },
    "en": {
        "path": ROOT / "en" / "forum" / "2024" / "logistics.html",
        "lang": "en",
        "title": "Logistics — WAAS",
        "description": "Forum 2024 — transport, Badamdar Hotel &amp; Residences, Gulustan Palace and meal arrangements for international participants.",
        "skip": "Skip to content",
        "nav_label": "Main navigation",
        "crumb_home": "Home",
        "crumb_forum": "Forum 2024",
        "crumb_current": "Logistics",
        "h1": "Transport, <span>hotel, catering</span>",
        "subtitle": "Travel, accommodation, and meal arrangements for Forum 2024 participants",
        "panel_label": "Logistics overview",
        "panel_title": "Logistics overview",
        "panel_lead": "Flight tickets for international participants and four nights of hotel accommodation (8–11 September) are covered by the state. Forum events take place at Gulustan Palace; guests stay at Badamdar Hotel &amp; Residences.",
        "toc_label": "📋 Contents",
        "toc_toggle": "Open table of contents",
        "toc_items": [
            ("umumi-melumat", "General information"),
            ("neqliyyat", "From the airport to the city"),
            ("hava-limani", "Heydar Aliyev International Airport"),
            ("gulustan", "Gulustan Palace"),
            ("badamdar", "Badamdar Hotel &amp; Residences"),
            ("qidalanma", "Catering and meals"),
        ],
        "main": EN_MAIN,
    },
}


def build_page(cfg: dict) -> str:
    lang = cfg["lang"]
    nav = _embed.forum_nav_strip(lang, active_nav_id="forum-logistics")
    toc_lines = "\n".join(
        f'<li><a href="#{anchor}">{label}</a></li>' for anchor, label in cfg["toc_items"]
    )
    return f"""<!DOCTYPE html>
<html lang="{lang}" data-daab-lang="{lang}" data-daab-asset-root="../../../" data-daab-page-id="forum-logistics" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{cfg["title"]}</title>
<meta name="description" content="{cfg["description"]}"/>
{HEAD}
</head>
<body>
<a class="skip" href="#content">{cfg["skip"]}</a>
{nav}
<div class="breadcrumbs forum-breadcrumbs" data-daab-breadcrumbs-static="1" role="navigation" aria-label="{'Səhifə yolu' if lang == 'az' else 'Breadcrumb'}"><a href="../../index.html">{cfg["crumb_home"]}</a><span aria-hidden="true">›</span><a href="index.html">{cfg["crumb_forum"]}</a><span aria-hidden="true">›</span><span class="forum-breadcrumbs-current" aria-current="page">{cfg["crumb_current"]}</span></div>
<header class="page-hero">
<div class="hero-wrap shell">
<section class="hero-copy">
<h1>{cfg["h1"]}</h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">{cfg["subtitle"]}</p>
</section>
<aside aria-label="{cfg["panel_label"]}" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">{cfg["panel_title"]}</h2>
<div class="panel-copy">
<p class="panel-copy-lead">{cfg["panel_lead"]}</p>
</div>
</div>
</aside>
</div>
</header>
<div class="content-wrap">
<aside class="sidebar">
<div class="sidebar-widget">
<div class="widget-head">
<span>{cfg["toc_label"]}</span>
<button type="button" class="events-menu-toggle" aria-controls="logisticsTOC" aria-expanded="false" aria-label="{cfg["toc_toggle"]}"><span></span><span></span><span></span></button>
</div>
<div class="widget-body">
<ul class="timeline-list" id="logisticsTOC">
{toc_lines}
</ul>
</div>
</div>
</aside>
<main class="news-feed main" id="content">
{cfg["main"].strip()}
</main>
</div>
{TOC_SCRIPT}
</body>
</html>
"""


def main() -> None:
    for cfg in PAGES.values():
        cfg["path"].write_text(build_page(cfg), encoding="utf-8", newline="\n")
        print(cfg["path"].relative_to(ROOT))


if __name__ == "__main__":
    main()
