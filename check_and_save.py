#!/usr/bin/env python3
import re
import socket
import time
import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

# ТВОЙ СПИСОК СЕРВЕРОВ
CUSTOM_KEYS_TEXT = """
vless://998f72fe-5039-44e4-84c2-26d84f73421e@138.124.118.130:443?security=reality&encryption=none&pbk=4ltYIatUJFFjrW8ZBDGLJaun0BnYIgxn-jmpmTEDGyc&fp=firefox&type=xhttp&sni=newyork.gosgenarchive.com#США
vless://8007dda2-aed2-4514-8299-6e3edbdb015b@104.243.44.241:443?security=reality&encryption=none&pbk=jIq_COD-tIXTvgDn-TslFGtB_a8HVgUOOIlUByv8fkg&headerType=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=us2.findreplayfoals.com&sid=8718c58d3d51db59#США
vless://b24ad12f-f6ce-4f0b-a264-d58a76104026@104.243.44.241:443?security=reality&encryption=none&pbk=jIq_COD-tIXTvgDn-TslFGtB_a8HVgUOOIlUByv8fkg&headerType=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=us2.freehiliters.com&sid=8718c58d3d51db59#США
vless://998f72fe-5039-44e4-84c2-26d84f73421e@45.136.228.194:443?security=reality&encryption=none&pbk=4ltYIatUJFFjrW8ZBDGLJaun0BnYIgxn-jmpmTEDGyc&fp=safari&type=xhttp&sni=losangeles.gosgenarchive.com#США
vless://998f72fe-5039-44e4-84c2-26d84f73421e@77.110.124.147:443?security=reality&encryption=none&pbk=4ltYIatUJFFjrW8ZBDGLJaun0BnYIgxn-jmpmTEDGyc&fp=firefox&type=xhttp&sni=houston.gosgenarchive.com#США
vless://998f72fe-5039-44e4-84c2-26d84f73421e@2.56.122.3:443?security=reality&encryption=none&pbk=4ltYIatUJFFjrW8ZBDGLJaun0BnYIgxn-jmpmTEDGyc&fp=safari&type=xhttp&sni=chicago.gosgenarchive.com#США
vless://88281d02-b387-4fe3-918e-26ed331e6d08@81.17.154.97:443?mode=auto&path=%2Fccxf5snr06b8xxb6&security=tls&alpn=h2&encryption=none&insecure=0&host=is-tw-relay.cdn.cachefleet.com&fp=firefox&type=xhttp&allowInsecure=0&sni=is-tw-relay.cdn.cachefleet.com#США
vless://7fc953d6-ae75-46fb-a970-10b57d513487@45.139.27.63:443?mode=auto&path=%2Fapi%2Fv2%2F&security=tls&alpn=h2&encryption=none&insecure=0&fp=firefox&type=xhttp&allowInsecure=0&sni=emerge-01.uiu.fyi#США
vless://b98d4c6e-6770-4a31-8256-a4750cdea0e7@t15.qifei.app:443?security=reality&encryption=none&pbk=0i_xAxYgSNx5NMpK2lOaWGS-CvAiD_LneYPO0MF0owo&headerType=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=www.amazon.com#США
vless://b98d4c6e-6770-4a31-8256-a4750cdea0e7@172.235.58.21:443?security=reality&encryption=none&pbk=0i_xAxYgSNx5NMpK2lOaWGS-CvAiD_LneYPO0MF0owo&headerType=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=www.amazon.com#США
vless://e7a4decb-631e-422b-9749-7e8f54618308@201.58.177.135:443?security=reality&encryption=none&pbk=9mJq2cP3srX_6K1YfMDp1yndvo5CtgL6TEVQ8tm4fVc&headerType=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=cdn.jsdelivr.net#США
vless://92e135b9-4c04-4e7e-8b28-d8074a202cf8@94.228.112.36:2053?mode=gun&security=reality&encryption=none&pbk=huWYSqGaqUTQWhee7SbQrNZ32qxCWQFvjTVkPRLQYTw&fp=firefox&type=grpc&serviceName=grpc&sni=files.polina.lol#США
vless://9ab9291e-fd72-4af9-b227-93419e90ff2e@45.151.30.245:443?security=reality&encryption=none&pbk=H0_ikooEh725UVXsMCoRPoRYMheLUL_L-xZA3fl_nS4&headerType=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=cl-fn-in.movietop24.site&sid=ae641bd0ef87fbfa#Финляндия
vless://ff0b6ba8-bed0-4c4d-bbc9-23af47582615@91.210.169.181:443?path=%2Fapi%2Fconnect&security=tls&encryption=none&insecure=0&host=wstg.datasynctrue.online&fp=firefox&type=ws&allowInsecure=0&sni=wstg.datasynctrue.online#Финляндия
vless://ff0b6ba8-bed0-4c4d-bbc9-23af47582615@188.225.33.141:443?path=%2Fapi%2Fconnect&security=tls&encryption=none&insecure=0&host=wstg.datasynctrue.online&fp=firefox&type=ws&allowInsecure=0&sni=wstg.datasynctrue.online#Финляндия
vless://ff0b6ba8-bed0-4c4d-bbc9-23af47582615@wstg.datasynctrue.online:443?path=%2Fapi%2Fconnect&security=tls&encryption=none&insecure=0&host=wstg.datasynctrue.online&fp=firefox&type=ws&allowInsecure=0&sni=wstg.datasynctrue.online#Финляндия
vless://92e135b9-4c04-4e7e-8b28-d8074a202cf8@94.228.112.60:7443?mode=gun&security=reality&encryption=none&pbk=36VgwCvCzW3ST22DrfRU7y8mVfm0PM7JpkXQnN9yLiE&fp=firefox&type=grpc&serviceName=grpc&sni=cdn.suzuki.lol#Финляндия
vless://9ab9291e-fd72-4af9-b227-93419e90ff2e@151.241.166.159:443?security=reality&encryption=none&pbk=tPhBRGpTbyaPFF3W0wpqncSrdNsV5I-eyM3S9CZoeCQ&headerType=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=pl-hsts.zloygo.com&sid=9a26e586f8cadc07#Польша
vless://8007dda2-aed2-4514-8299-6e3edbdb015b@188.119.123.217:443?security=reality&encryption=none&pbk=jIq_COD-tIXTvgDn-TslFGtB_a8HVgUOOIlUByv8fkg&headerType=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=pl2.magazinnarubeva.ru&sid=8718c58d3d51db59#Польша
vless://8007dda2-aed2-4514-8299-6e3edbdb015b@177.202.96.106:443?security=reality&encryption=none&pbk=jIq_COD-tIXTvgDn-TslFGtB_a8HVgUOOIlUByv8fkg&headerType=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=pl3.wolffast.net&sid=8718c58d3d51db59#Польша
vless://b24ad12f-f6ce-4f0b-a264-d58a76104026@188.119.123.217:443?security=reality&encryption=none&pbk=jIq_COD-tIXTvgDn-TslFGtB_a8HVgUOOIlUByv8fkg&headerType=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=pl1.wolffast.net&sid=8718c58d3d51db59#Польша
vless://b24ad12f-f6ce-4f0b-a264-d58a76104026@177.202.96.14:1443?security=reality&encryption=none&pbk=jIq_COD-tIXTvgDn-TslFGtB_a8HVgUOOIlUByv8fkg&headerType=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=pl2.greenzone12.com&sid=8718c58d3d51db59#Польша
vless://b24ad12f-f6ce-4f0b-a264-d58a76104026@177.202.96.106:443?security=reality&encryption=none&pbk=jIq_COD-tIXTvgDn-TslFGtB_a8HVgUOOIlUByv8fkg&headerType=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=pl1.spidermanshopping.com&sid=8718c58d3d51db59#Польша
vless://8007dda2-aed2-4514-8299-6e3edbdb015b@177.202.96.14:1443?security=reality&encryption=none&pbk=jIq_COD-tIXTvgDn-TslFGtB_a8HVgUOOIlUByv8fkg&headerType=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=pl3.magazinnarubeva.ru&sid=8718c58d3d51db59#Польша
vless://258d8fc5-206c-48fd-88df-169dbbe44d3f@103.246.248.20:443?security=reality&encryption=none&pbk=2YbfBDRn1xu5OOVvC6H7Pq0p0gRtZtvSqFS08-M-DUY&headerType=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=pl.atlanta-api.com#Польша
"""

MAX_WORKERS = 20
TEST_TIMEOUT = 5
MAX_LATENCY_MS = 2000

# Добавили США в список стран
COUNTRIES = {
    "usa":         ["сша", "usa", "united states"],
    "finland":     ["финляндия", "finland"],
    "poland":      ["польша", "poland"],
    "germany":     ["германия", "germany"],
}

COUNTRIES_ALL_KEYWORDS = [kw for kws in COUNTRIES.values() for kw in kws]

def fetch_keys_custom():
    lines = CUSTOM_KEYS_TEXT.strip().splitlines()
    return [line.strip() for line in lines if line.strip().startswith("vless://")]

def filter_keys(keys, mode):
    if mode in COUNTRIES:
        keywords = COUNTRIES[mode]
        return [k for k in keys if any(kw in k.lower() for kw in keywords)]
    return keys

def parse_host_port(key):
    try:
        without_scheme = key[len("vless://"):]
        at_idx = without_scheme.rfind("@")
        after_at = without_scheme[at_idx + 1:]
        host_port = after_at.split("?")[0].split("#")[0]
        if ":" in host_port:
            host, port = host_port.rsplit(":", 1)
            return host.strip("[]"), int(port)
    except Exception:
        pass
    return None, None

def test_key(key):
    host, port = parse_host_port(key)
    if not host:
        return None
    try:
        infos = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except Exception:
        return None
    best = None
    for (family, socktype, proto, canonname, sockaddr) in infos:
        start = time.time()
        try:
            sock = socket.socket(family, socktype)
            sock.settimeout(TEST_TIMEOUT)
            result = sock.connect_ex(sockaddr)
            sock.close()
            elapsed = round((time.time() - start) * 1000, 1)
            if result == 0 and elapsed <= MAX_LATENCY_MS:
                if best is None or elapsed < best["latency_ms"]:
                    best = {"key": key, "host": host, "port": port, "latency_ms": elapsed}
        except Exception:
            pass
    return best

def check_mode(keys):
    working = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(test_key, key): key for key in keys}
        for future in as_completed(futures):
            result = future.result()
            if result:
                working.append(result)

    working.sort(key=lambda x: x["latency_ms"])

    return {
        "best": working[0]["key"] if working else None,
        "top10": working[:10],
        "total_working": len(working),
        "total": len(keys),
    }

def main():
    print("Загружаем ВАШИ ключи...")
    all_keys = fetch_keys_custom()
    print(f"Загружено {len(all_keys)} ключей")

    results = {
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }

    for country in list(COUNTRIES.keys()):
        filtered = filter_keys(all_keys, country)
        print(f"[{country}] {len(filtered)} ключей, проверяем...")
        results[country] = check_mode(filtered)
        print(f"[{country}] Рабочих: {results[country]['total_working']}/{results[country]['total']}")

    os.makedirs("docs", exist_ok=True)
    with open("docs/keys.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Сохранено в docs/keys.json")

if __name__ == "__main__":
    main()
