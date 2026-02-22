<div align="center">
  
# 🌍 IP-Tracer V2 🌍

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python%203-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Version-1.0-brightgreen?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License">
  <img src="https://img.shields.io/badge/Author-xdeust-red?style=for-the-badge&logo=github" alt="Author">
</p>

**A powerfully simple, terminal-based IP Geolocation Tracer program.** 🕵️‍♂️💻  
*Easily gather detailed information about any given IP address or even your own!*

</div>

---

## 📝 Description

**IP-Tracer V2** is a fast and comprehensive command-line tool written in Python. It fetches detailed geolocation data, network information, and ISP details for any given IPv4 address. Its colorful and user-friendly interface makes it the perfect tool for network administrators, developers, and cybersecurity enthusiasts. 🛠️✨

## ✨ Features

- 🎯 **Accurate Geolocation:** Finds the country, region, city, zip code, and coordinates (latitude & longitude) of any IP.
- 🏢 **Network Info:** Displays ISP (Internet Service Provider) and ASN details.
- 🎨 **Colored Interface:** Beautiful, easy-to-read colored terminal output using `colorama`.
- 🔄 **Loop Mode:** Keeps asking for multiple IPs sequentially without restarting the program.
- 🛡️ **Validation & Error Handling:** Validates your IPv4 inputs and gracefully handles API/Connection errors.
- ⌛ **Loading Animations:** Includes a sleek terminal spinner while fetching data.

---

## 🚀 Installation

Ensure you have [Python 3](https://www.python.org/downloads/) installed on your system. 

1. **Clone the repository:**
   ```bash
   git clone https://github.com/xdeust/IP-Tracer-V2.git
   cd IP-Tracer-V2
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

Running the script is incredibly simple:

```bash
python ip_tracer.py
```

*Tip: If you leave the input blank, the tool will automatically fetch and trace your own public IP!* 🌐

---

## 📦 Build Executable (Windows)

Want to turn this script into a standalone `.exe` file? No problem! 

Just run the included batch file:
```bash
setup.bat
```
*(Note: It may be named `build.bat` depending on your version)*

Or you can compile it manually using PyInstaller:
```bash
pyinstaller --onefile --console --name "IP-Tracer" ip_tracer.py
```

---

## 👨‍💻 Author

Created with ❤️ by **[xdeust](https://github.com/xdeust)**.

## 📜 License

This project is licensed under the **MIT License**. For more details, see the [LICENSE](LICENSE) file. 📝
