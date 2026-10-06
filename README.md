# Bab Al Amani General Trading website

Static site. No framework, no cookies, no third-party requests (except the Google map, which loads only after the visitor clicks).

## Editing

Edit the files in `src/`, then rebuild:

```
python build.py
```

- `src/layout.html`: shared header, footer and `<head>` for every page
- `src/pages/*.html`: page content (the comment at the top sets title, description and active menu item)
- `styles.css`, `script.js`, `assets/`: used as-is

The build writes the finished `*.html` pages and `sitemap.xml` to the project root. Upload the root (without `src/`, `_handoff/`, `build.py`) to any static host.

## Deploying

Hosted on Cloudflare Pages, project `amani-trading`, production branch `production`:

```
python build.py
npx wrangler pages deploy dist --project-name amani-trading --branch production
```

Deploying with any other branch name creates a preview URL instead of updating the live site.

## Before launch

1. Fill every highlighted `[placeholder]`: trade licence no., TRN, office address, manager name, privacy contact, hosting and email provider, log retention.
2. Check that the `contact@babalamani.com` mailbox exists and is read daily.
3. Set the real domain in `build.py` (`SITE`), `robots.txt` and `.well-known/security.txt`, then rebuild.
4. Check every claim on the site (routes, transit times, sailings, 24 h quotes, product ranges) is true.
5. Have a lawyer review `privacy`, `terms`, and `cookies`. They are a careful starting point, not legal advice.
6. Sign data processing agreements with your hosting and email providers.
7. Serve over HTTPS. Security headers are ready in `_headers` (Netlify, Cloudflare Pages) and `.htaccess` (Apache).

## Keeping it cookie-free

The cookie policy says the site sets no cookies and loads nothing from other servers. If you add analytics, maps, YouTube, chat widgets or Google Fonts links, that stops being true: you'd need a consent banner and an updated cookie policy first.

## Licences

- **Fonts:** Schibsted Grotesk, Instrument Sans and JetBrains Mono, under the SIL Open Font License 1.1. The licence texts are in `assets/fonts/OFL-*.txt`.
- **Photos:** most are from [Unsplash](https://unsplash.com) and used under the Unsplash licence. `assets/img/food-wholesale.jpg` was supplied by the site owner.
- **Logo, text and design:** © Bab Al Amani General Trading LLC. All rights reserved. They aren't open for reuse.
