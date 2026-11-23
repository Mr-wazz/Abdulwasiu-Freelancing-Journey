(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Year
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = String(new Date().getFullYear());

  // Nav background on scroll
  var nav = document.querySelector('.nav');
  function onScroll() { if (nav) nav.classList.toggle('is-scrolled', window.scrollY > 20); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile menu
  var toggle = document.querySelector('.nav__toggle');
  var menu = document.getElementById('mobile-menu');
  function setMenu(open) {
    if (!toggle || !menu) return;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    menu.hidden = !open;
    document.body.classList.toggle('menu-open', open);
    if (open && nav) nav.classList.add('is-scrolled'); else onScroll();
  }
  if (toggle && menu) {
    toggle.addEventListener('click', function () { setMenu(menu.hidden); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !menu.hidden) { setMenu(false); toggle.focus(); } });
    window.addEventListener('resize', function () { if (window.innerWidth > 860 && !menu.hidden) setMenu(false); });
  }

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el, i) {
      var sib = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
      el.style.transitionDelay = Math.min(sib, 5) * 70 + 'ms';
      io.observe(el);
    });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Word-by-word highlight tied to scroll position
  var blocks = Array.prototype.slice.call(document.querySelectorAll('[data-highlight]'));
  blocks.forEach(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.setAttribute('aria-label', el.textContent.trim());
    el.innerHTML = words.map(function (w) { return '<span class="w" aria-hidden="true">' + w.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span>'; }).join(' ');
  });
  function paint() {
    var vh = window.innerHeight;
    blocks.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var start = vh * 0.85, end = vh * 0.35;
      var p = (start - r.top) / (start - end + r.height * 0.6);
      p = Math.max(0, Math.min(1, p));
      var ws = el.children, n = Math.round(p * ws.length);
      for (var i = 0; i < ws.length; i++) ws[i].classList.toggle('on', i < n);
    });
  }
  if (reduce) {
    blocks.forEach(function (el) { Array.prototype.forEach.call(el.children, function (w) { w.classList.add('on'); }); });
  } else if (blocks.length) {
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(function () { paint(); ticking = false; }); }
    }, { passive: true });
    window.addEventListener('resize', paint);
    paint();
  }


  // Project filter
  var filters = document.querySelectorAll('.filter');
  var projects = document.querySelectorAll('.project[data-cat]');
  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.getAttribute('data-filter');
      filters.forEach(function (b) { var on = b === btn; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', String(on)); });
      projects.forEach(function (pr) { var show = f === 'all' || pr.getAttribute('data-cat') === f; pr.hidden = !show; if (show) pr.classList.add('in'); });
    });
  });

  // Hero screenshot rotation
  var shots = document.querySelectorAll('.browser__screen img');
  var url = document.querySelector('.browser__url');
  if (shots.length > 1 && !reduce) {
    var idx = 0;
    setInterval(function () {
      if (document.hidden) return;
      shots[idx].classList.remove('is-on');
      idx = (idx + 1) % shots.length;
      shots[idx].classList.add('is-on');
      if (url) url.textContent = shots[idx].getAttribute('data-url');
    }, 3800);
  }
})();
