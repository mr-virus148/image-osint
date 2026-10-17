#!/usr/bin/env python3
# ============================================================
#   ANONFACE - Image OSINT Recon Tool  v1.2
#   Created by Mr.virus138 Team | The Anonymous Tanzania Hackers
#   Cooperation: Binno World Hacker
# ============================================================

import os
import sys
import json
import time
import base64
import hashlib
import urllib.parse
import subprocess

# -------------------- COLORS --------------------
RED    = "\033[1;31m"
GREEN  = "\033[1;32m"
YELLOW = "\033[1;33m"
CYAN   = "\033[1;36m"
PURPLE = "\033[1;35m"
WHITE  = "\033[1;37m"
RESET  = "\033[0m"

BANNER = f"""{PURPLE}
  █████╗ ███╗   ██╗ ██████╗ ███████╗███████╗ █████╗ ██████╗ ███████╗
 ██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝
 ███████║██╔██╗ ██║██║  ███╗█████╗  ███████╗███████║██║  ██║█████╗
 ██╔══██║██║╚██╗██║██║   ██║██╔══╝  ╚════██║██╔══██║██║  ██║██╔══╝
 ██║  ██║██║ ╚████║╚██████╔╝███████╗███████║██║  ██║██████╔╝███████╗
 ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝
{CYAN}        ═══════════════════════════════════════════════════
              IMAGE OSINT RECON TOOL  v1.2
{RED}     Created by : Mr.virus138 Team
     Team       : The Anonymous Tanzania Hackers
     Coop       : Binno World Hacker
{CYAN}        ═══════════════════════════════════════════════════{RESET}
"""

SEARCH_ENGINES = {
    "Yandex (Best for faces)": "https://yandex.com/images/search?rpt=imageview&url={}",
    "Google Lens":             "https://lens.google.com/uploadbyurl?url={}",
    "Bing Visual":             "https://www.bing.com/images/search?q=imgurl:{}&view=detailv2&iss=sbi",
    "TinEye (first seen)":     "https://tineye.com/search?url={}",
    "Baidu Image":             "https://graph.baidu.com/details?isfromtusoupc=1&tn=pc&image={}",
    "Karma Decay (Reddit)":    "https://karmadecay.com/search?q={}",
}

def slow_print(text, delay=0.005):
    for c in text:
        sys.stdout.write(c); sys.stdout.flush(); time.sleep(delay)
    print()

def open_browser(url):
    if sys.platform.startswith("linux"):
        subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", url])
    elif sys.platform.startswith("win"):
        os.startfile(url)

def run_curl(args, timeout=60):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.stderr.strip()
    except Exception as e:
        return "", str(e)

# ============================================================
# MODULE 1: EXIF
# ============================================================
def exif_dump(img):
    slow_print(f"{YELLOW}[*] Dumping EXIF metadata...{RESET}")
    if subprocess.call(["which", "exiftool"], stdout=subprocess.DEVNULL) == 0:
        subprocess.run(["exiftool", img])
        # GPS check
        out, _ = run_curl(["exiftool", "-n", "-gpslatitude", "-gpslongitude", img])
        coords = [l.split(":")[-1].strip() for l in out.splitlines() if l.strip()]
        if len(coords) == 2 and coords[0] and coords[1]:
            lat, lon = coords
            slow_print(f"{GREEN}[+] GPS FOUND! Google Maps: https://maps.google.com/?q={lat},{lon}{RESET}")
        else:
            slow_print(f"{RED}[-] No GPS metadata (photo was stripped by an app).{RESET}")
    else:
        slow_print(f"{RED}[-] exiftool not found. Install: sudo apt install exiftool{RESET}")

# ============================================================
# MODULE 2: UPLOAD + ENGINES
# ============================================================
def upload_image(img_path):
    slow_print(f"{YELLOW}[*] Uploading image to public host...{RESET}")

    out, err = run_curl(["curl", "-sS", "-F", "reqtype=fileupload",
                         "-F", f"fileToUpload=@{img_path}",
                         "https://catbox.moe/user/api.php"])
    if out.startswith("http"):
        slow_print(f"{GREEN}[+] Hosted on catbox.moe: {out}{RESET}")
        return out

    out, err = run_curl(["curl", "-sS", "-F", f"file=@{img_path}", "https://0x0.st"])
    if out.startswith("http"):
        slow_print(f"{GREEN}[+] Hosted on 0x0.st: {out}{RESET}")
        return out

    out, err = run_curl(["curl", "-sS", "-F", f"file=@{img_path}",
                         "https://tmpfiles.org/api/v1/upload"])
    try:
        url = json.loads(out)["data"]["url"].replace("tmpfiles.org/", "tmpfiles.org/dl/")
        slow_print(f"{GREEN}[+] Hosted on tmpfiles.org: {url}{RESET}")
        return url
    except Exception:
        pass

    out, err = run_curl(["curl", "-sS", "-F", f"file=@{img_path}", "https://file.io/?expires=1d"])
    try:
        url = json.loads(out)["link"]
        slow_print(f"{GREEN}[+] Hosted on file.io: {url}{RESET}")
        return url
    except Exception:
        pass

    slow_print(f"{RED}[-] All upload hosts failed. Check your internet connection:{RESET}")
    slow_print(f"{RED}    last error: {err or 'no output from any host'}{RESET}")
    slow_print(f"{YELLOW}[*] Tip: verify connectivity -> curl -s https://ifconfig.me{RESET}")
    return None

def open_engines(img_url):
    slow_print(f"{CYAN}[*] Preparing all search engines for this image...{RESET}")
    for name, tmpl in SEARCH_ENGINES.items():
        url = tmpl.format(urllib.parse.quote(img_url, safe=""))
        slow_print(f"{GREEN}  [+] {name}: {url}{RESET}")

    ans = input(f"{YELLOW}    Open all in browser? [y/N]: {RESET}").strip().lower()
    if ans == "y":
        for _, tmpl in SEARCH_ENGINES.items():
            open_browser(tmpl.format(urllib.parse.quote(img_url, safe="")))
    else:
        for name, tmpl in SEARCH_ENGINES.items():
            if input(f"{YELLOW}    Open {name}? [y/N]: {RESET}").strip().lower() == "y":
                open_browser(tmpl.format(urllib.parse.quote(img_url, safe="")))

# ============================================================
# MODULE 3: USERNAME PIVOT
# ============================================================
def username_pivot():
    slow_print(f"\n{CYAN}[*] Username PIVOT module - sherlock + maigret{RESET}")
    user = input(f"{WHITE}[?] Enter target username/name: {RESET}").strip()
    if not user:
        slow_print(f"{RED}[-] No username given, returning...{RESET}"); return

    os.makedirs("results", exist_ok=True)
    slow_print(f"{YELLOW}[*] Sherlock scanning 300+ sites for '{user}'...{RESET}")
    if subprocess.call(["which", "sherlock"], stdout=subprocess.DEVNULL) == 0:
        with open(f"results/sherlock_{user}.txt", "w") as f:
            subprocess.run(["sherlock", user], stdout=f)
        slow_print(f"{GREEN}[+] Results: results/sherlock_{user}.txt{RESET}")
    else:
        slow_print(f"{RED}[-] Sherlock not installed. Install: pip install sherlock{RESET}")

    slow_print(f"{YELLOW}[*] Maigret extracting deep profile intel...{RESET}")
    if subprocess.call(["which", "maigret"], stdout=subprocess.DEVNULL) == 0:
        subprocess.run(["maigret", user, "--all-sites", "--html", f"results/maigret_{user}"])
        slow_print(f"{GREEN}[+] Report: results/maigret_{user}/report.html{RESET}")
    else:
        slow_print(f"{RED}[-] Maigret not installed. Install: pip install maigret{RESET}")

    slow_print(f"{GREEN}[+] Pivot complete. Check folder: results/{RESET}")

# ============================================================
# MODULE 4: IMAGE FORENSICS (NEW)
# ============================================================
def image_forensics(img):
    slow_print(f"{CYAN}[*] IMAGE FORENSICS module{RESET}")

    # --- strings dump: hidden URLs, software names, comments inside the file
    slow_print(f"{YELLOW}[*] Scanning embedded strings (hidden URLs/software/comments)...{RESET}")
    out, _ = run_curl(["strings", img])
    interesting = [l for l in out.splitlines()
                   if any(k in l.lower() for k in ["http", "www.", ".com", ".org",
                        "adobe", "photoshop", "gimp", "canva", "picsart",
                        "samsung", "iphone", "xiaomi", "tecno", "infinix", "huawei",
                        "comment", "software", "author", "copyright"])]
    if interesting:
        slow_print(f"{GREEN}[+] Interesting strings found:{RESET}")
        for s in interesting[:30]:
            print(f"      {s}")
    else:
        slow_print(f"{RED}[-] No interesting strings (fully clean/re-encoded image).{RESET}")

    # --- ELA (Error Level Analysis) using PIL - highlights edited regions
    slow_print(f"{YELLOW}[*] Running Error Level Analysis (ELA)...{RESET}")
    try:
        from PIL import Image, ImageChops, ImageEnhance
        im = Image.open(img).convert("RGB")
        tmp = "ela_tmp.jpg"
        im.save(tmp, "JPEG", quality=90)
        ela = ImageChops.difference(im, Image.open(tmp))
        ela = ImageEnhance.Brightness(ela).enhance(15)
        os.makedirs("results", exist_ok=True)
        ela_path = "results/ela_output.png"
        ela.save(ela_path)
        os.remove(tmp)
        slow_print(f"{GREEN}[+] ELA saved: {ela_path} (bright spots = edited/modified regions){RESET}")
        slow_print(f"{WHITE}    Open it and look: uniform dark = original, bright patches = edits/insertions.{RESET}")
    except ImportError:
        slow_print(f"{RED}[-] Pillow not installed. Install: pip install Pillow{RESET}")
    except Exception as e:
        slow_print(f"{RED}[-] ELA failed: {e}{RESET}")

    # --- JPEG quantization table fingerprint (identifies editing software / camera)
    slow_print(f"{YELLOW}[*] JPEG quantization fingerprint...{RESET}")
    try:
        from PIL import Image
        im = Image.open(img)
        q = im.quantization
        if q:
            for tbl_id, data in q.items():
                avg = sum(data) / len(data)
                slow_print(f"{GREEN}    Table {tbl_id}: avg={avg:.1f} "
                           f"({'typical of camera/SNS re-encode' if avg > 60 else 'typical of heavy editing/app re-encode'}){RESET}")
        else:
            slow_print(f"{RED}[-] No quantization tables (unusual).{RESET}")
    except Exception:
        pass

    slow_print(f"{YELLOW}[*] Also try online: https://fotoforensics.com (upload image -> ELA + metadata){RESET}")

# ============================================================
# MODULE 5: HASH FINGERPRINT (NEW)
# ============================================================
def hash_fingerprint(img):
    slow_print(f"{CYAN}[*] HASH FINGERPRINT module{RESET}")
    data = open(img, "rb").read()
    md5  = hashlib.md5(data).hexdigest()
    sha1 = hashlib.sha1(data).hexdigest()
    sha256 = hashlib.sha256(data).hexdigest()
    slow_print(f"{GREEN}    MD5    : {md5}{RESET}")
    slow_print(f"{GREEN}    SHA1   : {sha1}{RESET}")
    slow_print(f"{GREEN}    SHA256 : {sha256}{RESET}")
    slow_print(f"{YELLOW}[*] Use these hashes to search breach/leak databases, VirusTotal, and dedupe across cases.{RESET}")
    os.makedirs("results", exist_ok=True)
    with open("results/hashes.txt", "w") as f:
        f.write(f"MD5: {md5}\nSHA1: {sha1}\nSHA256: {sha256}\n")
    slow_print(f"{GREEN}[+] Saved: results/hashes.txt{RESET}")

# ============================================================
# MODULE 6: STEGANOGRAPHY CHECK (NEW)
# ============================================================
def stego_check(img):
    slow_print(f"{CYAN}[*] STEGANOGRAPHY CHECK module{RESET}")
    found = False

    if subprocess.call(["which", "steghide"], stdout=subprocess.DEVNULL) == 0:
        slow_print(f"{YELLOW}[*] Running steghide extract (empty passphrase first)...{RESET}")
        r = subprocess.run(["steghide", "extract", "-sf", img, "-p", ""],
                           capture_output=True, text=True)
        if "wrote" in r.stderr.lower() or "extracted" in r.stderr.lower():
            slow_print(f"{GREEN}[+] steghide FOUND hidden data (empty passphrase)!{RESET}")
            found = True
        else:
            slow_print(f"{RED}[-] steghide: no hidden data with empty passphrase.{RESET}")
    else:
        slow_print(f"{RED}[-] steghide not installed. Install: sudo apt install steghide{RESET}")

    # trailing data check (data appended after JPEG EOI marker FFD9)
    slow_print(f"{YELLOW}[*] Checking for appended data after JPEG end-marker (FFD9)...{RESET}")
    data = open(img, "rb").read()
    idx = data.rfind(b"\xff\xd9")
    if idx != -1 and idx + 2 < len(data):
        extra = data[idx+2:]
        slow_print(f"{GREEN}[+] {len(extra)} bytes appended AFTER the image! Hidden payload likely.{RESET}")
        with open("results/appended_data.bin", "wb") as f:
            f.write(extra)
        slow_print(f"{GREEN}[+] Dumped: results/appended_data.bin (run: strings results/appended_data.bin){RESET}")
        found = True
    else:
        slow_print(f"{RED}[-] No appended data after EOI marker.{RESET}")

    if not found:
        slow_print(f"{YELLOW}[*] For deep stego also try: zsteg (PNG/BMP), stegsolve, https://stylesuxx.github.io/steganography/{RESET}")

# ============================================================
# MODULE 7: MANUAL FACE ENGINES
# ============================================================
def manual_face_search():
    slow_print(f"{CYAN}[*] Manual FACE search - paid engines{RESET}")
    slow_print(f"{WHITE}    The following paid engines have the largest face-matching databases:")
    print(f"{GREEN}    [1] PimEyes      : https://pimeyes.com")
    print(f"    [2] FaceCheck.ID : https://facecheck.id")
    print(f"    [3] Search4Faces : https://search4faces.com{RESET}")
    slow_print(f"{YELLOW}    Upload your image on one of these - they do face-matching across the whole web.{RESET}")

# ============================================================
# MAIN
# ============================================================
def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(BANNER)
    slow_print(f"{CYAN}      [1] Full flow (EXIF + Upload + All engines){RESET}")
    slow_print(f"{CYAN}      [2] Username pivot (Sherlock + Maigret){RESET}")
    slow_print(f"{CYAN}      [3] Manual face-search engines{RESET}")
    slow_print(f"{CYAN}      [4] Image forensics (ELA + strings + fingerprint){RESET}")
    slow_print(f"{CYAN}      [5] Hash fingerprint (MD5/SHA1/SHA256){RESET}")
    slow_print(f"{CYAN}      [6] Steganography check (steghide + appended data){RESET}")
    slow_print(f"{CYAN}      [0] Exit{RESET}\n")
    choice = input(f"{WHITE}  AnonFace >> {RESET}").strip()

    if choice == "1":
        img = input(f"{WHITE}[?] Image path (e.g. target.jpg): {RESET}").strip()
        if not os.path.isfile(img):
            slow_print(f"{RED}[-] Image not found at that path.{RESET}"); return
        exif_dump(img)
        url = upload_image(img)
        if url:
            open_engines(url)
        else:
            slow_print(f"{YELLOW}[*] Upload failed - open engines that accept manual upload:{RESET}")
            print(f"{GREEN}    Google Lens : https://lens.google.com  (drag & drop image)")
            print(f"    Yandex      : https://yandex.com/images/search  (click upload icon)")
            print(f"    Bing        : https://www.bing.com/images  (visual search icon)")
            print(f"    TinEye      : https://tineye.com  (upload button){RESET}")
    elif choice == "2":
        username_pivot()
    elif choice == "3":
        manual_face_search()
    elif choice == "4":
        img = input(f"{WHITE}[?] Image path: {RESET}").strip()
        if os.path.isfile(img): image_forensics(img)
        else: slow_print(f"{RED}[-] Image not found.{RESET}")
    elif choice == "5":
        img = input(f"{WHITE}[?] Image path: {RESET}").strip()
        if os.path.isfile(img): hash_fingerprint(img)
        else: slow_print(f"{RED}[-] Image not found.{RESET}")
    elif choice == "6":
        img = input(f"{WHITE}[?] Image path: {RESET}").strip()
        if os.path.isfile(img): stego_check(img)
        else: slow_print(f"{RED}[-] Image not found.{RESET}")
    elif choice == "0":
        slow_print(f"{RED}[~] Exiting... AnonFace out.{RESET}"); sys.exit(0)

if __name__ == "__main__":
    main()