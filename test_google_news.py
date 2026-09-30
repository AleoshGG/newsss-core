import asyncio
import httpx

async def test():
    async with httpx.AsyncClient(follow_redirects=True) as client:
        r = await client.get("https://news.google.com/rss/articles/CBMiigFBVV95cUxOVDMxeU5wLWV6cXdTcHk5T0k2d0VDbnRoT3BSNUFULW9DYmh1VTdSUy1aU3k5cksta1dXTV9DU0Joa2Rib19WLWV4alc5OW5DYkU0d2lrcUVKR0I0NGpkOVRvSVkyR1hXU2JybG1DUmc3emt3ajJmcDB2WlFtcUpBd0V4Q3NJU1lma2c?oc=5")
        print("HTML Snippet:", r.text[:1000])
        print("Length:", len(r.text))
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, 'lxml')
        a = soup.find('a')
        if a:
            print("Found link:", a.get('href'))

asyncio.run(test())
