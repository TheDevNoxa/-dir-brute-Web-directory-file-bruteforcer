#!/usr/bin/env python3
"""
dir-brute — Web directory & file bruteforcer
Author : Noxa (Valentin Lagarde)
Usage  : python3 dir_brute.py -u https://example.com -w wordlist.txt
"""

import argparse
import urllib.request
import urllib.error
import concurrent.futures
import time
from dataclasses import dataclass

DEFAULT_EXTENSIONS = ["", ".php", ".html", ".txt", ".bak", ".js", ".json"]

DEFAULT_WORDLIST = [
    "admin", "login", "dashboard", "panel", "api", "config", "backup",
    "uploads", "images", "static", "assets", "js", "css", "includes",
    "lib", "src", "test", "dev", "staging", "old", "tmp", "temp",
    "db", "database", "sql", "data", "files", "docs", "readme",
    "robots", "sitemap", "index", "home", "about", "contact", "help",
    "user", "users", "account", "accounts", "profile", "settings",
    "register", "signup", "logout", "auth", "token", "reset",
    "wp-admin", "wp-login", "wp-content", "xmlrpc",
    "phpmyadmin", "pma", "phpinfo", "server-status", "server-info",
]

STATUS_COLORS = {
    200: "\033[92m",  # green
    201: "\033[92m",
    204: "\033[92m",
    301: "\033[94m",  # blue
    302: "\033[94m",
    403: "\033[93m",  # yellow
    401: "\033[93m",
    500: "\033[91m",  # red
}
RESET = "\033[0m"


@dataclass
class ScanHit:
    url: str
    status: int
    size: int
    redirect: str = ""


def load_wordlist(path: str | None) -> list[str]:
    if path:
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                return [line.strip() for line in f if line.strip() and not line.startswith("#")]
        except FileNotFoundError:
            print(f"[!] Wordlist not found: {path} — using built-in list")
    return DEFAULT_WORDLIST


def check_url(url: str, timeout: float = 6.0) -> ScanHit | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (NoxaDirBrute/1.0)"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            size = int(resp.headers.get("Content-Length", 0) or len(resp.read(4096)))
            return ScanHit(url=url, status=resp.status, size=size)
    except urllib.error.HTTPError as e:
        # 403/401 are interesting — resource exists but access denied
        if e.code in (401, 403):
            return ScanHit(url=url, status=e.code, size=0)
        return None
    except Exception:
        return None


def build_urls(base: str, wordlist: list[str], extensions: list[str]) -> list[str]:
    base = base.rstrip("/")
    urls = []
    for word in wordlist:
        for ext in extensions:
            urls.append(f"{base}/{word}{ext}")
    return urls


def scan(base_url: str, wordlist: list[str], extensions: list[str],
         threads: int, delay: float) -> list[ScanHit]:
    urls = build_urls(base_url, wordlist, extensions)
    hits = []
    done = 0
    total = len(urls)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(check_url, url): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            done += 1
            if done % 100 == 0:
                print(f"\r[*] Progress: {done}/{total} ({done*100//total}%)   ", end="", flush=True)
            result = future.result()
            if result:
                hits.append(result)
                color = STATUS_COLORS.get(result.status, "")
                print(f"\r{color}[{result.status}]{RESET} {result.url:<65} {result.size}b")
            if delay > 0:
                time.sleep(delay / threads)

    print(f"\r[*] Done — {total} requests sent{' ' * 20}")
    return sorted(hits, key=lambda x: x.status)


def print_summary(hits: list[ScanHit]) -> None:
    if not hits:
        print("\n  [-] Nothing found.")
        return
    print(f"\n{'=' * 65}")
    print(f"  RESULTS — {len(hits)} path(s) found")
    print(f"{'=' * 65}")
    for h in hits:
        color = STATUS_COLORS.get(h.status, "")
        print(f"  {color}[{h.status}]{RESET}  {h.url}")
    print(f"{'=' * 65}\n")


def main():
    parser = argparse.ArgumentParser(description="Web directory & file bruteforcer (educational)")
    parser.add_argument("-u", "--url",      required=True, help="Target URL (e.g. https://example.com)")
    parser.add_argument("-w", "--wordlist", default=None,  help="Path to wordlist")
    parser.add_argument("-x", "--ext",      default="",    help="Extensions (comma-separated, e.g. .php,.html)")
    parser.add_argument("--threads", type=int,   default=20,  help="Threads (default: 20)")
    parser.add_argument("--delay",   type=float, default=0.0, help="Delay between requests in seconds")
    parser.add_argument("--no-ext",  action="store_true",     help="Only test paths without extensions")
    args = parser.parse_args()

    wordlist = load_wordlist(args.wordlist)

    if args.no_ext:
        extensions = [""]
    elif args.ext:
        extensions = [""] + [e if e.startswith(".") else f".{e}" for e in args.ext.split(",")]
    else:
        extensions = DEFAULT_EXTENSIONS

    print(f"[*] Target   : {args.url}")
    print(f"[*] Words    : {len(wordlist)}")
    print(f"[*] Extensions: {extensions}")
    print(f"[*] Threads  : {args.threads}")
    print(f"[*] Total URLs: {len(wordlist) * len(extensions)}")
    print(f"[*] Starting scan ...\n")

    hits = scan(args.url, wordlist, extensions, args.threads, args.delay)
    print_summary(hits)


if __name__ == "__main__":
    main()
