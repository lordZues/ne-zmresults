# ZM Results — how to go live

Your site has two parts:

1. **The website** (`site/` folder) — hosted on GitHub Pages, as now.
2. **The leads Worker** (`worker/worker.js`) — a small Cloudflare program that saves every form request to your Cloudflare database and gives you a private leads page at `zmresults.co.za/admin`.

The leads database (`zmresults-leads`) has already been created in your Cloudflare account.

---

## Part 1 — Update the website (fixes the broken design too)

1. Open your website's repository on github.com.
2. Click **Add file → Upload files**.
3. Drag in **everything inside the `site/` folder** (not the folder itself):
   `index.html`, `services.html`, `seo-durban.html`, `social-media-management-durban.html`,
   `google-ads-durban.html`, `thank-you.html`, `styles.css`, `script.js`, `sitemap.xml`, `favicon.svg`, `CNAME`
4. Click **Commit changes**. GitHub replaces the old files. The site updates in 1–2 minutes.

> The form already emails you through FormSubmit, so it works even before Part 2.

## Part 2 — Turn on the leads database and admin page

**Create the Worker**
1. Cloudflare dashboard → **Workers & Pages** → **Create** → **Create Worker**.
2. Name it `zmresults-leads` → **Deploy**.
3. Click **Edit code**, delete everything, paste the full contents of `worker/worker.js`, click **Deploy**.

**Connect the database**
4. Open the Worker → **Bindings** → **Add binding** → **D1 database**.
5. Variable name: `DB` · Database: `zmresults-leads` → **Add binding**.

**Set your admin password**
6. Worker → **Settings** → **Variables and Secrets** → **Add**.
7. Type: **Secret** · Name: `ADMIN_PASSWORD` · Value: a strong password only you know → **Deploy**.

**Point your domain at it**
8. Worker → **Settings** → **Domains & Routes** → **Add** → **Route**.
9. Zone: `zmresults.co.za` · Route: `zmresults.co.za/api/*` → **Add route**.
10. Add a second route: `zmresults.co.za/admin*`.

**Test**
- Visit `https://zmresults.co.za/api/health` — you should see `{"ok":true,"db":true}`.
- Submit the form on your site, then visit `https://zmresults.co.za/admin`.
  Log in with any username (e.g. `admin`) and your `ADMIN_PASSWORD`. Your test lead should be there.

## After going live

- **FormSubmit**: if you've never confirmed it, the first submission sends an activation email to zmresults@gmail.com — click the link in it once.
- **Google Search Console**: submit `https://zmresults.co.za/sitemap.xml` so Google finds the new service pages.
- **Admin page**: change each lead's status (new → contacted → audit sent → won/lost) and download everything as CSV.
