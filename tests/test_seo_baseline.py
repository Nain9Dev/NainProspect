"""Discoverability baseline for the public demo site (specs/003-seo-baseline)."""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

CLIENT_DIR = Path(__file__).resolve().parent.parent / "ProspectAI.Client"
PUBLIC_DIR = CLIENT_DIR / "public"
HOST_ROOT = "https://prospect.naindev.com/"
AUTHOR_ID = "https://www.naindev.com/#person"


class _Head(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, str]] = []
        self.metas: list[dict[str, str]] = []
        self.json_ld: list[str] = []
        self._in_json_ld = False

    def handle_starttag(self, tag, attrs):
        data = {k: (v or "") for k, v in attrs}
        if tag == "link":
            self.links.append(data)
        elif tag == "meta":
            self.metas.append(data)
        elif tag == "script" and data.get("type") == "application/ld+json":
            self._in_json_ld = True
            self.json_ld.append("")

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_json_ld = False

    def handle_data(self, data):
        if self._in_json_ld:
            self.json_ld[-1] += data


@pytest.fixture(scope="module")
def head() -> _Head:
    parser = _Head()
    parser.feed((CLIENT_DIR / "index.html").read_text(encoding="utf-8"))
    return parser


def _meta(head: _Head, key: str, value: str) -> list[str]:
    return [m.get("content", "") for m in head.metas if m.get(key) == value]


def test_canonical_is_the_host_root(head):
    canonicals = [l["href"] for l in head.links if l.get("rel") == "canonical"]
    assert canonicals == [HOST_ROOT]


def test_single_description_within_search_snippet_length(head):
    descriptions = _meta(head, "name", "description")
    assert len(descriptions) == 1
    assert 70 <= len(descriptions[0]) <= 160


def test_open_graph_matches_canonical(head):
    assert _meta(head, "property", "og:type") == ["website"]
    assert _meta(head, "property", "og:site_name") == ["NainProspect"]
    assert _meta(head, "property", "og:url") == [HOST_ROOT]
    assert len(_meta(head, "property", "og:title")) == 1
    assert _meta(head, "property", "og:description") == _meta(head, "name", "description")
    image = _meta(head, "property", "og:image")
    assert len(image) == 1 and image[0].startswith("https://")


def test_twitter_card_is_complete(head):
    assert _meta(head, "name", "twitter:card") == ["summary_large_image"]
    for key in ("twitter:title", "twitter:description", "twitter:image"):
        assert len(_meta(head, "name", key)) == 1


def test_author_link_points_to_the_main_site(head):
    assert [l["href"] for l in head.links if l.get("rel") == "author"] == ["https://www.naindev.com/"]


def test_json_ld_parses_and_names_the_author(head):
    assert len(head.json_ld) == 1
    assert "<" not in head.json_ld[0]
    data = json.loads(head.json_ld[0])
    assert data["@type"] == "SoftwareApplication"
    assert data["url"] == HOST_ROOT
    assert data["isAccessibleForFree"] is True
    assert data["author"]["@id"] == AUTHOR_ID
    assert data["sameAs"] == "https://github.com/Nain9Dev/NainProspect"


def test_robots_advertises_the_sitemap_and_blocks_nothing():
    robots = (PUBLIC_DIR / "robots.txt").read_text(encoding="utf-8")
    assert re.search(r"^User-agent: \*$", robots, re.M)
    assert re.search(r"^Allow: /$", robots, re.M)
    assert not re.search(r"^Disallow: *\S", robots, re.M)
    assert f"Sitemap: {HOST_ROOT}sitemap.xml" in robots


def test_sitemap_lists_the_canonical_root():
    sitemap = (PUBLIC_DIR / "sitemap.xml").read_text(encoding="utf-8")
    assert re.findall(r"<loc>([^<]+)</loc>", sitemap) == [HOST_ROOT]


def test_llms_txt_starts_with_a_heading():
    lines = (PUBLIC_DIR / "llms.txt").read_text(encoding="utf-8").splitlines()
    assert lines[0] == "# NainProspect"
    assert any(line.startswith("> ") for line in lines)
    assert any("https://www.naindev.com/" in line for line in lines)
