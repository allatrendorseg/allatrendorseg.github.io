#!/usr/bin/env python3
"""Checks the built Hugo site before it gets deployed.

Usage: python3 scripts/check_site.py <build dir>

- every expected page exists in both languages and contains its title
- every internal link, image, stylesheet and script points to a file that exists
- links to PDFs open in a new tab
"""

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

SITE_HOSTS = {"allatrendorseg.github.io", "www.allatrendorseg.com", "allatrendorseg.com"}

# page path -> text that must appear on it
EXPECTED_PAGES = {
    "index.html": "Üdvözlünk",
    "about/index.html": "Rólunk",
    "donate/index.html": "Adományozz",
    "help/index.html": "CicaOtthon",
    "contact/index.html": "info@allatrendorseg.com",
    "report/index.html": "Beszámolóink",
    "posts/forever/index.html": "Hagyaték átadás",
    "en/index.html": "Welcome",
    "en/about/index.html": "About",
    "en/donate/index.html": "Donate",
    "en/help/index.html": "CatHouse",
    "en/contact/index.html": "info@allatrendorseg.com",
    "en/report/index.html": "Reports",
    "en/posts/forever/index.html": "Transfer of Inheritance",
}

LINK_ATTRS = {"a": "href", "link": "href", "img": "src", "script": "src", "source": "src"}


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []  # (tag, url, attrs)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        url = attrs.get(LINK_ATTRS.get(tag, ""))
        if url:
            self.links.append((tag, url, attrs))


def page_url(site, html_file):
    rel = html_file.relative_to(site).as_posix()
    if rel.endswith("index.html"):
        rel = rel[: -len("index.html")]
    return "/" + rel


def resolve(site, path):
    """Return the file a site path points to, or None if it doesn't exist."""
    target = site / unquote(path).lstrip("/")
    if target.is_file():
        return target
    if (target / "index.html").is_file():
        return target / "index.html"
    return None


def check_pages(site):
    errors = []
    for rel, text in EXPECTED_PAGES.items():
        page = site / rel
        if not page.is_file():
            errors.append(f"missing page: /{rel}")
        elif text not in page.read_text(encoding="utf-8"):
            errors.append(f"/{rel}: expected text not found: {text!r}")
    return errors


def check_links(site):
    errors = []
    for html_file in sorted(site.rglob("*.html")):
        parser = LinkCollector()
        parser.feed(html_file.read_text(encoding="utf-8"))
        base = page_url(site, html_file)

        for tag, url, attrs in parser.links:
            parsed = urlparse(urljoin(base, url))
            if parsed.scheme not in ("", "http", "https"):
                continue  # mailto:, tel:, data:, ...
            if parsed.netloc and parsed.netloc not in SITE_HOSTS:
                continue  # external site
            if not parsed.path:
                continue  # same-page anchor

            where = f"{base}: <{tag}> {url}"
            if resolve(site, parsed.path) is None:
                errors.append(f"broken link {where}")
            if tag == "a" and parsed.path.lower().endswith(".pdf") and attrs.get("target") != "_blank":
                errors.append(f"PDF link does not open in a new tab {where}")
    return errors


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    site = Path(sys.argv[1])
    if not site.is_dir():
        sys.exit(f"not a directory: {site}")

    errors = check_pages(site) + check_links(site)
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        sys.exit(f"\n{len(errors)} problem(s) found")
    print(f"OK: {len(EXPECTED_PAGES)} pages and all internal links checked")


if __name__ == "__main__":
    main()
