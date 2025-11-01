#!/usr/bin/env python3
"""
Example script demonstrating MITM proxy usage
For educational purposes only
"""

import requests
import time

def test_proxy():
    """Test the MITM proxy with a simple HTTP request"""

    # Configure proxy
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }

    print("[*] Testing MITM Proxy")
    print("[*] Make sure the proxy is running on port 8080")
    print()

    try:
        # Test HTTP request
        print("[+] Sending test HTTP request through proxy...")
        response = requests.get(
            'http://httpbin.org/get',
            proxies=proxies,
            timeout=10
        )

        print(f"[+] Response Status: {response.status_code}")
        print(f"[+] Response received, check PCAP file for captured traffic")

    except requests.exceptions.ProxyError:
        print("[!] Could not connect to proxy. Is it running?")
    except requests.exceptions.ConnectionError:
        print("[!] Connection error. Check your network connection.")
    except Exception as e:
        print(f"[!] Error: {e}")


if __name__ == '__main__':
    test_proxy()
