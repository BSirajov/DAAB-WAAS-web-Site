/**
 * Sidebar timeline scroll-spy + mobile collapse (Activities Yeniliklər panel).
 * Used on activities and forum content pages with .timeline-list anchors.
 */
(function () {
  const links = Array.from(document.querySelectorAll('.timeline-list a[href^="#"]'));
  if (!links.length) return;

  const ids = links.map((a) => a.getAttribute('href').slice(1));
  const cards = ids.map((id) => document.getElementById(id)).filter(Boolean);
  const eventsWidget = document.querySelector('.sidebar-widget');
  const eventsToggle = document.querySelector('.events-menu-toggle');
  const mobileQuery = window.matchMedia('(max-width: 1060px)');

  function activate(link) {
    links.forEach((a) => a.classList.remove('tl-active'));
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
    activate(active !== null ? links[ids.indexOf(cards[active].id)] : null);
  }

  links.forEach((link) => link.addEventListener('click', jumpToTarget));
  if (eventsToggle) {
    eventsToggle.addEventListener('click', (event) => {
      event.stopPropagation();
      toggleEventsMenu();
    });
  }
  document.addEventListener('click', (event) => {
    if (!mobileQuery.matches || !eventsWidget || !eventsWidget.classList.contains('events-open')) return;
    if (eventsWidget.contains(event.target)) return;
    closeEventsMenu();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeEventsMenu();
  });
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
