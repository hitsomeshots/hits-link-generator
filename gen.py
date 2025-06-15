import os
import re
import ctypes
import asyncio
import platform
from urllib.parse import urlparse, unquote

import aiohttp
from bs4 import BeautifulSoup

def set_console_title(title):
    system = platform.system()
    if system == "Windows":
        os.system("cls")
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        os.system("clear")
        print(f"\33]0;{title}\a", end="", flush=True)

async def get_fuckingfast_link(session, download_url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
    async with session.get(download_url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "html.parser")
        scripts = soup.find_all("script")
        pattern = re.compile(r'https://fuckingfast.co/dl/[a-zA-Z0-9_-]+')
        for script in scripts:
            if script.string:
                match = pattern.search(script.string)
                if match:
                    return match.group()
    return None

async def get_datanodes_link(session, download_url):
    parsed_url = urlparse(download_url)
    path_segments = parsed_url.path.split("/")
    file_code = path_segments[1].encode("latin-1", "ignore").decode("latin-1")
    file_name = path_segments[-1].encode("latin-1", "ignore").decode("latin-1")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": f"lang=english; file_name={file_name}; file_code={file_code};",
        "Host": "datanodes.to",
        "Origin": "https://datanodes.to",
        "Referer": "https://datanodes.to/download",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }
    payload = {
        "op": "download2",
        "id": file_code,
        "rand": "",
        "referer": "https://datanodes.to/download",
        "method_free": "Free Download >>",
        "method_premium": "",
        "dl": 1
    }
    async with session.post("https://datanodes.to/download", data=payload, headers=headers, allow_redirects=False) as response:
        response_data = await response.json()
        download_url = unquote(response_data.get("url"))
        return download_url
    return None

async def process_links(urls):
    async with aiohttp.ClientSession() as session:
        download_links = []
        total_urls = len(urls)
        for index, url in enumerate(urls):
            url = url.strip()
            if url:
                parsed_url = urlparse(url)
                if "fuckingfast.co" in parsed_url.netloc:
                    download_link = await get_fuckingfast_link(session, url)
                    set_console_title(f"Fuckingfast Link Generator - {index + 1}/{total_urls}")
                elif "datanodes.to" in parsed_url.netloc:
                    download_link = await get_datanodes_link(session, url)
                    set_console_title(f"Datanodes Link Generator - {index + 1}/{total_urls}")
                else:
                    download_link = None
                download_links.append(download_link)
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
    input()
