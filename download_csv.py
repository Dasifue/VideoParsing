"module for scrapping videos and saving them in csv file"
import typing
import asyncio
import aiofiles
import aiohttp
import aiocsv

URL = "https://www.motionelements.com/v2/search/video?currency=USD&language=en&page=1&per_page=50&sort=popular&facetarray=1&page=1"

async def send_request(url: str) -> dict[typing.Any, typing.Any] | None:
    "function sends async request and gets json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json(encoding="utf-8")
            return None


async def get_urls(
        json_data_array: list[dict[typing.Any, typing.Any]]
    ) -> typing.AsyncGenerator[tuple[str, str], None]:
    "function parses json data and gets mp4 links"
    for json_data in json_data_array:
        name: str = json_data["name"].strip()
        mp4_url: str = json_data["thumbnails"]["mp4"]["url"]
        yield name, mp4_url


async def main() -> None:
    "main function"

    json = await send_request(url=URL)
    if json is not None:
        json_data = json['data']

        async with aiofiles.open(file="motionelements.csv", mode="w", encoding="utf-8") as file:
            writer = aiocsv.AsyncWriter(asyncfile=file)

            async for data in get_urls(json_data_array=json_data):
                await writer.writerow(data)



if __name__ == "__main__":
    asyncio.run(main())
