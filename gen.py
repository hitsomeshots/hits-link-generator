import os
import ctypes
from urllib.parse import urlparse

import requests

def get_download_link(download_url):
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
    }

    response = requests.post(
        "https://datanodes.to/download",
        data=payload,
        headers=headers,
        allow_redirects=False,
    )

    if response.status_code == 302:
        return response.headers.get("Location")


if __name__ == "__main__":
    if not os.path.exists("links.txt"):
        with open("links.txt", "w") as file:
            exit()

    with open("links.txt", "r") as file:
        urls = file.readlines()

    with open("output_links.txt", "a", encoding="utf-8") as output_file:
        for index, url in enumerate(urls):
            url = url.strip()
            if url:
                download_link = get_download_link(url)
                if download_link:
                    output_file.write(download_link + "\n")
                ctypes.windll.kernel32.SetConsoleTitleW(f"Datanodes Link Generator - {index+1}/{len(urls)}")

    print("[*] Done generating download links!")
