"""Install contract of the public demo site (specs/004-pwa-install): manifest, icons and head tags.

Opacity and the maskable safe zone are not checked here; the icon generator and its verification
script own that (see the plan).
"""

import json
import struct
from html.parser import HTMLParser
from pathlib import Path

import pytest

CLIENT_DIR = Path(__file__).resolve().parent.parent / "ProspectAI.Client"
PUBLIC_DIR = CLIENT_DIR / "public"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_ICONS = [
    ("/icons/icon-192.png", "192x192", "any"),
    ("/icons/icon-512.png", "512x512", "any"),
    ("/icons/icon-maskable-512.png", "512x512", "maskable"),
]


class _Head(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, str]] = []
        self.metas: list[dict[str, str]] = []

    def handle_starttag(self, tag, attrs):
        data = {k: (v or "") for k, v in attrs}
        if tag == "link":
            self.links.append(data)
        elif tag == "meta":
            self.metas.append(data)


@pytest.fixture(scope="module")
def manifest() -> dict:
    return json.loads((PUBLIC_DIR / "manifest.webmanifest").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def head() -> _Head:
    parser = _Head()
    parser.feed((CLIENT_DIR / "index.html").read_text(encoding="utf-8"))
    return parser


def _png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    assert data[:8] == PNG_SIGNATURE, f"{path.name} is not a PNG file"
    return struct.unpack(">II", data[16:24])


def _meta(head: _Head, name: str) -> list[str]:
    return [m.get("content", "") for m in head.metas if m.get("name") == name]


def test_pwa_002_manifest_members(manifest, head):
    description = _meta(head, "description")[0]
    assert manifest["name"] == "NainProspect"
    assert manifest["short_name"] == "NainProspect"
    assert len(manifest["short_name"]) <= 12
    assert manifest["description"] == description
    assert manifest["lang"] == "es"
    assert manifest["dir"] == "ltr"
    assert manifest["id"] == manifest["start_url"] == manifest["scope"] == "/"
    assert manifest["display"] == "standalone"
    assert manifest["theme_color"] == manifest["background_color"] == "#070a12"
    assert "prefer_related_applications" not in manifest


def test_pwa_003_icons_exist_at_declared_size(manifest):
    declared = [(i["src"], i["sizes"], i["purpose"]) for i in manifest["icons"]]
    assert declared == EXPECTED_ICONS
    assert all(i["type"] == "image/png" for i in manifest["icons"])
    for src, sizes, _purpose in declared:
        width, height = _png_size(PUBLIC_DIR / src.lstrip("/"))
        assert f"{width}x{height}" == sizes, f"{src} must measure what the manifest declares"
    assert _png_size(PUBLIC_DIR / "icons" / "apple-touch-icon.png") == (180, 180)


def test_pwa_001_head_links_manifest_and_touch_icon(head):
    manifests = [link["href"] for link in head.links if link.get("rel") == "manifest"]
    touch = [link["href"] for link in head.links if link.get("rel") == "apple-touch-icon"]
    assert manifests == ["/manifest.webmanifest"]
    assert touch == ["/icons/apple-touch-icon.png"]


def test_pwa_004_head_carries_the_ios_and_theme_tags(head, manifest):
    assert _meta(head, "mobile-web-app-capable") == ["yes"]
    assert _meta(head, "apple-mobile-web-app-capable") == ["yes"]
    assert _meta(head, "apple-mobile-web-app-title") == [manifest["short_name"]]
    assert _meta(head, "apple-mobile-web-app-status-bar-style") == ["black"]
    assert _meta(head, "theme-color") == [manifest["theme_color"]]


def test_pwa_005_no_service_worker_is_registered():
    sources = [CLIENT_DIR / "index.html", *(CLIENT_DIR / "src").rglob("*")]
    for path in sources:
        if path.is_file():
            assert "serviceWorker" not in path.read_text(encoding="utf-8", errors="ignore"), path.name
