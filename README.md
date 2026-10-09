# Hannan Seyfi — academic website

Personal research website for PhD applications, published at [hannanseyfi.github.io](https://hannanseyfi.github.io/).

## Edit and build

The site uses static HTML, CSS, and a small progressive-enhancement script. No Ruby, Node.js packages, or external font services are required.

- Page content: `site_src/pages/*.html`
- Page titles, descriptions, and URLs: `site_src/pages.json`
- Shared navigation, metadata, and footer: `site_src/layout.html`
- Styles and mobile menu: `assets/site.css` and `assets/site.js`

After changing source content or the layout, run:

```sh
python scripts/build_site.py
python scripts/check_site.py
```

Commit the generated HTML pages, sitemap, and robots file alongside the source. GitHub Pages publishes static files from the root of the `main` branch. `.nojekyll` disables the previous Jekyll build.

## Local preview

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/`. Check the homepage and the research, projects, experience, CV, and 404 pages at desktop and mobile widths.

## CV updates

The October 2026 website content is based on the updated CV provided by Hannan Seyfi. Replace `Hannan_Seyfi_CV.pdf` and the legacy `resume.pdf` with the same new PDF, update the HTML content, and revise the visible update date in the shared layout and CV introduction.

The existing `/projects/`, `/resume/`, `/Hannan_Seyfi_CV.pdf`, and `/resume.pdf` URLs remain available. `/resume/` now provides an accessible HTML CV with view and download links.

Research outcomes are reported as thesis results, not as publications. MSc graduation is expected in October 2026.
