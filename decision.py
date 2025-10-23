"""
NeuroHoneypot - Decision Engine
Rule-based decision system that analyzes sessions and triggers orchestrator actions
"""
import json
import os
import requests
from datetime import datetime
from collections import defaultdict

ORCHESTRATOR_URL = "http://localhost:5001"

class DecisionEngine:
    def __init__(self):
        self.sessions = []
        self.ip_activity = defaultdict(list)
        
    def load_sessions(self):
        """Load sessions from JSONL file"""
        self.sessions = []
        if os.path.exists('data/sessions.jsonl'):
            with open('data/sessions.jsonl', 'r') as f:
                for line in f:
                    if line.strip():
                        session = json.loads(line.strip())
                        self.sessions.append(session)
                        self.ip_activity[session.get('ip')].append(session)
        return len(self.sessions)
    
    def analyze_session(self, session):
        """Analyze a single session and return threat assessment"""
        ip = session.get('ip', 'unknown')
        action = session.get('action', '')
        severity = session.get('severity', 'low')
        attack_type = session.get('attack_type', 'normal')
        
        threat_score = 0
        threats = []
        
        # Check for high severity actions
        if severity == 'critical':
            threat_score += 50
            threats.append('critical_severity')
        elif severity == 'high':
            threat_score += 30
            threats.append('high_severity')
        
        # Check for specific attack types
        if attack_type == 'sql_injection':
            threat_score += 40
            threats.append('sql_injection_detected')
        elif attack_type == 'command_injection':
            threat_score += 45
            threats.append('command_injection_detected')
        elif attack_type == 'path_traversal':
            threat_score += 35
            threats.append('path_traversal_detected')
        
        # Check for sensitive endpoint access
        if action in ['api_config_access', 'admin_access_success']:
            threat_score += 25
            threats.append('sensitive_access')
        
        # Check for failed login attempts
        if action == 'login_attempt':
            threat_score += 10
            threats.append('login_attempt')
        
        return {
            'ip': ip,
            'threat_score': threat_score,
            'threats': threats,
            'severity': severity,
            'attack_type': attack_type
        }
    
    def analyze_ip_behavior(self, ip):
        """Analyze overall behavior for an IP"""
        sessions = self.ip_activity.get(ip, [])
        
        if not sessions:
            return None
        
        total_requests = len(sessions)
        failed_logins = sum(1 for s in sessions if s.get('action') == 'login_attempt')
        sql_injections = sum(1 for s in sessions if s.get('attack_type') == 'sql_injection')
        cmd_injections = sum(1 for s in sessions if s.get('attack_type') == 'command_injection')
        path_traversals = sum(1 for s in sessions if s.get('attack_type') == 'path_traversal')
        
        threat_score = 0
        behaviors = []
        
        # High request volume
        if total_requests > 20:
            threat_score += 30
            behaviors.append('high_volume')
        
        # Multiple failed logins (brute force)
        if failed_logins > 5:
            threat_score += 40
            behaviors.append('brute_force_attempt')
        
        # SQL injection attempts
        if sql_injections > 0:
            threat_score += 50
            behaviors.append('sql_injection_pattern')
        
        # Command injection attempts
        if cmd_injections > 0:
            threat_score += 55
            behaviors.append('command_injection_pattern')
        
        # Path traversal attempts
        if path_traversals > 0:
            threat_score += 45
            behaviors.append('path_traversal_pattern')
        
        return {
            'ip': ip,
            'total_requests': total_requests,
            'threat_score': threat_score,
            'behaviors': behaviors,
            'failed_logins': failed_logins,
            'attack_attempts': sql_injections + cmd_injections + path_traversals
        }
    
    def decide_action(self, analysis):
        """Decide what action to take based on analysis"""
        actions = []
        
        threat_score = analysis.get('threat_score', 0)
        ip = analysis.get('ip')
        threats = analysis.get('threats', [])
        behaviors = analysis.get('behaviors', [])
        
        # Critical threat - block immediately
        if threat_score >= 80:
            actions.append({
                'type': 'block_ip',
                'ip': ip,
                'reason': f"Critical threat score: {threat_score}"
            })
            actions.append({
                'type': 'alert',
                'severity': 'critical',
                'message': f"IP {ip} blocked due to critical threat",
                'details': analysis
            })
        
        # High threat - rate limit and alert
        elif threat_score >= 50:
            actions.append({
                'type': 'rate_limit',
                'ip': ip,
                'limit': 5,
                'reason': f"High threat score: {threat_score}"
            })
            actions.append({
                'type': 'alert',
                'severity': 'high',
                'message': f"High threat activity from {ip}",
                'details': analysis
            })
        
        # Medium threat - deploy decoy and monitor
        elif threat_score >= 30:
            actions.append({
                'type': 'alert',
                'severity': 'medium',
                'message': f"Suspicious activity from {ip}",
                'details': analysis
            })
        
        # Specific attack type responses
        if 'sql_injection_detected' in threats or 'sql_injection_pattern' in behaviors:
            actions.append({
                'type': 'deploy_decoy',
                'decoy_type': 'database',
                'target_ip': ip,
                'config': {'type': 'fake_database', 'purpose': 'sql_injection_trap'}
            })
        
        if 'command_injection_detected' in threats or 'command_injection_pattern' in behaviors:
            actions.append({
                'type': 'deploy_decoy',
                'decoy_type': 'shell',
                'target_ip': ip,
                'config': {'type': 'fake_shell', 'purpose': 'command_injection_trap'}
            })
        
        if 'brute_force_attempt' in behaviors:
            actions.append({
                'type': 'deploy_decoy',
                'decoy_type': 'credentials',
                'target_ip': ip,
                'config': {'type': 'honey_credentials', 'purpose': 'track_attacker'}
            })
        
        return actions
    
    def execute_action(self, action):
        """Execute action via orchestrator API"""
        action_type = action.get('type')
        
        try:
            if action_type == 'block_ip':
                response = requests.post(
                    f"{ORCHESTRATOR_URL}/action/block_ip",
                    json={'ip': action['ip'], 'reason': action['reason']},
                    timeout=5
                )
                return response.json()
            
            elif action_type == 'rate_limit':
                response = requests.post(
                    f"{ORCHESTRATOR_URL}/action/rate_limit",
                    json={
                        'ip': action['ip'],
                        'limit': action.get('limit', 10),
                        'reason': action['reason']
                    },
                    timeout=5
                )
                return response.json()
            
            elif action_type == 'deploy_decoy':
                response = requests.post(
                    f"{ORCHESTRATOR_URL}/action/deploy_decoy",
                    json={
                        'type': action.get('decoy_type', 'generic'),
                        'target_ip': action.get('target_ip', 'any'),
                        'config': action.get('config', {})
                    },
                    timeout=5
                )
                return response.json()
            
            elif action_type == 'alert':
                response = requests.post(
                    f"{ORCHESTRATOR_URL}/action/alert",
                    json={
                        'severity': action.get('severity', 'medium'),
                        'message': action.get('message', ''),
                        'details': action.get('details', {})
                    },
                    timeout=5
                )
                return response.json()
            
            elif action_type == 'log':
                response = requests.post(
                    f"{ORCHESTRATOR_URL}/action/log",
                    json={
                        'type': action.get('log_type', 'generic'),
                        'details': action.get('details', {})
                    },
                    timeout=5
                )
                return response.json()
            
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': str(e)}
    
    def run_analysis(self):
        """Run complete analysis cycle"""
        print("\n" + "="*60)
        print("🧠 NeuroHoneypot Decision Engine")
        print("="*60)
        
        # Load sessions
        session_count = self.load_sessions()
        print(f"\n📊 Loaded {session_count} sessions")
        
        if session_count == 0:
            print("⚠️  No sessions to analyze")
            return
        
        # Analyze each unique IP
        unique_ips = list(self.ip_activity.keys())
        print(f"🔍 Analyzing {len(unique_ips)} unique IPs\n")
        
        for ip in unique_ips:
            analysis = self.analyze_ip_behavior(ip)
            
            if analysis and analysis['threat_score'] > 0:
                print(f"\n🎯 IP: {ip}")
                print(f"   Requests: {analysis['total_requests']}")
                print(f"   Threat Score: {analysis['threat_score']}")
                print(f"   Behaviors: {', '.join(analysis['behaviors'])}")
                
                # Decide actions
                actions = self.decide_action(analysis)
                
                if actions:
                    print(f"   ⚡ Taking {len(actions)} action(s):")
                    for action in actions:
                        print(f"      - {action['type']}")
                        result = self.execute_action(action)
                        if result.get('success'):
                            print(f"        ✅ Success")
                        else:
                            print(f"        ❌ Failed: {result.get('error', 'Unknown error')}")
        
        print("\n" + "="*60)
        print("✅ Analysis complete")
        print("="*60 + "\n")

def main():
    """Main entry point"""
    engine = DecisionEngine()
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        print("🔄 Running in continuous mode (Ctrl+C to stop)...")
        import time
        while True:
            try:
                engine.run_analysis()
                print("⏳ Waiting 30 seconds before next analysis...")
                time.sleep(30)
            except KeyboardInterrupt:
                print("\n\n👋 Stopping decision engine...")
                break
    else:
        engine.run_analysis()

if __name__ == '__main__':
    main()

