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
    // Codes come from the shared js/daab-country-codes.js module.
    const COUNTRY_CODES = window.DAAB_COUNTRY_CODES || [];
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
})();
