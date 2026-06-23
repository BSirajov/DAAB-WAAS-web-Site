/**
 * Sidebar timeline scroll-spy + mobile collapse (Activities, Charter, forum pages).
 * Uses js/daab-sidebar-spy.js for shared scroll-spy logic.
 */
(function () {
  const links = Array.from(document.querySelectorAll('.timeline-list a[href^="#"]'));
  if (!links.length) return;

  const eventsWidget = document.querySelector('.sidebar-widget');
  const eventsToggle = document.querySelector('.events-menu-toggle');
  const Spy = window.DAAB_SIDEBAR_SPY;

  function sidebarStackMediaQuery() {
    if (window.DAAB_DESIGN && typeof window.DAAB_DESIGN.sidebarStackMq === 'function') {
      return window.DAAB_DESIGN.sidebarStackMq();
    }
    return window.matchMedia('(max-width: 1060px)');
  }

  const mobileQuery = sidebarStackMediaQuery();
  const spy =
    Spy && typeof Spy.fromTimelineLinks === 'function'
      ? Spy.fromTimelineLinks(links)
      : null;

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
    if (spy) spy.scrollToId(id);
    else target.scrollIntoView({ block: 'start', behavior: 'auto' });
    history.pushState(null, '', link.getAttribute('href'));
    if (mobileQuery.matches) closeEventsMenu();
  }

  function onScroll() {
    if (spy) spy.updateActive();
    else {
      const mid = window.scrollY + window.innerHeight * 0.35;
      let active = null;
      const cards = links
        .map((a) => document.getElementById(a.getAttribute('href').slice(1)))
        .filter(Boolean);
      for (let i = cards.length - 1; i >= 0; i--) {
        if (cards[i] && cards[i].offsetTop <= mid) {
          active = links[i];
          break;
        }
      }
      activate(active);
    }
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

  function syncFromHash() {
    const id = location.hash.slice(1);
    const idx = id ? links.findIndex((a) => a.getAttribute('href') === '#' + id) : -1;
    if (idx === -1) {
      activate(null);
      return;
    }
    activate(links[idx]);
    if (spy) spy.scrollToId(id);
  }

  window.addEventListener('popstate', syncFromHash);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
