import asyncio
from googlenewsdecoder import gnews_decoder_async

async def test():
    url = "https://news.google.com/rss/articles/CBMiigFBVV95cUxOVDMxeU5wLWV6cXdTcHk5T0k2d0VDbnRoT3BSNUFULW9DYmh1VTdSUy1aU3k5cksta1dXTV9DU0Joa2Rib19WLWV4alc5OW5DYkU0d2lrcUVKR0I0NGpkOVRvSVkyR1hXU2JybG1DUmc3emt3ajJmcDB2WlFtcUpBd0V4Q3NJU1lma2c?oc=5"
    try:
        res = await gnews_decoder_async(url)
        print("Decoded URL:", res.get('decoded_url'))
    except Exception as e:
        print("Error:", e)

asyncio.run(test())
