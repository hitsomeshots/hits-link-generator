import os
import asyncio
import ctypes
import platform
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup
from pypasser import reCaptchaV3

def set_console_title(title):
    system = platform.system()

    if system == "Windows":
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        print(f"\33]0;{title}\a", end="", flush=True)

async def get_captcha_response(session, download_url): #GETTING ANCHOR LINK IS BROKEN!!!!!!!
    async with session.get(download_url,
    ) as response:
        if response.status == 200:
            page_html = await response.text()
            soup = BeautifulSoup(page_html, "html.parser")

            captcha_tag = soup.find("iframe", {"title": "reCAPTCHA"})
            return reCaptchaV3(captcha_tag.get("src"))
        return None

async def get_rand_value(session, id, file_name):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": f"lang=english; file_name={file_name}; file_code={id};",
        "Host": "datanodes.to",
        "Origin": "https://datanodes.to",
        "Referer": "https://datanodes.to/download",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    }

    payload = {
        "op": "download1",
        "usr_login": "",
        "id": id, 
        "fname": file_name,
        "referer": "",
        "method_free": "Free Download >>"
    }

    async with session.post(
        "https://datanodes.to/download",
        data=payload,
        headers=headers,
        allow_redirects=False,
    ) as response:
        if response.status == 200:
            page_html = await response.text()
            soup = BeautifulSoup(page_html, "html.parser")

            download_tag = soup.find("download-countdown")
            return download_tag.get("rand")
        return None

async def get_download_link(session, download_url):
    parsed_url = urlparse(download_url)
    path_segments = parsed_url.path.split("/")

    file_code = path_segments[1].encode("latin-1", "ignore").decode("latin-1")
    file_name = path_segments[-1].encode("latin-1", "ignore").decode("latin-1")

    rand_value = await get_rand_value(session, file_code, file_name)
    captcha_response = await get_captcha_response(session, download_url)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": f"lang=english; file_name={file_name}; file_code={file_code};",
        "Host": "datanodes.to",
        "Origin": "https://datanodes.to",
        "Referer": "https://datanodes.to/download",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    }

    payload = {
        "op": "download2",
        "id": file_code,
        "rand": rand_value,
        "referer": "https://datanodes.to/download",
        "method_free": "Free Download >>",
        "method_premium": "",
        "g-recaptcha-response": captcha_response
    }

    async with session.post(
        "https://datanodes.to/download",
        data=payload,
        headers=headers,
        allow_redirects=False,
    ) as response:
        if response.status == 302:
            return response.headers.get("Location")
        return None

async def process_links(urls):
    async with aiohttp.ClientSession() as session:
        download_links = []
        total_urls = len(urls)
        
        for index, url in enumerate(urls):
            url = url.strip()
            if url:
                download_link = await get_download_link(session, url)
                download_links.append(download_link)
                set_console_title(f"Datanodes Link Generator - {index+1}/{total_urls}")

        return download_links

if __name__ == "__main__":
    if not os.path.exists("links.txt"):
        with open("links.txt", "w") as file:
            exit()

    with open("links.txt", "r") as file:
        urls = file.readlines()

    download_links = asyncio.run(process_links(urls))

    with open("output_links.txt", "a", encoding="utf-8") as output_file:
        for download_link in download_links:
            if download_link:
                output_file.write(download_link + "\n")

    print("[*] Done generating download links!")
