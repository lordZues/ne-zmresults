(() => {
  // Mobile menu
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');
  toggle?.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(isOpen));
  });
  document.querySelectorAll('.nav a').forEach((link) => link.addEventListener('click', () => {
    nav?.classList.remove('open');
    toggle?.setAttribute('aria-expanded', 'false');
  }));

  // Buttons like "Claim your growth plan" preselect the matching service in the form
  document.querySelectorAll('[data-service]').forEach((el) => el.addEventListener('click', () => {
    const select = document.querySelector('#contact select[name="service"]');
    if (select) select.value = el.dataset.service;
  }));

  // Footer year
  document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });

  // Audit form: saves to the Cloudflare leads database AND emails a copy via FormSubmit.
  // If both fail, the visitor is pointed to WhatsApp/phone instead of losing the enquiry.
  const LEADS_ENDPOINT = '/api/audit';
  const EMAIL_ENDPOINT = 'https://formsubmit.co/ajax/zuesjordan@gmail.com';

  document.querySelectorAll('.contact-form').forEach((form) => {
    const status = form.querySelector('.form-status');
    const button = form.querySelector('button[type="submit"]');
    const buttonHtml = button ? button.innerHTML : '';

    const show = (type, msg) => {
      if (!status) return;
      status.className = 'form-status ' + type;
      status.innerHTML = msg;
    };

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;

      const data = Object.fromEntries(new FormData(form).entries());
      data.source_page = location.pathname;
      const isQuery = form.dataset.form === 'query';
      if (!data.business_name) data.business_name = 'Not given';

      if (button) { button.disabled = true; button.textContent = 'Sending…'; }
      show('', '');

      const withTimeout = (p, ms) => Promise.race([p, new Promise((_, r) => setTimeout(() => r(new Error('timeout')), ms))]);

      const saveLead = withTimeout(fetch(LEADS_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      }).then((r) => { if (!r.ok) throw new Error('lead ' + r.status); return true; }), 12000);

      const emailLead = withTimeout(fetch(EMAIL_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({
          _subject: (isQuery ? 'New website query — ' : 'New free audit request — ') + data.name +
            (data.business_name !== 'Not given' ? ' (' + data.business_name + ')' : ''),
          _template: 'table',
          _captcha: 'false',
          _honey: data.company_url || '',
          _replyto: data.email || undefined,
          Type: isQuery ? 'General query' : 'Free growth audit request',
          Name: data.name,
          Business: data.business_name,
          Phone: data.phone,
          email: data.email || '—',
          'About': data.service,
          Message: data.message || '—',
          'Sent from page': 'zmresults.co.za' + data.source_page,
        }),
      }).then((r) => { if (!r.ok) throw new Error('email ' + r.status); return true; }), 12000);

      const results = await Promise.allSettled([saveLead, emailLead]);
      const anyOk = results.some((r) => r.status === 'fulfilled');

      if (anyOk) {
        form.reset();
        location.href = 'thank-you.html';
        return;
      }

      if (button) { button.disabled = false; button.innerHTML = buttonHtml; }
      show('error', 'Sorry, something went wrong sending your request. Please <a href="https://wa.me/27736957783?text=Hi%20ZM%20Results%2C%20I%27d%20like%20a%20free%20growth%20audit.">WhatsApp us</a> or call <a href="tel:+27736957783">073 695 7783</a>.');
    });
  });
})();
