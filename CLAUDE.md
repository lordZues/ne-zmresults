# Notes for working on this repo

- This is a static site served by a Cloudflare Worker (`ne-zmresults`) straight from the repo root. Pushing to `main` deploys it to production.
- Never hand-edit the generated `.html` files or `sitemap.xml`. Change `_build/build.py`, then run `python3 _build/build.py` from the repo root and commit the results.
- Keep everything flat in the repo root (no folders for pages or images). The owner uploads through GitHub's web UI, which drops folders.
- Phone/WhatsApp: 073 695 7783 (+27736957783). Public email: zmresults@gmail.com. Form submissions go to zuesjordan@gmail.com. Don't change these without being asked.

## Adding a blog post

1. Add a dict to `POSTS` in `_build/build.py` with: `slug` (`something.html`), `title`, `seo_title` (≤ 60 chars), `desc` (≤ 155 chars), `excerpt`, `date` (`YYYY-MM-DD`, the publish date), `read`, `body` (HTML using `<p>`, `<h2>`, `<ul>`).
2. The blog index sorts posts newest first by `date`. Optional `updated` sets the schema dateModified.
3. Write for Durban / South African small-business owners: practical, honest, no invented statistics, client results or testimonials. Link to the relevant service or area page and to other posts.
4. Build, check that the new page and the sitemap entry exist, then commit.
