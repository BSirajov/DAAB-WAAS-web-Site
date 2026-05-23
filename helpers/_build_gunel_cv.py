from pathlib import Path

OUT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site\cv\gunel_seferova.html")

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Curriculum Vitae — Gunel Safarova</title>
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
    .pub-category ul { padding-left: 20px; font-size: 14px; color: var(--body-text); line-height: 1.7; }
    .pub-category li { margin-bottom: 8px; }
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
          <span class="lang en">Gunel Safarova, Ph.D.</span>
          <span class="lang az">Günel Səfərova, Ph.D.</span>
        </h1>
        <p class="subtitle">
          <span class="lang en">Management scholar and change-management consultant specializing in innovation, organizational ambidexterity, and international cooperation. Change management consultant at Onepoint; lecturer at Université Paris-Saclay and ADA University Business School. Founder and president of the ALIM scientific association.</span>
          <span class="lang az">İnnovasiya, təşkilati ambidextriya və beynəlxalq əməkdaşlıq üzrə ixtisaslaşmış idarəetmə alimi və dəyişiklik idarəetməsi konsultantı. Onepoint-da change management konsultantı; Paris-Sakle Universitetində və ADA Universitetinin Biznes Məktəbində müəllim. ALİM elmi assosiasiyasının təsisçisi və sədri.</span>
        </p>
      </div>
      <figure class="hero-photo">
        <img src="../images/scientists-photos/gunel-seferova.png" alt="Gunel Safarova" width="160" height="200" loading="eager" />
      </figure>
    </div>
    <dl class="rank-bar">
      <div class="rank-item">
        <dt><span class="lang en">Academic Rank</span><span class="lang az">Akademik rütbə</span></dt>
        <dd><span class="lang en">Ph.D. in Management Sciences</span><span class="lang az">İdarəetmə elmləri üzrə PhD</span></dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">Affiliation</span><span class="lang az">Əlaqə</span></dt>
        <dd><span class="lang en">Onepoint; Université Paris-Saclay; ADA University</span><span class="lang az">Onepoint; Paris-Sakle Universiteti; ADA Universiteti</span></dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">E-mail</span><span class="lang az">E-poçt</span></dt>
        <dd>gunelsafarova@hotmail.com</dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">Location</span><span class="lang az">Yer</span></dt>
        <dd><span class="lang en">Lyon, France</span><span class="lang az">Lion, Fransa</span></dd>
      </div>
    </dl>
  </header>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Academic Profile</span><span class="lang az">Akademik profil</span></h2>
    <div class="callout">
      <span class="lang en block">Dr. Gunel Safarova holds a Ph.D. in Management Sciences (2019, Université Paris-Saclay / UVSQ) on innovation management and ambidexterity in U.S. family firms, supervised by Prof. Annie Bartoli. She led scientific research and education projects between the University of Versailles Saint-Quentin-en-Yvelines and Georgetown University for seven years. Currently a change-management consultant at Onepoint and an independent consultant on France&#8211;Azerbaijan cooperation projects (budget up to 3&nbsp;M&nbsp;&euro;). Lecturer at ADA University Business School and Université Paris-Saclay (project management, change management, HR, marketing, and strategy). Associate researcher at LAREQUOI laboratory. Founder and president of ALIM (Association Scientifique). Supervises approximately 10&#8211;15 MBA and master theses annually. First Azerbaijani representative of the Young Ambassadors Association of France (since 2019). Coordinator for Central Asian countries at the French Institute of Academic Studies (since 2020). Medal of the Republic of Azerbaijan for diaspora activity (2020).</span>
      <span class="lang az block">Günel Səfərova idarəetmə elmləri üzrə PhD dərəcəsinə malikdir (2019, Paris-Sakle Universiteti / UVSQ); dissertasiya mövzusu ABŞ ailə müəssisələrində innovasiya idarəetməsi və ambidextriya, elmi rəhbər Prof. Annie Bartoli. Yeddi il ərzində Versal &#8211; Saint-Quentin-en-Yvelines Universiteti ilə Corctaun Universiteti arasında elmi-tədqiqat və təhsil layihələrinə rəhbərlik etmişdir. Hazırda Onepoint-da change management konsultantı və Fransa&#8211;Azərbaycan əməkdaşlığı layihələrində müstəqil məsləhətçidir (3&nbsp;mln&nbsp;&euro;-dək büdcə). ADA Universitetinin Biznes Məktəbində və Paris-Sakle Universitetində müəllimdir (layihə idarəetməsi, dəyişiklik idarəetməsi, HR, marketinq, strategiya). LAREQUOI laboratoriyasının associate researcher üzvüdür. ALİM (Association Scientifique) assosiasiyasının təsisçisi və sədridir. İllik təxminən 10&#8211;15 MBA və magistr tezisinə rəhbərlik edir. 2019-cu ildən Fransa Gənc Səfirlər Assosiasiyasının ilk azərbaycanlı nümayəndəsidir. 2020-ci ildən Fransa Akademik Tədqiqatlar İnstitutunun Mərkəzi Asiya üzrə koordinatorudur. 2020-ci ildə diaspora fəaliyyətinə görə Azərbaycan Respublikasının medalı ilə təltif olunub.</span>
    </div>
    <div class="stats">
      <div class="stat-item"><span class="stat-num">PhD</span><span class="stat-label"><span class="lang en">2019</span><span class="lang az">2019</span></span></div>
      <div class="stat-item"><span class="stat-num">10&#8211;15</span><span class="stat-label"><span class="lang en">Theses / Year</span><span class="lang az">Tezis / il</span></span></div>
      <div class="stat-item"><span class="stat-num">ALIM</span><span class="stat-label"><span class="lang en">Founder &amp; President</span><span class="lang az">Təsisçi və sədr</span></span></div>
      <div class="stat-item"><span class="stat-num">3M&nbsp;&euro;</span><span class="stat-label"><span class="lang en">Cooperation Projects</span><span class="lang az">Əməkdaşlıq layihəsi</span></span></div>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Core Competencies</span><span class="lang az">Əsas kompetensiyalar</span></h2>
    <div class="competency-grid">
      <div class="comp-group">
        <h3><span class="lang en">Research &amp; Expertise</span><span class="lang az">Tədqiqat və ekspertiza</span></h3>
        <ul>
          <li><span class="lang en">Innovation management and organizational ambidexterity</span><span class="lang az">İnnovasiya idarəetməsi və təşkilati ambidextriya</span></li>
          <li><span class="lang en">Change management and digital transformation</span><span class="lang az">Dəyişiklik idarəetməsi və rəqəmsal transformasiya</span></li>
          <li><span class="lang en">International and intercultural management</span><span class="lang az">Beynəlxalq və mədəniyyətlərarası idarəetmə</span></li>
          <li><span class="lang en">HR, marketing, strategy, and project management</span><span class="lang az">HR, marketinq, strategiya və layihə idarəetməsi</span></li>
        </ul>
      </div>
      <div class="comp-group">
        <h3><span class="lang en">Teaching</span><span class="lang az">Tədris</span></h3>
        <ul>
          <li><span class="lang en">Change management, project management, leadership (ADA University MBA, since 2024)</span><span class="lang az">Dəyişiklik idarəetməsi, layihə idarəetməsi, liderlik (ADA MBA, 2024-dən)</span></li>
          <li><span class="lang en">HR in consulting; public-health project management (UVSQ, since 2023)</span><span class="lang az">Konsaltinqdə HR; ictimai sağlamlıq layihə idarəetməsi (UVSQ, 2023-dən)</span></li>
          <li><span class="lang en">Management, marketing, strategy, organizational psychosociology (IUT Mantes, 2015&#8211;2017)</span><span class="lang az">Menecment, marketinq, strategiya, təşkilati psixososiologiya (IUT Mantes, 2015&#8211;2017)</span></li>
        </ul>
      </div>
      <div class="comp-group">
        <h3><span class="lang en">Consulting &amp; Industry</span><span class="lang az">Konsaltinq və sənaye</span></h3>
        <ul>
          <li><span class="lang en">Digital transformation clients: BioMérieux, Engie Digital, Allianz Partners, EDF Hydro</span><span class="lang az">Rəqəmsal transformasiya müştəriləri: BioMérieux, Engie Digital, Allianz Partners, EDF Hydro</span></li>
          <li><span class="lang en">Brand management, Evian/Danone Azerbaijan (2007&#8211;2008)</span><span class="lang az">Brend menecmenti, Evian/Danone Azərbaycanda (2007&#8211;2008)</span></li>
          <li><span class="lang en">HR and restructuring projects, AF Bank / AF Holding (2006&#8211;2007)</span><span class="lang az">HR və restrukturizasiya layihələri, AF Bank / AF Holding (2006&#8211;2007)</span></li>
        </ul>
      </div>
      <div class="comp-group">
        <h3><span class="lang en">Languages</span><span class="lang az">Dillər</span></h3>
        <ul>
          <li><span class="lang en">Azerbaijani (native); French, English, Russian, Turkish (fluent)</span><span class="lang az">Azərbaycan dili (ana dili); fransız, ingilis, rus, türk (səlis)</span></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Professional Experience</span><span class="lang az">Peşəkar fəaliyyət</span></h2>
    <div class="timeline">
      <article class="item"><div class="period"><span class="lang en">Since 2022</span><span class="lang az">2022-dən</span></div><div><h3>Onepoint, France</h3><span class="role"><span class="lang en">Change Management Consultant</span><span class="lang az">Dəyişiklik idarəetməsi konsultantı</span></span><p><span class="lang en">Supports clients&#8217; digital transformation; designs change-management strategy; leads training projects.</span><span class="lang az">Müştərilərin rəqəmsal transformasiyasını dəstəkləyir; change management strategiyasını hazırlayır; təlim layihələrinə rəhbərlik edir.</span></p></div></article>
      <article class="item"><div class="period"><span class="lang en">Since 2018</span><span class="lang az">2018-dən</span></div><div><h3><span class="lang en">Independent Consultant, France / Azerbaijan</span><span class="lang az">Müstəqil məsləhətçi, Fransa / Azərbaycan</span></h3><span class="role"><span class="lang en">International Cooperation Projects</span><span class="lang az">Beynəlxalq əməkdaşlıq layihələri</span></span><p><span class="lang en">Designs and implements cooperation projects between French and Azerbaijani public and private organizations (budget 3&nbsp;M&nbsp;&euro;).</span><span class="lang az">Fransız və azərbaycan dövlət və özəl qurumları arasında əməkdaşlıq layihələrini hazırlayır və həyata keçirir (3&nbsp;mln&nbsp;&euro; büdcə).</span></p></div></article>
      <article class="item"><div class="period">2011 &#8211; 2017</div><div><h3><span class="lang en">Université de Versailles / Georgetown University</span><span class="lang az">Versal Universiteti / Corctaun Universiteti</span></h3><span class="role"><span class="lang en">International Projects Officer</span><span class="lang az">Beynəlxalq layihələr üzrə məsul</span></span><p><span class="lang en">Managed custom training and research projects (~30 groups/year); supported UNESCO Chair on Entrepreneurship, Innovation and Change Management and MBA programmes.</span><span class="lang az">Fərdi təlim və tədqiqat layihələrini idarə etmişdir (~30 qrup/il); UNESCO Sahibkarlıq, İnnovasiya və Dəyişiklik İdarəetməsi kafedrasını və MBA proqramlarını dəstəkləmişdir.</span></p></div></article>
      <article class="item"><div class="period">2007 &#8211; 2008</div><div><h3>Evian / Danone, Azerbaijan</h3><span class="role"><span class="lang en">Brand Manager</span><span class="lang az">Brend meneceri</span></span><p><span class="lang en">Promoted Evian brand; quadrupled import volume; managed 45-person cross-functional team; merged marketing and distribution departments.</span><span class="lang az">Evian brendini təbliğ etmişdir; idxal həcmini 4 dəfə artırmışdır; 45 nəfərlik komandaya rəhbərlik etmişdir; marketinq və distribusiya şöbələrini birləşdirmişdir.</span></p></div></article>
      <article class="item"><div class="period">2006 &#8211; 2007</div><div><h3>AF Bank / AF Holding, Azerbaijan</h3><span class="role"><span class="lang en">HR Project Manager</span><span class="lang az">HR layihə meneceri</span></span></div></article>
      <article class="item"><div class="period">2004 &#8211; 2006</div><div><h3><span class="lang en">Investment Group, Azerbaijan / UAE</span><span class="lang az">İnvestisiya qrupu, Azərbaycan / BƏƏ</span></h3><span class="role"><span class="lang en">International Projects Officer</span><span class="lang az">Beynəlxalq layihələr üzrə məsul</span></span><p><span class="lang en">Investment projects, supplier negotiations, export relations; expatriation to Dubai; New Life modular housing projects in Sudan and Ethiopia.</span><span class="lang az">İnvestisiya layihələri, təchizatçılarla danışıqlar, ixrac əlaqələri; Dubaya ezamiyyə; Sudan və Efiopiyada modul ev layihələri.</span></p></div></article>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Education</span><span class="lang az">Təhsil</span></h2>
    <div class="education-grid">
      <article class="edu-card"><div class="period">2019</div><h3><span class="lang en">Ph.D. in Management Sciences</span><span class="lang az">İdarəetmə elmləri üzrə PhD</span></h3><p><span class="lang en">Université Paris-Saclay (UVSQ). Thesis: <em>Innovation management and ambidexterity in the American context: the case of family businesses</em>. Supervisor: Prof. Annie Bartoli. Rapporteurs: Dominique Besson (Lille), Jose-Luis Guerrero-Cusumano (Georgetown).</span><span class="lang az">Paris-Sakle Universiteti (UVSQ). Dissertasiya: <em>İnnovasiya idarəetməsi və ambidextriya: ABŞ kontekstində ailə müəssisələri</em>. Elmi rəhbər: Prof. Annie Bartoli.</span></p></article>
      <article class="edu-card"><div class="period">2012</div><h3><span class="lang en">Master 2, Business Administration</span><span class="lang az">Magistr 2, Biznes administrasiyası</span></h3><p><span class="lang en">Institut Supérieur de Management, Université de Versailles Saint-Quentin-en-Yvelines. Mention Bien.</span><span class="lang az">Institut Supérieur de Management, Versal Universiteti. Mention Bien.</span></p></article>
      <article class="edu-card"><div class="period">2010</div><h3><span class="lang en">Master 2, Trilingual International Management</span><span class="lang az">Magistr 2, Trilingual beynəlxalq menecment</span></h3><p><span class="lang en">Université Paris-Est Créteil. Mention Bien.</span><span class="lang az">Université Paris-Est Créteil. Mention Bien.</span></p></article>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Research &amp; Publications</span><span class="lang az">Tədqiqat və nəşrlər</span></h2>
    <div class="pub-block">
      <div class="pub-category">
        <ul>
          <li>Bartoli, A., Hermel, P., Safarova, G. (2017), &ldquo;Does the balance between conformity and innovation make companies more responsible? The case of four Ambidextrous SMEs,&rdquo; <em>RIMHE &#8211; Management &amp; Human Enterprise</em>, vol. 5, n°29, pp. 74&#8211;88.</li>
          <li>Bartoli, A., Hermel, P., Safarova, G. (2013), &ldquo;Tensions in managing change: Innovation vs Tradition?&rdquo; 11th International Conference &ldquo;Management and Engineering 2013,&rdquo; Sozopol, Bulgaria.</li>
          <li>Kadji, M., Safarova, G., Ngalla, A. (2015), &ldquo;Managerial innovation in the governance of a virtual community: the case of an Open Source Software Project,&rdquo; VII International Scientific Conference &ldquo;e-Governance,&rdquo; Sozopol, Bulgaria.</li>
        </ul>
      </div>
      <div class="callout" style="margin-top: 0;">
        <span class="lang en block">Participation in LAREQUOI laboratory research projects on innovation management. Member of organizing committees of international conferences. Author of scientific and publicistic articles on Azerbaijan in the French-language press.</span>
        <span class="lang az block">LAREQUOI laboratoriyasında innovasiya idarəetməsi üzrə tədqiqat layihələrində iştirak. Beynəlxalq konfransların təşkilat komitələrinin üzvü. Fransız dilində mətbuatda Azərbaycana dair elmi-publisistik məqalələrin müəllifi.</span>
      </div>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Administrative, Pedagogical &amp; Civic Activity</span><span class="lang az">İnzibati, pedaqoji və ictimai fəaliyyət</span></h2>
    <div class="callout">
      <span class="lang en block"><strong>2012&#8211;2017 (UVSQ / ISM / IUT):</strong> Supervision of Master 2 and professional licence theses; organization of thesis defences and VAE juries; organization of international seminars at Georgetown University.<br /><strong>ALIM Association (Loi 1901):</strong> Founder and president; fundraising (10&nbsp;k&nbsp;&euro;) for foreign students during the pandemic; training programme for Azerbaijan State Agency for Mandatory Medical Insurance.</span>
      <span class="lang az block"><strong>2012&#8211;2017 (UVSQ / ISM / IUT):</strong> Magistr 2 və peşə lisenziyası tezislərinə rəhbərlik; müdafiə və VAE jury-lərinin təşkili; Corctaun Universitetində beynəlxalq seminarların təşkili.<br /><strong>ALİM Assosiasiyası (Loi 1901):</strong> Təsisçi və sədr; pandemiya dövründə xarici tələbələr üçün vəsait yığımı (10&nbsp;min&nbsp;&euro;); Azərbaycan Dövlət Məcburi Tibbi Sığorta Agentliyi üçün təlim proqramının yaradılması.</span>
    </div>
  </section>

  <footer>
    <span class="lang en">Gunel Safarova, Ph.D. &ensp;·&ensp; Curriculum Vitae &ensp;·&ensp; Lyon, France</span>
    <span class="lang az">Günel Səfərova, Ph.D. &ensp;·&ensp; Tərcümeyi-hal &ensp;·&ensp; Lion, Fransa</span>
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
