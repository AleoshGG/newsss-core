"""
Test de integración: YouTube Transcript API v1.2.4
================================================
Diagnostica si la extracción de transcripciones funciona correctamente
con la nueva API de youtube-transcript-api >= 1.0.

Ejecutar desde la raíz del proyecto:
    python -m tests.test_youtube_transcript

O directamente:
    python tests/test_youtube_transcript.py
"""

import asyncio
import sys

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# ---------------------------------------------------------------------------
# Videos públicos conocidos con subtítulos disponibles
# ---------------------------------------------------------------------------
TEST_VIDEOS = [
    # (video_id, descripción, idiomas esperados)
    ("dQw4w9WgXcQ", "Rick Astley - Never Gonna Give You Up", ["en"]),
    ("jNQXAC9IVRw", "Me at the zoo (primer video de YouTube)", ["en"]),
    ("kJQP7kiw5Fk", "Despacito - Luis Fonsi", ["es", "en"]),
    ("pRpeEdMmmQ0", "Shakira - Waka Waka", ["es", "en"]),
]

LANGS_TO_TRY = ["es", "en"]


# ---------------------------------------------------------------------------
# Lógica de transcripción (replica la lógica del use case con la API correcta)
# ---------------------------------------------------------------------------
def fetch_transcript(video_id: str) -> dict:
    """
    Usa YouTubeTranscriptApi v1.2.4 (instancia, no método estático).
    Retorna un dict con resultado y diagnóstico.
    """
    result = {
        "video_id": video_id,
        "transcript": None,
        "lang_found": None,
        "available_langs": [],
        "error": None,
    }

    try:
        api = YouTubeTranscriptApi()
        t_list = api.list(video_id)

        # Recolectar idiomas disponibles para diagnóstico
        result["available_langs"] = [t.language_code for t in t_list]

        found = None

        # 1. Intentar idiomas preferidos
        for lang in LANGS_TO_TRY:
            try:
                found = t_list.find_transcript([lang])
                result["lang_found"] = lang
                break
            except Exception:
                pass

        # 2. Fallback: primer transcript disponible (el LLM traducirá después)
        if not found:
            for t in t_list:
                found = t
                result["lang_found"] = f"{t.language_code} (fallback)"
                break

        if found:
            fetched = found.fetch()
            formatter = TextFormatter()
            result["transcript"] = (
                formatter.format_transcript(fetched).replace("\n", " ").strip()
            )

    except Exception as e:
        result["error"] = str(e)

    return result


# ---------------------------------------------------------------------------
# Runner asíncrono
# ---------------------------------------------------------------------------
async def main():
    print("=" * 70)
    print("  YouTube Transcript API — Test de Integración")
    print(f"  Librería: youtube-transcript-api (instancia-based API v1.x)")
    print(f"  Idiomas preferidos: {LANGS_TO_TRY}")
    print("=" * 70)

    ok_count = 0
    fail_count = 0

    for video_id, label, _ in TEST_VIDEOS:
        print(f"\n{'─'*70}")
        print(f"  Video : {label}")
        print(f"  ID    : {video_id}")
        print(f"  URL   : https://www.youtube.com/watch?v={video_id}")

        # Ejecutar en thread porque youtube_transcript_api es síncrono
        result = await asyncio.to_thread(fetch_transcript, video_id)

        print(f"  Idiomas disponibles : {result['available_langs']}")
        print(f"  Idioma encontrado   : {result['lang_found']}")

        if result["error"]:
            print(f"  ❌ ERROR : {result['error']}")
            fail_count += 1
        elif result["transcript"]:
            length = len(result["transcript"])
            preview = result["transcript"][:300]
            status = "✅ OK" if length > 50 else "⚠️  MUY CORTO"
            print(f"  Longitud            : {length} chars  {status}")
            print(f"  Preview             : {preview}...")
            if length > 50:
                ok_count += 1
            else:
                fail_count += 1
        else:
            print("  ❌ Sin transcripción y sin error")
            fail_count += 1

    print(f"\n{'='*70}")
    print(f"  Resultado: {ok_count} ✅  /  {fail_count} ❌  de {len(TEST_VIDEOS)} videos")
    print("=" * 70)

    # Salir con código de error si todo falla (útil en CI)
    if ok_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
