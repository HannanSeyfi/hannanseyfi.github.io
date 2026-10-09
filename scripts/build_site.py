"""Build the dependency-free GitHub Pages site from its shared layout and page content."""
import html
import json
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site_src"
URL = "https://hannanseyfi.github.io"
NAV = [("home", "/", "Home"), ("research", "/research/", "Research"),
       ("projects", "/projects/", "Projects"), ("experience", "/experience/", "Experience"),
       ("resume", "/resume/", "CV")]


def build():
    pages = json.loads((SOURCE / "pages.json").read_text(encoding="utf-8"))
    layout = Template((SOURCE / "layout.html").read_text(encoding="utf-8"))
    person = {"@context": "https://schema.org", "@type": "Person", "name": "Hannan Seyfi",
              "url": URL + "/", "image": URL + "/picture.jpg",
              "email": "mailto:hannanseyfi0@gmail.com", "jobTitle": "MSc researcher",
              "affiliation": {"@type": "CollegeOrUniversity", "name": "Khatam University"},
              "sameAs": ["https://github.com/HannanSeyfi", "https://www.linkedin.com/in/HannanSeyfi"],
              "knowsAbout": ["Machine unlearning", "Model editing", "Large language models", "Trustworthy AI"]}
    for page in pages:
        slug = page["slug"]
        navigation = "\n".join(
            f'<a href="{path}"' + (' aria-current="page"' if item == slug else '') + f'>{label}</a>'
            for item, path, label in NAV) + '\n<a class="nav-contact" href="#contact">Contact <span aria-hidden="true">↗</span></a>'
        target = ROOT / ("index.html" if slug == "home" else "404.html" if slug == "404" else f"{slug}/index.html")
        target.parent.mkdir(parents=True, exist_ok=True)
        result = layout.substitute(
            title=html.escape(page["title"], quote=True), description=html.escape(page["description"], quote=True),
            canonical=URL + page["path"], slug=slug, navigation=navigation,
            structured_data='<script type="application/ld+json">' + json.dumps(person) + '</script>' if slug == "home" else '',
            content=(SOURCE / "pages" / f"{slug}.html").read_text(encoding="utf-8"))
        result = "\n".join(line.rstrip() for line in result.splitlines()) + "\n"
        target.write_text(result, encoding="utf-8", newline="\n")
        print(f"Built {target.relative_to(ROOT)}")
    urls = "\n".join(f"  <url><loc>{URL}{p['path']}</loc></url>" for p in pages if p["slug"] != "404")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '\n</urlset>\n', encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {URL}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    build()
