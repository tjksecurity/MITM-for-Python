#!/usr/bin/env python3
"""
MITM Proxy with PCAP Export
WARNING: Use only for authorized security testing, penetration testing,
CTF challenges, or educational purposes. Unauthorized interception of
network traffic is illegal.
"""

import socket
import threading
import argparse
import sys
import time
from datetime import datetime

# Disable IPv6 in scapy to avoid environment issues
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# Import only what we need from scapy to avoid IPv6 issues
try:
    from scapy.utils import wrpcap
    from scapy.packet import Packet
    from scapy.layers.l2 import Ether
    from scapy.layers.inet import IP, TCP, UDP
    from scapy.packet import Raw
    from scapy import config
    config.conf.ipv6_enabled = False
except KeyError:
    # Ignore IPv6 route errors
    pass

class MITMProxy:
    def __init__(self, listen_host='0.0.0.0', listen_port=8080, buffer_size=4096):
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.buffer_size = buffer_size
        self.packets = []
        self.running = False
        self.packet_count = 0
        self.pcap_file = f"mitm_capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"

    def create_packet(self, data, src_ip, dst_ip, src_port, dst_port, protocol='TCP'):
        """Create a Scapy packet from raw data"""
        try:
            # Create basic IP packet
            pkt = Ether() / IP(src=src_ip, dst=dst_ip)

            if protocol == 'TCP':
                pkt = pkt / TCP(sport=src_port, dport=dst_port)
            elif protocol == 'UDP':
                pkt = pkt / UDP(sport=src_port, dport=dst_port)

            # Add raw data payload
            if data:
                pkt = pkt / Raw(load=data)

            return pkt
        except Exception as e:
            print(f"[!] Error creating packet: {e}")
            return None

    def save_packet(self, packet):
        """Save packet to list for PCAP export"""
        if packet:
            self.packets.append(packet)
            self.packet_count += 1

    def export_pcap(self):
        """Export captured packets to PCAP file"""
        if self.packets:
            try:
                wrpcap(self.pcap_file, self.packets)
                print(f"\n[+] Captured {len(self.packets)} packets")
                print(f"[+] PCAP file saved: {self.pcap_file}")
            except Exception as e:
                print(f"[!] Error saving PCAP: {e}")
        else:
            print("[!] No packets captured")

    def handle_client(self, client_socket, client_address):
        """Handle individual client connection"""
        try:
            # Receive the request from client
            request = client_socket.recv(self.buffer_size)

            if not request:
                client_socket.close()
                return

            # Parse the HTTP request to get destination
            first_line = request.split(b'\n')[0]
            url = first_line.split(b' ')[1]

            # Find the position of http:// or https://
            http_pos = url.find(b'://')
            if http_pos == -1:
                temp = url
            else:
                temp = url[(http_pos + 3):]

            # Find the port position (if any)
            port_pos = temp.find(b':')

            # Find the end of web server
            webserver_pos = temp.find(b'/')
            if webserver_pos == -1:
                webserver_pos = len(temp)

            # Get webserver and port
            if port_pos == -1 or webserver_pos < port_pos:
                port = 80
                webserver = temp[:webserver_pos]
            else:
                port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
                webserver = temp[:port_pos]

            print(f"[+] {client_address[0]}:{client_address[1]} -> {webserver.decode('utf-8', errors='ignore')}:{port}")

            # Create packet for request
            pkt = self.create_packet(
                request,
                client_address[0],
                webserver.decode('utf-8', errors='ignore'),
                client_address[1],
                port
            )
            self.save_packet(pkt)

            # Connect to destination server
            try:
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.settimeout(10)
                server_socket.connect((webserver, port))
                server_socket.sendall(request)

                # Receive response from server
                while True:
                    response = server_socket.recv(self.buffer_size)
                    if len(response) > 0:
                        # Save response packet
                        resp_pkt = self.create_packet(
                            response,
                            webserver.decode('utf-8', errors='ignore'),
                            client_address[0],
                            port,
                            client_address[1]
                        )
                        self.save_packet(resp_pkt)

                        # Forward to client
                        client_socket.sendall(response)
                    else:
                        break

                server_socket.close()

            except socket.timeout:
                print(f"[!] Connection timeout to {webserver.decode('utf-8', errors='ignore')}")
            except Exception as e:
                print(f"[!] Error connecting to server: {e}")

        except Exception as e:
            print(f"[!] Error handling client: {e}")
        finally:
            client_socket.close()

    def start(self):
        """Start the MITM proxy server"""
        try:
            # Create socket
            proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind and listen
            proxy_socket.bind((self.listen_host, self.listen_port))
            proxy_socket.listen(5)

            self.running = True

            print(f"[*] MITM Proxy started on {self.listen_host}:{self.listen_port}")
            print(f"[*] PCAP file will be saved as: {self.pcap_file}")
            print("[*] Press Ctrl+C to stop and save capture\n")

            while self.running:
                try:
                    client_socket, client_address = proxy_socket.accept()

                    # Handle each client in a separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()

                except KeyboardInterrupt:
                    print("\n[*] Stopping proxy...")
                    self.running = False
                    break
                except Exception as e:
                    if self.running:
                        print(f"[!] Error accepting connection: {e}")

            proxy_socket.close()

        except Exception as e:
            print(f"[!] Error starting proxy: {e}")
            sys.exit(1)
        finally:
            # Export captured packets
            self.export_pcap()


def print_banner():
    """Print banner with warnings"""
    banner = """
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
    """
    print(banner)


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description='MITM Proxy with PCAP export for authorized security testing'
    )
    parser.add_argument(
        '-H', '--host',
        default='0.0.0.0',
        help='Listen host (default: 0.0.0.0)'
    )
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=8080,
        help='Listen port (default: 8080)'
    )
    parser.add_argument(
        '-b', '--buffer',
        type=int,
        default=4096,
        help='Buffer size (default: 4096)'
    )

    args = parser.parse_args()

    # Create and start proxy
    proxy = MITMProxy(
        listen_host=args.host,
        listen_port=args.port,
        buffer_size=args.buffer
    )

    try:
        proxy.start()
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
        proxy.export_pcap()
        sys.exit(0)


if __name__ == '__main__':
    main()
