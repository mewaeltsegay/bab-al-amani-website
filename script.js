// Header border once the page scrolls
const header = document.querySelector('.site-header');
const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 8);
onScroll();
window.addEventListener('scroll', onScroll, { passive: true });

// Mobile menu
const toggle = document.querySelector('.nav-toggle');
const links = document.getElementById('nav-links');
const setMenu = (open) => {
  links.classList.toggle('open', open);
  toggle.setAttribute('aria-expanded', open);
  toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
};
toggle.addEventListener('click', () => setMenu(!links.classList.contains('open')));
links.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && links.classList.contains('open')) { setMenu(false); toggle.focus(); }
});

// Reveal on scroll
const io = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    if (entry.isIntersecting) {
      entry.target.classList.add('in');
      io.unobserve(entry.target);
    }
  }
}, { rootMargin: '0px 0px -10% 0px' });
document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

// Google map: nothing loads from Google until the visitor presses the button.
// The choice isn't stored, so the map is off again on the next visit.
document.querySelectorAll('.map[data-map-src]').forEach((map) => {
  map.querySelector('.map-load').addEventListener('click', () => {
    const frame = document.createElement('iframe');
    frame.src = map.dataset.mapSrc;
    frame.title = 'Map showing Al Ghurair Centre, Deira, Dubai';
    frame.loading = 'lazy';
    frame.referrerPolicy = 'no-referrer-when-downgrade';
    frame.allowFullscreen = true;
    map.replaceChildren(frame);
  });
});

// Quote form: no backend, so it hands the request to the visitor's own email app.
// Nothing is stored or sent by the website itself.
const form = document.querySelector('.quote-form');
if (form) {
  const status = form.querySelector('.form-status');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    const d = Object.fromEntries(new FormData(form));
    const lines = [`Name: ${d.name}`];
    if (d.company) lines.push(`Company: ${d.company}`);
    lines.push(`Email: ${d.email}`);
    if (d.phone) lines.push(`Phone: ${d.phone}`);
    lines.push(`Category: ${d.category}`, `Destination: ${d.destination}`, '', d.message);
    const to = 'contact@babalamani.com';
    const subject = `Quote request: ${d.category} → ${d.destination}`;
    window.location.href = `mailto:${to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
    status.hidden = false;
    status.textContent = `Your email app should open with the request filled in. If nothing opens, email ${to} directly.`;
  });
}
