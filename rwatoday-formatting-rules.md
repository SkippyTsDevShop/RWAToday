# RWAToday.news — Formatting Rules

## Links that must display as stacked list items (never run-on)

All `<a>` tags in the following contexts **must** have `style="display:block;"` applied inline. This overrides any CSS cascade issues and guarantees correct rendering across all browsers and Cloudflare-served static pages.

### Applies to:
- **Series navigation links** — `.series-nav a`
- **Sidebar related-item links** — `.sidebar-related-item`
- **Sidebar card links** — any `<a>` inside `.sidebar-card`

### Rule:
Always write sidebar and series nav links as:
```html
<a class="sidebar-related-item" style="display:block;" href="...">
```
```html
<a href="..." style="display:block;padding:9px 12px;...">
```

Never rely on the class-based CSS alone — inject `display:block` as an inline style on every link in these contexts.

---

## Series nav format

Series navigation must use **inline-styled anchor tags**, one per line in the HTML, each with `display:block` inline. Do not use `<ul><li>` wrappers — the block-level styling on the `<a>` tag itself is sufficient and more robust.

```html
<div style="background:var(--surface,#0D1810);border:1px solid var(--border,#1E3020);border-radius:6px;padding:18px 22px;margin:1.5rem 0;">
  <div style="font-family:'Archivo Narrow',sans-serif;font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#3DAA6E;margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid var(--border,#1E3020);">Series Title</div>
  <a href="part-01.html" style="display:block;padding:9px 12px;border-bottom:1px solid rgba(30,64,40,0.6);text-decoration:none;color:#A8C4B0;font-size:13px;line-height:1.4;"><span style="...">01</span>Part title</a>
  <a href="part-02.html" style="display:block;padding:9px 12px;border-bottom:1px solid rgba(30,64,40,0.6);text-decoration:none;color:#F0F4FA;font-size:13px;font-weight:600;line-height:1.4;"><span style="...">02</span>Current part ← you are here</a>
  <a href="#" style="display:block;padding:9px 12px;text-decoration:none;color:#A8C4B0;font-size:13px;line-height:1.4;"><span style="...">03</span>Coming Soon</a>
</div>
```

---

## Back-link
Always use explicit `color:#3DAA6E` — never `color:var(--muted)` which renders as blue in some article templates.

```html
<a href="index.html" class="back-link" style="...;color:#3DAA6E;...">← Back to RWAToday.news</a>
```

---

## Footer logo
Must be wrapped in `<a href="index.html" style="text-decoration:none;">` so it links back to homepage.

---

## og:image
Always use hosted URL, never base64:
```html
<meta property="og:image" content="https://rwatoday.news/og-image.png"/>
```

---

## Ticker CSS
The ticker has been fully removed from the site. Never include `.ticker-wrap`, `.ticker-track`, `.ticker-item`, or `@keyframes ticker-scroll` in any new article.
