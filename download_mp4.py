"module for scrapping videos and downloading them"
import typing
import asyncio
import aiofiles
import aiohttp

URL = "https://www.motionelements.com/v2/search/video?currency=USD&language=en&page=1&per_page=50&sort=popular&facetarray=1&page=1"

class MediaError(Exception):
    "Exception for media folder"


async def get_bytes_content(url: str) -> bytes | None:
    "function sends async request and gets bytes content"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.content.read()
            return None


async def send_request(url: str) -> dict[typing.Any, typing.Any] | None:
    "function sends async request and gets json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json(encoding="utf-8")
            return None


async def save_mp4(content: bytes, file_name: str) -> None:
    "function for writing mp4 files"
    try:
        async with aiofiles.open(file=f"media/{file_name}.mp4", mode="wb") as file:
            await file.write(content)
    except FileNotFoundError as exc:
        raise MediaError("Please create folder 'media' in current folder!") from exc


async def get_urls(
        json_data_array: list[dict[typing.Any, typing.Any]]
    ) -> typing.AsyncGenerator[tuple[str, str], None]:
    "function parses json data and gets mp4 links"
    for json_data in json_data_array:
        name: str = json_data["name"].strip().replace(" ", "_")
        mp4_url: str = json_data["thumbnails"]["mp4"]["url"]
        yield name, mp4_url


async def download_mp4(url: str, file_name: str):
    "function downloads mp4 file"
    bytes_content = await get_bytes_content(url=url)
    if bytes_content is not None:
        await save_mp4(content=bytes_content, file_name=file_name)


async def main() -> None:
    "main function"

    json = await send_request(url=URL)
    if json is not None:
        json_data = json['data']

        tasks = []
        async for object_data in get_urls(json_data_array=json_data):
            tasks.append(download_mp4(url=object_data[1], file_name=object_data[0]))

        await asyncio.gather(*tasks)



if __name__ == "__main__":
    asyncio.run(main())
