import re
from base64 import b64encode
from io import BytesIO
from random import randint
from typing import Optional

import aiohttp
from PIL import Image, UnidentifiedImageError
from pyquery import PyQuery
from yarl import URL

from .config import config


# 将图片转化为 base64
async def get_pic_base64_by_url(url: str, cookies: Optional[str] = None) -> str:
    headers = {"Cookie": cookies} if cookies else None
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, proxy=config.proxy) as resp:
            if resp.status == 200 and (
                image_bytes := await pic_anti_shielding(await resp.read())
            ):
                return b64encode(image_bytes).decode()
    return ""


# 图片反和谐
async def pic_anti_shielding(content: bytes) -> Optional[bytes]:
    try:
        im = Image.open(BytesIO(content))
    except UnidentifiedImageError:
        return None
    width, height = im.size
    points = [(0, 0), (0, height - 1), (width - 1, 0), (width - 1, height - 1)]
    for x, y in points:
        im.putpixel((x, y), randint(0, 255))
    with BytesIO() as output:
        im.save(output, format=im.format)
        return output.getvalue()


async def handle_img(
    url: str,
    hide_img: bool,
    cookies: Optional[str] = None,
) -> str:
    if not hide_img:
        if img_base64 := await get_pic_base64_by_url(url, cookies):
            return f"[CQ:image,file=base64://{img_base64}]"
    return f"预览图链接：{url}"


def handle_reply_msg(message_id: int) -> str:
    return f"[CQ:reply,id={message_id}]"


async def get_source(url: str) -> str:
    source = ""
    async with aiohttp.ClientSession() as session:
        if URL(url).host in ["danbooru.donmai.us", "gelbooru.com"]:
            async with session.get(url, proxy=config.proxy) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    source = PyQuery(html)(".image-container").attr(
                        "data-normalized-source"
                    )
        elif URL(url).host in ["yande.re", "konachan.com"]:
            async with session.get(url, proxy=config.proxy) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    source = PyQuery(html)("#post_source").attr("value")
    return source


async def shorten_url(url: str) -> str:
    pid_search = re.compile(
        r"(?:pixiv.+(?:illust_id=|artworks/)|/img-original/img/(?:\d+/){6})(\d+)"
    )
    if pid_search.search(url):
        return f"https://pixiv.net/i/{pid_search.search(url)[1]}"  # type: ignore
    if URL(url).host == "danbooru.donmai.us":
        return url.replace("/post/show/", "/posts/")
    if URL(url).host in ["exhentai.org", "e-hentai.org"]:
        flag = len(url) > 1024
        async with aiohttp.ClientSession() as session:
            if not flag:
                resp = await session.post("https://yww.uy/shorten", json={"url": url})
                if resp.status == 200:
                    return (await resp.json())["url"]  # type: ignore
                else:
                    flag = True
            if flag:
                resp = await session.post(
                    "https://www.shorturl.at/shortener.php", data={"u": url}
                )
                if resp.status == 200:
                    html = await resp.text()
                    final_url = PyQuery(html)("#shortenurl").attr("value")
                    return f"https://{final_url}"
    return url
