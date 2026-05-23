from pathlib import Path

OUT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site\cv\elvin_afandi.html")

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Curriculum Vitae — Elvin Afandi</title>
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
    h1 { font-size: clamp(32px, 5vw, 56px); font-weight: 700; line-height: 1.05; letter-spacing: -0.01em; color: var(--white); margin-bottom: 14px; }
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
          <span class="lang en">Elvin N. Afandi, Ph.D.</span>
          <span class="lang az">Elvin N. Əfəndi, Ph.D.</span>
        </h1>
        <p class="subtitle">
          <span class="lang en">Development economist specializing in private sector strategy, economic policy, and applied microeconometrics. Division Head, Corporate Strategy &amp; Research at the Islamic Corporation for the Development of the Private Sector (ICD), Islamic Development Bank Group, Jeddah, Saudi Arabia.</span>
          <span class="lang az">Özəl sektor strategiyası, iqtisadi siyasət və tətbiqi mikroekonometriya üzrə ixtisaslaşmış inkişaf iqtisadçısı. İslam İnkişaf Bankı Qrupunun İslam Özəl Sektorun İnkişafı Korporasiyasında (ICD) Korporativ strategiya və tədqiqatlar şöbəsinin rəhbəri, Ciddə, Səudiyyə Ərəbistanı.</span>
        </p>
      </div>
      <figure class="hero-photo">
        <img src="../images/scientists-photos/elvin-efendi.png" alt="Elvin Afandi" width="160" height="200" loading="eager" />
      </figure>
    </div>
    <dl class="rank-bar">
      <div class="rank-item">
        <dt><span class="lang en">Academic Rank</span><span class="lang az">Akademik rütbə</span></dt>
        <dd><span class="lang en">Ph.D. in Economics</span><span class="lang az">İqtisadiyyat üzrə PhD</span></dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">Institution</span><span class="lang az">Qurum</span></dt>
        <dd><span class="lang en">ICD, Islamic Development Bank Group</span><span class="lang az">ICD, İslam İnkişaf Bankı Qrupu</span></dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">E-mail</span><span class="lang az">E-poçt</span></dt>
        <dd>e.afandi@yahoo.com</dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">Location</span><span class="lang az">Yer</span></dt>
        <dd><span class="lang en">Jeddah, Saudi Arabia</span><span class="lang az">Ciddə, Səudiyyə Ərəbistanı</span></dd>
      </div>
    </dl>
  </header>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Academic Profile</span><span class="lang az">Akademik profil</span></h2>
    <div class="callout">
      <span class="lang en block">Dr. Elvin N. Afandi is an economist with extensive international experience in development economics, economic policy, and private sector strategy. Since January 2022 he has served as Division Head, Corporate Strategy &amp; Research at the Islamic Corporation for the Development of the Private Sector (ICD), overseeing corporate and country strategy, economic research, flagship publications, and private sector development strategies across IDB member countries. Author of more than 20 peer-reviewed journal articles and 25+ research papers and policy reports. He developed the Private Sector Development Index of 57 OIC member countries, published in the <em>Journal of Economic Cooperation and Development</em> (2019). He has taught more than 300 graduate and undergraduate students in development economics, econometrics, and macroeconomics at Dar Al Hekma University, Khazar University, and Azerbaijan State University of Economics. Humphrey Fellow (2009&#8211;2010, U.S. State Department). Member of editorial boards of several international journals.</span>
      <span class="lang az block">Elvin N. Əfəndi inkişaf iqtisadiyyatı, iqtisadi siyasət və özəl sektor strategiyası sahəsində geniş beynəlxalq təcrübəyə malik iqtisadçıdır. 2022-ci ilin yanvarından İslam Özəl Sektorun İnkişafı Korporasiyasında (ICD) Korporativ strategiya və tədqiqatlar şöbəsinin rəhbəri kimi korporativ və ölkə strategiyalarına, iqtisadi tədqiqatlara, aparıcı hesabatlara və İİBK üzv ölkələrində özəl sektorun inkişaf strategiyalarına rəhbərlik edir. 20-dən artıq rəyli jurnal məqaləsi və 25-dən çox tədqiqat sənədinin müəllifidir. 57 İHK üzv ölkəsi üzrə Özəl Sektorun İnkişaf İndeksini hazırlamışdır (<em>Journal of Economic Cooperation and Development</em>, 2019). Dar Al Hekma Universiteti, Xəzər Universiteti və UNEC-də 300-dən artıq magistr və bakalavr tələbəsinə inkişaf iqtisadiyyatı, ekonometriya və makroiqtisadiyyat dərs demişdir. ABŞ Dövlət Departamentinin H. Humphrey təqaüdçüsü (2009&#8211;2010). Bir sıra beynəlxalq jurnalların redaksiya heyətinin üzvüdür.</span>
    </div>
    <div class="stats">
      <div class="stat-item"><span class="stat-num">20+</span><span class="stat-label"><span class="lang en">Peer-reviewed Articles</span><span class="lang az">Rəyli məqalə</span></span></div>
      <div class="stat-item"><span class="stat-num">25+</span><span class="stat-label"><span class="lang en">Research Papers</span><span class="lang az">Tədqiqat sənədi</span></span></div>
      <div class="stat-item"><span class="stat-num">300+</span><span class="stat-label"><span class="lang en">Students Taught</span><span class="lang az">Tələbə</span></span></div>
      <div class="stat-item"><span class="stat-num">2019</span><span class="stat-label"><span class="lang en">PSD Index (OIC)</span><span class="lang az">ÖSİ (İHK)</span></span></div>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Core Competencies</span><span class="lang az">Əsas kompetensiyalar</span></h2>
    <div class="competency-grid">
      <div class="comp-group">
        <h3><span class="lang en">Research Fields</span><span class="lang az">Tədqiqat sahələri</span></h3>
        <ul>
          <li><span class="lang en">Development economics and pro-poor growth</span><span class="lang az">İnkişaf iqtisadiyyatı və yoxsulluğa yönəlmiş artım</span></li>
          <li><span class="lang en">Private sector development and entrepreneurship</span><span class="lang az">Özəl sektorun inkişafı və sahibkarlıq</span></li>
          <li><span class="lang en">Social capital, trust, and household coping strategies</span><span class="lang az">Sosial kapital, etimad və ailə strategiyaları</span></li>
          <li><span class="lang en">Firm innovation, financing constraints, and institutional trust</span><span class="lang az">Müəssisə innovasiyası, maliyyələşdirmə maneələri və institusional etimad</span></li>
          <li><span class="lang en">Subjective well-being and health in transitional economies</span><span class="lang az">Keçid iqtisadiyyatlarında subyektiv rifah və sağlamlıq</span></li>
        </ul>
      </div>
      <div class="comp-group">
        <h3><span class="lang en">Policy &amp; Strategy</span><span class="lang az">Siyasət və strategiya</span></h3>
        <ul>
          <li><span class="lang en">Corporate and country strategy formulation for ICD</span><span class="lang az">ICD üçün korporativ və ölkə strategiyalarının hazırlanması</span></li>
          <li><span class="lang en">Member Country Partnership Strategies (MCPS) and PSD diagnostics</span><span class="lang az">Üzv ölkə tərəfdaşlıq strategiyaları (MCPS) və ÖSİ diaqnostikası</span></li>
          <li><span class="lang en">Flagship reports: Annual Report, Private Sector Factbook, Market Attractiveness Index</span><span class="lang az">Aparıcı hesabatlar: İllik hesabat, Özəl Sektor Factbook, Bazar Cəlbediciliyi İndeksi</span></li>
          <li><span class="lang en">OIC infrastructure and investment outlook reports (2022&#8211;2023)</span><span class="lang az">İHK infrastruktur və investisiya proqnozu hesabatları (2022&#8211;2023)</span></li>
        </ul>
      </div>
      <div class="comp-group">
        <h3><span class="lang en">Teaching &amp; Training</span><span class="lang az">Tədris və təlim</span></h3>
        <ul>
          <li><span class="lang en">Econometrics, development economics, and international development</span><span class="lang az">Ekonometriya, inkişaf iqtisadiyyatı və beynəlxalq inkişaf</span></li>
          <li><span class="lang en">Dar Al Hekma University (2014&#8211;2015), UNEC (2010&#8211;2011), Khazar University (2006&#8211;2009)</span><span class="lang az">Dar Al Hekma Universiteti (2014&#8211;2015), UNEC (2010&#8211;2011), Xəzər Universiteti (2006&#8211;2009)</span></li>
          <li><span class="lang en">Executive Program on Corporate Strategy, Chicago Booth (2024)</span><span class="lang az">Korporativ strategiya üzrə icra proqramı, Chicago Booth (2024)</span></li>
          <li><span class="lang en">MIT J-PAL randomized controlled trials course (2013); IMF macroeconomic diagnostics (2008)</span><span class="lang az">MIT J-PAL randomizasiya olunmuş sınaqlar kursu (2013); IMF makroiqtisadi diaqnostika (2008)</span></li>
        </ul>
      </div>
      <div class="comp-group">
        <h3><span class="lang en">Technical &amp; Languages</span><span class="lang az">Texniki bacarıqlar və dillər</span></h3>
        <ul>
          <li><span class="lang en">Statistical software: Stata, SPSS, E-Views</span><span class="lang az">Statistik proqramlar: Stata, SPSS, E-Views</span></li>
          <li><span class="lang en">Panel and non-linear econometric models; policy evaluation methods</span><span class="lang az">Panel və qeyri-xətti ekonometrik modellər; siyasət qiymətləndirmə metodları</span></li>
          <li><span class="lang en">Azerbaijani (native), English (fluent), Russian and Turkish (good), Arabic (beginner)</span><span class="lang az">Azərbaycan dili (ana dili), ingilis dili (sərbəst), rus və türk dilləri (yaxşı), ərəb dili (başlanğıc)</span></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Professional Experience</span><span class="lang az">Peşəkar fəaliyyət</span></h2>
    <div class="timeline">
      <article class="item"><div class="period"><span class="lang en">Jan 2022 &#8211; Present</span><span class="lang az">Yan 2022 &#8211; indiyədək</span></div><div><h3><span class="lang en">Islamic Corporation for the Development of the Private Sector (ICD)</span><span class="lang az">İslam Özəl Sektorun İnkişafı Korporasiyası (ICD)</span></h3><span class="role"><span class="lang en">Division Head, Corporate Strategy &amp; Research</span><span class="lang az">Korporativ strategiya və tədqiqatlar şöbəsinin rəhbəri</span></span><p><span class="lang en">Strategy Department, Islamic Development Bank Group, Jeddah. Oversees corporate and country strategy, economic research, flagship reports, and PSD strategies in member countries.</span><span class="lang az">İslam İnkişaf Bankı Qrupu, Strateji departament, Ciddə. Korporativ və ölkə strategiyalarına, iqtisadi tədqiqatlara, aparıcı hesabatlara və üzv ölkələrdə ÖSİ strategiyalarına rəhbərlik edir.</span></p></div></article>
      <article class="item"><div class="period">Aug 2020 &#8211; Jan 2022</div><div><h3><span class="lang en">ICD, Strategy and Policy Department</span><span class="lang az">ICD, Strategiya və siyasət departamenti</span></h3><span class="role"><span class="lang en">Division Head, Economic Policy &amp; Research</span><span class="lang az">İqtisadi siyasət və tədqiqatlar şöbəsinin rəhbəri</span></span></div></article>
      <article class="item"><div class="period">Jul 2014 &#8211; Aug 2020</div><div><h3><span class="lang en">ICD, Strategy and Policy Department</span><span class="lang az">ICD, Strategiya və siyasət departamenti</span></h3><span class="role"><span class="lang en">Principal Economist</span><span class="lang az">Baş iqtisadçı</span></span><p><span class="lang en">Led flagship reports and private sector development strategies within MCPS frameworks.</span><span class="lang az">MCPS çərçivəsində aparıcı hesabatların və özəl sektor inkişaf strategiyalarının hazırlanmasına rəhbərlik etmişdir.</span></p></div></article>
      <article class="item"><div class="period">Jul 2011 &#8211; Jul 2014</div><div><h3><span class="lang en">ICD, Strategy and Policy Department</span><span class="lang az">ICD, Strategiya və siyasət departamenti</span></h3><span class="role"><span class="lang en">Senior Economist</span><span class="lang az">Baş iqtisadçı</span></span></div></article>
      <article class="item"><div class="period">Jul 2010 &#8211; Jul 2011</div><div><h3><span class="lang en">Central Bank of Azerbaijan</span><span class="lang az">Azərbaycan Mərkəzi Bankı</span></h3><span class="role"><span class="lang en">Senior Economist, Research Department</span><span class="lang az">Baş iqtisadçı, Tədqiqat departamenti</span></span></div></article>
      <article class="item"><div class="period">May &#8211; Jul 2010</div><div><h3><span class="lang en">The World Bank, Europe and Central Asia Region</span><span class="lang az">Dünya Bankı, Avropa və Mərkəzi Asiya regionu</span></h3><span class="role"><span class="lang en">Consultant</span><span class="lang az">Məsləhətçi</span></span><p><span class="lang en">Institutional challenges of oil-exporting former Soviet Union countries.</span><span class="lang az">Neft ixrac edən sovet sonrası ölkələrin institusional çətinlikləri layihəsi.</span></p></div></article>
      <article class="item"><div class="period">Sep 2008 &#8211; Aug 2009</div><div><h3><span class="lang en">Central Bank of Azerbaijan</span><span class="lang az">Azərbaycan Mərkəzi Bankı</span></h3><span class="role"><span class="lang en">Senior Economist, Research Department</span><span class="lang az">Baş iqtisadçı, Tədqiqat departamenti</span></span></div></article>
      <article class="item"><div class="period">Jan 2006 &#8211; Sep 2008</div><div><h3><span class="lang en">SOAS, University of London (Asian Development Bank project)</span><span class="lang az">SOAS, London Universiteti (ADB layihəsi)</span></h3><span class="role"><span class="lang en">Principal Coordinator</span><span class="lang az">Baş koordinator</span></span><p><span class="lang en">Capacity building for macroeconomic growth modelling at the Ministry of Economy.</span><span class="lang az">İqtisadiyyat Nazirliyində makroiqtisadi artım modelinin yaradılması üçün institusional gücləndirmə.</span></p></div></article>
      <article class="item"><div class="period">Jan 2004 &#8211; Dec 2005</div><div><h3><span class="lang en">Center for Economic Reforms, Ministry of Economic Development of Azerbaijan</span><span class="lang az">İqtisadi İslahatlar Mərkəzi, Azərbaycan İqtisadi İnkişaf Nazirliyi</span></h3><span class="role"><span class="lang en">Economic Analyst</span><span class="lang az">İqtisadi analitik</span></span></div></article>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Board Memberships</span><span class="lang az">İdarə heyəti üzvlükləri</span></h2>
    <div class="callout">
      <span class="lang en block"><strong>2019 &#8211; present:</strong> Chairman of the Investment Committee, Euro-Mediterranean Investment Company (EMIC).<br /><strong>2019 &#8211; present:</strong> Chairman of Advisory Board, Islamic Bank Growth Fund (IBGF).</span>
      <span class="lang az block"><strong>2019 &#8211; indiyədək:</strong> Avro-Mediterranean İnvestisiya Şirkətinin (EMIC) İnvestisiya Komitəsinin sədri.<br /><strong>2019 &#8211; indiyədək:</strong> İslam Bank Growth Fund (IBGF) Məsləhət Heyətinin sədri.</span>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Education &amp; Academic Credentials</span><span class="lang az">Təhsil və akademik göstəricilər</span></h2>
    <div class="education-grid">
      <article class="edu-card"><div class="period">2009 &#8211; 2010</div><h3><span class="lang en">Post-Graduate Studies</span><span class="lang az">Aspirantura (post-qraduat)</span></h3><p><span class="lang en">Michigan State University, USA &#8212; Development Economics (Humphrey Fellowship).</span><span class="lang az">Miçiqan Dövlət Universiteti, ABŞ &#8212; İnkişaf iqtisadiyyatı (Humphrey təqaüdü).</span></p></article>
      <article class="edu-card"><div class="period">2006 &#8211; 2008</div><h3><span class="lang en">Ph.D. in Economics</span><span class="lang az">İqtisadiyyat üzrə PhD</span></h3><p><span class="lang en">Baku State University, Azerbaijan. Thesis: <em>Essays on Pro-poor Growth</em>.</span><span class="lang az">Bakı Dövlət Universiteti, Azərbaycan. Dissertasiya: <em>Yoxsulluğa yönəlmiş artım üzrə esselər</em>.</span></p></article>
      <article class="edu-card"><div class="period">2003 &#8211; 2005</div><h3><span class="lang en">M.Sc. in Economics</span><span class="lang az">İqtisadiyyat üzrə magistr</span></h3><p><span class="lang en">Azerbaijan State University of Economics (UNEC).</span><span class="lang az">Azərbaycan Dövlət İqtisad Universiteti (UNEC).</span></p></article>
      <article class="edu-card"><div class="period">1999 &#8211; 2003</div><h3><span class="lang en">B.Sc. in Economics</span><span class="lang az">İqtisadiyyat üzrə bakalavr</span></h3><p><span class="lang en">Azerbaijan State University of Economics (UNEC). Honor diploma.</span><span class="lang az">Azərbaycan Dövlət İqtisad Universiteti (UNEC). Fərqlənmə diplomu.</span></p></article>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Awards &amp; Honors</span><span class="lang az">Mükafatlar və fəxri adlar</span></h2>
    <div class="callout">
      <span class="lang en block">Best Paper Award, Conference of World Business Institute (2013) &middot; H. Humphrey Fellowship, U.S. State Department (2009&#8211;2010) &middot; Research and Development Grant, Economics Education and Research Consortium of Russia (2006) &middot; Best Student 2001&#8211;2002, Azerbaijan State University of Economics &middot; Honor diplomas for bachelor and master degrees.</span>
      <span class="lang az block">World Business Institute konfransında Ən yaxşı məqalə mükafatı (2013) &middot; ABŞ Dövlət Departamentinin H. Humphrey təqaüdü (2009&#8211;2010) &middot; Rusiya İqtisadiyyat Təhsili və Tədqiqat Konsorsiumunun T&amp;D qrantı (2006) &middot; UNEC-də 2001&#8211;2002-ci illərin ən yaxşı tələbəsi &middot; Bakalavr və magistr dərəcələri üzrə fərqlənmə diplomları.</span>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Selected Publications</span><span class="lang az">Seçilmiş nəşrlər</span></h2>
    <div class="pub-block">
      <div class="pub-category">
        <h3><span class="lang en">Peer-reviewed Journal Articles (Selection)</span><span class="lang az">Rəyli jurnal məqalələri (seçmə)</span></h3>
        <ul>
          <li>Introducing Private Sector Development Index of 57 OIC Member Countries, <em>Journal of Economic Cooperation and Development</em>, 2019, 40(3), 141&#8211;157.</li>
          <li>Sand or grease? Corruption-institutional trust nexus in post-Soviet countries, <em>Journal of Eurasian Studies</em>, 2017.</li>
          <li>What is the effect of university education on chances to be self-employed?, <em>International Entrepreneurship and Management Journal</em>, 2017, 13(2), 487&#8211;500.</li>
          <li>Pre-and-post Crisis Trust in Banks: Lessons from Developing Countries, <em>Journal of Economic Development</em>, 2017, 42(1), 73&#8211;94.</li>
          <li>Community Social Capital and Household Strategies for Coping with Global Crisis in Transitional Countries, <em>Social Indicators Research</em>, 2017, 130(2), 687&#8211;710.</li>
          <li>Social Trust and Use of Banking Services across Households in 28 Countries, <em>International Journal of Social Economics</em>, 2016, 43(4), 431&#8211;443.</li>
          <li>Bridging the Gender Gap in Entrepreneurship: An Empirical Analysis, <em>Journal of Developmental Entrepreneurship</em>, 2015, 20(2).</li>
          <li>What Prevents Firms from Access to Finance? A Case Study of OIC countries, <em>Journal of Economic Cooperation and Development</em>, 2014, 35(1), 103&#8211;132.</li>
          <li>Self-rated Health and Social Capital in Transitional Countries, <em>Social Science &amp; Medicine</em>, 2011, 72(7), 1193&#8211;1204.</li>
          <li>Evidence of Pro-Poor Growth in the Republic of Azerbaijan, <em>Problems of Economic Transition</em>, 2007, 50(6), 5&#8211;31.</li>
        </ul>
      </div>
      <div class="pub-category">
        <h3><span class="lang en">Policy Reports &amp; Working Papers (Selection)</span><span class="lang az">Siyasət hesabatları və working paper-lar (seçmə)</span></h3>
        <ul>
          <li>OIC Infrastructure Outlook 2023 &#8212; joint report with Refinitiv, 2023.</li>
          <li>Investment Outlook in OIC Countries 2022 &#8212; joint report with SESRIC, 2023.</li>
          <li>Private Sector Diagnostics of Member Countries: Binding Constraints &#8212; ICD Working Paper, 2017.</li>
          <li>Market Attractiveness Ranking of IDB Member Countries &#8212; ICD Working Paper, 2013&#8211;2017.</li>
          <li>Role of Private Sector Development in Climate Change &#8212; IDB Group policy study, 2015.</li>
          <li>SMEs Diagnostics Study Series (Kazakhstan, Tajikistan, Turkey, Niger, and others) &#8212; ICD Research Brief, 2012&#8211;2014.</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Selected Projects</span><span class="lang az">Seçilmiş layihələr</span></h2>
    <div class="callout">
      <span class="lang en block">University of Delaware &amp; Michigan State University (2010): Determinants of worker performance in transition economies &#8212; Research Coordinator. UN Human Rights Committee (2008): Migration policy in Azerbaijan &#8212; Principal Author. UN &amp; European Commission (2007): Central Asia integration through technical cooperation &#8212; Principal Researcher. CRRC (2007): Survey Sampling Design &#8212; Team Leader. USAID (2006): Public Investment Policy and Efficiency &#8212; Trainer &amp; Researcher. UNDP (2005): Effect of economic growth on poverty &#8212; Principal Author.</span>
      <span class="lang az block">Delaware və Miçiqan Dövlət universitetləri (2010): Keçid iqtisadiyyatlarında işçi məhsuldarlığının determinantları &#8212; Tədqiqat koordinatoru. BMT İnsan Hüquqları Komitəsi (2008): Azərbaycanda miqrasiya siyasəti &#8212; Baş müəllif. BMT və Avropa Komissiyası (2007): Mərkəzi Asiyanın texniki əməkdaşlıq vasitəsilə inteqrasiyası &#8212; Baş tədqiqatçı. CRRC (2007): Sorğu nümunə dizaynı &#8212; Komanda rəhbəri. USAID (2006): İctimai investisiya siyasəti və səmərəlilik &#8212; Təlimçi və tədqiqatçı. UNDP (2005): İqtisadi artımın yoxsulluğa təsiri &#8212; Baş müəllif.</span>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Conferences &amp; Editorial Service</span><span class="lang az">Konfranslar və redaktorluq</span></h2>
    <div class="callout">
      <span class="lang en block"><strong>Conferences (selection):</strong> Astana Economic Forum (2019); Oxford Economic Forum (2017); EBES Conference, Istanbul (2014); IBSSRC, Dubai (2013); EERC Workshop, Moscow (2006).<br /><strong>Editorial boards:</strong> <em>International Entrepreneurship and Management Journal</em>, <em>Journal of Global Entrepreneurship</em>, <em>International Journal of Social Economics</em>, <em>Social Indicators Research</em>, <em>International Review of Business Research Papers</em>, <em>Tax Journal of Azerbaijan</em>, <em>Asian Economic and Financial Review</em>.</span>
      <span class="lang az block"><strong>Konfranslar (seçmə):</strong> Astana İqtisadi Forumu (2019); Oksford İqtisadi Forumu (2017); EBES konfransı, İstanbul (2014); IBSSRC, Dubay (2013); EERC seminarı, Moskva (2006).<br /><strong>Redaksiya heyətləri:</strong> <em>International Entrepreneurship and Management Journal</em>, <em>Journal of Global Entrepreneurship</em>, <em>International Journal of Social Economics</em>, <em>Social Indicators Research</em>, <em>International Review of Business Research Papers</em>, <em>Tax Journal of Azerbaijan</em>, <em>Asian Economic and Financial Review</em>.</span>
    </div>
  </section>

  <footer>
    <span class="lang en">Elvin N. Afandi, Ph.D. &ensp;·&ensp; Curriculum Vitae &ensp;·&ensp; Jeddah, Saudi Arabia</span>
    <span class="lang az">Elvin N. Əfəndi, Ph.D. &ensp;·&ensp; Tərcümeyi-hal &ensp;·&ensp; Ciddə, Səudiyyə Ərəbistanı</span>
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
