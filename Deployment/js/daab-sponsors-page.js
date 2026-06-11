/** Sponsors page interactions (scroll reveal, form validation). */
(function () {
  // Scroll reveal
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((e, i) => {
        if (e.isIntersecting) {
          setTimeout(() => e.target.classList.add('visible'), i * 80);
          observer.unobserve(e.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    // Smooth anchor scrolls
    document.querySelectorAll('a[href^="#"]').forEach(a => {
      a.addEventListener('click', e => {
        const target = document.querySelector(a.getAttribute('href'));
        if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
      });
    });

    // Populate country dropdowns with full ISO country list (localized by page language)
    const COUNTRY_CODES = [
      "AF","AL","DZ","AD","AO","AG","AR","AM","AU","AT","AZ","BS","BH","BD","BB","BY","BE","BZ","BJ","BT","BO","BA","BW","BR","BN","BG","BF","BI","CV","KH","CM","CA","CF","TD","CL","CN","CO","KM","CG","CD","CR","CI","HR","CU","CY","CZ","DK","DJ","DM","DO","EC","EG","SV","GQ","ER","EE","SZ","ET","FJ","FI","FR","GA","GM","GE","DE","GH","GR","GD","GT","GN","GW","GY","HT","HN","HU","IS","IN","ID","IR","IQ","IE","IL","IT","JM","JP","JO","KZ","KE","KI","KP","KR","KW","KG","LA","LV","LB","LS","LR","LY","LI","LT","LU","MG","MW","MY","MV","ML","MT","MH","MR","MU","MX","FM","MD","MC","MN","ME","MA","MZ","MM","NA","NR","NP","NL","NZ","NI","NE","NG","MK","NO","OM","PK","PW","PS","PA","PG","PY","PE","PH","PL","PT","QA","RO","RU","RW","KN","LC","VC","WS","SM","ST","SA","SN","RS","SC","SL","SG","SK","SI","SB","SO","ZA","SS","ES","LK","SD","SR","SE","CH","SY","TJ","TZ","TH","TL","TG","TO","TT","TN","TR","TM","TV","UG","UA","AE","GB","US","UY","UZ","VU","VA","VE","VN","YE","ZM","ZW"
    ];
    const countrySelects = document.querySelectorAll('select[data-country-list="1"]');
    countrySelects.forEach((select) => {
      const locale = select.dataset.locale || document.documentElement.lang || "en";
      const formatter = (typeof Intl !== "undefined" && typeof Intl.DisplayNames === "function")
        ? new Intl.DisplayNames([locale], { type: "region" })
        : null;
      COUNTRY_CODES.forEach((code) => {
        const option = document.createElement("option");
        option.value = code;
        option.textContent = formatter ? (formatter.of(code) || code) : code;
        select.appendChild(option);
      });
    });

    // Email validation for contact form
    const sponsorForm = document.querySelector('.sponsor-form');
    const emailInput = sponsorForm?.querySelector('input[type="email"]');
    const submitBtn = sponsorForm?.querySelector('.btn-submit');
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    const emailErrorText =
      sponsorForm?.dataset.emailError || 'Please enter a valid email address.';
    function clearEmailError() {
      if (!emailInput) return;
      emailInput.removeAttribute('aria-invalid');
      const existing = sponsorForm?.querySelector('.field-error[data-for="email"]');
      if (existing) existing.remove();
    }
    function showEmailError() {
      if (!emailInput || !sponsorForm) return;
      clearEmailError();
      emailInput.setAttribute('aria-invalid', 'true');
      const message = document.createElement('small');
      message.className = 'field-error';
      message.dataset.for = 'email';
      message.textContent = emailErrorText;
      emailInput.insertAdjacentElement('afterend', message);
    }
    function isEmailValid() {
      if (!emailInput) return true;
      const value = emailInput.value.trim();
      return emailPattern.test(value);
    }
    submitBtn?.addEventListener('click', () => {
      if (!isEmailValid()) {
        showEmailError();
        emailInput?.focus();
        return;
      }
      clearEmailError();
    });
    emailInput?.addEventListener('blur', () => {
      if (!emailInput.value.trim()) return;
      if (!isEmailValid()) showEmailError();
      else clearEmailError();
    });
    emailInput?.addEventListener('input', () => {
      if (isEmailValid()) clearEmailError();
    });

    // Counter animation for stats
    function animateCounter(el, target, suffix='') {
      let start = 0;
      const dur = 1800;
      const step = timestamp => {
        if (!start) start = timestamp;
        const progress = Math.min((timestamp - start) / dur, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        el.querySelector('.num').textContent = Math.floor(ease * target) + suffix;
        if (progress < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }
})();
