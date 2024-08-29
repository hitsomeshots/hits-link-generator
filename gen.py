import os
import re
import ctypes
import asyncio
import platform
from urllib.parse import urlparse
import tkinter as tk
from tkinter import filedialog, messagebox

import aiohttp
from bs4 import BeautifulSoup

class FuckingfastLinkGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Fuckingfast Link Generator")
        self.root.geometry("400x300")

        self.urls_label = tk.Label(root, text="Enter URLs (one per line):")
        self.urls_label.pack()

        self.urls_text = tk.Text(root, width=40, height=10)
        self.urls_text.pack()

        self.generate_button = tk.Button(root, text="Generate Links", command=self.generate_links)
        self.generate_button.pack()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

    async def get_fuckingfast_link(self, session, download_url):
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

    async def get_datanodes_link(self, session, download_url):
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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }
        payload = {
            "op": "download2",
            "id": file_code,
            "rand": "",
            "referer": "https://datanodes.to/download",
            "method_free": "Free Download >>",
            "method_premium": "",
            "adblock_detected": ""
        }
        async with session.post("https://datanodes.to/download", data=payload, headers=headers, allow_redirects=False) as response:
            if response.status == 302:
                return response.headers.get("Location")
            return None

    async def process_links(self, urls):
        async with aiohttp.ClientSession() as session:
            download_links = []
            total_urls = len(urls)
            for index, url in enumerate(urls):
                url = url.strip()
                if url:
                    parsed_url = urlparse(url)
                    if "fuckingfast.co" in parsed_url.netloc:
                        download_link = await self.get_fuckingfast_link(session, url)
                        self.status_label.config(text=f"Fuckingfast Link Generator - {index + 1}/{total_urls}")
                    elif "datanodes.to" in parsed_url.netloc:
                        download_link = await self.get_datanodes_link(session, url)
                        self.status_label.config(text=f"Datanodes Link Generator - {index + 1}/{total_urls}")
                    else:
                        download_link = None
                    download_links.append(download_link)
            return download_links

    def generate_links(self):
        urls = self.urls_text.get("1.0", "end-1c").splitlines()
        self.status_label.config(text="Generating links...")
        download_links = asyncio.run(self.process_links(urls))
        with open("output_links.txt", "a", encoding="utf-8") as output_file:
            for download_link in download_links:
                if download_link:
                    output_file.write(download_link + "\n")
        self.status_label.config(text="Done generating download links!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FuckingfastLinkGenerator(root)
    root.mainloop()
