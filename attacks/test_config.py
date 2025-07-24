#!/usr/bin/env python3
"""
Test Configuration for Intrusion Detection System
Run this to test your localhost setup
"""

import socket
import subprocess
import sys
from scapy.all import *

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def test_basic_traffic():
    """Generate some basic test traffic to localhost"""
    print("Generating basic test traffic...")
    
    target_ip = "127.0.0.1"
    
    # Generate some HTTP-like traffic
    for i in range(10):
        try:
            # TCP SYN to port 80
            packet = IP(dst=target_ip) / TCP(dport=80, flags="S")
            send(packet, verbose=0)
            
            # HTTP request simulation
            http_packet = IP(dst=target_ip) / TCP(dport=80, flags="PA") / \
                         Raw(load=b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            send(http_packet, verbose=0)
            
            print(f"Sent packet {i+1}/10")
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error sending packet: {e}")
            break

def quick_attack_test(target_ip):
    """Quick attack simulation for testing"""
    print(f"Running quick attack test against {target_ip}")
    
    # Simulate suspicious activity
    suspicious_activities = [
        # Port scanning
        lambda: [send(IP(dst=target_ip) / TCP(dport=port, flags="S"), verbose=0) 
                for port in [21, 22, 23, 25, 53, 80, 135, 139, 443, 445]],
        
        # Potential DDoS
        lambda: [send(IP(dst=target_ip) / TCP(dport=80, flags="S"), verbose=0) 
                for _ in range(20)],
        
        # Suspicious DNS queries
        lambda: [send(IP(dst="8.8.8.8") / UDP(dport=53) / 
                     DNS(qd=DNSQR(qname=f"suspicious{i}.example.com")), verbose=0) 
                for i in range(5)]
    ]
    
    for i, activity in enumerate(suspicious_activities):
        print(f"Running test activity {i+1}/3...")
        try:
            activity()
            time.sleep(2)
        except Exception as e:
            print(f"Error in activity {i+1}: {e}")

def main():
    print("=== IDS Test Configuration ===")
    
    # Get network information
    local_ip = get_local_ip()
    print(f"Local IP address: {local_ip}")
    print(f"Localhost: 127.0.0.1")
    
    # Check if running as root/admin
    try:
        # Try to create a raw socket
        socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        print("✓ Running with sufficient privileges")
    except PermissionError:
        print("✗ Need to run with sudo/administrator privileges")
        print("  Run: sudo python3 test_config.py")
        return
    
    # Test basic connectivity
    print("\n=== Testing Basic Traffic Generation ===")
    test_basic_traffic()
    
    print("\n=== Configuration Recommendations ===")
    print("For your simulation scripts, use:")
    print(f"TARGET_IP = '127.0.0.1'  # For localhost testing")
    print(f"# OR")
    print(f"TARGET_IP = '{local_ip}'  # For local network testing")
    
    # Quick attack test
    choice = input("\nRun quick attack test? (y/n): ").lower()
    if choice == 'y':
        target = input(f"Target IP (default: 127.0.0.1): ").strip() or "127.0.0.1"
        quick_attack_test(target)
    
    print("\n=== Setup Complete ===")
    print("Your IDS should now be detecting the generated traffic.")
    print("Check your Flask app at http://localhost:5000")

if __name__ == "__main__":
    main()