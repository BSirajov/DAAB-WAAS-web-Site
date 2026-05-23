from pathlib import Path

OUT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site\cv\emil_ahmadov.html")

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Curriculum Vitae — Emil Akhmedov</title>
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
    .awards-list { padding: 18px 22px 22px 42px; font-size: 14px; line-height: 1.75; }
    .awards-list li { margin-bottom: 8px; }
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
          <span class="lang en">Emil T. Akhmedov, Ph.D.</span>
          <span class="lang az">Emil T. Əhmədov, Ph.D.</span>
        </h1>
        <p class="subtitle">
          <span class="lang en">Theoretical and high-energy physicist. Chair of the Landau Department of Theoretical Physics at the Moscow Institute of Physics and Technology (MIPT). Leading researcher at MIPT and the Institute for Theoretical and Experimental Physics (ITEP), Moscow.</span>
          <span class="lang az">Nəzəri və yüksək enerjili fizika üzrə mütəxəssis. Moskva Fizika-Texniki İnstitutunda (MFTİ) L. D. Landau adına Nəzəri Fizika kafedrasının müdiri. MFTİ və Moskva Nəzəri və Eksperimental Fizika İnstitutunda (ITEP) aparıcı elmi işçi.</span>
        </p>
      </div>
      <figure class="hero-photo">
        <img src="../images/scientists-photos/emil-ahmadov.png" alt="Emil Akhmedov" width="160" height="200" loading="eager" />
      </figure>
    </div>
    <dl class="rank-bar">
      <div class="rank-item">
        <dt><span class="lang en">Academic Rank</span><span class="lang az">Akademik rütbə</span></dt>
        <dd><span class="lang en">Ph.D.; Habilitation (Dr. habil.)</span><span class="lang az">PhD; Habilitasiya (Dr. habil.)</span></dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">Institution</span><span class="lang az">Qurum</span></dt>
        <dd><span class="lang en">Moscow Institute of Physics and Technology (MIPT)</span><span class="lang az">Moskva Fizika-Texniki İnstitutu (MFTİ)</span></dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">E-mail</span><span class="lang az">E-poçt</span></dt>
        <dd>akhmedov.et@mipt.ru</dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">Location</span><span class="lang az">Yer</span></dt>
        <dd><span class="lang en">Dolgoprudny, Moscow Region, Russia</span><span class="lang az">Dolqoprudnı, Moskva vilayəti, Rusiya</span></dd>
      </div>
    </dl>
  </header>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Academic Profile</span><span class="lang az">Akademik profil</span></h2>
    <div class="callout">
      <span class="lang en block">Dr. Emil T. Akhmedov is a theoretical physicist specializing in theoretical physics, mathematics, and high-energy physics. He is Chair of the Landau Department of Theoretical Physics at MIPT and a leading researcher at MIPT&rsquo;s High Energy Physics Laboratory and at ITEP, Moscow. Author of 6 scientific books and a textbook in theoretical physics and mathematics, with approximately 80 articles in prestigious international journals. He has presented nearly 100 reports at international conferences in Europe, America, India, Korea, and Japan. Scientific supervisor of 6 PhD students. Repeated recipient of grants and honors from the Ministry of Science and Education of the Russian Federation, the Presidential Foundation, the Basis and Dynasty foundations, and international institutions. Visiting professor and researcher at the Albert Einstein Institute (MPI, Golm, Germany, 2005&#8211;2020) and KEK (Tsukuba, Japan, 2002). Awarded the Medal of the Honorary Education Worker (2023) for active service in science and education.</span>
      <span class="lang az block">Emil T. Əhmədov nəzəri fizika, riyaziyyat və yüksək enerjili fizika üzrə ixtisaslaşmış nəzəri fizikdir. MFTİ-də L. D. Landau adına Nəzəri Fizika kafedrasının müdiri, MFTİ-nin Yüksək Enerjili Fizika Laboratoriyasında və Moskva ITEP-də aparıcı elmi işçidir. Nəzəri fizika və riyaziyyat sahəsində 6 elmi kitabın və bir dərsliyin müəllifidir; nüfuzlu beynəlxalq jurnallarda təxminən 80 elmi məqaləsi dərc olunmuşdur. Avropa, Amerika, Hindistan, Koreya və Yaponiyada keçirilən beynəlxalq konfranslarda 100-ə yaxın məruzə ilə çıxış etmişdir. 6 PhD tələbəsinin elmi rəhbəri olmuşdur. Rusiya Elm və Təhsil Nazirliyi, Prezident Fondu, Basis və Dynasty fondları, həmçinin beynəlxalq elmi qurumlar tərəfindən dəfələrlə qrant və təltiflərə layiq görülmüşdür. Albert Einstein İnstitutunda (MPI, Golm, Almaniya, 2005&#8211;2020) və KEK-də (Tsukuba, Yaponiya, 2002) qonaq professor və tədqiqatçı kimi fəaliyyət göstərmişdir. Elm və təhsildə fəal xidmətlərinə görə 2023-cü ildə &ldquo;Fəxri Təhsil işçisi&rdquo; medalı ilə təltif olunmuşdur.</span>
    </div>
    <div class="stats">
      <div class="stat-item"><span class="stat-num">80+</span><span class="stat-label"><span class="lang en">Publications</span><span class="lang az">Nəşr</span></span></div>
      <div class="stat-item"><span class="stat-num">PhD</span><span class="stat-label"><span class="lang en">1998</span><span class="lang az">1998</span></span></div>
      <div class="stat-item"><span class="stat-num">6</span><span class="stat-label"><span class="lang en">PhD Students</span><span class="lang az">PhD rəhbərliyi</span></span></div>
      <div class="stat-item"><span class="stat-num">100</span><span class="stat-label"><span class="lang en">Conference Talks</span><span class="lang az">Konfrans məruzəsi</span></span></div>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Core Competencies</span><span class="lang az">Əsas kompetensiyalar</span></h2>
    <div class="competency-grid">
      <div class="comp-group">
        <h3><span class="lang en">Research Fields</span><span class="lang az">Tədqiqat sahələri</span></h3>
        <ul>
          <li><span class="lang en">Theoretical physics and mathematical physics</span><span class="lang az">Nəzəri fizika və riyazi fizika</span></li>
          <li><span class="lang en">High-energy physics</span><span class="lang az">Yüksək enerjili fizika</span></li>
          <li><span class="lang en">Advanced mathematical methods in physics</span><span class="lang az">Fizikada qabaqcıl riyazi metodlar</span></li>
        </ul>
      </div>
      <div class="comp-group">
        <h3><span class="lang en">Academic Leadership</span><span class="lang az">Akademik rəhbərlik</span></h3>
        <ul>
          <li><span class="lang en">Chair, Landau Department of Theoretical Physics, MIPT</span><span class="lang az">MFTİ-də L. D. Landau adına Nəzəri Fizika kafedrasının müdiri</span></li>
          <li><span class="lang en">Leading researcher, High Energy Physics Lab, MIPT</span><span class="lang az">MFTİ Yüksək Enerjili Fizika Laboratoriyasının aparıcı elmi işçisi</span></li>
          <li><span class="lang en">Leading researcher, ITEP, Moscow</span><span class="lang az">Moskva ITEP-də aparıcı elmi işçi</span></li>
        </ul>
      </div>
      <div class="comp-group">
        <h3><span class="lang en">Teaching &amp; Supervision</span><span class="lang az">Tədris və rəhbərlik</span></h3>
        <ul>
          <li><span class="lang en">Author of 6 scientific books and a textbook in theoretical physics and mathematics</span><span class="lang az">Nəzəri fizika və riyaziyyat üzrə 6 elmi kitab və bir dərslik müəllifi</span></li>
          <li><span class="lang en">Scientific supervision of 6 PhD students</span><span class="lang az">6 PhD tələbəsinə elmi rəhbərlik</span></li>
        </ul>
      </div>
      <div class="comp-group">
        <h3><span class="lang en">International Collaboration</span><span class="lang az">Beynəlxalq əməkdaşlıq</span></h3>
        <ul>
          <li><span class="lang en">Visiting professor/researcher, Albert Einstein Institute, MPI Golm, Germany (2005&#8211;2020)</span><span class="lang az">Qonaq professor/tədqiqatçı, Albert Einstein İnstitutu, MPI Golm, Almaniya (2005&#8211;2020)</span></li>
          <li><span class="lang en">Visiting professor/researcher, KEK, Tsukuba, Japan (2002)</span><span class="lang az">Qonaq professor/tədqiqatçı, KEK, Tsukuba, Yaponiya (2002)</span></li>
          <li><span class="lang en">Languages: English and Russian (fluent)</span><span class="lang az">Dillər: ingilis və rus (sərbəst)</span></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Present Positions</span><span class="lang az">Cari vəzifələr</span></h2>
    <div class="timeline">
      <article class="item"><div class="period"><span class="lang en">Present</span><span class="lang az">indiyədək</span></div><div><h3><span class="lang en">Moscow Institute of Physics and Technology (MIPT)</span><span class="lang az">Moskva Fizika-Texniki İnstitutu (MFTİ)</span></h3><span class="role"><span class="lang en">Chair, Landau Department of Theoretical Physics</span><span class="lang az">L. D. Landau adına Nəzəri Fizika kafedrasının müdiri</span></span></div></article>
      <article class="item"><div class="period"><span class="lang en">Present</span><span class="lang az">indiyədək</span></div><div><h3><span class="lang en">MIPT, High Energy Physics Laboratory</span><span class="lang az">MFTİ, Yüksək Enerjili Fizika Laboratoriyası</span></h3><span class="role"><span class="lang en">Leading Researcher</span><span class="lang az">Aparıcı elmi işçi</span></span></div></article>
      <article class="item"><div class="period"><span class="lang en">Present</span><span class="lang az">indiyədək</span></div><div><h3><span class="lang en">Institute for Theoretical and Experimental Physics (ITEP), Moscow</span><span class="lang az">Nəzəri və Eksperimental Fizika İnstitutu (ITEP), Moskva</span></h3><span class="role"><span class="lang en">Leading Researcher</span><span class="lang az">Aparıcı elmi işçi</span></span></div></article>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Education &amp; Academic Credentials</span><span class="lang az">Təhsil və akademik göstəricilər</span></h2>
    <div class="education-grid">
      <article class="edu-card"><div class="period">3 Jun 2009</div><h3><span class="lang en">Habilitation Thesis</span><span class="lang az">Habilitasiya dissertasiyası</span></h3><p><span class="lang en">Doctor of Science (habilitation), defended 3 June 2009.</span><span class="lang az">Elmlər doktoru (habilitasiya), 3 iyun 2009-cu ildə müdafiə olunub.</span></p></article>
      <article class="edu-card"><div class="period">11 Apr 1998</div><h3><span class="lang en">Ph.D.</span><span class="lang az">PhD</span></h3><p><span class="lang en">PhD thesis defended 11 April 1998.</span><span class="lang az">PhD dissertasiyası 11 aprel 1998-ci ildə müdafiə olunub.</span></p></article>
    </div>
  </section>

  <section class="section">
    <h2 class="section-title"><span class="lang en">Awards, Grants &amp; Honors</span><span class="lang az">Mükafatlar, qrantlar və fəxri adlar</span></h2>
    <ul class="awards-list">
      <li><span class="lang en">2021&#8211;2024: State grant Goszadanie, Ministry of Education and Science of the Russian Federation.</span><span class="lang az">2021&#8211;2024: Rusiya Federasiyasının Təhsil və Elm Nazirliyinin Goszadanie dövlət qrantı.</span></li>
      <li><span class="lang en">2021&#8211;2024: Grant from the Basis foundation (Group Leader).</span><span class="lang az">2021&#8211;2024: Basis fondu qrantı (Qrup rəhbəri).</span></li>
      <li><span class="lang en">2023: Medal of the Honorary Education Worker, Ministry of Science and Education of Russia.</span><span class="lang az">2023: Rusiya Elm və Təhsil Nazirliyinin &ldquo;Fəxri Təhsil işçisi&rdquo; medalı.</span></li>
      <li><span class="lang en">2020: Honor from the Ministry of Science and Education of the Russian Federation.</span><span class="lang az">2020: Rusiya Elm və Təhsil Nazirliyinin fəxri adı/təltifi.</span></li>
      <li><span class="lang en">2018&#8211;2021: Grant from the Basis foundation (Young Leader).</span><span class="lang az">2018&#8211;2021: Basis fondu qrantı (Gənc lider).</span></li>
      <li><span class="lang en">2017&#8211;2019: State grant Goszadanie, Ministry of Education and Science of the Russian Federation.</span><span class="lang az">2017&#8211;2019: Rusiya Təhsil və Elm Nazirliyinin Goszadanie dövlət qrantı.</span></li>
      <li><span class="lang en">2005&#8211;2020: Visiting professor/researcher, Albert Einstein Institute, Max Planck Institute, Golm, Germany.</span><span class="lang az">2005&#8211;2020: Albert Einstein İnstitutu, Maks Plank İnstitutu, Golm, Almaniyada qonaq professor/tədqiqatçı.</span></li>
      <li><span class="lang en">2014&#8211;2015: Grant for young professors, Dynasty foundation.</span><span class="lang az">2014&#8211;2015: Dynasty fondu gənc professorlar qrantı.</span></li>
      <li><span class="lang en">2006: Honor from the Head of the Ministry of Atomic Energy of the Russian Federation.</span><span class="lang az">2006: Rusiya Atom Enerjisi Nazirliyinin rəhbərliyinin fəxri adı/təltifi.</span></li>
      <li><span class="lang en">2004&#8211;2005: Grant from the President of the Russian Federation.</span><span class="lang az">2004&#8211;2005: Rusiya Federasiyası Prezidentinin qrantı.</span></li>
      <li><span class="lang en">2002: Visiting professor/researcher, KEK, Tsukuba, Japan.</span><span class="lang az">2002: KEK, Tsukuba, Yaponiyada qonaq professor/tədqiqatçı.</span></li>
    </ul>
  </section>

  <footer>
    <span class="lang en">Emil T. Akhmedov, Ph.D. &ensp;·&ensp; Curriculum Vitae &ensp;·&ensp; Dolgoprudny, Moscow Region, Russia</span>
    <span class="lang az">Emil T. Əhmədov, Ph.D. &ensp;·&ensp; Tərcümeyi-hal &ensp;·&ensp; Dolqoprudnı, Moskva vilayəti, Rusiya</span>
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
