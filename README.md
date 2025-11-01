# MITM-for-Python

A simple man-in-the-middle proxy script in Python that captures network traffic and exports to a PCAP file in the same directory.

## ⚠️ Legal Warning

**FOR AUTHORIZED USE ONLY**

This tool is intended for:
- ✅ Authorized security testing and penetration testing engagements
- ✅ Educational purposes and cybersecurity learning
- ✅ CTF (Capture The Flag) challenges and competitions
- ✅ Network debugging and analysis with proper authorization
- ✅ Security research in controlled environments

**Unauthorized interception of network traffic is ILLEGAL** and may violate:
- Computer Fraud and Abuse Act (CFAA)
- Electronic Communications Privacy Act (ECPA)
- Similar laws in your jurisdiction

Always obtain explicit written permission before testing any network or system you do not own.

## Features

- 🔍 HTTP/HTTPS proxy with traffic interception
- 📦 Automatic PCAP file generation
- 🧵 Multi-threaded connection handling
- ⚙️ Configurable host, port, and buffer settings
- 📊 Real-time connection logging
- 💾 Exports captured packets for analysis with Wireshark

## Requirements

- Python 3.6+
- Scapy library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tjksecurity/MITM-for-Python.git
cd MITM-for-Python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install scapy
```

## Usage

### Basic Usage

Start the proxy on default port (8080):
```bash
sudo python3 mitm_proxy.py
```

**Note:** Root/sudo privileges may be required for packet capture.

### Advanced Usage

Specify custom host and port:
```bash
sudo python3 mitm_proxy.py -H 127.0.0.1 -p 9090
```

All available options:
```bash
sudo python3 mitm_proxy.py -h
```

Options:
- `-H, --host`: Listen host (default: 0.0.0.0)
- `-p, --port`: Listen port (default: 8080)
- `-b, --buffer`: Buffer size (default: 4096)

### Configuring Browser/Client

To use the MITM proxy, configure your browser or application to use it:

1. **Firefox:**
   - Settings → Network Settings → Manual proxy configuration
   - HTTP Proxy: `127.0.0.1`, Port: `8080`

2. **Chrome/Edge:**
   - Settings → System → Open proxy settings
   - Set HTTP proxy to `127.0.0.1:8080`

3. **Command Line (curl):**
```bash
curl --proxy http://127.0.0.1:8080 http://example.com
```

### Stopping the Proxy

Press `Ctrl+C` to stop the proxy. The captured packets will automatically be exported to a PCAP file.

## Output

The proxy will create a PCAP file with a timestamp:
```
mitm_capture_20231101_143052.pcap
```

This file can be analyzed using:
- **Wireshark**: `wireshark mitm_capture_*.pcap`
- **tcpdump**: `tcpdump -r mitm_capture_*.pcap`
- **tshark**: `tshark -r mitm_capture_*.pcap`

## Example Output

```
╔═══════════════════════════════════════════════════════════╗
║           MITM Proxy with PCAP Export                     ║
║                                                           ║
║  WARNING: For authorized use only!                       ║
║  - Security testing with proper authorization            ║
║  - Educational purposes and learning                     ║
║  - CTF challenges and competitions                       ║
║  - Penetration testing engagements                       ║
║                                                           ║
║  Unauthorized interception is ILLEGAL                    ║
╚═══════════════════════════════════════════════════════════╝

[*] MITM Proxy started on 0.0.0.0:8080
[*] PCAP file will be saved as: mitm_capture_20231101_143052.pcap
[*] Press Ctrl+C to stop and save capture

[+] 192.168.1.100:54321 -> example.com:80
[+] 192.168.1.100:54322 -> api.example.com:80
```

## How It Works

1. **Proxy Server**: Listens for incoming HTTP connections
2. **Request Interception**: Captures client requests
3. **Packet Creation**: Converts traffic to Scapy packets
4. **Forwarding**: Forwards requests to destination servers
5. **Response Capture**: Captures server responses
6. **PCAP Export**: Saves all packets to PCAP file

## Limitations

- Currently supports HTTP traffic (not HTTPS with SSL/TLS decryption)
- For HTTPS interception, SSL/TLS certificate manipulation is required
- Some applications may detect and block proxy connections

## Future Enhancements

- [ ] SSL/TLS interception with certificate generation
- [ ] DNS spoofing capabilities
- [ ] Traffic modification and injection
- [ ] Web-based dashboard for real-time monitoring
- [ ] Filtering and pattern matching
- [ ] Multiple output formats

## Contributing

Contributions are welcome! Please ensure all contributions maintain the tool's focus on authorized security testing and education.

## Disclaimer

The authors and contributors of this project are not responsible for any misuse or damage caused by this tool. Use responsibly and ethically.

## License

MIT License - See LICENSE file for details

## Educational Resources

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Wireshark Documentation](https://www.wireshark.org/docs/)
- [Scapy Documentation](https://scapy.readthedocs.io/)

---

**Remember:** Always get permission before testing!
