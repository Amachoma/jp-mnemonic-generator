import aiohttp
import asyncio


class AsyncFetcher:
    def __init__(self, delay_between_requests):
        self.delay_between_requests = delay_between_requests

    def get(self, urls, after_callback=lambda x: x):
        async def fetch_all():
            async with aiohttp.ClientSession() as session:
                async def fetch(url, delay):
                    await asyncio.sleep(delay)
                    async with session.get(url) as response:
                        response_text = await response.text()
                        return after_callback(response_text)

                tasks = []
                for index in range(len(urls)):
                    tasks.append(fetch(urls[index], self.delay_between_requests * index))

                responses = await asyncio.gather(*tasks)
                return responses

        return asyncio.run(fetch_all())
