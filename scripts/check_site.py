"""Check generated pages, local links, fragment targets, metadata, and PDF aliases."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.ids, self.links, self.errors = path, set(), [], []
        self.headings = 0
        self.main = 0
        self.description = 0
        self.canonical = 0
        self.current = 0
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.errors.append(f"duplicate ID: {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.headings += 1
        if tag == "main":
            self.main += 1
        if tag == "meta" and attrs.get("name") == "description" and attrs.get("content"):
            self.description += 1
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical += 1
        if tag == "a" and attrs.get("aria-current") == "page":
            self.current += 1
        for attribute in ("href", "src"):
            if attribute in attrs:
                self.links.append(attrs[attribute])
        if tag == "img" and not attrs.get("alt"):
            self.errors.append("image missing alternative text")


def check():
    entries = json.loads((ROOT / "site_src/pages.json").read_text(encoding="utf-8"))
    pages = {}
    for entry in entries:
        path = ROOT / ("index.html" if entry["slug"] == "home" else "404.html" if entry["slug"] == "404" else f"{entry['slug']}/index.html")
        pages[path.resolve()] = Page(path)
    failures = []
    count = 0
    for path, page in pages.items():
        for label, value in (("h1", page.headings), ("main landmark", page.main),
                             ("description", page.description), ("canonical URL", page.canonical)):
            if value != 1:
                page.errors.append(f"expected one {label}, found {value}")
        if path.name != "404.html" and page.current != 1:
            page.errors.append("missing or duplicate current-page navigation")
        for link in page.links:
            split = urlsplit(link)
            if split.scheme or split.netloc:
                continue
            target = (ROOT / unquote(split.path).lstrip("/")) if split.path.startswith("/") else (path.parent / unquote(split.path)) if split.path else path
            if target.is_dir():
                target /= "index.html"
            target = target.resolve()
            count += 1
            if not target.is_file():
                page.errors.append(f"broken local URL: {link}")
            elif split.fragment and target.suffix == ".html":
                target_page = pages.get(target) or Page(target)
                if unquote(split.fragment) not in target_page.ids:
                    page.errors.append(f"missing fragment target: {link}")
        failures.extend(f"{path.relative_to(ROOT)}: {error}" for error in page.errors)
    primary = ROOT / "Hannan_Seyfi_CV.pdf"
    legacy = ROOT / "resume.pdf"
    if hashlib.sha256(primary.read_bytes()).digest() != hashlib.sha256(legacy.read_bytes()).digest():
        failures.append("CV PDF aliases do not match")
    if not (ROOT / ".nojekyll").exists():
        failures.append("static GitHub Pages marker is missing")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"Passed: {len(pages)} pages; {count} local URLs and fragments; metadata, landmarks, image alternatives, navigation, and PDF aliases.")


if __name__ == "__main__":
    check()
