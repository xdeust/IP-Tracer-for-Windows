#!/usr/bin/env python3
"""
IP-Tracer — Terminal-based IP Geolocation Tool
Author: xdeust
Version: 1.0
"""

import os
import re
import sys
import time
import socket
import requests
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama with autoreset
init(autoreset=True)

# ─── Constants ───────────────────────────────────────────────────────────────

BANNER = r"""
  ___  ____        _____
 |_ _||  _ \      |_   _| __ __ _  ___ ___ _ __
  | | | |_) |_____ | || '__/ _` |/ __/ _ \ '__|
  | | |  __/_____| | || | | (_| | (_|  __/ |
 |___||_|          |_||_|  \__,_|\___\___|_|
"""

SEPARATOR = "  " + "=" * 48

IP_API_URL = "http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
PUBLIC_IP_URL = "https://api.ipify.org?format=json"

# Regex pattern for a valid IPv4 address
IPV4_PATTERN = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)


# ─── Helper Functions ────────────────────────────────────────────────────────

def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    """Print the ASCII art banner and subtitle."""
    print(Fore.CYAN + BANNER)
    print(Fore.YELLOW + "         Coded by xdeust | IP Geolocation Tool")
    print(Fore.BLUE + SEPARATOR)


def spinner(message: str, duration: float = 1.5):
    """
    Show a spinning loading animation for the given duration.
    Characters cycle through: | / - \\
    """
    spin_chars = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    idx = 0
    while time.time() < end_time:
        sys.stdout.write(
            f"\r  {Fore.CYAN}[*]{Style.RESET_ALL} {message} {spin_chars[idx % len(spin_chars)]}"
        )
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1
    # Clear the spinner line
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()


def validate_ip(ip: str) -> bool:
    """Return True if `ip` is a valid IPv4 address."""
    return bool(IPV4_PATTERN.match(ip))


def get_public_ip() -> str | None:
    """Fetch the user's own public IP address via ipify."""
    try:
        response = requests.get(PUBLIC_IP_URL, timeout=10)
        response.raise_for_status()
        return response.json().get("ip")
    except requests.ConnectionError:
        print(f"\n  {Fore.RED}[-] No internet connection. Please check your network.{Style.RESET_ALL}")
        return None
    except requests.RequestException as exc:
        print(f"\n  {Fore.RED}[-] Failed to fetch your public IP: {exc}{Style.RESET_ALL}")
        return None


def fetch_ip_data(ip: str) -> dict | None:
    """Query ip-api.com for geolocation data about the given IP."""
    try:
        url = IP_API_URL.replace("{ip}", ip)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "fail":
            msg = data.get("message", "Unknown error")
            print(f"\n  {Fore.RED}[-] API error: {msg}{Style.RESET_ALL}")
            return None

        return data

    except requests.ConnectionError:
        print(f"\n  {Fore.RED}[-] No internet connection. Please check your network.{Style.RESET_ALL}")
        return None
    except requests.RequestException as exc:
        print(f"\n  {Fore.RED}[-] Request failed: {exc}{Style.RESET_ALL}")
        return None


def current_datetime_str() -> str:
    """Return the current local date & time formatted like: April 21, 2020, 5:35 pm."""
    now = datetime.now()
    # %-I is platform-dependent; use lstrip("0") for cross-platform support
    hour = now.strftime("%I").lstrip("0")
    minute = now.strftime("%M")
    ampm = now.strftime("%p").lower()
    date_part = now.strftime("%B %d, %Y").replace(" 0", " ")
    return f"{date_part}, {hour}:{minute} {ampm}"


def display_results(data: dict):
    """Pretty-print the geolocation results with colors."""
    dt = current_datetime_str()
    lat = data.get("lat", "N/A")
    lon = data.get("lon", "N/A")

    fields = [
        ("IP Address", data.get("query", "N/A")),
        ("Country Code", data.get("countryCode", "N/A")),
        ("Country", data.get("country", "N/A")),
        ("Date & Time", dt),
        ("Region Code", data.get("region", "N/A")),
        ("Region", data.get("regionName", "N/A")),
        ("City", data.get("city", "N/A")),
        ("Zip Code", data.get("zip", "N/A")),
        ("Time Zone", data.get("timezone", "N/A")),
        ("ISP", data.get("isp", "N/A")),
        ("Organization", data.get("org", "N/A")),
        ("ASN", data.get("as", "N/A")),
        ("Latitude", str(lat)),
        ("Longitude", str(lon)),
        ("Location", f"{lat}, {lon}"),
    ]

    print()
    print(Fore.BLUE + SEPARATOR)
    print()

    for label, value in fields:
        print(
            f"  {Fore.CYAN}{label:<14}{Fore.YELLOW} > "
            f" {Style.BRIGHT}{Fore.WHITE}{value}{Style.RESET_ALL}"
        )

    print()
    print(Fore.BLUE + SEPARATOR)
    print(f"  {Fore.GREEN}[+] Trace completed successfully.")
    print(Fore.BLUE + SEPARATOR)


# ─── Main Loop ───────────────────────────────────────────────────────────────

def main():
    """Entry point — runs the trace loop."""
    while True:
        clear_screen()
        print_banner()
        print()

        # ── Get target IP ────────────────────────────────────────────────
        while True:
            target = input(
                f"  {Fore.YELLOW}[?]{Style.RESET_ALL} Enter target IP "
                f"(leave blank for your own IP): "
            ).strip()

            if target == "":
                # Fetch user's own public IP
                spinner("Fetching your public IP...")
                target = get_public_ip()
                if target is None:
                    # Error already printed; ask again
                    continue
                break

            if validate_ip(target):
                break

            print(
                f"\n  {Fore.RED}[-] Invalid IP address format. "
                f"Please try again.{Style.RESET_ALL}\n"
            )

        # ── Fetch & display data ─────────────────────────────────────────
        spinner("Fetching data...")
        data = fetch_ip_data(target)

        if data:
            display_results(data)
        # If data is None, the error was already printed by fetch_ip_data.

        # ── Ask to continue ──────────────────────────────────────────────
        print()
        again = input(
            f"  {Fore.YELLOW}[?]{Style.RESET_ALL} Trace another IP? (y/n): "
        ).strip().lower()

        if again != "y":
            print(f"\n  {Fore.GREEN}[+] Goodbye! Thanks for using IP-Tracer.{Style.RESET_ALL}\n")
            break


if __name__ == "__main__":
    main()
