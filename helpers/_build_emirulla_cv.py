from pathlib import Path

OUT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site\cv\emirulla_memmedov.html")

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Curriculum Vitae — Emirullah Mehmetov</title>
  <style>
    :root {
      --blue-dark:   #1A6FA8;
      --blue-mid:    #2E9FD4;
      --blue-light:  #D0EEFB;
      --blue-accent: #56B4E8;
      --blue-soft:   #AACDE6;
      --body-text:   #555555;
      --footer-text: #999999;
      --bg:          #F2F2F2;
      --white:       #FFFFFF;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Times New Roman', Times, serif; background: var(--bg); color: var(--body-text); line-height: 1.65; }
    .page { max-width: 1080px; margin: 0 auto; padding: 28px 20px 60px; }
    .lang-switch { display: flex; justify-content: flex-end; gap: 8px; margin-bottom: 16px; }
    .lang-switch button { padding: 7px 18px; border: 2px solid var(--blue-dark); background: var(--white); color: var(--blue-dark); font-family: 'Times New Roman', serif; font-size: 14px; font-weight: 700; cursor: pointer; border-radius: 4px; transition: all 0.2s; }
    .lang-switch button.active, .lang-switch button:hover { background: var(--blue-dark); color: var(--white); }
    .lang { display: none; }
    .lang.active { display: inline; }
    .lang.block.active { display: block; }
    .hero { background: var(--blue-dark); color: var(--white); padding: 0; border-radius: 4px 4px 0 0; overflow: hidden; }
    .hero-top { padding: 36px 40px 28px; background: linear-gradient(135deg, #1A6FA8 60%, #2E9FD4 100%); border-bottom: 4px solid var(--blue-mid); display: flex; align-items: center; gap: 32px; }
    .hero-text { flex: 1; min-width: 0; }
    .hero-photo { flex-shrink: 0; margin-left: auto; width: 160px; height: 200px; border-radius: 6px; overflow: hidden; background: var(--white); box-shadow: 0 6px 24px rgba(0,0,0,0.25); border: 3px solid var(--white); }
    .hero-photo img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .cv-label { display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: 0.3em; text-transform: uppercase; color: var(--blue-light); margin-bottom: 10px; }
    h1 { font-size: clamp(28px, 4.5vw, 52px); font-weight: 700; line-height: 1.05; letter-spacing: -0.01em; color: var(--white); margin-bottom: 14px; }
    .subtitle { font-size: 16px; color: rgba(255,255,255,0.88); max-width: 680px; line-height: 1.7; }
    .rank-bar { background: var(--blue-mid); padding: 16px 40px; display: flex; flex-wrap: wrap; gap: 32px; }
    .rank-item dt { font-size: 10px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: rgba(255,255,255,0.75); }
    .rank-item dd { font-size: 15px; font-weight: 700; color: var(--white); margin-top: 2px; }
    .section { background: var(--white); border: 1px solid #d0dde8; border-radius: 4px; overflow: hidden; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(26,111,168,0.07); }
    .section-title { display: flex; align-items: center; margin: 0; padding: 14px 22px; background: var(--blue-dark); color: var(--white); font-size: 17px; font-weight: 700; letter-spacing: 0.03em; }
    .callout { background: var(--blue-light); border-left: 5px solid var(--blue-mid); padding: 18px 22px; margin: 0; color: var(--body-text); font-size: 15px; line-height: 1.75; }
    .competency-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; padding: 20px 22px; }
    .comp-group { background: var(--bg); border: 1px solid #d0dde8; border-left: 4px solid var(--blue-mid); padding: 16px 18px; border-radius: 3px; }
    .comp-group h3 { margin: 0 0 10px; font-size: 15px; font-weight: 700; color: var(--blue-dark); }
    .comp-group ul { margin: 0; padding-left: 18px; color: var(--body-text); font-size: 14px; }
    .comp-group li { margin-bottom: 5px; }
    .timeline { padding: 8px 22px 22px; }
    .item { display: grid; grid-template-columns: 200px 1fr; gap: 24px; padding: 22px 0; border-bottom: 1px solid #e0eaf2; }
    .item:last-child { border-bottom: 0; padding-bottom: 0; }
    .period { font-size: 14px; font-weight: 700; color: var(--blue-dark); padding-top: 3px; line-height: 1.4; }
    .item h3 { margin: 0 0 8px; font-size: 18px; font-weight: 700; color: #333; line-height: 1.3; }
    .role { display: inline-block; padding: 5px 12px; background: var(--blue-light); color: var(--blue-dark); font-size: 13px; font-weight: 700; border-radius: 3px; border: 1px solid var(--blue-accent); margin-bottom: 10px; }
    .item p { margin: 8px 0 0; font-size: 14.5px; color: var(--body-text); line-height: 1.7; }
    .education-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; padding: 20px 22px; }
    .edu-card { background: var(--bg); border: 1px solid #d0dde8; border-top: 4px solid var(--blue-dark); padding: 20px 18px; border-radius: 3px; }
    .edu-card .period { font-size: 13px; color: var(--blue-mid); font-weight: 700; margin-bottom: 8px; letter-spacing: 0.05em; }
    .edu-card h3 { margin: 0 0 8px; font-size: 17px; font-weight: 700; color: var(--blue-dark); line-height: 1.35; }
    .edu-card p { margin: 0; font-size: 14px; color: var(--body-text); line-height: 1.65; }
    .pub-block { padding: 18px 22px; }
    .pub-category { margin-bottom: 22px; }
    .pub-category:last-child { margin-bottom: 0; }
    .pub-category h3 { font-size: 14px; font-weight: 700; color: var(--blue-dark); text-transform: uppercase; letter-spacing: 0.07em; border-bottom: 2px solid var(--blue-light); padding-bottom: 6px; margin-bottom: 12px; }
    .pub-category ol, .pub-category ul { padding-left: 20px; font-size: 14px; color: var(--body-text); line-height: 1.7; }
    .pub-category li { margin-bottom: 6px; }
    .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; border-top: 1px solid #d0dde8; }
    .stat-item { padding: 18px 16px; text-align: center; border-right: 1px solid #d0dde8; }
    .stat-item:last-child { border-right: none; }
    .stat-num { display: block; font-size: 30px; font-weight: 700; color: var(--blue-dark); line-height: 1; margin-bottom: 5px; }
    .stat-label { font-size: 12px; color: var(--body-text); font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; }
    footer { text-align: center; margin-top: 32px; padding-top: 16px; border-top: 1px solid #d0dde8; font-size: 13px; color: var(--footer-text); font-family: 'Times New Roman', serif; }
    @media (max-width: 760px) {
      .competency-grid, .education-grid, .item, .stats { grid-template-columns: 1fr; }
      .hero-top { padding: 26px 20px 20px; flex-direction: column-reverse; gap: 20px; text-align: center; }
      .hero-photo { width: 140px; height: 175px; align-self: flex-end; }
      .subtitle { margin: 0 auto; }
      .rank-bar { padding: 14px 20px; gap: 18px; }
      .timeline { padding: 8px 16px 16px; }
      .stat-item { border-right: none; border-bottom: 1px solid #d0dde8; }
    }
    @media print { body { background: #fff; } .page { padding: 0; } .lang-switch { display: none; } .section { box-shadow: none; break-inside: avoid; } }
  </style>
</head>
<body>
<main class="page">

  <div class="lang-switch">
    <button id="btn-en" type="button" onclick="setLang('en')">English</button>
    <button id="btn-az" type="button" onclick="setLang('az')">Azərbaycan</button>
  </div>

  <header class="hero">
    <div class="hero-top">
      <div class="hero-text">
        <span class="cv-label">
          <span class="lang en">Curriculum Vitae</span>
          <span class="lang az">Tərcümeyi-hal</span>
        </span>
        <h1>
          <span class="lang en">Emirullah M. Mehmetov, Prof. Dr.</span>
          <span class="lang az">Əmirulla M. Məmmədov, Prof. Dr.</span>
        </h1>
        <p class="subtitle">
          <span class="lang en">Internationally recognized scientist in optics, nonlinear optics, metamaterials, photonics, and nanophotonics. Emeritus Professor and leading researcher at NANOTAM, Bilkent University, Ankara. President of the Association of Azerbaijani Scientists in Turkey (ABID). Published as Amirullah M. Mamedov in scientific literature.</span>
          <span class="lang az">Optika, qeyri-xətti optika, metamateriallar, fotonika və nanofotonika sahələrində beynəlxalq səviyyədə tanınan alim. Bilkent Universitetinin NANOTAM mərkəzində fəxri professor və aparıcı elmi işçi, Ankara. Türkiyədə fəaliyyət göstərən Azərbaycanlı Alimlər Assosiasiyasının (ABİD) sədri. Elmi nəşrlərdə Amirullah M. Mamedov adı ilə tanınır.</span>
        </p>
      </div>
      <figure class="hero-photo">
        <img src="../images/scientists-photos/emirulla-memmedov.png" alt="Emirullah Mehmetov" width="160" height="200" loading="eager" />
      </figure>
    </div>
    <dl class="rank-bar">
      <div class="rank-item">
        <dt><span class="lang en">Academic Rank</span><span class="lang az">Akademik rütbə</span></dt>
        <dd><span class="lang en">Professor of Optics; Dr. Sci. (habil.)</span><span class="lang az">Optika professoru; Elmlər doktoru (habil.)</span></dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">Institution</span><span class="lang az">Qurum</span></dt>
        <dd><span class="lang en">Bilkent University, NANOTAM</span><span class="lang az">Bilkent Universiteti, NANOTAM</span></dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">E-mail</span><span class="lang az">E-poçt</span></dt>
        <dd>mamedov@bilkent.edu.tr</dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">Location</span><span class="lang az">Yer</span></dt>
        <dd><span class="lang en">Ankara, Turkey</span><span class="lang az">Ankara, Türkiyə</span></dd>
      </div>
    </dl>
  </header>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Academic Profile</span><span class="lang az">Akademik profil</span></h2>
    <div class="callout">
      <span class="lang en block">Prof. Dr. Emirullah M. Mehmetov (Amirullah M. Mamedov in publications) is a distinguished physicist specializing in optics, nonlinear and laser physics, topological insulators, metamaterials, photonic and phononic crystals, optical information technology, and bio-medical modeling. Born 24 July 1946 in Baku. Ph.D. in physics and mathematics (1973, A.F. Ioffe Institute, Leningrad/St. Petersburg), Doctor of Sciences habilitation (1982, Riga), and Full Professor in Optics (1988, Moscow). Author of more than 350 SCI-indexed international journal articles. Invited speaker at more than 50 international conferences. Research appointments at Stanford, Caltech, Wisconsin-Madison, Nebraska-Lincoln, US Naval Air Warfare Center (China Lake), Tsukuba (Japan), La Sapienza (Rome), and advisory roles at ASELSAN and the Turkish Ministry of National Defence. State Prize laureate (USSR, Azerbaijan), Honored Scientist of Azerbaijan, Fellow of the Turkish Physical Society, and recipient of the Order of Friendship and diaspora service medal of Azerbaijan.</span>
      <span class="lang az block">Prof. Dr. Əmirulla M. Məmmədov (elmi nəşrlərdə Amirullah M. Mamedov) optika, qeyri-xətti və lazer fizikası, topoloji izolyatorlar, metamateriallar, fotonik və fononik kristallar, optik informasiya texnologiyaları və bio-tibbi modelləşdirmə üzrə görkəmli fizikdir. 24 iyul 1946-cı ildə Bakıda anadan olub. Fizika və riyaziyyat üzrə PhD (1973, A.F. İoffe İnstitutu), elmlər doktoru habilitasiyası (1982, Riqa) və &ldquo;Optika&rdquo; üzrə professor adı (1988, Moskva). 350-dən çox beynəlxalq SCI jurnalında məqalənin müəllifidir. 50-dən çox beynəlxalq konfransda dəvətli məruzəçi olmuşdur. Stanford, Kaltek, Viskonsin-Madison, Nebraska-Lincoln, ABŞ Hərbi Donanması China Lake mərkəzi, Tsukuba (Yaponiya), La Sapienza (Roma) və ASELSAN, Türkiyə Milli Müdafiə Nazirliyi ilə məsləhətçi fəaliyyəti. Elm üzrə Dövlət Mükafatı laureatı (SSRİ, Azərbaycan), Azərbaycanın Əməkdar elm xadimi, Türkiyə Fizika Cəmiyyətinin üzvü, Dostluq ordeni və diaspora fəaliyyətinə görə medal laureatı.</span>
    </div>
    <div class="stats">
      <div class="stat-item"><span class="stat-num">350+</span><span class="stat-label"><span class="lang en">Publications</span><span class="lang az">Nəşr</span></span></div>
      <div class="stat-item"><span class="stat-num">Dr. Sci.</span><span class="stat-label"><span class="lang en">1982</span><span class="lang az">1982</span></span></div>
      <div class="stat-item"><span class="stat-num">50+</span><span class="stat-label"><span class="lang en">Invited Talks</span><span class="lang az">Dəvətli məruzə</span></span></div>
      <div class="stat-item"><span class="stat-num">ABİD</span><span class="stat-label"><span class="lang en">President</span><span class="lang az">Sədr</span></span></div>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Core Competencies</span><span class="lang az">Əsas kompetensiyalar</span></h2>
    <div class="competency-grid">
      <div class="comp-group">
        <h3><span class="lang en">Research Fields</span><span class="lang az">Tədqiqat sahələri</span></h3>
        <ul>
          <li><span class="lang en">Nonlinear optics and laser physics</span><span class="lang az">Qeyri-xətti optika və lazer fizikası</span></li>
          <li><span class="lang en">Metamaterials, topological insulators, photonic and phononic crystals</span><span class="lang az">Metamateriallar, topoloji izolyatorlar, fotonik və fononik kristallar</span></li>
          <li><span class="lang en">Photonics, nanophotonics, and optical information technology</span><span class="lang az">Fotonika, nanofotonika və optik informasiya texnologiyaları</span></li>
          <li><span class="lang en">Bio-medical modeling and instrumentation; artificial neural networks</span><span class="lang az">Bio-tibbi modelləşdirmə və avadanlıqlar; süni sinir şəbəkəsi</span></li>
        </ul>
      </div>
      <div class="comp-group">
        <h3><span class="lang en">Methods &amp; Tools</span><span class="lang az">Metodlar və alətlər</span></h3>
        <ul>
          <li><span class="lang en">First-principles and ab initio calculations</span><span class="lang az">First-principles və ab initio hesablamalar</span></li>
          <li><span class="lang en">FDTD and finite element (FEM) analysis</span><span class="lang az">FDTD və sonlu element (FEM) analizi</span></li>
          <li><span class="lang en">Ferroelectric, multiferroic, and guidance-system modeling</span><span class="lang az">Ferroelektrik, multiferroik və yönləndirmə sistemlərinin modelləşdirilməsi</span></li>
        </ul>
      </div>
      <div class="comp-group">
        <h3><span class="lang en">Leadership &amp; Advisory Roles</span><span class="lang az">Rəhbərlik və məsləhətçilik</span></h3>
        <ul>
          <li><span class="lang en">President, Association of Azerbaijani Scientists in Turkey (ABID)</span><span class="lang az">Türkiyədə fəaliyyət göstərən Azərbaycanlı Alimlər Assosiasiyasının (ABİD) sədri</span></li>
          <li><span class="lang en">Head, Nonlinear Optics Division, Baku State University</span><span class="lang az">Bakı Dövlət Universitetində Qeyri-Xətti Optika Bölməsinin rəhbəri</span></li>
          <li><span class="lang en">Scientific advisor, ASELSAN (1992&#8211;2006); advisor, SATEM/T&Uuml;BİTAK (2004&#8211;2010)</span><span class="lang az">ASELSAN elmi məsləhətçisi (1992&#8211;2006); SATEM/T&Uuml;BİTAK məsləhətçisi (2004&#8211;2010)</span></li>
        </ul>
      </div>
      <div class="comp-group">
        <h3><span class="lang en">Languages</span><span class="lang az">Dillər</span></h3>
        <ul>
          <li><span class="lang en">English, Turkish, Russian, and Azerbaijani (fluent); Hebrew (good)</span><span class="lang az">İngilis, türk, rus və azərbaycan (səlis); ivrit (yaxşı səviyyədə)</span></li>
          <li><span class="lang en">Citizenship: Turkey and Azerbaijan</span><span class="lang az">Vətəndaşlıq: Türkiyə və Azərbaycan</span></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Professional Experience</span><span class="lang az">Peşəkar fəaliyyət</span></h2>
    <div class="timeline">
      <article class="item"><div class="period"><span class="lang en">2011 &#8211; Present</span><span class="lang az">2011 &#8211; indiyədək</span></div><div><h3><span class="lang en">Bilkent University, NANOTAM, Ankara</span><span class="lang az">Bilkent Universiteti, NANOTAM, Ankara</span></h3><span class="role"><span class="lang en">Emeritus Professor &amp; Leading Researcher</span><span class="lang az">Fəxri professor və aparıcı elmi işçi</span></span></div></article>
      <article class="item"><div class="period">2004 &#8211; 2010</div><div><h3><span class="lang en">SATEM Branch, Ministry of National Defence of Turkey</span><span class="lang az">SATEM, Türkiyə Milli Müdafiə Nazirliyi</span></h3><span class="role"><span class="lang en">Scientific Advisor</span><span class="lang az">Elmi məsləhətçi</span></span></div></article>
      <article class="item"><div class="period">1992 &#8211; 2006</div><div><h3><span class="lang en">ASELSAN, Turkey</span><span class="lang az">ASELSAN, Türkiyə</span></h3><span class="role"><span class="lang en">Scientific Advisor (Microelectronics, Guidance, Electrooptics)</span><span class="lang az">Elmi məsləhətçi (Mikroelektronika, Yönləndirmə, Elektrooptika)</span></span></div></article>
      <article class="item"><div class="period"><span class="lang en">Professor</span><span class="lang az">Professor</span></div><div><h3><span class="lang en">Cukurova University, Adana, Turkey</span><span class="lang az">Çukurova Universiteti, Adana, Türkiyə</span></h3><span class="role"><span class="lang en">Professor, Physics and Electrical &amp; Electronics Engineering</span><span class="lang az">Professor, Fizika və Elektrik-Elektronika Mühəndisliyi</span></span></div></article>
      <article class="item"><div class="period"><span class="lang en">Visiting</span><span class="lang az">Qonaq</span></div><div><h3><span class="lang en">University &ldquo;La Sapienza&rdquo;, Rome, Italy</span><span class="lang az">&ldquo;La Sapienza&rdquo; Universiteti, Roma, İtaliya</span></h3><span class="role"><span class="lang en">Visiting Professor</span><span class="lang az">Dəvətli professor</span></span></div></article>
      <article class="item"><div class="period"><span class="lang en">Visiting</span><span class="lang az">Qonaq</span></div><div><h3><span class="lang en">Tsukuba Scientific Center, Japan</span><span class="lang az">Tsukuba Elmi Mərkəzi, Yaponiya</span></h3><span class="role"><span class="lang en">Visiting Senior Researcher</span><span class="lang az">Dəvətli baş elmi işçi</span></span></div></article>
      <article class="item"><div class="period"><span class="lang en">Professor</span><span class="lang az">Professor</span></div><div><h3><span class="lang en">Baku State University, Azerbaijan</span><span class="lang az">Bakı Dövlət Universiteti, Azərbaycan</span></h3><span class="role"><span class="lang en">Head, Nonlinear Optics Division</span><span class="lang az">Qeyri-Xətti Optika Bölməsinin rəhbəri</span></span></div></article>
      <article class="item"><div class="period"><span class="lang en">Visiting</span><span class="lang az">Qonaq</span></div><div><h3><span class="lang en">Stanford, Caltech, Wisconsin-Madison, Nebraska-Lincoln; NAWC China Lake, USA</span><span class="lang az">Stanford, Kaltek, Viskonsin-Madison, Nebraska-Lincoln; NAWC China Lake, ABŞ</span></h3><span class="role"><span class="lang en">Visiting Senior Researcher</span><span class="lang az">Dəvətli baş elmi işçi</span></span></div></article>
      <article class="item"><div class="period">1968 &#8211; <span class="lang en">onward</span><span class="lang az">indiyədək</span></div><div><h3><span class="lang en">Vavilov State Optical Institute, St. Petersburg</span><span class="lang az">Vavilov Dövlət Optika İnstitutu, Sankt-Peterburq</span></h3><span class="role"><span class="lang en">Junior Researcher to Researcher</span><span class="lang az">Kiçik elmi işçidən elmi işçiyə qədər</span></span><p><span class="lang en">Also researcher, senior researcher, associate professor, and professor at Baku State University.</span><span class="lang az">Həmçinin BDUD-da elmi işçi, baş elmi işçi, dosent və professor.</span></p></div></article>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Education &amp; Academic Credentials</span><span class="lang az">Təhsil və akademik göstəricilər</span></h2>
    <div class="education-grid">
      <article class="edu-card"><div class="period">1988</div><h3><span class="lang en">Full Professor in Optics</span><span class="lang az">&ldquo;Optika&rdquo; üzrə professor</span></h3><p><span class="lang en">Supreme Attestation Committee of the USSR, Moscow, Russia.</span><span class="lang az">SSRİ Ali Attestasiya Komissiyası, Moskva, Rusiya.</span></p></article>
      <article class="edu-card"><div class="period">1982</div><h3><span class="lang en">Doctor of Sciences (Habilitation)</span><span class="lang az">Elmlər doktoru (habilitasiya)</span></h3><p><span class="lang en">Physics and Mathematics. Regional Council, Supreme Attestation Committee, Riga, Latvia.</span><span class="lang az">Fizika və riyaziyyat. Regional Şura, Ali Attestasiya Komissiyası, Riqa, Latviya.</span></p></article>
      <article class="edu-card"><div class="period">1977</div><h3><span class="lang en">Associate Professor (Dosent)</span><span class="lang az">Dosent dərəcəsi</span></h3><p><span class="lang en">Solid State Physics, USSR.</span><span class="lang az">Bərk cisim fizikası, SSRİ.</span></p></article>
      <article class="edu-card"><div class="period">1973</div><h3><span class="lang en">Ph.D. in Physics and Mathematics</span><span class="lang az">Fizika və riyaziyyat üzrə PhD</span></h3><p><span class="lang en">A.F. Ioffe Physical-Technical Institute, USSR Academy of Sciences, St. Petersburg. Thesis: <em>Optical and Electrooptical Properties of Photoferroelectric Materials</em> (performed at Vavilov State Optical Institute).</span><span class="lang az">A.F. İoffe Fiziki-Texniki İnstitutu, SSRİ EA, Sankt-Peterburq. Dissertasiya: <em>Fotoferroelektrik materialların optik və elektrooptik xüsusiyyətləri</em> (Vavilov Dövlət Optika İnstitutunda yerinə yetirilib).</span></p></article>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Honors, Awards &amp; Social Activity</span><span class="lang az">Fəxri adlar, mükafatlar və ictimai fəaliyyət</span></h2>
    <div class="callout">
      <span class="lang en block">State Prizes (USSR, Azerbaijan) &middot; Fellow of the Turkish Physical Society &middot; Honored Scientist of Azerbaijan &middot; Member of the Trustees Board, Turkey-Azerbaijan Foundation of Friendship, Cooperation and Solidarity &middot; Order of Friendship of the Republic of Azerbaijan &middot; Medal for service in diaspora activity &middot; Jubilee medal of the 100th Anniversary of Baku State University (1919&#8211;2019) &middot; President of ABID (Association of Azerbaijani Scientists Working in Turkey).</span>
      <span class="lang az block">Elm üzrə Dövlət Mükafatı (SSRİ, Azərbaycan) &middot; Türkiyə Fizika Cəmiyyətinin üzvü &middot; Azərbaycan Respublikasının Əməkdar elm xadimi &middot; Türkiyə-Azərbaycan Dostluq, Əməkdaşlıq və Həmrəylik Fondu Qəyyumlar Şurasının üzvü &middot; Azərbaycan Respublikasının Dostluq ordeni &middot; Diaspora fəaliyyətində xidmətə görə medal &middot; Bakı Dövlət Universitetinin 100 illiyi yubiley medalı (1919&#8211;2019) &middot; ABİD sədri.</span>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Selected Publications</span><span class="lang az">Seçilmiş nəşrlər</span></h2>
    <div class="pub-block">
      <div class="pub-category">
        <h3><span class="lang en">Recent Publications (2024&#8211;2025)</span><span class="lang az">Son nəşrlər (2024&#8211;2025)</span></h3>
        <ol>
          <li>Topological semimetals in the ZrB5 (B = Se, Te) material class: Weyl points and electronic properties, <em>Ferroelectrics</em>, 2024, 618(4).</li>
          <li>Observation of elastic Weyl points in ferroelectric-based sonic metamaterials, <em>Ferroelectrics</em>, 2024, 618(4).</li>
          <li>The structural, elastic, electronic, and optical properties of Li2RuO3 compound in different structures, <em>Chinese Journal of Physics</em>, 2024, 90, 1026.</li>
          <li>The structural, elastic, electronic, and optical properties of the rhombohedral La2NiMnO6 double perovskite compound at different temperatures, <em>Computational Condensed Matter</em>, 2024, 41, e00984.</li>
          <li>The structural, mechanical, electronic, and optical properties of multiferroic LiCu2O2 under different pressures, <em>Bulletin of Materials Science</em>, 2025, 48:6.</li>
        </ol>
      </div>
      <div class="pub-category">
        <h3><span class="lang en">Representative Earlier Work (Selection)</span><span class="lang az">Əvvəlki işlər (seçmə)</span></h3>
        <ul>
          <li>Topological Insulator Based Locally Resonant Phononic Crystals, <em>Ferroelectrics</em>, 2016, 499(1), 123&#8211;129.</li>
          <li>Phononic band gap and wave propagation on polyvinylidene fluoride-based acoustic metamaterials, <em>Cogent Physics</em>, 2016, 2, 1169570.</li>
          <li>Electron Energy Loss Spectroscopy and the Electronic Band Structure of KNbO3 Ferroelectric, <em>Ferroelectrics</em>, 2014, 461(1), 1.</li>
          <li>Modeling and Simulation of the Ferroelectric Based Micro-Gyroscope: FEM Analysis, <em>Ferroelectrics</em>, 2013, 447(1), 46.</li>
        </ul>
      </div>
      <div class="callout" style="margin: 0 22px 18px;">
        <span class="lang en block">More than 350 publications in international journals including <em>JETP</em>, <em>Phys. Solid State</em>, <em>J. Phys.</em>, <em>Appl. Phys.</em>, <em>Physica</em>, <em>Phil. Mag.</em>, <em>Ferroelectrics</em>, <em>Integrated Ferroelectrics</em>, <em>J. Modern Optics</em>, <em>JOAM</em>, and others.</span>
        <span class="lang az block">350-dən çox beynəlxalq jurnal məqaləsi, o cümlədən <em>JETP</em>, <em>Phys. Solid State</em>, <em>J. Phys.</em>, <em>Appl. Phys.</em>, <em>Physica</em>, <em>Phil. Mag.</em>, <em>Ferroelectrics</em>, <em>Integrated Ferroelectrics</em>, <em>J. Modern Optics</em>, <em>JOAM</em> və s.</span>
      </div>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Selected Conferences</span><span class="lang az">Seçilmiş konfranslar</span></h2>
    <div class="callout">
      <span class="lang en block">Invited presentations at more than 50 international conferences. Recent examples: EMF-2015 (Porto); RCBJSF-2016 (Shimane); META-2016 (Malaga); IMF 2017 (San Antonio); EMF-2019 (Lausanne); META-2019 (Lisbon); TPS-36 (Istanbul, 2020); FM&amp;NT 2020 (Vilnius); IC-CMTP 6 (2021, Hungary); MTP-7 (2021, Baku); IMF 2023 (Tel-Aviv); MTP-8 (2023, Baku); Functional Materials Symposium (2024, Mersin); ICETEA (2024, Baku).</span>
      <span class="lang az block">50-dən çox beynəlxalq konfransda dəvətli məruzəçi. Son tədbirlər: EMF-2015 (Porto); RCBJSF-2016 (Shimane); META-2016 (Malaqa); IMF 2017 (San-Antonio); EMF-2019 (Lausanne); META-2019 (Lissabon); TPS-36 (İstanbul, 2020); FM&amp;NT 2020 (Vilnius); IC-CMTP 6 (2021, Macarıstan); MTP-7 (2021, Bakı); IMF 2023 (Tel-Aviv); MTP-8 (2023, Bakı); Functional Materials Symposium (2024, Mersin); ICETEA (2024, Bakı).</span>
    </div>
  </section>

  <footer>
    <span class="lang en">Emirullah M. Mehmetov, Prof. Dr. &ensp;·&ensp; Curriculum Vitae &ensp;·&ensp; Ankara, Turkey</span>
    <span class="lang az">Əmirulla M. Məmmədov, Prof. Dr. &ensp;·&ensp; Tərcümeyi-hal &ensp;·&ensp; Ankara, Türkiyə</span>
  </footer>

</main>

<script>
  function setLang(lang) {
    document.documentElement.lang = lang;
    document.querySelectorAll('.lang').forEach(function(el) {
      el.classList.remove('active');
    });
    document.querySelectorAll('.lang.' + lang).forEach(function(el) {
      el.classList.add('active');
    });
    document.getElementById('btn-en').classList.toggle('active', lang === 'en');
    document.getElementById('btn-az').classList.toggle('active', lang === 'az');
  }
  setLang('en');
</script>
</body>
</html>"""

OUT.write_text(HTML, encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
