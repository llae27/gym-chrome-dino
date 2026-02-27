#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Elvis Yu-Jing Lin <elvisyjlin@gmail.com>
# Licensed under the MIT License - https://opensource.org/licenses/MIT


def rgba2rgb(im):
    from PIL import Image

    bg = Image.new("RGB", im.size, (255, 255, 255))  # fill background as white color
    bg.paste(im, mask=im.split()[3])  # 3 is the alpha channel
    return bg


def download_file(url):
    import requests

    local_filename = url.split("/")[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                # f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


def download_chromedriver():
    # We're getting chrome 145 driver
    import platform
    
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        if machine in ("amd64", "x86_64"):
            keyword = "win64"
        else:
            keyword = "win32"
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    elif system == "darwin":
        if machine in ("arm64", "aarch64"):
            keyword = "mac-arm64"
        else:
            keyword = "mac-x64"
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    elif system == "linux":
        keyword = "linux64"
        chrome_path = "/usr/bin/google-chrome"
    
    else:
        raise RuntimeError("Unrecognized operating system: " + system)

    import requests
    import re
    from bs4 import BeautifulSoup as BS

    url = f"https://storage.googleapis.com/chrome-for-testing-public/145.0.7632.77/{keyword}/chromedriver-{keyword}.zip"
    filename = "chromedriver.zip"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()  # fail immediately if HTTP error
        with open(filename, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

    import zipfile

    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(".")
        extracted = zip_ref.namelist()
    import shutil

    executable = "chromedriver"
    for extracted_file in extracted:
        if system == "windows":
            if extracted_file.endswith("chromedriver.exe"):
                shutil.move(extracted_file, executable)
                break
        else:
            if extracted_file.endswith("chromedriver"):
                shutil.move(extracted_file, executable)
    shutil.rmtree(extracted_file.split("/")[0])

    import os
    import stat

    st = os.stat(executable)
    os.chmod(executable, st.st_mode | stat.S_IEXEC)


import time


class Timer:
    def __init__(self):
        self.t0 = time.time()

    def tick(self):
        t1 = time.time()
        dt = t1 - self.t0
        self.t0 = t1
        return dt
