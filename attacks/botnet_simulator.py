#!/usr/bin/env python3
"""
Botnet Traffic Simulator
Simulates botnet command and control (C&C) traffic patterns
"""

import socket
import threading
import time
import random
import requests
from scapy.all import *

class BotnetSimulator:
    def __init__(self):
        self.running = False
        self.c2_servers = [
            "192.168.1.100",
            "10.0.0.50",
            "172.16.0.10"
        ]
        self.bot_ips = [
            f"192.168.1.{random.randint(10, 250)}" for _ in range(20)
        ]
        
    def generate_dns_queries(self):
        """Generate suspicious DNS queries (DGA - Domain Generation Algorithm)"""
        tlds = ['.com', '.net', '.org', '.info', '.biz']
        
        while self.running:
            try:
                # Generate random domain name (DGA-like)
                domain_length = random.randint(8, 20)
                domain = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=domain_length))
                domain += random.choice(tlds)
                
                # Create DNS query
                src_ip = random.choice(self.bot_ips)
                packet = IP(src=src_ip, dst="8.8.8.8") / \
                        UDP(sport=random.randint(1024, 65535), dport=53) / \
                        DNS(rd=1, qd=DNSQR(qname=domain))
                
                send(packet, verbose=0)
                time.sleep(random.uniform(1, 5))
                
            except Exception as e:
                print(f"Error in DNS queries: {e}")
                break
    
    def c2_communication(self):
        """Simulate C&C server communication"""
        while self.running:
            try:
                src_ip = random.choice(self.bot_ips)
                c2_ip = random.choice(self.c2_servers)
                
                # Heartbeat packets
                packet = IP(src=src_ip, dst=c2_ip) / \
                        TCP(sport=random.randint(1024, 65535), dport=8080, flags="PA") / \
                        Raw(load=b"HEARTBEAT|" + os.urandom(16))
                
                send(packet, verbose=0)
                
                # Simulate response from C&C
                time.sleep(0.5)
                response = IP(src=c2_ip, dst=src_ip) / \
                          TCP(sport=8080, dport=packet[TCP].sport, flags="PA") / \
                          Raw(load=b"CMD|" + os.urandom(32))
                
                send(response, verbose=0)
                
                time.sleep(random.uniform(30, 120))  # Periodic communication
                
            except Exception as e:
                print(f"Error in C&C communication: {e}")
                break
    
    def data_exfiltration(self):
        """Simulate data exfiltration"""
        while self.running:
            try:
                src_ip = random.choice(self.bot_ips)
                external_ip = f"{random.randint(1, 223)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
                
                # Large data transfer
                payload_size = random.randint(1024, 8192)
                payload = os.urandom(payload_size)
                
                packet = IP(src=src_ip, dst=external_ip) / \
                        TCP(sport=random.randint(1024, 65535), dport=443, flags="PA") / \
                        Raw(load=payload)
                
                send(packet, verbose=0)
                time.sleep(random.uniform(10, 30))
                
            except Exception as e:
                print(f"Error in data exfiltration: {e}")
                break
    
    def p2p_communication(self):
        """Simulate peer-to-peer botnet communication"""
        while self.running:
            try:
                # Random peer-to-peer communication
                src_ip = random.choice(self.bot_ips)
                dst_ip = random.choice(self.bot_ips)
                
                if src_ip != dst_ip:
                    # P2P update/command sharing
                    packet = IP(src=src_ip, dst=dst_ip) / \
                            UDP(sport=random.randint(1024, 65535), dport=random.randint(6000, 7000)) / \
                            Raw(load=b"P2P_UPDATE|" + os.urandom(64))
                    
                    send(packet, verbose=0)
                
                time.sleep(random.uniform(5, 15))
                
            except Exception as e:
                print(f"Error in P2P communication: {e}")
                break
    
    def port_scanning(self):
        """Simulate automated port scanning from bots"""
        while self.running:
            try:
                src_ip = random.choice(self.bot_ips)
                target_ip = "127.0.0.1"
                
                # Scan common ports
                common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5900]
                
                for port in random.sample(common_ports, 5):
                    packet = IP(src=src_ip, dst=target_ip) / \
                            TCP(sport=random.randint(1024, 65535), dport=port, flags="S")
                    
                    send(packet, verbose=0)
                    time.sleep(0.1)
                
                time.sleep(random.uniform(60, 180))  # Scan every 1-3 minutes
                
            except Exception as e:
                print(f"Error in port scanning: {e}")
                break
    
    def start_simulation(self, duration=300):
        """Start botnet simulation"""
        print("Starting Botnet Traffic Simulation")
        print(f"Duration: {duration} seconds")
        print(f"Simulated bots: {len(self.bot_ips)}")
        print(f"C&C servers: {len(self.c2_servers)}")
        
        self.running = True
        
        # Start different botnet activities
        activities = [
            threading.Thread(target=self.generate_dns_queries, daemon=True),
            threading.Thread(target=self.c2_communication, daemon=True),
            threading.Thread(target=self.data_exfiltration, daemon=True),
            threading.Thread(target=self.p2p_communication, daemon=True),
            threading.Thread(target=self.port_scanning, daemon=True)
        ]
        
        for activity in activities:
            activity.start()
        
        # Run simulation
        time.sleep(duration)
        
        # Stop simulation
        self.running = False
        print("\nBotnet simulation completed")

if __name__ == "__main__":
    botnet = BotnetSimulator()
    botnet.start_simulation(duration=180)  # Run for 3 minutes