# Blog auto-publish runbook (for the scheduled session)

This is the standalone procedure a scheduled Routine follows to publish ONE new
SEO article to storymodeguy.com without any human involvement. It is written so a
fresh session that just cloned `main` can execute it top to bottom.

**Goal:** keep the site publishing genuinely useful, keyword-targeted photography
articles that rank in Google and funnel readers to the Payhip products. One article
per run. Additive only — never touch anything outside `blog/`, `blog-src/`, and
`sitemap.xml`.

## Steps

1. **Pick the next topic.** Open `blog-src/backlog.json`. Take the **first** entry in
   `topics`. That's the article to write this run. (If `topics` is empty, STOP and
   instead append 8–12 fresh topic ideas to the backlog — new photography searches
   that funnel to a product — then end the run without publishing.)

2. **Write the body.** Create `blog-src/<slug>.html` — the article body only (it gets
   wrapped in the site shell by the builder). House style, follow it exactly:
   - Only these tags: `<p> <h2> <h3> <ul> <ol> <li> <strong> <em> <a>`. No `<html>`,
     `<head>`, `<style>`, `<img>`, or `<h1>` — the builder adds all of that.
   - 600–1000 words. Genuinely useful and specific — real settings, real places,
     real numbers. Write like a working photographer, first person, warm and plain.
     No fluff, no keyword stuffing. This has to be worth reading.
   - Work the target keyword naturally into the first paragraph, an `<h2>`, and the
     title.
   - Include exactly **one** call-to-action block, placed about 60% of the way down:
     ```html
     <div class="cta">
       <h3>Short benefit-driven headline</h3>
       <p>One sentence on what the product gives them.</p>
       <a class="btn" href="{cta_url from backlog}">{cta_button from backlog}</a>
     </div>
     ```
   - Optionally add one inline text link to a product or to `/gallery.html` in the
     closing paragraph. Don't overdo links.

3. **Register it.** Add an object to the `articles` array in `blog-src/manifest.json`
   with these fields (copy slug/title/description/keywords/hero/hero_alt from the
   backlog entry; set today's date):
   ```json
   {"slug":"...","title":"...","description":"...","keywords":"...",
    "hero":"...","hero_alt":"...","date":"YYYY-MM-DD","date_h":"Month D, YYYY"}
   ```
   Then **remove** that entry from `blog-src/backlog.json`.

4. **Build.** From the repo root: `python3 promo/build/blog.py`
   This regenerates every `blog/*.html`, rebuilds `blog/index.html`, and injects the
   new URL into `sitemap.xml`. Confirm it printed `wrote blog/<slug>.html`.

5. **Publish to `main` (additive, byte-exact).** `main` holds the authoritative site
   and must never be overwritten wholesale. Push ONLY the changed files:
   ```bash
   git add blog/ blog-src/ sitemap.xml
   git commit -m "Journal: publish <title>"
   git push origin HEAD:main    # if on main already; else push the two/three paths
   ```
   If working from a non-`main` checkout, use a detached `origin/main` worktree,
   copy `blog/*.html` + `sitemap.xml` in, commit, and `git push origin HEAD:main`.
   The changed set must be only `blog/**`, `blog-src/**`, and `sitemap.xml`.
   (Note: `blog.py` also writes `blog/feed.xml` — it's inside `blog/`, so it's already staged.)

6. **Ping IndexNow** so Bing/Yandex crawl the new page fast (no account needed):
   `python3 promo/build/indexnow.py https://storymodeguy.com/blog/<slug>.html https://storymodeguy.com/blog/`
   This is best-effort — if it errors, ignore it and continue.

7. **Done.** GitHub Pages redeploys `main` automatically. Do not post anywhere, do
   not message the user unless something failed. End the run.

## Guardrails
- One article per run. Never rewrite or delete existing articles.
- Never modify `index.html`, `gallery.html`, `guides.html`, products, or photos.
- If the build or push fails, leave the repo clean and report the error; don't retry
  destructively.
- Product links live in `blog-src/backlog.json` (and `promo/COMMAND-CENTER.md`). Use
  those exact Payhip URLs.
