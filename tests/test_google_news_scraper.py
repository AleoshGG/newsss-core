"""
Test de integración: Google News Scraper
========================================
Diagnostica la calidad del contenido extraído de artículos de Google News,
comparando dos estrategias:
  A) trafilatura  — extracción semántica de contenido (nuevo, más robusto)
  B) BeautifulSoup — búsqueda de tags <article>/<main> (implementación actual)

Ejecutar desde la raíz del proyecto:
    python -m tests.test_google_news_scraper

O directamente:
    python tests/test_google_news_scraper.py
"""

import asyncio
import sys

import feedparser
import httpx
import trafilatura
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Intento de importar el decoder de URLs de Google News
# ---------------------------------------------------------------------------
try:
    from googlenewsdecoder import gnews_decoder_async
except ImportError:
    gnews_decoder_async = None
    print("⚠️  googlenewsdecoder no instalado — se usarán URLs directas")

# ---------------------------------------------------------------------------
# Configuración del feed RSS (mismos parámetros que el use case en producción)
# ---------------------------------------------------------------------------
FEED_CONFIGS = [
    {
        "label": "Español (MX) — Inteligencia Artificial",
        "url": "https://news.google.com/rss/search",
        "params": {
            "q": "Inteligencia Artificial OR IA",
            "hl": "es-419",
            "gl": "MX",
            "ceid": "MX:es-419",
            "when": "1d",
        },
    },
    {
        "label": "English (US) — Artificial Intelligence AI",
        "url": "https://news.google.com/rss/search",
        "params": {
            "q": "Artificial Intelligence AI",
            "hl": "en-US",
            "gl": "US",
            "ceid": "US:en",
            "when": "1d",
        },
    },
]

MAX_ARTICLES_PER_FEED = 5

# Headers que simulan un navegador real (reduce bloqueos 403)
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


# ---------------------------------------------------------------------------
# Decodificador de URLs de Google News
# ---------------------------------------------------------------------------
async def decode_google_url(link: str) -> str:
    """Decodifica la URL encriptada de Google News al artículo real."""
    if gnews_decoder_async and "news.google.com" in link:
        try:
            decoded = await gnews_decoder_async(link)
            if decoded and decoded.get("decoded_url"):
                return decoded["decoded_url"]
        except Exception as e:
            print(f"    ⚠️  decode error: {e}")
    return link


# ---------------------------------------------------------------------------
# Estrategias de extracción de contenido
# ---------------------------------------------------------------------------
def extract_with_trafilatura(html: str) -> str | None:
    """Estrategia A: trafilatura — extracción semántica de contenido de artículo."""
    result = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=False,
        no_fallback=False,
    )
    return result.strip() if result and result.strip() else None


def extract_with_bs4(html: str) -> str | None:
    """Estrategia B: BeautifulSoup — implementación actual del use case."""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    article_tag = soup.find("article") or soup.find("main")
    if article_tag:
        text = article_tag.get_text(separator=" ", strip=True)[:5000]
        return text if text else None
    return None


# ---------------------------------------------------------------------------
# Scraping de un artículo
# ---------------------------------------------------------------------------
async def scrape_article(client: httpx.AsyncClient, entry) -> dict:
    link = getattr(entry, "link", "")
    title = getattr(entry, "title", "sin título")
    rss_summary = getattr(entry, "summary", "") or getattr(entry, "description", "")

    real_url = await decode_google_url(link)

    result = {
        "title": title,
        "original_url": link,
        "real_url": real_url,
        "http_status": None,
        "trafilatura_chars": 0,
        "bs4_chars": 0,
        "rss_summary_chars": len(BeautifulSoup(rss_summary, "lxml").get_text()) if rss_summary else 0,
        "trafilatura_preview": "",
        "bs4_preview": "",
        "error": None,
    }

    try:
        r = await client.get(
            real_url,
            headers=BROWSER_HEADERS,
            timeout=12.0,
            follow_redirects=True,
        )
        result["http_status"] = r.status_code

        if r.status_code == 200:
            html = r.text

            # Estrategia A: trafilatura
            content_a = extract_with_trafilatura(html)
            if content_a:
                result["trafilatura_chars"] = len(content_a)
                result["trafilatura_preview"] = content_a[:250]

            # Estrategia B: BeautifulSoup (actual)
            content_b = extract_with_bs4(html)
            if content_b:
                result["bs4_chars"] = len(content_b)
                result["bs4_preview"] = content_b[:250]

    except Exception as e:
        result["error"] = str(e)

    return result


# ---------------------------------------------------------------------------
# Procesamiento de un feed
# ---------------------------------------------------------------------------
async def process_feed(client: httpx.AsyncClient, config: dict) -> list[dict]:
    print(f"\n{'━'*70}")
    print(f"  📡 Feed: {config['label']}")

    try:
        r = await client.get(config["url"], params=config["params"], timeout=15.0)
        feed = feedparser.parse(r.text)
        entries = feed.entries[:MAX_ARTICLES_PER_FEED]
        print(f"  Entradas totales: {len(feed.entries)}  |  Probando: {len(entries)}")
    except Exception as e:
        print(f"  ❌ Error al obtener feed: {e}")
        return []

    results = []
    for i, entry in enumerate(entries, 1):
        print(f"\n  [{i}/{len(entries)}] {getattr(entry, 'title', 'sin título')[:60]}")
        result = await scrape_article(client, entry)
        results.append(result)

        status_icon = "✅" if result["http_status"] == 200 else "⚠️ "
        traf_icon = "✅" if result["trafilatura_chars"] > 100 else "❌"
        bs4_icon = "✅" if result["bs4_chars"] > 100 else "❌"

        print(f"    HTTP {result['http_status']} {status_icon}")
        print(f"    trafilatura : {result['trafilatura_chars']:>5} chars  {traf_icon}")
        print(f"    BeautifulSoup: {result['bs4_chars']:>5} chars  {bs4_icon}")
        print(f"    RSS summary  : {result['rss_summary_chars']:>5} chars  (referencia)")

        if result["trafilatura_preview"]:
            print(f"    Preview: {result['trafilatura_preview'][:180]}...")
        elif result["error"]:
            print(f"    Error: {result['error']}")

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
async def main():
    print("\n" + "=" * 70)
    print("  Google News Scraper — Test de Integración")
    print("  Comparativa: trafilatura (nuevo) vs BeautifulSoup (actual)")
    print("=" * 70)

    limits = httpx.Limits(max_keepalive_connections=10, max_connections=20)
    async with httpx.AsyncClient(limits=limits, follow_redirects=True) as client:
        all_results = []
        for feed_config in FEED_CONFIGS:
            results = await process_feed(client, feed_config)
            all_results.extend(results)

    # Resumen final
    total = len(all_results)
    traf_ok = sum(1 for r in all_results if r["trafilatura_chars"] > 100)
    bs4_ok = sum(1 for r in all_results if r["bs4_chars"] > 100)
    errors = sum(1 for r in all_results if r["error"])

    print(f"\n{'='*70}")
    print(f"  RESUMEN FINAL ({total} artículos)")
    print(f"{'─'*70}")
    print(f"  trafilatura  : {traf_ok:>2}/{total} artículos con contenido real  {'✅' if traf_ok > total // 2 else '❌'}")
    print(f"  BeautifulSoup: {bs4_ok:>2}/{total} artículos con contenido real  {'✅' if bs4_ok > total // 2 else '❌'}")
    print(f"  Errores HTTP : {errors:>2}/{total}")
    print("=" * 70)

    if traf_ok == 0 and bs4_ok == 0:
        print("\n⚠️  Ninguna estrategia extrajo contenido. Posibles causas:")
        print("   - Rate limiting de Google News RSS")
        print("   - Todos los artículos tienen paywall")
        print("   - Problema de red / IP bloqueada")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
