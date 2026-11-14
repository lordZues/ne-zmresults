"""Builds the ZM Results website pages from shared templates.

Run from the repo root:  python3 _build/build.py
It regenerates every .html page plus sitemap.xml in the repo root.
Edit content (pages, area pages, blog POSTS) in this file, never the generated .html files.
"""
import json, html, pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent  # repo root: pages are served from here
BASE = "https://zmresults.co.za"
PHONE_DISPLAY = "073 695 7783"
PHONE_TEL = "+27736957783"
WA = "https://wa.me/27736957783?text=Hi%20ZM%20Results%2C%20I%27d%20like%20a%20free%20growth%20audit."
EMAIL = "zmresults@gmail.com"          # shown publicly on the site
FORM_EMAIL = "zuesjordan@gmail.com"   # where every form submission is emailed
REVIEW_URL = "https://g.page/r/CQwwFzKsM4ULEAE/review"  # Google Business Profile review link
MAPS_URL = "https://share.google/gZWnF4aFIT76BYTSZ"  # Google Business Profile / Maps listing
LINKEDIN_URL = "https://www.linkedin.com/in/zusakhe-mazibu-55b72037a"  # owner's personal LinkedIn
LINKEDIN_COMPANY_URL = "https://www.linkedin.com/company/zm-results/"  # ZM Results company page
FACEBOOK_URL = "https://www.facebook.com/ZMResults"  # ZM Results Facebook page
INSTAGRAM_URL = "https://www.instagram.com/zm_results/"  # ZM Results Instagram

BUSINESS = {
    "@type": "ProfessionalService",
    "@id": BASE + "/#business",
    "name": "ZM Results",
    "url": BASE + "/",
    "telephone": PHONE_TEL,
    "email": EMAIL,
    "description": "Digital marketing for Durban businesses: SEO, social media management and Google Ads.",
    "address": {"@type": "PostalAddress", "addressLocality": "Durban", "addressRegion": "KwaZulu-Natal", "addressCountry": "ZA"},
    "areaServed": [{"@type": "City", "name": n} for n in ["Durban", "Umhlanga", "Ballito", "Pinetown", "Pietermaritzburg"]],
    "priceRange": "R",
    "logo": BASE + "/logo.png",
    "image": BASE + "/og-image.png",
    "hasMap": MAPS_URL,
    "sameAs": [MAPS_URL, LINKEDIN_COMPANY_URL, FACEBOOK_URL, INSTAGRAM_URL],
}

WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm5.8 14.13c-.24.68-1.42 1.3-1.96 1.35-.5.05-.97.23-3.28-.68-2.78-1.1-4.55-3.95-4.69-4.13-.13-.18-1.11-1.48-1.11-2.82 0-1.34.7-2 .95-2.27.25-.27.54-.34.72-.34h.52c.17 0 .39-.06.61.47.24.56.79 1.92.86 2.06.07.14.11.3.02.48-.09.18-.14.3-.27.46-.14.16-.29.36-.41.48-.14.14-.28.29-.12.56.16.27.71 1.17 1.52 1.9 1.05.93 1.93 1.22 2.2 1.36.27.14.43.11.59-.07.16-.18.68-.8.86-1.07.18-.27.36-.23.61-.14.25.09 1.59.75 1.86.89.27.14.45.2.52.32.07.11.07.66-.17 1.34Z"/></svg>'


def header(active=""):
    def link(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f"""<a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header" id="top">
      <div class="container nav-wrap">
        <a class="brand" href="/" aria-label="ZM Results home"><span class="brand-mark"><img src="logo-icon.svg" alt="" width="30" height="25" /></span><span class="brand-name">ZM <em>Results</em></span></a>
        <button class="menu-toggle" type="button" aria-label="Open navigation" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span></button>
        <nav class="nav" id="site-nav" aria-label="Main navigation">
          {link("services.html", "Services", "services")}
          {link("seo-durban.html", "SEO", "seo")}
          {link("social-media-management-durban.html", "Social media", "social")}
          {link("google-ads-durban.html", "Google Ads", "ads")}
          {link("/#pricing", "Pricing", "pricing")}
          {link("blog.html", "Blog", "blog")}
          {link("contact.html", "Contact", "contact")}
          <a class="button button-dark nav-cta" href="#contact">Get your free audit</a>
        </nav>
      </div>
    </header>"""


def footer():
    return f"""<footer class="footer">
      <div class="container">
        <div class="footer-top">
          <div>
            <a class="brand" href="/"><span class="brand-mark"><img src="logo-icon.svg" alt="" width="30" height="25" /></span><span class="brand-name">ZM <em>Results</em></span></a>
            <p>Digital marketing for Durban businesses. We help good local businesses get found, get trusted and get chosen.</p>
          </div>
          <div>
            <h4>Services</h4>
            <ul>
              <li><a href="seo-durban.html">SEO in Durban</a></li>
              <li><a href="social-media-management-durban.html">Social media management</a></li>
              <li><a href="google-ads-durban.html">Google Ads management</a></li>
              <li><a href="website-design-durban.html">Website design</a></li>
              <li><a href="chatbot-ai-integration-durban.html">Chatbots &amp; AI integration</a></li>
              <li><a href="/#pricing">90-Day Google Growth Plan</a></li>
              <li><a href="blog.html">Marketing tips blog</a></li>
            </ul>
          </div>
          <div>
            <h4>Areas we serve</h4>
            <ul>
              <li><a href="/">Durban</a></li>
              <li><a href="marketing-agency-umhlanga.html">Umhlanga</a></li>
              <li><a href="marketing-agency-ballito.html">Ballito</a></li>
              <li><a href="marketing-agency-pinetown.html">Pinetown</a></li>
              <li><a href="marketing-agency-pietermaritzburg.html">Pietermaritzburg</a></li>
            </ul>
          </div>
          <div>
            <h4>Contact</h4>
            <ul>
              <li><a href="contact.html">Send us a query</a></li>
              <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
              <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp us</a></li>
              <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
              <li><a href="{REVIEW_URL}" target="_blank" rel="noopener">★ Leave us a Google review</a></li>
              <li><a href="{FACEBOOK_URL}" target="_blank" rel="noopener">f&nbsp; Follow us on Facebook</a></li>
              <li><a href="{INSTAGRAM_URL}" target="_blank" rel="noopener">◎&nbsp; Follow us on Instagram</a></li>
              <li><a href="{LINKEDIN_COMPANY_URL}" target="_blank" rel="noopener">in&nbsp; Follow ZM Results on LinkedIn</a></li>
              <li><a href="{LINKEDIN_URL}" target="_blank" rel="noopener">in&nbsp; Connect with the founder</a></li>
              <li><a href="{MAPS_URL}" target="_blank" rel="noopener">📍 Durban, KwaZulu-Natal (Google Maps)</a></li>
            </ul>
          </div>
        </div>
        <p class="footer-bottom">© <span data-year>2026</span> ZM Results. Built for growth in Durban.</p>
      </div>
    </footer>
    <a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Chat with ZM Results on WhatsApp">{WA_SVG}</a>
    <script src="script.js" defer></script>"""


def contact(eyebrow="Ready to grow?", title="Let's get your<br /><em>business seen.</em>",
            intro="Tell us a little about your business and we'll get back to you with a free growth audit.",
            preselect="SEO & Google rankings"):
    options = ["SEO & Google rankings", "Social media management", "Google Ads", "90-Day Google Growth Plan", "Website design", "Chatbot & AI integration", "Everything / not sure yet"]
    opts = "".join(f'<option{" selected" if o == preselect else ""}>{html.escape(o)}</option>' for o in options)
    return f"""<section class="contact section" id="contact">
        <div class="container contact-grid">
          <div>
            <p class="eyebrow">{eyebrow}</p>
            <h2>{title}</h2>
            <p>{intro}</p>
            <div class="contact-links">
              <a class="whatsapp-link" href="{WA}" target="_blank" rel="noopener">☏ WhatsApp {PHONE_DISPLAY}</a>
              <a href="tel:{PHONE_TEL}">☎ Call {PHONE_DISPLAY}</a>
              <a href="mailto:{EMAIL}">✉ {EMAIL}</a>
            </div>
          </div>
          <form class="contact-form" action="https://formsubmit.co/{FORM_EMAIL}" method="POST" novalidate>
            <input type="hidden" name="_next" value="{BASE}/thank-you.html" />
            <input type="hidden" name="_subject" value="New ZM Results audit request" />
            <input type="hidden" name="_captcha" value="false" />
            <label class="hp" aria-hidden="true">Leave this empty<input name="company_url" type="text" tabindex="-1" autocomplete="off" /></label>
            <label>Your name<input name="name" type="text" autocomplete="name" required maxlength="100" /></label>
            <label>Business name<input name="business_name" type="text" autocomplete="organization" required maxlength="120" /></label>
            <label>Phone number<input name="phone" type="tel" autocomplete="tel" required maxlength="30" inputmode="tel" /></label>
            <label><span>Email <span class="optional">(optional)</span></span><input name="email" type="email" autocomplete="email" maxlength="160" /></label>
            <label class="full">What do you need help with?<select name="service">{opts}</select></label>
            <label class="full"><span>Your website or anything we should know <span class="optional">(optional)</span></span><textarea name="message" maxlength="2000"></textarea></label>
            <p class="form-status" role="alert"></p>
            <button class="button button-dark" type="submit">Request my free audit <span>→</span></button>
            <p class="form-note">No obligation. We'll only use your details to contact you about your audit.</p>
          </form>
        </div>
      </section>"""


def page(filename, title, description, body, active="", schema=None, noindex=False):
    canonical = BASE + "/" + ("" if filename == "index.html" else filename)
    graph = [BUSINESS] + (schema or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    robots = '\n    <meta name="robots" content="noindex" />' if noindex else ""
    doc = f"""<!doctype html>
<html lang="en-ZA">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description)}" />{robots}
    <link rel="canonical" href="{canonical}" />
    <meta name="theme-color" content="#f5f2eb" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="ZM Results" />
    <meta property="og:locale" content="en_ZA" />
    <meta property="og:title" content="{html.escape(title)}" />
    <meta property="og:description" content="{html.escape(description)}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:image" content="{BASE}/og-image.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="icon" href="favicon.svg" type="image/svg+xml" />
    <link rel="apple-touch-icon" href="apple-touch-icon.png" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600;1,700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="styles.css" />
    <script type="application/ld+json">
{ld}
    </script>
  </head>
  <body>
    {header(active)}
    <main id="main">
      {body}
    </main>
    {footer()}
  </body>
</html>
"""
    (SITE / filename).write_text(doc, encoding="utf-8")
    return canonical


def faq_html(items):
    return "".join(f"<details><summary>{html.escape(q)}</summary><p>{a}</p></details>" for q, a in items)


def faq_schema(items):
    import re
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
        for q, a in items]}


def breadcrumb_schema(name, file):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{BASE}/{file}"}]}


def cta_band(eyebrow, title, text, label="Get your free audit"):
    return f"""<section class="service-cta"><div class="container service-cta-inner"><div><p class="eyebrow">{eyebrow}</p><h2>{title}</h2><p>{text}</p></div><a class="button button-dark" href="#contact">{label} <span>→</span></a></div></section>"""


urls = []

# ---------------- CLIENT LOGOS ----------------
CLIENTS = [
    ("client-chiliza-attorneys.jpg", "Chiliza Attorneys"),
    ("client-scm-logistics.jpg", "SCM Logistics"),
    ("client-hustletrack.jpg", "HustleTrack"),
    ("client-ultra-intellects.jpg", "Ultra Intellects"),
    ("client-quick-fix-laptop-repairs.jpg", "Quick Fix Laptop Repairs"),
    ("client-zm-accessories-outdoor.jpg", "ZM Accessories Outdoor"),
    ("client-roof-rackers.jpg", "Roof Rackers"),
]
CLIENT_TILES = "".join(
    f'<li><img src="{f}" alt="{html.escape(n) + " logo" if n else "Client logo"}" width="480" height="480" loading="lazy" decoding="async" />'
    + (f"<span>{html.escape(n)}</span>" if n else "") + "</li>"
    for f, n in CLIENTS)

# ---------------- TESTIMONIALS ----------------
# Real Google reviews of ZM Results, supplied by the owner. Names shortened to first name + initial.
TESTIMONIALS = [
    ("It was a pleasure working with you guys, appreciate the transparency. The marketing was perfectly executed. Looking forward to working together in the future.", "Masande N.", 4),
    ("It was a pleasure working with you, you were very professional and did the marketing perfectly. Your service is exceptional.", "Nondumiso M.", 5),
    ("It was a pleasure working with you. Everything was very professional, and the marketing was done perfectly.", "Slindile G.", 5),
    ("Very great service, quick TAT and excellent quality. Highly recommended ZM Results.", "Lindokuhle L.", 5),
]
TESTIMONIAL_CARDS = "".join(
    f'''<figure class="review-card"><div class="review-stars" role="img" aria-label="{s} out of 5 stars">{"★" * s}<span>{"★" * (5 - s)}</span></div><blockquote>“{html.escape(q)}”</blockquote><figcaption><b>{html.escape(n)}</b><span>Google review</span></figcaption></figure>'''
    for q, n, s in TESTIMONIALS)

# ---------------- HOME ----------------
home_faq = [
    ("What's included in the 90-Day Google Growth Plan?",
     "A complete SEO audit and strategy, local SEO and Google Business Profile optimisation, website optimisation, a content and keyword strategy, and monthly reporting and support — all for a one-time investment of R15 000."),
    ("Is the R15 000 a monthly fee?",
     "No. The 90-Day Google Growth Plan is a one-time investment, not a monthly retainer."),
    ("Do I have to sign a long-term contract?",
     "No. We don't lock you into long-term contracts. We'd rather keep your business by getting you results."),
    ("How long does SEO take to work?",
     "SEO builds over time. The 90-day plan is designed to build real page-one momentum, and most businesses see rankings and enquiries keep improving in the months after the core work is done. We'll give you an honest view of your market in your free audit."),
    ("What happens in the free growth audit?",
     "We look at how your business currently shows up on Google, your website and your competitors, then tell you where the biggest opportunities are. There's no obligation to buy anything."),
]
home = f"""
      <section class="hero">
        <div class="container hero-grid">
          <div class="hero-copy">
            <p class="eyebrow">Digital marketing agency · Durban</p>
            <h1 class="hero-title">Not on page one?<br /><span>Your competitors are.</span></h1>
            <p class="hero-lead">Right now, someone in Durban is searching Google for exactly what you sell, and calling whoever shows up first. If that isn't you, those customers are going straight to your competitors. We get your business onto page one so the calls come to you.</p>
            <div class="hero-actions"><a class="button button-accent" href="#contact">See where you rank, free <span>→</span></a><a class="text-link" href="#process">How it works <span>→</span></a></div>
            <p class="hero-note"><span class="spark">✦</span> Free growth audit · No long-term contracts</p>
          </div>
          <div class="hero-visual" aria-hidden="true">
            <div class="orbit orbit-one"></div><div class="orbit orbit-two"></div>
            <div class="search-card">
              <div class="search-top"><span class="search-icon">⌕</span><span>plumber near me durban</span><span class="dots">•••</span></div>
              <div class="result-line"></div><div class="result-line short"></div>
              <div class="google-result"><div class="result-url">yourbusiness.co.za</div><strong>Your Business | Durban</strong><p>The first result your customers see when they search.</p><span class="result-badge">Page one, top spot</span></div>
              <div class="result-line"></div><div class="result-line short"></div>
            </div>
            <div class="float-card rank-card"><span class="float-icon">↗</span><div><small>The goal</small><strong>Page one</strong></div></div>
            <div class="float-card growth-card"><span class="float-icon">✦</span><div><small>The result</small><strong>More enquiries</strong></div></div>
            <div class="scribble">be seen<br /><span>be chosen</span></div>
          </div>
        </div>
      </section>

      <section class="trust-bar"><div class="container trust-inner"><span>WHY DURBAN BUSINESSES CHOOSE US</span><div class="trust-items"><strong>Durban-based</strong><strong>No long-term contracts</strong><strong>Monthly reporting</strong><strong>Free growth audit</strong></div></div></section>

      <section class="clients section" id="clients"><div class="container">
        <div class="section-head centered"><p class="eyebrow">Our clients</p><h2>Businesses we've<br /><em>worked with.</em></h2><p class="section-intro">From attorneys and logistics companies to contractors and repair shops, we help businesses across industries get seen.</p></div>
        <ul class="client-grid">{CLIENT_TILES}</ul>
      </div></section>

      <section class="reviews section" id="reviews"><div class="container">
        <div class="section-head centered"><p class="eyebrow">Client reviews</p><h2>What our clients<br /><em>say about us.</em></h2></div>
        <div class="review-grid">{TESTIMONIAL_CARDS}</div>
        <div class="reviews-actions"><a class="button button-dark" href="{MAPS_URL}" target="_blank" rel="noopener">Read all our Google reviews <span>→</span></a><a class="text-link" href="{REVIEW_URL}" target="_blank" rel="noopener">Worked with us? Leave a review <span>→</span></a></div>
      </div></section>

      <section class="services section" id="services"><div class="container"><div class="section-head"><div><p class="eyebrow">What we do</p><h2>More visibility.<br /><em>More business.</em></h2></div><p class="section-intro">Your customers are searching online. We make sure they find you, trust you and choose you.</p></div><div class="service-grid">
        <article class="service-card featured"><span class="service-number">01</span><span class="service-icon">⌕</span><h3>SEO that gets you<br />on page one</h3><p>We optimise your website and online presence to rank higher and bring in customers who are ready to buy.</p><a href="seo-durban.html">Explore SEO <span>→</span></a></article>
        <article class="service-card"><span class="service-number">02</span><span class="service-icon">◎</span><h3>Social media that<br />builds your brand</h3><p>We create content and manage your social media so your business stays visible, relevant and top of mind.</p><a href="social-media-management-durban.html">Explore social media <span>→</span></a></article>
        <article class="service-card"><span class="service-number">03</span><span class="service-icon">↗</span><h3>Google Ads that<br />drive real leads</h3><p>Get in front of people searching for exactly what you offer with campaigns built for results.</p><a href="google-ads-durban.html">Explore Google Ads <span>→</span></a></article>
      </div><p class="note" style="text-align:center;margin-top:30px">We also build <a href="website-design-durban.html">websites that convert</a> and set up <a href="chatbot-ai-integration-durban.html">chatbots &amp; AI assistants</a> that answer customers after hours.</p></div></section>

      <section class="promise section"><div class="container promise-grid"><div><p class="eyebrow">Our promise</p><h2>Be the business<br /><em>people find first.</em></h2><p class="promise-copy">If your business isn't on the first page of Google, your customers might never see you. That's where we come in.</p><a class="button button-dark" href="#contact">Let's grow your business <span>→</span></a></div><div class="promise-stats"><div class="big-stat"><strong>90</strong><span>days to page-one<br />momentum</span></div><div class="stat-row"><div><strong>R15k</strong><span>all-in SEO<br />investment</span></div><div><strong>100%</strong><span>focused on<br />your growth</span></div></div></div></div></section>

      <section class="process section" id="process"><div class="container"><div class="section-head centered"><p class="eyebrow">How it works</p><h2>A simple plan.<br /><em>Serious results.</em></h2><p class="section-intro">No confusing jargon. No guesswork. Just a clear, proven process to get your business growing.</p></div><div class="steps"><article><span>01</span><h3>We audit</h3><p>We look at where you are now and find the biggest opportunities.</p></article><article><span>02</span><h3>We plan</h3><p>We build a strategy around your goals, your market and your budget.</p></article><article><span>03</span><h3>We execute</h3><p>We do the work — SEO, content, social and ads — to move you forward.</p></article><article><span>04</span><h3>You grow</h3><p>You get more visibility, more enquiries and more business.</p></article></div></div></section>

      <section class="pricing section" id="pricing"><div class="container pricing-grid"><div><p class="eyebrow">Our flagship offer</p><h2>First page<br /><em>in 90 days.</em></h2><p>Our most popular package for businesses ready to be seen and chosen more often.</p><ul class="check-list"><li>Complete SEO audit &amp; strategy</li><li>Local SEO &amp; Google Business Profile</li><li>Website optimisation</li><li>Content &amp; keyword strategy</li><li>Monthly reporting &amp; support</li></ul></div><div class="price-box"><p class="price-label">90-Day Google Growth Plan</p><div class="price">R15 000</div><span class="once">one-time investment · no monthly retainer</span><div class="price-divider"></div><p>Get the visibility your business deserves. Start your journey to page one today.</p><a class="button button-accent" href="#contact" data-service="90-Day Google Growth Plan">Claim your growth plan <span>→</span></a><small>Limited spaces available each month.</small></div></div></section>

      <section class="about section" id="about"><div class="container about-grid"><div><p class="eyebrow">Why ZM Results?</p><h2>We don't just<br /><em>do marketing.</em></h2></div><div><p class="about-lead">We help good businesses become the obvious choice.</p><p>Based in Durban, ZM Results is a results-focused digital marketing company built for local businesses that want to grow. We believe marketing should be simple, honest and tied to real business outcomes.</p><p>You'll deal directly with the person doing the work, get plain-language reports every month, and always know what we're doing and why.</p><a class="text-link" href="#contact">Meet your growth partner <span>→</span></a></div></div></section>

      <section class="faq section" id="faq"><div class="container"><div class="section-head centered"><p class="eyebrow">Questions</p><h2>Good to <em>know.</em></h2></div><div class="faq-list">{faq_html(home_faq)}</div></div></section>

      {contact()}"""
urls.append(page("index.html", "Marketing Agency Durban | SEO & Google Ads | ZM Results",
                 "ZM Results helps Durban businesses get found, trusted and chosen with SEO, social media management and Google Ads. Get a free growth audit.",
                 home, schema=[
                     {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "ZM Results", "publisher": {"@id": BASE + "/#business"}},
                     {"@type": "Offer", "name": "90-Day Google Growth Plan", "price": "15000", "priceCurrency": "ZAR", "seller": {"@id": BASE + "/#business"}},
                     faq_schema(home_faq)]))


# ---------------- SERVICE PAGE BUILDER ----------------
def service_page(file, crumb, title, desc, eyebrow, h1, lead, intro_lead, intro_body, fit, features, steps, faq, cta, preselect, service_name, active):
    feats = "".join(f'<article><span class="service-icon">{i}</span><h3>{h}</h3><p>{p}</p></article>' for i, h, p in features)
    step_html = "".join(f"<article><span>{n:02d}</span><h3>{h}</h3><p>{p}</p></article>" for n, (h, p) in enumerate(steps, 1))
    fit_html = "".join(f"<li>{x}</li>" for x in fit)
    body = f"""
      <section class="page-hero"><div class="container">
        <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="services.html">Services</a> / <span>{crumb}</span></nav>
        <p class="eyebrow">{eyebrow}</p>
        <h1>{h1}</h1>
        <p class="hero-lead">{lead}</p>
        <div class="hero-actions"><a class="button button-accent" href="#contact">Get your free audit <span>→</span></a><a class="text-link" href="#included">What's included <span>→</span></a></div>
      </div></section>

      <section class="section"><div class="container split">
        <div class="prose"><p class="lead">{intro_lead}</p>{intro_body}</div>
        <div class="fit-box"><h3>A good fit if you…</h3><ul class="check-list">{fit_html}</ul></div>
      </div></section>

      <section class="section" id="included" style="padding-top:0"><div class="container">
        <div class="section-head"><div><p class="eyebrow">What's included</p><h2>Everything you need,<br /><em>nothing you don't.</em></h2></div><p class="section-intro">Clear deliverables, plain-language reporting and a direct line to the person doing the work.</p></div>
        <div class="feature-grid">{feats}</div>
      </div></section>

      <section class="process section" style="background:var(--paper-dark)"><div class="container">
        <div class="section-head centered"><p class="eyebrow">How it works</p><h2>From audit to <em>results.</em></h2></div>
        <div class="steps">{step_html}</div>
      </div></section>

      {cta_band(*cta)}

      <section class="faq section"><div class="container"><div class="section-head centered"><p class="eyebrow">Questions</p><h2>{crumb} <em>FAQs</em></h2></div><div class="faq-list">{faq_html(faq)}</div></div></section>

      {contact(eyebrow="Free growth audit", title="Let's see where<br /><em>you stand.</em>", intro="Send us a few details and we'll come back to you with a free, no-obligation audit and clear next steps.", preselect=preselect)}"""
    schema = [
        {"@type": "Service", "name": service_name, "serviceType": service_name, "provider": {"@id": BASE + "/#business"},
         "areaServed": {"@type": "City", "name": "Durban"}, "url": f"{BASE}/{file}", "description": desc},
        breadcrumb_schema(crumb, file), faq_schema(faq)]
    urls.append(page(file, title, desc, body, active=active, schema=schema))


service_page(
    "seo-durban.html", "SEO",
    "SEO Durban | Get Your Business on Page One of Google | ZM Results",
    "Local SEO for Durban businesses. We optimise your website and Google Business Profile so customers who are ready to buy find you first. 90-Day Growth Plan from R15 000.",
    "SEO in Durban", "Get on page one.<br /><span>Stay there.</span>",
    "Local SEO for Durban businesses that want more calls, enquiries and walk-ins from people already searching for what they sell.",
    "Most people never scroll past the first page of Google. If you're not there, your competitors get the call.",
    "<p>We make your business easier for Google to understand and easier for customers to choose: a faster, clearer website, a strong Google Business Profile, content that matches what Durban customers actually search for, and steady reputation building.</p><p>Our flagship <a href='/#pricing'>90-Day Google Growth Plan</a> packages all of this for a one-time R15 000.</p>",
    ["Serve customers in Durban or greater eThekwini", "Get most of your work from calls, WhatsApps or walk-ins", "Have a website that isn't bringing in enquiries", "Want growth you own, not just paid clicks"],
    [("⌕", "SEO audit & roadmap", "A full review of your site, rankings and competitors, turned into a prioritised plan."),
     ("◉", "Google Business Profile", "Set up, optimised and kept active so you show up in the map pack and \"near me\" searches."),
     ("⚙", "Website optimisation", "Speed, mobile experience, page titles, structure and technical fixes Google rewards."),
     ("✎", "Keyword & content strategy", "Pages and content built around what your customers actually type into Google."),
     ("★", "Reviews & local trust", "A simple system to earn more Google reviews and consistent local listings."),
     ("↗", "Monthly reporting", "Plain-language reports on rankings, traffic and enquiries — and what we're doing next.")],
    [("Audit", "We benchmark your rankings, site health and competitors."), ("Fix", "We sort out the technical and on-page issues holding you back."),
     ("Build", "We grow your content, profile and local authority."), ("Report", "Monthly updates so you always see progress.")],
    [("How much does SEO cost?", "Our 90-Day Google Growth Plan is a one-time R15 000 and covers the audit, strategy, local SEO, website optimisation, content strategy and monthly reporting. We'll confirm the right scope after your free audit."),
     ("How long until I see results?", "SEO builds momentum over time. Within 90 days we aim to have the foundations in place and rankings moving; competitive industries can take longer. Your free audit will give you an honest picture of your market."),
     ("Can you guarantee the number one spot?", "No honest agency can guarantee a specific Google position, because Google controls the rankings. What we do commit to is doing the work that moves rankings and showing you clearly what's changing."),
     ("Do I need a new website?", "Not usually. Most sites can be improved. If something is seriously holding you back, we'll tell you in the audit.")],
    ("Start with clarity", "Find out what's stopping you ranking.", "Your free audit shows exactly where you stand on Google and the quickest wins available."),
    "SEO & Google rankings", "Search engine optimisation (SEO)", "seo")

service_page(
    "social-media-management-durban.html", "Social media",
    "Social Media Management Durban | Content & Posting | ZM Results",
    "Social media management for Durban businesses: content planning, design, captions, posting and engagement on Facebook, Instagram and more.",
    "Social media management in Durban", "Stay visible.<br /><span>Stay top of mind.</span>",
    "Consistent, on-brand social media that keeps your business in front of local customers — without you having to think about what to post.",
    "Customers check your socials before they call. An empty or outdated page costs you trust.",
    "<p>We plan, create and publish content that shows off your work, answers customer questions and gives people a reason to choose you. You approve the plan; we handle the rest.</p><p>Social works best alongside <a href='seo-durban.html'>SEO</a>: Google brings people to you, and your socials help convince them.</p>",
    ["Know you should post more but never have time", "Have great work that nobody is seeing", "Want a consistent, professional look", "Get enquiries through Facebook, Instagram or WhatsApp"],
    [("◎", "Content plan", "A monthly content calendar built around your services, seasons and promotions."),
     ("✎", "Design & captions", "On-brand graphics and captions written to get people engaging and enquiring."),
     ("⏱", "Scheduling & posting", "Posts go out consistently on the platforms that matter for your business."),
     ("☺", "Community support", "Help staying on top of comments and messages so no enquiry goes cold."),
     ("✦", "Profile clean-up", "Bios, links, contact buttons and highlights set up to convert visitors."),
     ("↗", "Monthly review", "What performed, what didn't, and what we'll do next month.")],
    [("Discover", "We learn your brand, customers and goals."), ("Plan", "You get a monthly content calendar to approve."),
     ("Create & post", "We design, write and publish on schedule."), ("Review", "Monthly results and improvements.")],
    [("Which platforms do you manage?", "Usually Facebook and Instagram, and others like LinkedIn or TikTok where your customers are. We'll recommend the right mix in your audit."),
     ("How much does social media management cost?", "It depends on how many platforms and posts you need. We'll give you a clear monthly quote after your free audit — no long-term contract."),
     ("Do I need to supply photos?", "Photos of your real work, team and premises perform best, so we'll guide you on what to capture. We can also create graphics and use quality stock where it fits."),
     ("Will I approve posts before they go out?", "Yes. You'll see and approve the content plan before anything is published.")],
    ("Start with clarity", "Not sure what to post?", "We'll review your current pages and show you what a consistent, effective month of content looks like."),
    "Social media management", "Social media management", "social")

service_page(
    "google-ads-durban.html", "Google Ads",
    "Google Ads Management Durban | Leads From Paid Search | ZM Results",
    "Google Ads management for Durban businesses. Campaigns built to reach people searching for your services, with conversion tracking and ongoing optimisation.",
    "Google Ads in Durban", "Show up today.<br /><span>Get leads this week.</span>",
    "Google Ads put your business at the top of search results right now — in front of Durban customers already looking for what you offer.",
    "SEO takes time. Google Ads can start bringing enquiries as soon as your campaign is live.",
    "<p>We build tightly targeted campaigns around high-intent searches, write ads that earn the click, and track every call and form so you know exactly what you're getting for your budget.</p><p>Many clients use ads for fast leads while <a href='seo-durban.html'>SEO</a> builds long-term visibility.</p>",
    ["Need enquiries quickly", "Have tried Google Ads and wasted budget", "Want to know exactly which ads bring in leads", "Serve a clear local area"],
    [("↗", "Campaign setup", "Account structure, keywords, locations and schedules built around your best customers."),
     ("✎", "Ad copy", "Clear, compelling ads with the right extensions — call, location and more."),
     ("◎", "Conversion tracking", "Calls, WhatsApps and form submissions tracked so results are measurable."),
     ("⌕", "Negative keywords", "Ongoing filtering so you stop paying for irrelevant clicks."),
     ("⚙", "Landing page guidance", "Recommendations to turn more clicks into enquiries."),
     ("★", "Optimisation & reporting", "Regular bid and budget tuning, with a simple monthly report.")],
    [("Audit", "We review your market, competitors and any past campaigns."), ("Build", "Keywords, ads and tracking set up properly."),
     ("Launch", "Campaigns go live, watched closely from day one."), ("Optimise", "We cut waste and scale what works.")],
    [("How much should I spend on Google Ads?", "It depends on your industry and area. We'll recommend a starting budget in your free audit. Your ad spend is paid directly to Google, separately from our management fee."),
     ("How quickly will I get leads?", "Ads can start showing as soon as the campaign is approved and live. The first few weeks are about learning what converts, then we optimise."),
     ("I tried Google Ads before and it didn't work. Why would this be different?", "The most common causes are broad targeting, missing negative keywords and no conversion tracking. We fix those first, so every rand is accounted for."),
     ("Do you lock me into a contract?", "No long-term contracts. You stay because it's working.")],
    ("Start with clarity", "Stop guessing with your ad budget.", "We'll review your market and show you what a focused Durban campaign could look like."),
    "Google Ads", "Google Ads management", "ads")


service_page(
    "website-design-durban.html", "Website design",
    "Website Design Durban | New Sites & Upgrades | ZM Results",
    "Website design and upgrades for Durban businesses: fast, mobile-friendly sites built to rank on Google and turn visitors into calls and enquiries.",
    "Website design in Durban", "A website that<br /><span>works for you.</span>",
    "New websites and upgrades for Durban businesses: fast, mobile-friendly and built from day one to show up on Google and turn visitors into enquiries.",
    "Most visitors decide within seconds whether to stay, call or leave. Your website should make that decision easy.",
    "<p>We design clear, fast websites that work properly on phones, explain what you do in plain language and make it effortless to call, WhatsApp or send an enquiry. Every site is built with <a href='seo-durban.html'>SEO</a> in mind from the start, so it's ready to rank instead of needing to be fixed later.</p><p>Already have a website? We can upgrade it, improving speed, design, mobile layout and the path to an enquiry, without starting from scratch.</p>",
    ["Don't have a website yet, or aren't proud of your current one", "Get visitors but very few enquiries", "Have a site that's slow or hard to use on a phone", "Want a site you can grow with SEO and Google Ads"],
    [("✎", "Custom design", "A clean, professional design built around your brand, logo and colours, not a generic template."),
     ("☎", "Built to convert", "Clear calls to action, click-to-call and WhatsApp buttons, and enquiry forms that land in your inbox."),
     ("⚙", "Fast & mobile-first", "Lightweight pages that load quickly and work properly on every phone and screen size."),
     ("⌕", "SEO-ready", "Page titles, descriptions, structure and Google Search Console set up correctly from launch."),
     ("◎", "Upgrades & redesigns", "Refresh an existing site with new pages, better speed, a modern design and clearer messaging."),
     ("★", "Ongoing support", "Changes, new pages and updates when you need them, so your site keeps up with your business.")],
    [("Discover", "We learn about your business, customers and goals."), ("Design", "You see and approve the layout and content."),
     ("Build", "We build, test on every device and set up tracking."), ("Launch", "Your site goes live, connected to Google and ready to grow.")],
    [("How long does a new website take?", "It depends on the size of the site and how quickly the content is ready. We'll give you a clear timeline after your free consultation."),
     ("How much does a website cost?", "It depends on how many pages and features you need. We'll give you a clear, fixed quote before any work starts."),
     ("Can you improve my existing website instead of building a new one?", "Yes. Often an upgrade, with better speed, mobile layout, clearer content and stronger calls to action, gets you most of the benefit at a lower cost."),
     ("Will my new website show up on Google?", "We build every site to be search-friendly and connect it to Google Search Console. To rank for competitive searches, most businesses pair their website with our SEO service.")],
    ("Start with clarity", "Is your website costing you customers?", "We'll review your current site, or your plans for one, and show you what to fix first."),
    "Website design", "Website design", "services")

service_page(
    "chatbot-ai-integration-durban.html", "Chatbots & AI",
    "Chatbot & AI Integration Durban | ZM Results",
    "Chatbots and AI assistants for Durban businesses: answer customer questions on your website or WhatsApp and capture leads, even after hours.",
    "Chatbot & AI integration", "Answer every enquiry.<br /><span>Even after hours.</span>",
    "We add chatbots and AI assistants to your website and WhatsApp, so customers get quick answers and you don't miss leads while you're busy or closed.",
    "When a customer can't get a quick answer, many simply move on to the next business.",
    "<p>A well-built chatbot answers common questions straight away (services, hours, areas you cover, how to book) and then collects the customer's details so you can follow up. It doesn't replace you. It makes sure nobody slips through the cracks while you're on a job, in a meeting or asleep.</p><p>We set it up around your real business information, test it carefully, and make it easy for customers to reach a real person. Chatbots work best alongside a strong <a href='website-design-durban.html'>website</a> and <a href='seo-durban.html'>SEO</a> that bring visitors in.</p>",
    ["Get the same customer questions over and over", "Miss enquiries after hours or while you're busy", "Get more WhatsApp messages than you can answer quickly", "Want to capture more leads from the visitors you already get"],
    [("◎", "Website chatbot", "A chat assistant on your website that answers questions and guides visitors to book or enquire."),
     ("☏", "WhatsApp automation", "Instant replies and FAQs for WhatsApp Business, with an easy handover to you."),
     ("✎", "Set up for your business", "Built around your services, hours and policies, so answers are accurate and sound like you."),
     ("☎", "Lead capture", "Collects names, numbers and what the customer needs, and sends them straight to you."),
     ("⚙", "Connected to your tools", "Links with your email, forms or booking system where possible, so leads land where you work."),
     ("★", "Monitoring & improvements", "We review conversations and improve the answers over time.")],
    [("Map", "We list the questions customers ask and what a good answer looks like."), ("Build", "We set up the assistant using information you approve."),
     ("Test", "We test it thoroughly before customers ever see it."), ("Launch & refine", "It goes live, and we keep improving it based on real conversations.")],
    [("Will a chatbot give customers wrong answers?", "We set it up only around information you approve, test it before launch, and configure it to hand over to you when it isn't sure instead of guessing."),
     ("Can it work on WhatsApp?", "Yes. We can set up automated replies and FAQs for WhatsApp Business, with an easy way for customers to reach you directly."),
     ("What about customers' personal information?", "We set chatbots up to collect only what you need to follow up, and help you handle that information in line with POPIA."),
     ("How much does it cost?", "It depends on where it runs (website, WhatsApp or both) and how much it needs to do. We'll give you a clear quote after a free consultation.")],
    ("Start with clarity", "How many enquiries are you missing?", "We'll look at how customers contact you now and show you where a chatbot could help."),
    "Chatbot & AI integration", "Chatbot and AI integration", "services")


# ---------------- SERVICES HUB ----------------
hub = f"""
      <section class="page-hero"><div class="container">
        <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <span>Services</span></nav>
        <p class="eyebrow">Services</p>
        <h1>Marketing that<br /><span>moves business.</span></h1>
        <p class="hero-lead">From page-one SEO and high-intent Google Ads to websites that convert and chatbots that answer after hours, we help Durban businesses get seen and chosen by the right customers.</p>
      </div></section>
      <section class="section"><div class="container"><div class="service-detail-grid">
        <article><span class="service-icon">⌕</span><p class="eyebrow">01 · Search</p><h2>SEO &amp; Google rankings</h2><p>Keyword research, technical improvements, local SEO, Google Business Profile optimisation and conversion-focused content.</p><ul class="check-list"><li>SEO audit and roadmap</li><li>Local search optimisation</li><li>Google Business Profile growth</li><li>Monthly progress reporting</li></ul><a class="button button-dark" href="seo-durban.html">Explore SEO <span>→</span></a></article>
        <article><span class="service-icon">◎</span><p class="eyebrow">02 · Social</p><h2>Social media management</h2><p>A consistent social presence designed around your brand, audience and business goals.</p><ul class="check-list"><li>Content planning and captions</li><li>Design and posting</li><li>Community engagement support</li><li>Monthly performance review</li></ul><a class="button button-dark" href="social-media-management-durban.html">Explore social media <span>→</span></a></article>
        <article><span class="service-icon">↗</span><p class="eyebrow">03 · Paid growth</p><h2>Google Ads</h2><p>Reach people already searching for your services with structured campaigns, clear targeting and ongoing optimisation.</p><ul class="check-list"><li>Campaign setup and targeting</li><li>Ad copy and landing page guidance</li><li>Conversion tracking</li><li>Budget optimisation</li></ul><a class="button button-dark" href="google-ads-durban.html">Explore Google Ads <span>→</span></a></article>
        <article><span class="service-icon">✎</span><p class="eyebrow">04 · Websites</p><h2>Website design</h2><p>Fast, mobile-friendly websites and upgrades, built to rank on Google and turn visitors into enquiries.</p><ul class="check-list"><li>Custom design for your brand</li><li>Click-to-call, WhatsApp and enquiry forms</li><li>SEO-ready from launch</li><li>Upgrades for existing sites</li></ul><a class="button button-dark" href="website-design-durban.html">Explore website design <span>→</span></a></article>
        <article><span class="service-icon">◎</span><p class="eyebrow">05 · Automation</p><h2>Chatbots &amp; AI</h2><p>Chat assistants for your website and WhatsApp that answer common questions and capture leads, even after hours.</p><ul class="check-list"><li>Website chatbot</li><li>WhatsApp automation</li><li>Lead capture to your inbox</li><li>Ongoing improvements</li></ul><a class="button button-dark" href="chatbot-ai-integration-durban.html">Explore chatbots &amp; AI <span>→</span></a></article>
      </div></div></section>
      {cta_band("Start with clarity", "Not sure what your business needs?", "Book a free growth audit and we'll identify the best opportunities for your business.")}
      {contact(eyebrow="Let's talk", title="Ready to get<br /><em>more visible?</em>", intro="Contact ZM Results in Durban and let's plan your next growth move.", preselect="Everything / not sure yet")}"""
urls.append(page("services.html", "Marketing Services Durban | ZM Results",
                 "Explore ZM Results services in Durban: SEO and Google rankings, social media management and Google Ads management.",
                 hub, active="services", schema=[breadcrumb_schema("Services", "services.html")]))

# ---------------- CONTACT / QUERIES ----------------
query_topics = ["General question", "SEO & Google rankings", "Social media management", "Google Ads",
                "90-Day Google Growth Plan", "Pricing / quote", "Existing client support", "Something else"]
topic_opts = "".join(f"<option>{html.escape(t)}</option>" for t in query_topics)
contact_page = f"""
      <section class="page-hero"><div class="container">
        <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <span>Contact</span></nav>
        <p class="eyebrow">Contact us</p>
        <h1>Got a question?<br /><span>We're here to help.</span></h1>
        <p class="hero-lead">Send us your query using the form below and we'll get back to you as soon as possible. Prefer to chat? WhatsApp or call us on {PHONE_DISPLAY}.</p>
      </div></section>

      <section class="contact section" id="contact">
        <div class="container contact-grid">
          <div>
            <p class="eyebrow">Get in touch</p>
            <h2>Send us<br /><em>your query.</em></h2>
            <p>Whether it's a quick question, a quote, or help with an existing project, tell us what you need and we'll be in contact with you soon.</p>
            <div class="contact-links">
              <a class="whatsapp-link" href="{WA}" target="_blank" rel="noopener">☏ WhatsApp {PHONE_DISPLAY}</a>
              <a href="tel:{PHONE_TEL}">☎ Call {PHONE_DISPLAY}</a>
              <a href="mailto:{EMAIL}">✉ {EMAIL}</a>
              <a href="{REVIEW_URL}" target="_blank" rel="noopener">★ Leave us a Google review</a>
            </div>
          </div>
          <form class="contact-form" data-form="query" action="https://formsubmit.co/{FORM_EMAIL}" method="POST" novalidate>
            <input type="hidden" name="_next" value="{BASE}/thank-you.html" />
            <input type="hidden" name="_subject" value="New website query" />
            <input type="hidden" name="_captcha" value="false" />
            <label class="hp" aria-hidden="true">Leave this empty<input name="company_url" type="text" tabindex="-1" autocomplete="off" /></label>
            <label>Your name<input name="name" type="text" autocomplete="name" required maxlength="100" /></label>
            <label><span>Business name <span class="optional">(optional)</span></span><input name="business_name" type="text" autocomplete="organization" maxlength="120" /></label>
            <label>Email<input name="email" type="email" autocomplete="email" required maxlength="160" /></label>
            <label>Phone number<input name="phone" type="tel" autocomplete="tel" required maxlength="30" inputmode="tel" /></label>
            <label class="full">What is your query about?<select name="service">{topic_opts}</select></label>
            <label class="full">Your message<textarea name="message" required maxlength="2000" rows="6" placeholder="Tell us how we can help…"></textarea></label>
            <p class="form-status" role="alert"></p>
            <button class="button button-dark" type="submit">Send my query <span>→</span></button>
            <p class="form-note">We'll only use your details to respond to your query.</p>
          </form>
        </div>
      </section>"""
urls.append(page("contact.html", "Contact Us | ZM Results Digital Marketing Durban",
                 "Contact ZM Results in Durban. Send us your question about SEO, social media or Google Ads and we'll be in contact with you soon.",
                 contact_page, active="contact", schema=[breadcrumb_schema("Contact", "contact.html"),
                 {"@type": "ContactPage", "url": BASE + "/contact.html", "about": {"@id": BASE + "/#business"}}]))

# ---------------- THANK YOU ----------------
thanks = f"""
      <section class="thanks"><div class="container">
        <div class="badge">✓</div>
        <p class="eyebrow" style="justify-content:center">Message received</p>
        <h1>Thank you!</h1>
        <p>We have received your message and we will be in contact with you soon. Need an answer faster? Send us a quick WhatsApp.</p>
        <div class="hero-actions"><a class="button button-accent" href="{WA}" target="_blank" rel="noopener">WhatsApp {PHONE_DISPLAY} <span>→</span></a><a class="text-link" href="/">Back to home <span>→</span></a></div>
      </div></section>"""
page("thank-you.html", "Thank you | ZM Results", "Thanks for contacting ZM Results. We will be in contact with you soon.", thanks, noindex=True)
# thank-you page has no contact form, so its header CTA should go home
tp = SITE / "thank-you.html"
tp.write_text(tp.read_text().replace('href="#contact">Get your free audit', 'href="/#contact">Get your free audit'))

# ---------------- AREA PAGES ----------------
AREAS = [
    {
        "slug": "marketing-agency-umhlanga.html", "town": "Umhlanga", "nav": "Umhlanga",
        "title": "Marketing Agency Umhlanga | SEO & Google Ads | ZM Results",
        "desc": "Digital marketing for Umhlanga businesses. SEO, Google Business Profile, social media and Google Ads from ZM Results, just down the road in Durban.",
        "h1": "Marketing agency<br /><span>for Umhlanga.</span>",
        "lead": "Umhlanga is one of the most competitive places in KwaZulu-Natal to win customers online. We help Umhlanga businesses stand out on Google and social media.",
        "intro_lead": "In Umhlanga, your customers have plenty of choice — and they make it on their phones.",
        "intro": [
            "Between Umhlanga Ridge's office parks, the restaurants and shops around Gateway and the Village, and the holiday apartments along the beachfront, Umhlanga is packed with businesses chasing the same customers. Many of those customers are visitors, new residents or professionals working in the area who don't yet know who to trust, so they search Google, compare reviews and pick from the first few results.",
            "That's why visibility matters more here than almost anywhere else in Durban. We focus on getting your business into Google's map results for Umhlanga searches, making your website convert busy, mobile-first visitors, and keeping your social media looking as polished as your competitors'.",
        ],
        "who": ["Professional services in Umhlanga Ridge — attorneys, accountants, financial advisors, consultants",
                "Restaurants, cafés, salons and wellness studios competing for foot traffic",
                "Property, short-stay and hospitality businesses that rely on visitors finding them",
                "Medical and dental practices that need patients to choose them online"],
        "cards": [
            ("◉", "Win the Umhlanga map pack", "We optimise your Google Business Profile so you show up when people search for your service in Umhlanga — on Google Search and Google Maps."),
            ("★", "Stand out on reviews", "In a crowded area, reviews are often the tie-breaker. We help you build a steady flow of genuine Google reviews from happy customers."),
            ("↗", "Reach professionals and visitors", "Targeted Google Ads put you in front of people searching right now, including visitors who are new to the area."),
        ],
        "faq": [
            ("Do you have an office in Umhlanga?", "We're based in Durban and work with Umhlanga businesses remotely and in person. Umhlanga is a short drive away, so we can meet you at your business when it helps."),
            ("Umhlanga is very competitive online. Can a small business still rank?", "Yes. Google's map results for local searches favour businesses that are relevant, close to the searcher and well reviewed. A complete, active Google Business Profile with genuine reviews can compete with much bigger brands for local searches."),
            ("Should an Umhlanga business focus on SEO or Google Ads?", "Often both. Ads bring enquiries quickly in a competitive area, while SEO builds visibility you don't pay for per click. We'll recommend the right mix for your budget in your free audit."),
        ],
    },
    {
        "slug": "marketing-agency-ballito.html", "town": "Ballito", "nav": "Ballito",
        "title": "Marketing Agency Ballito | SEO & Google Ads | ZM Results",
        "desc": "Digital marketing for Ballito and Dolphin Coast businesses: local SEO, Google Business Profile, social media management and Google Ads from ZM Results.",
        "h1": "Marketing agency<br /><span>for Ballito.</span>",
        "lead": "From holiday-season peaks to a fast-growing year-round community, Ballito businesses need to be found by both locals and visitors. We help you do both.",
        "intro_lead": "Ballito has two audiences: the people who live here, and the people who visit.",
        "intro": [
            "Ballito and the wider Dolphin Coast have grown quickly, with new residential estates, shopping centres and businesses opening every year, while still welcoming thousands of holidaymakers in peak season. That means your marketing has to work for a resident looking for a reliable local service and for a visitor who has just arrived and searches \"near me\".",
            "We help Ballito businesses show up in Google Maps for both groups, plan social media around the season so you're visible before the holiday rush, and run Google Ads that can be scaled up when visitor numbers peak and scaled back when they drop.",
        ],
        "who": ["Restaurants, coffee shops and beach-side businesses that depend on visitors",
                "Holiday rentals, guesthouses and tourism and activity operators",
                "Home services serving the estates — builders, electricians, pool and garden services",
                "Retailers, gyms, salons and practices serving the growing local community"],
        "cards": [
            ("◉", "Be found by visitors", "People on holiday search \"near me\" on their phones. We make sure your Google Business Profile, photos and hours are ready for them."),
            ("◎", "Seasonal social media", "We plan your content around school holidays and the festive season so you're top of mind before the rush starts."),
            ("↗", "Ads that flex with the season", "Google Ads budgets can rise in peak season and drop in quiet months, so you only spend when the customers are there."),
        ],
        "faq": [
            ("Do you work with businesses outside Ballito on the North Coast?", "Yes. We work with businesses across the Dolphin Coast and north of Durban, including Salt Rock, Shaka's Rock and Zimbali, as well as greater Durban."),
            ("How do I get more visitors to find my Ballito business on Google?", "Start with a complete, verified Google Business Profile: the right category, accurate hours (including holiday hours), good photos and genuine reviews. Visitors rely heavily on Google Maps when they're somewhere new."),
            ("When should a Ballito business start marketing for the holiday season?", "Ideally several weeks before. SEO and reviews take time to build, and social media works best when people already recognise you by the time they arrive."),
        ],
    },
    {
        "slug": "marketing-agency-pinetown.html", "town": "Pinetown", "nav": "Pinetown",
        "title": "Marketing Agency Pinetown | SEO & Google Ads | ZM Results",
        "desc": "Digital marketing for Pinetown businesses, from trades and manufacturers to retailers. Local SEO, Google Ads and social media from ZM Results in Durban.",
        "h1": "Marketing agency<br /><span>for Pinetown.</span>",
        "lead": "Pinetown runs on practical businesses — trades, manufacturers, suppliers and family-run shops. We help them get more calls and quotes from Google.",
        "intro_lead": "When a Pinetown customer needs a supplier or a tradesperson, they search Google and call the first business that looks reliable.",
        "intro": [
            "Pinetown and the surrounding areas, including Westmead and New Germany, are home to a large mix of industrial, trade and service businesses, alongside a busy retail centre serving the Upper Highway and outer-west suburbs. For many of these businesses, a single new contract or regular customer from Google is worth far more than the cost of marketing.",
            "Our approach for Pinetown is straightforward: make sure you appear when people search for your service in the area, make it easy for them to call or WhatsApp you, and track which enquiries actually came from your marketing.",
        ],
        "who": ["Trades and home services — plumbers, electricians, builders, solar and security installers",
                "Manufacturers, engineering firms and industrial suppliers looking for B2B leads",
                "Auto services — panel beaters, mechanics, tyre and parts suppliers",
                "Retailers and family businesses serving Pinetown and the outer-west suburbs"],
        "cards": [
            ("☎", "More calls, not just clicks", "We set up your website and Google profile so the most important action — calling or WhatsApping you — is one tap away."),
            ("⌕", "Rank for what you actually do", "We target the specific searches your customers use, like your service plus \"Pinetown\", instead of vague keywords that never convert."),
            ("◎", "Track every lead", "Call and form tracking show you which marketing brings in real enquiries, so you know your money is working."),
        ],
        "faq": [
            ("Can SEO work for industrial and B2B businesses in Pinetown?", "Yes. Buyers and procurement teams search Google for suppliers too. Clear service pages, a complete Google Business Profile and listings on relevant directories help them find you."),
            ("I'm a tradesperson without a proper website. Can you still help?", "Absolutely. A well-run Google Business Profile can bring in calls on its own, and we can advise on a simple website when you're ready."),
            ("Do you cover areas around Pinetown?", "Yes, including Westmead, New Germany, Kloof, Hillcrest, Queensburgh and the rest of greater Durban."),
        ],
    },
    {
        "slug": "marketing-agency-pietermaritzburg.html", "town": "Pietermaritzburg", "nav": "Pietermaritzburg",
        "title": "Marketing Agency Pietermaritzburg | ZM Results",
        "desc": "Digital marketing for Pietermaritzburg and Midlands businesses: local SEO, Google Business Profile, social media management and Google Ads from ZM Results.",
        "h1": "Marketing agency<br /><span>for Pietermaritzburg.</span>",
        "lead": "We help Pietermaritzburg and Midlands businesses get found on Google, build trust on social media and turn searches into customers.",
        "intro_lead": "Pietermaritzburg customers are loyal — once they find a business they trust. The challenge is being found first.",
        "intro": [
            "As the capital of KwaZulu-Natal and a university city, Pietermaritzburg has a steady mix of government employees, students, families and professionals, plus businesses serving the wider Midlands. Many local businesses still rely mainly on word of mouth, which means a strong Google presence can quickly set you apart.",
            "We help Pietermaritzburg businesses show up for local searches, keep their Google Business Profile and social media active, and use Google Ads to reach people across the city and Midlands without paying for clicks from people too far away to become customers.",
        ],
        "who": ["Practices and professional services — medical, dental, legal and accounting",
                "Schools, tutors, training providers and businesses serving students",
                "Restaurants, retail and services in the city and surrounding suburbs",
                "Midlands tourism, hospitality and venue businesses"],
        "cards": [
            ("◉", "Own your local listing", "A complete, verified Google Business Profile makes you the obvious choice when someone in Pietermaritzburg searches for your service."),
            ("✎", "Content that builds trust", "Helpful posts and social content show local customers who you are before they ever call."),
            ("↗", "Targeted Google Ads", "Ads targeted to Pietermaritzburg and the Midlands so your budget is spent on people who can actually become customers."),
        ],
        "faq": [
            ("Can a Durban-based agency help a Pietermaritzburg business?", "Yes. Most local SEO and digital marketing work is done online, and Pietermaritzburg is close enough for in-person meetings when they're useful."),
            ("Do you work with businesses in the Midlands as well?", "Yes, including Howick, Hilton and the Midlands Meander area. Google Ads and your Google Business Profile service area can be set up to cover exactly where your customers are."),
            ("My business relies on word of mouth. Do I still need Google?", "Even referred customers usually look you up before they call. A strong Google profile with good reviews turns those referrals into confident customers, and brings in new ones too."),
        ],
    },
]


def area_page(a):
    others = [x for x in AREAS if x is not a]
    who = "".join(f"<li>{w}</li>" for w in a["who"])
    cards = "".join(f'<article><span class="service-icon">{i}</span><h3>{h}</h3><p>{p}</p></article>' for i, h, p in a["cards"])
    intro = "".join(f"<p>{p}</p>" for p in a["intro"])
    other_links = " · ".join(f'<a href="{o["slug"]}">{o["town"]}</a>' for o in others)
    body = f"""
      <section class="page-hero"><div class="container">
        <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <span>Areas</span> / <span>{a["town"]}</span></nav>
        <p class="eyebrow">Digital marketing in {a["town"]}</p>
        <h1>{a["h1"]}</h1>
        <p class="hero-lead">{a["lead"]}</p>
        <div class="hero-actions"><a class="button button-accent" href="#contact">Get your free audit <span>→</span></a><a class="text-link" href="#how">How we help <span>→</span></a></div>
      </div></section>

      <section class="section"><div class="container split">
        <div class="prose"><p class="lead">{a["intro_lead"]}</p>{intro}</div>
        <div class="fit-box"><h3>Who we help in {a["town"]}</h3><ul class="check-list">{who}</ul></div>
      </div></section>

      <section class="section" id="how" style="padding-top:0"><div class="container">
        <div class="section-head"><div><p class="eyebrow">How we help</p><h2>Get found in<br /><em>{a["town"]}.</em></h2></div><p class="section-intro">The same proven services we offer across Durban, focused on the customers in your area.</p></div>
        <div class="feature-grid">{cards}</div>
      </div></section>

      <section class="section" style="background:var(--paper-dark)"><div class="container">
        <div class="section-head centered"><p class="eyebrow">Our services</p><h2>Everything you need<br /><em>to grow locally.</em></h2></div>
        <div class="service-grid">
          <article class="service-card featured"><span class="service-icon">⌕</span><h3>SEO &amp; Google Maps</h3><p>Rank higher in Google search and the map results for {a["town"]} searches.</p><a href="seo-durban.html">Explore SEO <span>→</span></a></article>
          <article class="service-card"><span class="service-icon">◎</span><h3>Social media</h3><p>Consistent, on-brand content that keeps local customers engaged.</p><a href="social-media-management-durban.html">Explore social media <span>→</span></a></article>
          <article class="service-card"><span class="service-icon">↗</span><h3>Google Ads</h3><p>Campaigns targeted to {a["town"]} so your budget reaches real local customers.</p><a href="google-ads-durban.html">Explore Google Ads <span>→</span></a></article>
        </div>
        <p class="note" style="text-align:center;margin-top:34px">Also serving: <a href="/">Durban</a> · {other_links}</p>
      </div></section>

      <section class="faq section"><div class="container"><div class="section-head centered"><p class="eyebrow">Questions</p><h2>{a["town"]} <em>FAQs</em></h2></div><div class="faq-list">{faq_html(a["faq"])}</div></div></section>

      {contact(eyebrow="Free growth audit", title=f"Let's grow your<br /><em>{a['town']} business.</em>", intro=f"Tell us about your business and we'll send you a free audit showing how you currently appear on Google in {a['town']} and where the biggest opportunities are.", preselect="Everything / not sure yet")}"""
    schema = [
        {"@type": "Service", "name": f"Digital marketing in {a['town']}", "serviceType": "Digital marketing agency",
         "provider": {"@id": BASE + "/#business"}, "areaServed": {"@type": "City", "name": a["town"]},
         "url": f"{BASE}/{a['slug']}", "description": a["desc"]},
        breadcrumb_schema(a["town"], a["slug"]), faq_schema(a["faq"])]
    urls.append(page(a["slug"], a["title"], a["desc"], body, schema=schema))


for a in AREAS:
    area_page(a)


# ---------------- BLOG ----------------
PUBLISHED = "2026-11-11"  # date of the first three posts; new posts set their own "date"
POSTS = [
    {
        "slug": "google-business-profile-guide.html",
        "title": "How to Set Up and Optimise Your Google Business Profile",
        "seo_title": "Google Business Profile Guide for Durban Businesses | ZM Results",
        "desc": "A step-by-step guide to setting up and optimising your free Google Business Profile so more local customers find you on Google Search and Maps.",
        "excerpt": "Your free Google Business Profile is the single biggest factor in showing up for \"near me\" searches. Here's how to set it up properly.",
        "date": "2026-11-11",
        "read": "6 min read",
        "body": """
<p>When someone searches for a business like yours "near me" or "in Durban", Google usually shows a map with three businesses before any normal website results. Those businesses come from <strong>Google Business Profile</strong>, a free listing that every local business should have. If yours is missing, incomplete or unverified, you're giving those spots to your competitors.</p>
<h2>1. Claim and verify your profile</h2>
<p>Go to <strong>business.google.com</strong> and search for your business name. If a listing already exists, claim it. If not, create one. Google will ask you to verify that you own the business. Depending on your business, this can be by video, phone, email or postcard. <strong>Unverified profiles rarely rank well</strong>, so don't skip this step.</p>
<h2>2. Get the basics exactly right</h2>
<ul>
<li><strong>Business name:</strong> use your real-world name only. Adding keywords like "Best Plumber Durban" to your name breaks Google's guidelines and can get your profile suspended.</li>
<li><strong>Primary category:</strong> this matters more than almost anything else. Choose the most specific category that describes your main service, then add a few relevant secondary categories.</li>
<li><strong>Address or service area:</strong> if customers visit you, show your address. If you travel to customers (like most trades), hide your address and set the areas you serve instead.</li>
<li><strong>Phone, website and hours:</strong> make sure they match your website exactly, and remember to update holiday hours.</li>
</ul>
<h2>3. Fill in every section</h2>
<p>Write a clear description of what you do and where. Add your services or products with short descriptions. Answer the common questions customers ask. Profiles that are complete give Google more information to match you with the right searches.</p>
<h2>4. Add real photos, regularly</h2>
<p>Upload your logo, a cover photo, and real photos of your premises, team and work. Customers want to see who they're dealing with. Adding new photos over time also shows Google that your business is active.</p>
<h2>5. Build a steady flow of reviews</h2>
<p>Reviews influence both your ranking and whether people choose you. Ask every happy customer for a review and reply to every review, good or bad. We cover how to do this the right way in <a href="how-to-get-more-google-reviews.html">How to Get More Google Reviews</a>.</p>
<h2>6. Post updates</h2>
<p>Use the Updates feature to share news, offers, tips and recent work. A short post every week or two keeps your profile fresh and gives customers another reason to contact you.</p>
<h2>7. Keep your details consistent everywhere</h2>
<p>Your business name, address and phone number should be identical on your website, Facebook page and directories like Yellow Pages SA, Brabys and Cylex. Inconsistent details confuse Google and can hold your ranking back.</p>
<h2>The bottom line</h2>
<p>A well-run Google Business Profile is free and is often the fastest way for a local business to get more calls. If you'd like us to check yours, <a href="#contact">request a free growth audit</a> and we'll show you exactly what to improve.</p>""",
    },
    {
        "slug": "how-to-get-more-google-reviews.html",
        "title": "How to Get More Google Reviews (Without Breaking the Rules)",
        "seo_title": "How to Get More Google Reviews for Your Business | ZM Results",
        "desc": "Practical, rule-friendly ways for South African small businesses to get more genuine Google reviews and use them to win more customers.",
        "excerpt": "Reviews help you rank in Google Maps and help customers choose you. Here's how to get more of them, the right way.",
        "date": "2026-11-11",
        "read": "5 min read",
        "body": """
<p>Google reviews do two jobs at once. They're one of the factors Google uses to decide which local businesses to show, and they're often the deciding factor when a customer compares you with a competitor. Yet most happy customers never leave a review simply because nobody asked them.</p>
<h2>1. Ask at the right moment</h2>
<p>The best time to ask is right after a customer tells you they're happy: when you finish a job, deliver an order or receive a thank-you message. A quick, personal "Would you mind leaving us a Google review? It really helps a small business like ours" works far better than a generic request weeks later.</p>
<h2>2. Make it one tap</h2>
<p>In your Google Business Profile, find the option to <strong>ask for reviews</strong> and copy your review link. Save it somewhere handy and send it on WhatsApp, in your email signature and on your invoices. You can also turn it into a QR code for your counter, vehicle or business card.</p>
<h2>3. Make it part of your routine</h2>
<p>Reviews work best as a steady flow rather than a sudden burst. Build the request into your normal process, for example a WhatsApp message template you send after every completed job.</p>
<h2>4. Reply to every review</h2>
<p>Thank people for positive reviews, ideally mentioning the service they used. For negative reviews, stay calm, acknowledge the issue and offer to resolve it offline. Future customers read your replies, and a professional response to a complaint can build more trust than a perfect score.</p>
<h2>5. What not to do</h2>
<ul>
<li><strong>Don't offer discounts or gifts in exchange for reviews.</strong> Google's policies prohibit incentivised reviews.</li>
<li><strong>Don't write reviews yourself</strong> or ask staff, friends or family to pose as customers.</li>
<li><strong>Don't only ask customers you think will be positive</strong> (sometimes called "review gating"). Google's guidelines prohibit selectively soliciting positive reviews.</li>
<li><strong>Don't buy reviews.</strong> Fake reviews can be removed and can put your profile at risk.</li>
</ul>
<h2>6. Show your reviews off</h2>
<p>Share your best reviews on social media and mention your rating on your website. Social proof works everywhere, not just on Google.</p>
<h2>Need help?</h2>
<p>Building a reliable review system is part of every SEO project we run. <a href="#contact">Get a free growth audit</a> and we'll show you how your reviews compare with your local competitors. You might also like our <a href="google-business-profile-guide.html">Google Business Profile guide</a>.</p>""",
    },
    {
        "slug": "seo-vs-google-ads.html",
        "title": "SEO vs Google Ads: Which Should Your Small Business Start With?",
        "seo_title": "SEO vs Google Ads for Small Businesses in South Africa | ZM Results",
        "desc": "SEO or Google Ads? A plain-language comparison of cost, speed and long-term value to help South African small businesses decide where to start.",
        "excerpt": "Both put your business on Google, but they work very differently. Here's how to decide where to spend first.",
        "date": "2026-11-11",
        "read": "5 min read",
        "body": """
<p>"Should I do SEO or Google Ads?" is one of the most common questions we hear from small business owners. Both can put you in front of people searching for what you sell, but they work in very different ways.</p>
<h2>How they differ</h2>
<ul>
<li><strong>Google Ads</strong> are paid listings marked "Sponsored". You pay each time someone clicks. They can start bringing traffic as soon as your campaign is approved, and they stop when you stop paying.</li>
<li><strong>SEO</strong> (search engine optimisation) is about earning the normal, unpaid results and the map listings. You don't pay per click, but it takes time and ongoing work to build.</li>
</ul>
<h2>Choose Google Ads first if…</h2>
<ul>
<li>You need enquiries quickly, for example you've just opened or have a quiet month ahead.</li>
<li>You want to test which services or areas bring in the best customers.</li>
<li>Your service has a high value per customer, so a click can easily pay for itself.</li>
<li>You have a budget for ad spend each month, separate from management fees.</li>
</ul>
<h2>Choose SEO first if…</h2>
<ul>
<li>You want a steady flow of enquiries that doesn't stop the moment you stop paying.</li>
<li>Your customers mostly search locally, for example "plumber near me" or "accountant in Durban". Here, your Google Business Profile and reviews can make a big difference.</li>
<li>You're building a business for the long term and want an asset you own.</li>
</ul>
<h2>Why the best answer is often both</h2>
<p>Many businesses use Google Ads to bring in enquiries now while SEO builds momentum in the background. Over time, as your unpaid rankings improve, you can rely less on ads, or keep them running for your most profitable services.</p>
<h2>Avoid the common mistakes</h2>
<ul>
<li><strong>Ads:</strong> targeting keywords that are too broad, forgetting negative keywords (like "jobs" or "free") and not tracking which clicks turn into calls.</li>
<li><strong>SEO:</strong> ignoring your Google Business Profile, expecting overnight results, and choosing keywords nobody actually searches for.</li>
</ul>
<h2>Not sure where to start?</h2>
<p>We'll look at your market, your competitors and your budget and give you an honest recommendation. <a href="#contact">Request a free growth audit</a>, or read more about our <a href="seo-durban.html">SEO</a> and <a href="google-ads-durban.html">Google Ads</a> services.</p>""",
    },
    {
        "slug": "how-much-does-seo-cost-south-africa.html",
        "title": "How Much Does SEO Cost in South Africa?",
        "seo_title": "How Much Does SEO Cost in South Africa? | ZM Results",
        "desc": "What affects the price of SEO in South Africa, the common pricing models, what you should get for your money, and the red flags to avoid.",
        "excerpt": "There's no single price for SEO, but there are clear things that drive the cost. Here's how to judge a quote before you sign.",
        "date": "2026-11-14",
        "read": "3 min read",
        "body": """
<p>Ask five agencies what SEO costs and you'll probably get five very different answers. That's confusing when you're trying to budget, but it isn't because everyone is making it up. The price depends on what your business needs, how competitive your market is and how much work is actually included. This guide explains what drives the cost, so you can compare quotes properly and spot the ones to avoid.</p>
<h2>Why there's no single price for SEO</h2>
<p>SEO (search engine optimisation) is the work that helps your business show up in Google's normal results and map listings when people search for what you sell. Unlike an advert, it isn't one product with a fixed price. A plumber in one suburb and an online shop selling nationwide need very different amounts of work to reach page one.</p>
<h2>What affects the cost</h2>
<ul>
<li><strong>Competition:</strong> ranking for "dentist Durban" takes more work than ranking for a niche service in a small town, because more businesses are fighting for the same spots.</li>
<li><strong>Where you want to rank:</strong> local SEO for one city is usually more affordable than trying to rank across all of South Africa.</li>
<li><strong>The state of your website:</strong> a slow, outdated or badly built site needs fixing before content and links can do their job.</li>
<li><strong>Your Google Business Profile:</strong> if it's missing, unverified or incomplete, setting it up properly is part of the work.</li>
<li><strong>Content needs:</strong> new service pages, area pages and blog posts take time to research and write well.</li>
<li><strong>How much is done for you:</strong> a report full of recommendations costs less than someone actually carrying them out.</li>
</ul>
<h2>The common ways SEO is priced</h2>
<ul>
<li><strong>Monthly retainer:</strong> you pay every month for ongoing work. Good for competitive markets where you need continuous effort.</li>
<li><strong>Once-off package or project:</strong> a fixed price for a defined scope, such as an audit plus a set period of work. Easier to budget for, and you know exactly what you're getting.</li>
<li><strong>Hourly or consulting:</strong> you pay for advice and do the work yourself or in-house.</li>
</ul>
<p>None of these is automatically better. What matters is that the scope is clear and you can see what was done.</p>
<h2>What you should get for your money</h2>
<p>Whatever the price, a proper SEO service should include:</p>
<ul>
<li>An audit of where you stand now, including your competitors</li>
<li>A clear plan with the keywords and pages that matter for your business</li>
<li>Google Business Profile optimisation, if you serve local customers</li>
<li>Fixes to your website's speed, structure, titles and content</li>
<li>Regular reporting in plain language, showing what was done and what's changing</li>
<li>Your business keeping ownership of its website, Google profile and Search Console</li>
</ul>
<h2>Red flags to watch out for</h2>
<ul>
<li><strong>Guaranteed number one rankings.</strong> Nobody controls Google, so nobody can honestly guarantee a position.</li>
<li><strong>Packages of hundreds or thousands of backlinks.</strong> Cheap bulk links can do more harm than good.</li>
<li><strong>No reporting, or reports you can't understand.</strong> You should always know what you're paying for.</li>
<li><strong>Long lock-in contracts</strong> with no way out if nothing improves.</li>
<li><strong>The agency owning your accounts.</strong> If you leave, you should keep your website and Google profile.</li>
</ul>
<h2>Questions to ask before you sign</h2>
<ul>
<li>What exactly will you do in the first month?</li>
<li>Which searches are you targeting, and why?</li>
<li>How will you report on progress, and how often?</li>
<li>Who owns the website, Google profile and analytics accounts?</li>
<li>What happens if I want to stop?</li>
</ul>
<h2>How we price SEO</h2>
<p>We keep it simple. Our <a href="seo-durban.html">90-Day Google Growth Plan</a> is a <strong>once-off R15 000</strong> package for local businesses. It covers a full SEO audit and strategy, local SEO and Google Business Profile optimisation, website optimisation, a content and keyword strategy, and monthly reporting and support. There's no long-term contract, and you own everything we set up.</p>
<p>If your business needs something different, we'll tell you honestly after a free audit. You might also find our guide on <a href="seo-vs-google-ads.html">SEO vs Google Ads</a> useful when deciding where to start.</p>
<p>Want to know what it would take for your business to reach page one? <a href="#contact">Request a free growth audit</a> and we'll show you where you stand.</p>""",
    },
    {
        "slug": "how-much-does-a-website-cost-south-africa.html",
        "title": "How Much Does a Website Cost in South Africa?",
        "seo_title": "How Much Does a Website Cost in South Africa? | ZM Results",
        "desc": "What affects website prices in South Africa, the ongoing costs people forget, and how to get a site that actually brings in enquiries.",
        "excerpt": "Website quotes can vary hugely. Here's what you're really paying for, the costs people forget, and what every small-business site needs.",
        "date": "2026-11-14",
        "read": "3 min read",
        "body": """
<p>One designer quotes you a small amount, another quotes many times more, and a website builder advert says you can do it yourself for almost nothing. So what should a website actually cost? The honest answer is that it depends on what the site needs to do for your business. This guide explains what you're paying for, the ongoing costs that catch people out, and how to make sure your money buys a website that brings in customers, not just one that looks nice.</p>
<h2>Why website prices vary so much</h2>
<p>A website can be anything from a single page with your phone number to an online shop with hundreds of products and a booking system. Two quotes that look wildly different are often for very different things. Before comparing prices, compare exactly what's included.</p>
<h2>What affects the price</h2>
<ul>
<li><strong>Number of pages:</strong> a home page, services, about and contact page is very different from a site with separate pages for every service and area.</li>
<li><strong>Custom design or template:</strong> a design built around your brand takes more work than adjusting a ready-made template.</li>
<li><strong>Features:</strong> online booking, e-commerce, payment, client logins or a <a href="chatbot-ai-integration-durban.html">chatbot</a> all add work.</li>
<li><strong>Content:</strong> who writes the text and supplies the photos? Professional copywriting and photography add cost but make a big difference.</li>
<li><strong>SEO setup:</strong> a site built properly for Google, with good page titles, structure, speed and Search Console set up, saves you money later.</li>
<li><strong>Training and handover:</strong> whether you'll be able to make simple changes yourself.</li>
</ul>
<h2>The ongoing costs people forget</h2>
<p>The build is only part of the cost. Make sure you know who pays for these, and how much, every year:</p>
<ul>
<li><strong>Domain name</strong> (like yourbusiness.co.za), which needs renewing</li>
<li><strong>Hosting</strong>, where your website lives</li>
<li><strong>Business email</strong>, if it isn't included with your hosting</li>
<li><strong>Maintenance and updates</strong>, to keep the site secure and working</li>
<li><strong>Changes and new pages</strong> as your business grows</li>
</ul>
<p>Always make sure the domain name is registered in <strong>your business's name</strong>, not the designer's. Losing control of your domain is one of the most painful and expensive problems to fix.</p>
<h2>DIY website builders vs a professional</h2>
<p>DIY builders can be a sensible start if you have more time than budget and are comfortable with technology. The trade-off is your time, and the fact that many DIY sites look fine but don't bring in enquiries, because they miss the basics below. A professional site costs more upfront but should be built to generate business from day one.</p>
<h2>What every small-business website needs</h2>
<ul>
<li>Works properly on phones, because most of your visitors will be on one</li>
<li>Loads quickly</li>
<li>Explains clearly what you do, where you work and why to choose you</li>
<li>A separate page for each main service</li>
<li>Click-to-call and WhatsApp buttons, plus a simple enquiry form</li>
<li>Reviews or examples of your work</li>
<li>Google Search Console set up, and a link to your <a href="google-business-profile-guide.html">Google Business Profile</a></li>
</ul>
<h2>Questions to ask before you pay</h2>
<ul>
<li>Exactly which pages and features are included?</li>
<li>Who writes the content and supplies the images?</li>
<li>What are the yearly costs after launch?</li>
<li>Will the domain and website be owned by my business?</li>
<li>Is the site set up for Google from the start?</li>
<li>How do changes work after launch, and what do they cost?</li>
</ul>
<h2>How we price websites</h2>
<p>Every business needs something slightly different, so we give you a clear, <strong>fixed quote</strong> before any work starts, with everything included listed in writing. Our <a href="website-design-durban.html">websites</a> are mobile-first, fast and SEO-ready from launch, and we can also upgrade an existing site if a full rebuild isn't needed.</p>
<p>Thinking about a new website or wondering whether your current one is costing you customers? <a href="#contact">Get in touch for a free review</a> and we'll tell you what we'd fix first.</p>""",
    },
    {
        "slug": "how-much-to-spend-on-google-ads.html",
        "title": "How Much Should a Small Business Spend on Google Ads?",
        "seo_title": "How Much to Spend on Google Ads? | ZM Results",
        "desc": "How Google Ads pricing works, how to work out a sensible starting budget for your small business, and how to make sure every rand is tracked.",
        "excerpt": "You control your Google Ads budget, but how much is enough? Here's a simple way to work out a starting budget that makes sense for your business.",
        "date": "2026-11-14",
        "read": "3 min read",
        "body": """
<p>One of the best things about Google Ads is that you're in control of what you spend. One of the most confusing things is working out how much that should be. Spend too little and you won't get enough data or enquiries to judge it. Spend too much too soon and you can waste money before the campaign is set up properly. Here's how Google Ads pricing works and a simple way to work out a sensible starting budget.</p>
<h2>How you're charged</h2>
<ul>
<li><strong>You pay per click.</strong> In most search campaigns you're only charged when someone clicks your ad, not when it's shown.</li>
<li><strong>You set a daily budget.</strong> Google spreads your spending across the month, so you won't be surprised by a huge bill.</li>
<li><strong>Prices are set by an auction.</strong> The cost of a click depends on how many other businesses want to appear for the same search, and on how relevant and useful Google thinks your ad and website are.</li>
<li><strong>Ad spend and management are separate.</strong> Your ad spend goes directly to Google. If you use an agency, its management fee is a separate cost, so make sure any quote shows both clearly.</li>
</ul>
<h2>What affects the cost of a click</h2>
<ul>
<li><strong>Your industry:</strong> services where one customer is worth a lot, like legal or financial services, usually have more expensive clicks.</li>
<li><strong>Your area:</strong> competition varies between cities and suburbs.</li>
<li><strong>Your keywords:</strong> specific searches like "emergency plumber Pinetown" often cost less and convert better than broad ones like "plumber".</li>
<li><strong>Your ad and landing page:</strong> Google rewards relevant ads and pages that give people what they searched for, which can lower what you pay.</li>
</ul>
<h2>Work out your budget backwards</h2>
<p>Instead of picking a number out of the air, start with the result you want and work backwards. You need three figures:</p>
<ul>
<li><strong>How many enquiries you want each month.</strong></li>
<li><strong>Roughly how many visitors turn into an enquiry</strong> on your website. If you don't know yet, your first month of ads will tell you.</li>
<li><strong>The estimated cost per click</strong> for your keywords. Google's free Keyword Planner tool shows estimates for your area.</li>
</ul>
<p><strong>A simple example</strong> (made-up numbers, just to show the method): say clicks for your service are estimated at R20 each and about 1 in 10 visitors sends an enquiry. Each enquiry would then cost around R200. If you want 15 enquiries a month, you'd need a budget of about R3 000. Your real numbers will be different, but the method stays the same.</p>
<p>Then ask the most important question: <strong>what is a new customer worth to you?</strong> If one job is worth far more than the cost of the enquiries it takes to win it, Google Ads can be very profitable.</p>
<h2>Start small and focused</h2>
<ul>
<li>Start with <strong>one main service</strong> and <strong>one area</strong> rather than everything at once.</li>
<li>Use specific keywords that show someone is ready to buy.</li>
<li>Add <strong>negative keywords</strong> like "jobs", "free", "course" and "DIY" so you don't pay for the wrong clicks.</li>
<li>Show ads during the hours you can actually answer the phone.</li>
<li>Send people to a page about that exact service, not just your home page.</li>
</ul>
<h2>Track every enquiry</h2>
<p>Set up conversion tracking for calls, WhatsApp messages and form submissions before you spend seriously. Without it, you're guessing. With it, you can see exactly which keywords bring in customers, cut the ones that don't, and confidently put more money into the ones that do.</p>
<h2>When to increase your budget</h2>
<p>Once you know what an enquiry costs and that the enquiries are turning into paying customers, increasing your budget becomes a simple business decision. Scale up gradually and keep an eye on whether the cost per enquiry stays sensible.</p>
<h2>Need help?</h2>
<p>We set up and manage <a href="google-ads-durban.html">Google Ads for local businesses</a>, with tracking built in from day one so you know what every rand is doing. If you're still deciding between ads and SEO, read <a href="seo-vs-google-ads.html">SEO vs Google Ads: which should you start with?</a>, or <a href="#contact">request a free growth audit</a> and we'll recommend a starting budget for your business.</p>""",
    },
]


def nice_date(iso):
    import datetime
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def post_page(p):
    body = f"""
      <section class="page-hero"><div class="container">
        <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="blog.html">Blog</a> / <span>{html.escape(p["title"])}</span></nav>
        <p class="eyebrow">Marketing tips</p>
        <h1 class="post-title">{html.escape(p["title"])}</h1>
        <p class="post-meta">By ZM Results · <time datetime="{p["date"]}">{nice_date(p["date"])}</time> · {p["read"]}</p>
      </div></section>
      <section class="section"><div class="container"><article class="post">{p["body"]}</article></div></section>
      {cta_band("Free growth audit", "Want us to check your business?", "We'll show you how you currently appear on Google and the quickest ways to win more local customers.")}
      {contact(eyebrow="Get in touch", title="Let's get your<br /><em>business seen.</em>")}"""
    schema = [
        {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
         "author": {"@type": "Organization", "name": "ZM Results", "url": BASE + "/"}, "publisher": {"@id": BASE + "/#business"},
         "image": BASE + "/og-image.png", "mainEntityOfPage": f"{BASE}/{p['slug']}"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE + "/blog.html"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": f"{BASE}/{p['slug']}"}]}]
    urls.append(page(p["slug"], p["seo_title"], p["desc"], body, active="blog", schema=schema))


for p in POSTS:
    post_page(p)

cards = "".join(f"""<article class="post-card"><p class="post-meta">{nice_date(p["date"])} · {p["read"]}</p><h2><a href="{p["slug"]}">{html.escape(p["title"])}</a></h2><p>{html.escape(p["excerpt"])}</p><a class="text-link" href="{p["slug"]}" aria-hidden="true" tabindex="-1">Read the guide <span>→</span></a></article>""" for p in sorted(POSTS, key=lambda x: x["date"], reverse=True))
blog = f"""
      <section class="page-hero"><div class="container">
        <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <span>Blog</span></nav>
        <p class="eyebrow">Marketing tips</p>
        <h1>Local marketing,<br /><span>made simple.</span></h1>
        <p class="hero-lead">Practical, jargon-free guides to help South African small businesses get found on Google and win more customers.</p>
      </div></section>
      <section class="section"><div class="container"><div class="post-grid">{cards}</div></div></section>
      {contact(eyebrow="Want a hand?", title="Let's get your<br /><em>business seen.</em>")}"""
urls.append(page("blog.html", "Marketing Tips Blog for Local Businesses | ZM Results",
                 "Practical guides on Google Business Profile, Google reviews, SEO and Google Ads for Durban and South African small businesses.",
                 blog, active="blog", schema=[breadcrumb_schema("Blog", "blog.html"),
                 {"@type": "Blog", "name": "ZM Results marketing tips", "url": BASE + "/blog.html", "publisher": {"@id": BASE + "/#business"}}]))

# ---------------- SITEMAP + FAVICON ----------------
sm = "\n".join(f"  <url><loc>{u}</loc><lastmod>2026-11-11</lastmod></url>" for u in urls)
(SITE / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>\n')
(SITE / "CNAME").write_text("zmresults.co.za\n")
print("built:", sorted(p.name for p in SITE.iterdir()))
