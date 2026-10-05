# Guide Authoring Spec — READ THIS FULLY

You are writing the **body content** of a premium, sellable photography PDF guide for the brand **Story Mode Guy**. The design shell (cover, table of contents, fonts, colors, footer) is added automatically — you write ONLY the chapter body as an HTML fragment.

A reference implementation you should study for tone, depth, and component usage is at:
`/home/user/story-mode-guy/guides/src/05-why-blurry.html`

## Hard rules

1. Output is an **HTML fragment only** — NO `<!doctype>`, `<html>`, `<head>`, `<body>`, `<style>`, or `<script>` tags. Start directly with the first `<h1>`.
2. **Every chapter begins with:** `<h1><span class="n">CHAPTER N</span>Chapter Title</h1>` (the very first chapter uses `<span class="n">START HERE</span>` or `<span class="n">INTRODUCTION</span>` instead of CHAPTER 1 — your call). Each `<h1>` starts a new page automatically, so make each chapter a substantial, self-contained unit.
3. Use ONLY the components listed below. Do not invent new class names, do not add inline `style=` attributes, do not reference images (no `<img>`).
4. **Length & depth:** 8–10 chapters, roughly **3,000–4,200 words** of genuinely useful, accurate content. This sells for real money — it must teach, not pad. Be specific: real settings, real numbers, real technique. No fluff, no filler, no "in today's fast-paced world" intros.
5. **Accuracy:** Stick to well-established photography fundamentals that are true across camera brands. When a setting has different names by brand, give them (e.g. "Continuous AF (AF-C / AI Servo)"). Do NOT give app menu paths that change between software versions ("click Edit > Preferences > tab 3") — describe what to look for instead.
6. Write in a warm, confident, plain-spoken second-person voice ("you"). Encouraging, never condescending. Short paragraphs.
7. End the final chapter with the sign-off block (see bottom).
8. Escape literal `<`, `>`, `&` inside text as `&lt; &gt; &amp;`. Use `&times;` for ×, `&rarr;` for →.

## Component vocabulary (use these liberally — they are what makes it feel premium)

### Lead-in paragraph (once, right after chapter 1's h1)
```
<p class="lead-in">One punchy paragraph that hooks the reader and frames the whole guide.</p>
```

### Body headings inside a chapter
```
<h2>Section heading</h2>
<h3>Sub-point (renders in the accent color)</h3>
<p>Normal paragraph. Use <strong>bold</strong> and <em>italics</em> for emphasis.</p>
```

### Key takeaway (bold colored banner — use 1–3 per guide for the biggest ideas)
```
<div class="key"><div class="kt">Remember</div><p>The single most important sentence.</p></div>
```

### Callouts (tinted boxes with an emoji icon — use several per chapter)
Variants: `tip` (💡), `warn` (⚠️), `note` (📷), `pro` (🎓 pro tip), `try` (🎯 do-this drill), `gear` (🛠️ gear).
```
<div class="callout tip"><div class="ct"><span class="ico">💡</span>Short title</div><p>The advice.</p></div>
<div class="callout warn"><div class="ct"><span class="ico">⚠️</span>Watch out</div><p>The pitfall.</p></div>
<div class="callout pro"><div class="ct"><span class="ico">🎓</span>Pro habit</div><p>Advanced tip.</p></div>
<div class="callout try"><div class="ct"><span class="ico">🎯</span>Try this</div><p>An action drill.</p></div>
<div class="callout gear"><div class="ct"><span class="ico">🛠️</span>Gear note</div><p>A purchase or kit tip.</p></div>
<div class="callout note"><div class="ct"><span class="ico">📷</span>Note</div><p>A clarification.</p></div>
```

### Numbered steps (for any walkthrough / workflow)
```
<ol class="steps">
  <li><span class="sh">Bold step headline.</span> Explanation of the step.</li>
  <li><span class="sh">Next step.</span> Explanation.</li>
</ol>
```

### Checklist (ticked boxes — great for "before you shoot" / gear lists)
```
<ul class="check">
  <li>First checklist item.</li>
  <li>Second checklist item.</li>
</ul>
```

### Settings recipe card (a signature element — use for "settings for X scene")
```
<div class="recipe">
  <div class="rh"><span>Recipe title (e.g. Indoor portrait)</span><span class="tag">STARTING POINT</span></div>
  <div class="rb">
    <div class="chips"><span class="chip">Aperture <b>f/2.8</b></span><span class="chip">Shutter <b>1/200s</b></span><span class="chip">ISO <b>800</b></span></div>
    <p class="small">One line of context about when/why to adjust.</p>
  </div>
</div>
```

### Card grid (2-up by default, or add class `three` for 3-up)
```
<div class="cards">
  <div class="card"><div class="ch">🔆 Card title</div><p>Short content, or a &lt;ul&gt;.</p></div>
  <div class="card"><div class="ch">🎨 Card title</div><ul><li>point</li><li>point</li></ul></div>
</div>
```
(Use `<div class="cards three">` for three across; add class `solid` to a card for a tinted background.)

### Table (comparisons, settings matrices)
```
<table>
  <tr><th>Column A</th><th>Column B</th><th>Column C</th></tr>
  <tr><td>cell</td><td>cell</td><td>cell</td></tr>
</table>
```

### Pull quote
```
<blockquote>A memorable line worth setting apart.</blockquote>
```

### Divider
```
<hr>
```

### REQUIRED sign-off at the very end of the last chapter
```
<div class="key"><div class="kt">Remember</div><p>A final one-sentence motivator specific to this guide's topic.</p></div>
<div class="end"><div class="mark">Story Mode Guy</div><div class="sub">Photography guides for people who treat everything like it has a plot. · storymodeguy.com</div></div>
```

## Quality bar
Study `05-why-blurry.html`. Match that density of recipe cards, callouts, tables, and step lists — a reader should hit a visual component every half page. Every chapter should teach something concrete they can do on their next shoot. Write the whole thing; do not stop early or leave placeholders.
