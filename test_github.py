import asyncio
import httpx

async def test():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://api.github.com/repos/tiangolo/fastapi/readme",
            headers={"Accept": "application/vnd.github.v3.raw"}
        )
        print("Status:", r.status_code)
        print("Headers:", r.headers.get("x-ratelimit-remaining"))
        if r.status_code == 200:
            print("Content:", r.text[:50])

asyncio.run(test())
