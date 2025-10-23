"""
NeuroHoneypot - Orchestrator API
Executes defensive actions and logs them
"""
from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# In-memory state
blocked_ips = set()
rate_limited_ips = {}
deployed_decoys = []

def log_action(action_data):
    """Log action to JSONL file"""
    with open('data/actions.jsonl', 'a') as f:
        f.write(json.dumps(action_data) + '\n')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'blocked_ips': len(blocked_ips),
        'rate_limited': len(rate_limited_ips),
        'active_decoys': len(deployed_decoys)
    })

@app.route('/action/block_ip', methods=['POST'])
def block_ip():
    """Block an IP address"""
    data = request.json
    ip = data.get('ip')
    reason = data.get('reason', 'Unknown')
    
    if not ip:
        return jsonify({'error': 'IP address required'}), 400
    
    blocked_ips.add(ip)
    
    action_log = {
        'timestamp': datetime.now().isoformat(),
        'action': 'block_ip',
        'ip': ip,
        'reason': reason,
        'status': 'success'
    }
    
    log_action(action_log)
    
    return jsonify({
        'success': True,
        'message': f'IP {ip} blocked',
        'action': action_log
    })

@app.route('/action/rate_limit', methods=['POST'])
def rate_limit():
    """Apply rate limiting to an IP"""
    data = request.json
    ip = data.get('ip')
    limit = data.get('limit', 10)  # requests per minute
    reason = data.get('reason', 'Suspicious activity')
    
    if not ip:
        return jsonify({'error': 'IP address required'}), 400
    
    rate_limited_ips[ip] = {
        'limit': limit,
        'reason': reason,
        'applied_at': datetime.now().isoformat()
    }
    
    action_log = {
        'timestamp': datetime.now().isoformat(),
        'action': 'rate_limit',
        'ip': ip,
        'limit': limit,
        'reason': reason,
        'status': 'success'
    }
    
    log_action(action_log)
    
    return jsonify({
        'success': True,
        'message': f'Rate limit applied to {ip}',
        'action': action_log
    })

@app.route('/action/deploy_decoy', methods=['POST'])
def deploy_decoy():
    """Deploy a decoy resource"""
    data = request.json
    decoy_type = data.get('type', 'generic')
    target_ip = data.get('target_ip', 'any')
    config = data.get('config', {})
    
    decoy = {
        'id': f"decoy_{len(deployed_decoys) + 1}",
        'type': decoy_type,
        'target_ip': target_ip,
        'config': config,
        'deployed_at': datetime.now().isoformat()
    }
    
    deployed_decoys.append(decoy)
    
    action_log = {
        'timestamp': datetime.now().isoformat(),
        'action': 'deploy_decoy',
        'decoy': decoy,
        'status': 'success'
    }
    
    log_action(action_log)
    
    return jsonify({
        'success': True,
        'message': f'Decoy {decoy["id"]} deployed',
        'decoy': decoy,
        'action': action_log
    })

@app.route('/action/alert', methods=['POST'])
def alert():
    """Create a security alert"""
    data = request.json
    severity = data.get('severity', 'medium')
    message = data.get('message', 'Security event detected')
    details = data.get('details', {})
    
    action_log = {
        'timestamp': datetime.now().isoformat(),
        'action': 'alert',
        'severity': severity,
        'message': message,
        'details': details,
        'status': 'success'
    }
    
    log_action(action_log)
    
    return jsonify({
        'success': True,
        'message': 'Alert created',
        'action': action_log
    })

@app.route('/action/log', methods=['POST'])
def log_event():
    """Log a generic event"""
    data = request.json
    event_type = data.get('type', 'generic')
    details = data.get('details', {})
    
    action_log = {
        'timestamp': datetime.now().isoformat(),
        'action': 'log_event',
        'type': event_type,
        'details': details,
        'status': 'success'
    }
    
    log_action(action_log)
    
    return jsonify({
        'success': True,
        'message': 'Event logged',
        'action': action_log
    })

@app.route('/state')
def get_state():
    """Get current orchestrator state"""
    return jsonify({
        'blocked_ips': list(blocked_ips),
        'rate_limited_ips': rate_limited_ips,
        'deployed_decoys': deployed_decoys,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/actions/recent')
def recent_actions():
    """Get recent actions from log"""
    try:
        actions = []
        if os.path.exists('data/actions.jsonl'):
            with open('data/actions.jsonl', 'r') as f:
                lines = f.readlines()
                # Get last 50 actions
                for line in lines[-50:]:
                    actions.append(json.loads(line.strip()))
        
        return jsonify({
            'actions': actions,
            'count': len(actions)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🎯 NeuroHoneypot Orchestrator Starting...")
    print("📊 Logging actions to: data/actions.jsonl")
    print("🌐 API available at: http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)

