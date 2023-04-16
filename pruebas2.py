import os
import random
import asyncio
import aiohttp
import time

async def download_image(session, url):
    try:
        start_time = time.monotonic()
        async with session.get(url) as response:
            content = await response.read()
            filename = f"{url.split('/')[-1]}.png"
            filepath = os.path.join("images", filename)
            with open(filepath, "wb") as file:
                file.write(content)
                end_time = time.monotonic()
                print(f"{filename} downloaded in {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

async def download_images(num_images):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(num_images):
            url = f"https://picsum.photos/{random.randint(200, 500)}/{random.randint(200, 500)}"
            task = asyncio.ensure_future(download_image(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    num_images = 5
    if not os.path.exists("images"):
        os.mkdir("images")
    asyncio.run(download_images(num_images))