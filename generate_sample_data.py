"""
NeuroHoneypot - Sample Data Generator
Creates sample data for testing the dashboard without running full attacks
"""
import json
import os
from datetime import datetime, timedelta
import random

def generate_sample_sessions(count=50):
    """Generate sample session data"""
    os.makedirs('data', exist_ok=True)
    
    ips = [
        '192.168.1.100',
        '10.0.0.50',
        '172.16.5.20',
        '203.0.113.42',
        '198.51.100.33'
    ]
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'python-requests/2.28.0',
        'curl/7.68.0',
        'Mozilla/5.0 (compatible; AttackBot/1.0)'
    ]
    
    actions = [
        'visit_home',
        'login_attempt',
        'api_users_access',
        'api_config_access',
        'database_query',
        'command_execution',
        'path_access'
    ]
    
    attack_types = [
        'normal',
        'sql_injection',
        'command_injection',
        'path_traversal'
    ]
    
    severities = ['low', 'medium', 'high', 'critical']
    
    start_time = datetime.now() - timedelta(hours=1)
    
    with open('data/sessions.jsonl', 'w') as f:
        for i in range(count):
            session = {
                'ip': random.choice(ips),
                'user_agent': random.choice(user_agents),
                'timestamp': (start_time + timedelta(minutes=i)).isoformat(),
                'method': 'GET' if random.random() > 0.3 else 'POST',
                'path': random.choice([
                    '/',
                    '/login',
                    '/admin',
                    '/api/users',
                    '/api/config',
                    '/api/database',
                    '/../../etc/passwd'
                ]),
                'action': random.choice(actions),
                'attack_type': random.choice(attack_types),
                'severity': random.choice(severities),
                'args': {},
                'form': {},
                'headers': {},
                'session_id': f"sess_{i}"
            }
            
            # Add some attack-specific data
            if session['action'] == 'login_attempt':
                session['username'] = random.choice(['admin', 'root', 'user', 'test'])
                session['password'] = '****'
            
            if session['attack_type'] == 'sql_injection':
                session['query'] = random.choice([
                    "' OR '1'='1",
                    "admin' --",
                    "UNION SELECT NULL"
                ])
            
            f.write(json.dumps(session) + '\n')
    
    print(f"✅ Generated {count} sample sessions")

def generate_sample_actions(count=20):
    """Generate sample action data"""
    os.makedirs('data', exist_ok=True)
    
    ips = [
        '192.168.1.100',
        '10.0.0.50',
        '172.16.5.20',
        '203.0.113.42',
        '198.51.100.33'
    ]
    
    action_types = [
        'block_ip',
        'rate_limit',
        'deploy_decoy',
        'alert',
        'log_event'
    ]
    
    start_time = datetime.now() - timedelta(hours=1)
    
    with open('data/actions.jsonl', 'w') as f:
        for i in range(count):
            action = {
                'timestamp': (start_time + timedelta(minutes=i*3)).isoformat(),
                'action': random.choice(action_types),
                'status': 'success'
            }
            
            if action['action'] == 'block_ip':
                action['ip'] = random.choice(ips)
                action['reason'] = random.choice([
                    'Critical threat score: 85',
                    'Multiple attack attempts',
                    'SQL injection detected'
                ])
            
            elif action['action'] == 'rate_limit':
                action['ip'] = random.choice(ips)
                action['limit'] = random.choice([5, 10, 20])
                action['reason'] = 'High threat score'
            
            elif action['action'] == 'deploy_decoy':
                action['decoy'] = {
                    'id': f'decoy_{i}',
                    'type': random.choice(['database', 'shell', 'credentials']),
                    'target_ip': random.choice(ips)
                }
            
            elif action['action'] == 'alert':
                action['severity'] = random.choice(['medium', 'high', 'critical'])
                action['message'] = random.choice([
                    'Suspicious activity detected',
                    'Critical threat identified',
                    'Attack pattern matched'
                ])
            
            f.write(json.dumps(action) + '\n')
    
    print(f"✅ Generated {count} sample actions")

def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("🍯 NeuroHoneypot - Sample Data Generator")
    print("="*60 + "\n")
    
    generate_sample_sessions(50)
    generate_sample_actions(20)
    
    print("\n" + "="*60)
    print("✅ Sample data generated successfully!")
    print("="*60)
    print("\nYou can now:")
    print("  1. Start the dashboard: streamlit run dashboard.py")
    print("  2. View the sample data")
    print("  3. Test all dashboard features")
    print("\nNote: This is sample data for testing.")
    print("      For real demo, use: python sim_attacker.py full")
    print()

if __name__ == '__main__':
    main()

