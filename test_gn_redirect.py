import asyncio
import httpx
import re

async def test():
    url = "https://news.google.com/rss/articles/CBMiigFBVV95cUxOVDMxeU5wLWV6cXdTcHk5T0k2d0VDbnRoT3BSNUFULW9DYmh1VTdSUy1aU3k5cksta1dXTV9DU0Joa2Rib19WLWV4alc5OW5DYkU0d2lrcUVKR0I0NGpkOVRvSVkyR1hXU2JybG1DUmc3emt3ajJmcDB2WlFtcUpBd0V4Q3NJU1lma2c?oc=5"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        r = await client.get(url)
        # Search for real urls inside the text
        urls = re.findall(r'https?://[^\s<>"]+', r.text)
        print("Found URLs:", [u for u in urls if 'nytimes.com' in u or 'example.com' in u])

asyncio.run(test())
