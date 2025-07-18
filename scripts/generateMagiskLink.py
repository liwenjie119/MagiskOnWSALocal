#!/usr/bin/python3
#
# This file is part of MagiskOnWSALocal.
#
# MagiskOnWSALocal is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# MagiskOnWSALocal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with MagiskOnWSALocal.  If not, see <https://www.gnu.org/licenses/>.
#
# Copyright (C) 2025 LSPosed Contributors
#
import sys

import json
import requests
from pathlib import Path

magisk_ver = sys.argv[1]
download_dir = (Path.cwd().parent / "download" if sys.argv[2] == "" else Path(sys.argv[2]))
tempScript = sys.argv[3]
download_files = {}
cdn_hosts = [
    "cdn.jsdelivr.net",
    "fastly.jsdelivr.net",
    "testingcf.jsdelivr.net",
    "gcore.jsdelivr.net",
]
print(f"Generating Magisk download link: release type={magisk_ver}", flush=True)
magisk_link = None
if not magisk_ver:
    magisk_ver = "stable"
if (
    magisk_ver == "stable"
    or magisk_ver == "beta"
    or magisk_ver == "canary"
    or magisk_ver == "debug"
):
    try:
        magisk_link = json.loads(requests.get(f"https://topjohnwu.github.io/magisk-files/{magisk_ver}.json").content)["magisk"]["link"]
        download_files[f"magisk-{magisk_ver}.zip"] = magisk_link
    except Exception:
        print("Failed to fetch from GitHub API, fallbacking to jsdelivr...")
        for host in cdn_hosts:
            try:
                magisk_link = json.loads(requests.get(f"https://{host}/gh/topjohnwu/magisk-files@master/{magisk_ver}.json").content)["magisk"]["link"]
                download_files[f"magisk-{magisk_ver}.zip"] = magisk_link
                break
            except Exception:
                print(f"Failed to fetch from {host}, trying next...", flush=True)
                pass
    finally:
        if magisk_link is None:
            print("Failed to fetch Magisk download link", flush=True)
            exit(1)

download_files["cust.img"] = "https://github.com/LSPosed/WSA-Addon/releases/latest/download/cust.img"
with open(download_dir / tempScript, "a") as f:
    for key, value in download_files.items():
        print(f"download link: {value}\npath: {download_dir / key}\n", flush=True)
        f.writelines(value + "\n")
        f.writelines(f"  dir={download_dir}\n")
        f.writelines(f"  out={key}\n")
