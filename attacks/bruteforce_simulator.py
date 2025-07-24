#!/usr/bin/env python3
"""
Brute Force Attack Simulator
Simulates SSH-Patator and FTP-Patator attacks
"""

import socket
import threading
import time
import random
from scapy.all import *
import paramiko
import ftplib

class BruteForceSimulator:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.running = False
        
        # Common usernames and passwords for brute force
        self.usernames = [
            'admin', 'administrator', 'root', 'user', 'test', 'guest',
            'oracle', 'postgres', 'mysql', 'ftp', 'www', 'mail',
            'service', 'operator', 'manager', 'support', 'demo'
        ]
        
        self.passwords = [
            'password', '123456', 'admin', 'root', 'test', 'guest',
            'password123', '1234', 'qwerty', 'abc123', 'letmein',
            'welcome', 'monkey', 'dragon', 'pass', 'master',
            '', 'login', 'administrator', 'passw0rd', '12345678'
        ]
    
    def ssh_brute_force(self):
        """Simulate SSH brute force attack (SSH-Patator)"""
        print(f"Starting SSH brute force against {self.target_ip}:22")
        
        attempt_count = 0
        while self.running and attempt_count < 100:
            try:
                username = random.choice(self.usernames)
                password = random.choice(self.passwords)
                
                # Generate SSH connection attempt traffic
                src_port = random.randint(1024, 65535)
                
                # TCP SYN to port 22
                syn_packet = IP(src=get_if_addr(conf.iface), dst=self.target_ip) / \
                           TCP(sport=src_port, dport=22, flags="S", seq=random.randint(1000, 9000))
                send(syn_packet, verbose=0)
                
                # Simulate SSH handshake traffic
                time.sleep(0.1)
                
                # SSH protocol identification
                ssh_ident = IP(src=get_if_addr(conf.iface), dst=self.target_ip) / \
                          TCP(sport=src_port, dport=22, flags="PA") / \
                          Raw(load=b"SSH-2.0-OpenSSH_7.4\r\n")
                send(ssh_ident, verbose=0)
                
                # Key exchange and authentication attempts
                for i in range(3):  # Multiple packets per attempt
                    auth_packet = IP(src=get_if_addr(conf.iface), dst=self.target_ip) / \
                                TCP(sport=src_port, dport=22, flags="PA") / \
                                Raw(load=os.urandom(random.randint(50, 200)))
                    send(auth_packet, verbose=0)
                    time.sleep(0.05)
                
                # Connection termination
                fin_packet = IP(src=get_if_addr(conf.iface), dst=self.target_ip) / \
                           TCP(sport=src_port, dport=22, flags="FA")
                send(fin_packet, verbose=0)
                
                attempt_count += 1
                print(f"SSH attempt {attempt_count}: {username}:{password}")
                
                # Delay between attempts (realistic brute force timing)
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"Error in SSH brute force: {e}")
                break
    
    def ftp_brute_force(self):
        """Simulate FTP brute force attack (FTP-Patator)"""
        print(f"Starting FTP brute force against {self.target_ip}:21")
        
        attempt_count = 0
        while self.running and attempt_count < 100:
            try:
                username = random.choice(self.usernames)
                password = random.choice(self.passwords)
                
                src_port = random.randint(1024, 65535)
                
                # TCP connection to FTP port
                syn_packet = IP(src=get_if_addr(conf.iface), dst=self.target_ip) / \
                           TCP(sport=src_port, dport=21, flags="S")
                send(syn_packet, verbose=0)
                
                time.sleep(0.1)
                
                # FTP commands simulation
                ftp_commands = [
                    f"USER {username}\r\n",
                    f"PASS {password}\r\n",
                    "QUIT\r\n"
                ]
                
                for cmd in ftp_commands:
                    ftp_packet = IP(src=get_if_addr(conf.iface), dst=self.target_ip) / \
                               TCP(sport=src_port, dport=21, flags="PA") / \
                               Raw(load=cmd.encode())
                    send(ftp_packet, verbose=0)
                    time.sleep(0.1)
                
                # Connection termination
                fin_packet = IP(src=get_if_addr(conf.iface), dst=self.target_ip) / \
                           TCP(sport=src_port, dport=21, flags="FA")
                send(fin_packet, verbose=0)
                
                attempt_count += 1
                print(f"FTP attempt {attempt_count}: {username}:{password}")
                
                time.sleep(random.uniform(0.5, 2))
                
            except Exception as e:
                print(f"Error in FTP brute force: {e}")
                break
    
    def telnet_brute_force(self):
        """Simulate Telnet brute force attack"""
        print(f"Starting Telnet brute force against {self.target_ip}:23")
        
        attempt_count = 0
        while self.running and attempt_count < 50:
            try:
                username = random.choice(self.usernames)
                password = random.choice(self.passwords)
                
                src_port = random.randint(1024, 65535)
                
                # TCP connection to Telnet port
                syn_packet = IP(src=get_if_addr(conf.iface), dst=self.target_ip) / \
                           TCP(sport=src_port, dport=23, flags="S")
                send(syn_packet, verbose=0)
                
                time.sleep(0.1)
                
                # Telnet negotiation and login simulation
                telnet_data = [
                    b"\xff\xfb\x01\xff\xfb\x03\xff\xfd\x03",  # Telnet negotiation
                    username.encode() + b"\r\n",
                    password.encode() + b"\r\n",
                    b"exit\r\n"
                ]
                
                for data in telnet_data:
                    telnet_packet = IP(src=get_if_addr(conf.iface), dst=self.target_ip) / \
                                  TCP(sport=src_port, dport=23, flags="PA") / \
                                  Raw(load=data)
                    send(telnet_packet, verbose=0)
                    time.sleep(0.2)
                
                # Connection termination
                fin_packet = IP(src=get_if_addr(conf.iface), dst=self.target_ip) / \
                           TCP(sport=src_port, dport=23, flags="FA")
                send(fin_packet, verbose=0)
                
                attempt_count += 1
                print(f"Telnet attempt {attempt_count}: {username}:{password}")
                
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"Error in Telnet brute force: {e}")
                break
    
    def web_brute_force(self):
        """Simulate web application brute force (login forms)"""
        print(f"Starting Web brute force against {self.target_ip}:80")
        
        attempt_count = 0
        while self.running and attempt_count < 75:
            try:
                username = random.choice(self.usernames)
                password = random.choice(self.passwords)
                
                src_port = random.randint(1024, 65535)
                
                # HTTP POST request simulation
                post_data = f"username={username}&password={password}&submit=Login"
                http_request = f"POST /login HTTP/1.1\r\n" \
                             f"Host: {self.target_ip}\r\n" \
                             f"Content-Type: application/x-www-form-urlencoded\r\n" \
                             f"Content-Length: {len(post_data)}\r\n" \
                             f"User-Agent: Mozilla/5.0 (compatible; BruteForcer)\r\n" \
                             f"Connection: close\r\n\r\n" \
                             f"{post_data}"
                
                # TCP connection and HTTP request
                syn_packet = IP(src=get_if_addr(conf.iface), dst=self.target_ip) / \
                           TCP(sport=src_port, dport=80, flags="S")
                send(syn_packet, verbose=0)
                
                time.sleep(0.1)
                
                http_packet = IP(src=get_if_addr(conf.iface), dst=self.target_ip) / \
                            TCP(sport=src_port, dport=80, flags="PA") / \
                            Raw(load=http_request.encode())
                send(http_packet, verbose=0)
                
                time.sleep(0.1)
                
                # Connection close
                fin_packet = IP(src=get_if_addr(conf.iface), dst=self.target_ip) / \
                           TCP(sport=src_port, dport=80, flags="FA")
                send(fin_packet, verbose=0)
                
                attempt_count += 1
                print(f"Web attempt {attempt_count}: {username}:{password}")
                
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                print(f"Error in Web brute force: {e}")
                break
    
    def start_attack(self, attack_type="ssh", duration=120):
        """Start brute force attack simulation"""
        print(f"Starting {attack_type.upper()} brute force simulation")
        print(f"Target: {self.target_ip}")
        print(f"Duration: {duration} seconds")
        
        self.running = True
        
        # Choose attack method
        attack_methods = {
            "ssh": self.ssh_brute_force,
            "ftp": self.ftp_brute_force,
            "telnet": self.telnet_brute_force,
            "web": self.web_brute_force
        }
        
        if attack_type.lower() not in attack_methods:
            print("Invalid attack type. Use 'ssh', 'ftp', 'telnet', or 'web'")
            return
        
        # Start attack in thread
        attack_thread = threading.Thread(target=attack_methods[attack_type.lower()], daemon=True)
        attack_thread.start()
        
        # Run for specified duration
        time.sleep(duration)
        
        # Stop attack
        self.running = False
        print(f"\n{attack_type.upper()} brute force simulation completed")

if __name__ == "__main__":
    TARGET_IP = "127.0.0.1"  # Change to your target IP
    
    brute_force = BruteForceSimulator(TARGET_IP)
    
    print("=== Brute Force Attack Simulation ===")
    
    # Test different brute force attacks
    brute_force.start_attack("ssh", 60)
    time.sleep(5)
    
    brute_force.start_attack("ftp", 60)
    time.sleep(5)
    
    brute_force.start_attack("web", 60)