from typing import List, Dict
import ssl
import socket
from urllib.parse import urlparse

SUSPICIOUS_TLDS = ['tk', 'ml', 'ga', 'cf']

def _check_https(url: str) -> Dict:
    if url.startswith('https://'):
        return {"name": "HTTPS Enabled", "passed": True, "detail": "Site uses secure HTTPS connection."}
    return {"name": "HTTPS Enabled", "passed": False, "detail": "Site does not use HTTPS (not secure)."}

def _check_ssl_cert(url: str) -> Dict:
    try:
        domain = urlparse(url).netloc
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                if cert:
                    return {"name": "SSL Certificate Valid", "passed": True, "detail": "Valid SSL certificate found."}
    except Exception as e:
        return {"name": "SSL Certificate Valid", "passed": False, "detail": f"SSL check skipped: {str(e)[:40]}"}
    return {"name": "SSL Certificate Valid", "passed": False, "detail": "No valid SSL certificate."}

def _check_domain_age(url: str) -> Dict:
    return {"name": "Domain Age", "passed": True, "detail": "Domain age check skipped (requires API key)."}

def _check_suspicious_tld(url: str) -> Dict:
    domain = urlparse(url).netloc.lower()
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(f".{tld}"):
            return {"name": "Suspicious TLD", "passed": False, "detail": f"Domain uses suspicious TLD: .{tld}"}
    return {"name": "Suspicious TLD", "passed": True, "detail": "Domain uses standard TLD."}

def check_trust(url: str) -> List[Dict]:
    return [_check_https(url), _check_ssl_cert(url), _check_suspicious_tld(url), _check_domain_age(url)]
