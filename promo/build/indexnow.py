#!/usr/bin/env python3
"""Ping IndexNow (Bing, Yandex, etc.) so new/updated URLs get crawled fast.
No account needed - ownership is proven by hosting <KEY>.txt at the site root.
Usage: python3 promo/build/indexnow.py <url> [<url> ...]
"""
import os, ssl, json, sys, urllib.request
KEY = "a7f3c9e21b8d6405e7c3a1f9d2b6e480"
HOST = "storymodeguy.com"
def _ctx():
    for ca in (os.environ.get("REQUESTS_CA_BUNDLE"), os.environ.get("SSL_CERT_FILE"), "/root/.ccr/ca-bundle.crt"):
        try:
            if ca and os.path.exists(ca): return ssl.create_default_context(cafile=ca)
        except Exception: pass
    return ssl.create_default_context()
def ping(urls):
    body = json.dumps({"host":HOST,"key":KEY,"keyLocation":f"https://{HOST}/{KEY}.txt","urlList":urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
        headers={"Content-Type":"application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=20, context=_ctx()) as r:
            print(f"IndexNow: {r.status} for {len(urls)} url(s)")
    except Exception as e:
        print("IndexNow ping failed (non-fatal):", e)
if __name__ == "__main__":
    ping(sys.argv[1:] or [f"https://{HOST}/"])
