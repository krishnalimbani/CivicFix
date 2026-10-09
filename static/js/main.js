/* ============================================================
   CivicFix — main.js
   Scroll animations, counter, navbar scroll effect
   ============================================================ */

// ── Navbar scroll effect ─────────────────────────────────────
const nav = document.getElementById('mainNav');
if (nav) {
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 20);
  });
}

// ── AOS-like scroll animation ────────────────────────────────
function initScrollAnimations() {
  const els = document.querySelectorAll('[data-aos]');
  const delays = {'0': 0, '80': 80, '100': 100, '150': 150, '200': 200, '300': 300};

  function checkVisible() {
    els.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight - 60) {
        const delay = el.dataset.aosDelay ? parseInt(el.dataset.aosDelay) : 0;
        setTimeout(() => el.classList.add('aos-animate'), delay);
      }
    });
  }

  window.addEventListener('scroll', checkVisible, { passive: true });
  window.addEventListener('resize', checkVisible);
  checkVisible(); // run on load
}

// ── Counter animation ─────────────────────────────────────────
function animateCounters() {
  document.querySelectorAll('.counter, .stat-num[data-target]').forEach(el => {
    const target = parseInt(el.dataset.target || el.textContent);
    if (isNaN(target)) return;
    let start = 0;
    const duration = 1200;
    const step = 16;
    const increment = target / (duration / step);
    const timer = setInterval(() => {
      start += increment;
      if (start >= target) { el.textContent = target; clearInterval(timer); }
      else el.textContent = Math.floor(start);
    }, step);
  });
}

// ── Observe counters becoming visible ────────────────────────
function initCounters() {
  const targets = document.querySelectorAll('.counter, .stat-num[data-target]');
  if (!targets.length) return;
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting && !e.target.dataset.counted) {
        e.target.dataset.counted = '1';
        const t = parseInt(e.target.dataset.target || e.target.textContent);
        if (!isNaN(t)) animateSingle(e.target, t);
      }
    });
  }, { threshold: 0.5 });
  targets.forEach(t => obs.observe(t));
}

function animateSingle(el, target) {
  let start = 0;
  const duration = 1500;
  const step = 20;
  const increment = target / (duration / step);
  const timer = setInterval(() => {
    start += increment;
    if (start >= target) { el.textContent = target; clearInterval(timer); }
    else el.textContent = Math.floor(start);
  }, step);
}

// ── Auto-dismiss flash messages ───────────────────────────────
function initFlashAutoDismiss() {
  document.querySelectorAll('.flash-alert').forEach(el => {
    setTimeout(() => {
      el.classList.remove('show');
      setTimeout(() => el.remove(), 300);
    }, 6000);
  });
}

// ── Smooth active link ────────────────────────────────────────
function initNavActiveHighlight() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === path) link.classList.add('active');
  });
}

// ── Report ID auto-uppercase ──────────────────────────────────
function initReportIdInput() {
  const inp = document.getElementById('reportIdInput');
  if (inp) {
    inp.addEventListener('input', () => { inp.value = inp.value.toUpperCase(); });
  }
}

// ── Dark mode ─────────────────────────────────────────────────
function initDarkMode() {
  const toggle = document.getElementById('darkToggle');
  const icon   = document.getElementById('darkIcon');
  if (!toggle) return;

  // Restore saved preference
  const saved = localStorage.getItem('civicfix-theme');
  if (saved === 'dark') applyDark(true);

  toggle.addEventListener('click', () => {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    applyDark(!isDark);
    localStorage.setItem('civicfix-theme', !isDark ? 'dark' : 'light');
  });

  function applyDark(on) {
    if (on) {
      document.documentElement.setAttribute('data-theme', 'dark');
      icon.className = 'bi bi-sun-fill';
    } else {
      document.documentElement.removeAttribute('data-theme');
      icon.className = 'bi bi-moon-fill';
    }
  }
}

// ── Scroll to top ─────────────────────────────────────────────
function initScrollTop() {
  const btn = document.getElementById('scrollTop');
  if (!btn) return;
  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 300);
  }, { passive: true });
  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ── Init everything ───────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initScrollAnimations();
  initCounters();
  initFlashAutoDismiss();
  initNavActiveHighlight();
  initReportIdInput();
  initDarkMode();
  initScrollTop();
});
