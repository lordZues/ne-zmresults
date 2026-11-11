# ZM Results website

Source for **zmresults.co.za**, a digital marketing agency in Durban.

Cloudflare Workers (Worker name `ne-zmresults`) deploys this repository automatically every time something is committed to `main`.

## What's here

| Path | What it is |
|---|---|
| `*.html`, `styles.css`, `script.js`, images | The website itself (served as static files) |
| `worker.js` | Handles the contact/audit forms (`/api/audit`) and the private leads page (`/admin`) |
| `wrangler.jsonc` | Cloudflare config, including the `zmresults-leads` D1 database |
| `schema.sql` | The leads database table |
| `_build/build.py` | Generates all the HTML pages from shared templates |

`.assetsignore` keeps the code, config and `_build` folder from being published as web pages.

## Changing the site

The `.html` files are generated. To change content, edit `_build/build.py` and run:

```
python3 _build/build.py
```

Then commit the changed files. Cloudflare redeploys automatically.

## Forms

- Every form emails **zuesjordan@gmail.com** via FormSubmit and also saves to the `zmresults-leads` database.
- Leads page: `https://zmresults.co.za/admin` (password = the `ADMIN_PASSWORD` secret on the Worker).
