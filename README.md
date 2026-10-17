# -Image-OSINT-Recon-Tool 

# ═══════════════════════════════════════════════
#   ANONFACE - Image OSINT Recon Tool v1.2
# ═══════════════════════════════════════════════

<p align="center">
  <b>Created by:</b> Mr.virus138 Team<br>
  <b>Team:</b> The Anonymous Tanzania Hackers<br>
  <b>Cooperation:</b> Binno World Hacker
</p>

---

## ⚠️ DISCLAIMER
This tool is for **educational purposes and authorized OSINT investigations only**.
The authors are not responsible for any misuse. Use responsibly and legally.

---

## 📖 ABOUT

**AnonFace** is an Image-based OSINT (Open Source Intelligence) recon tool.
Give it a photo of a target and it helps you:

- Extract hidden metadata (EXIF / GPS / device info)
- Run the image through all major reverse-image search engines
- Pivot from a username to 300+ social media accounts
- Perform image forensics (detect edits & editing software)
- Fingerprint the image with hashes for breach-database lookups
- Detect hidden data inside the image (steganography)

---

## 🧩 MODULES

| # | Module | Description |
|---|--------|-------------|
| 1 | Full Flow | EXIF dump → upload to public host → open all search engines |
| 2 | Username Pivot | Sherlock + Maigret scan 300+ social media sites |
| 3 | Face Engines | Links to PimEyes, FaceCheck.ID, Search4Faces (paid face-matching) |
| 4 | Image Forensics | ELA (Error Level Analysis), embedded strings scan, JPEG quantization fingerprint |
| 5 | Hash Fingerprint | MD5 / SHA1 / SHA256 (saved to `results/hashes.txt`) |
| 6 | Steganography Check | steghide extraction + appended-data detection after JPEG EOI marker |

---

## 🖥️ SUPPORTED OS

- ✅ Kali Linux / Ubuntu / Debian (recommended)
- ✅ Termux (Android)
- ✅ Windows (with Python + Git Bash)
- ✅ macOS

---

## 📦 REQUIREMENTS

### System packages

```bash
sudo apt update
sudo apt install -y exiftool steghide curl strings xdg-utils

On Termux: pkg install exiftool steghide curl libimage-exiftool-perl

pip install Pillow
pip install sherlock     # username pivot
pip install maigret      # deep username intel

Python 3.8+ required.


🚀 INSTALLATION
git clone
cd image-Osint-Recon
chmod +x osintv1.py
Then install the requirements above (System packages + Python packages).

Example session

AnonFace >> 1
[?] Image path (e.g. target.jpg): /home/user/Downloads/target.jpeg
[*] Dumping EXIF metadata...
[*] Uploading image to public host...
[+] Hosted on catbox.moe: https://files.catbox.moe/abc123.jpeg
[*] Preparing all search engines for this image...
    Open all in browser? [y/N]: y

Results are saved in the results/ folder:

results/ela_output.png — Error Level Analysis image
results/hashes.txt — MD5/SHA1/SHA256 fingerprints
results/sherlock_<user>.txt — social media accounts found
results/maigret_<user>/report.html — deep profile report
results/appended_data.bin — hidden data extracted from stego

🔍 RECOMMENDED WORKFLOW (REAL OSINT)

Photo
  │
  ├─→ [1] Full Flow (EXIF → upload → Yandex/Lens/Bing/TinEye)
  │        └─ Find original source / first upload / profiles
  │
  ├─→ [4] Forensics (is the photo edited? which software?)
  │
  ├─→ [3] Face engines (PimEyes / FaceCheck for face-matching)
  │        └─ Get usernames & profile URLs
  │
  ├─→ [2] Username Pivot (Sherlock + Maigret → all accounts)
  │
  └─→ [5] Hashes → search VirusTotal / breach databases

🌐 SEARCH ENGINES USED

Engine	Best for
Yandex	Faces (best in the world for faces)
Google Lens	Context, objects, pages
Bing Visual	Social pages
TinEye	First appearance of an image
Baidu Image	Asian platforms
Karma Decay	Reddit reposts


👥 CREDITS

Created by : Mr.virus138 Team
Team       : The Anonymous Tanzania Hackers
Coop       : Binno World Hacker



