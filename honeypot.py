"""
NeuroHoneypot - Flask Web Honeypot
Logs all interactions to data/sessions.jsonl
"""
from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime
import hashlib

app = Flask(__name__)

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

def log_session(data):
    """Log session data to JSONL file"""
    with open('data/sessions.jsonl', 'a') as f:
        f.write(json.dumps(data) + '\n')

def get_client_info():
    """Extract client information from request"""
    return {
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', ''),
        'timestamp': datetime.now().isoformat(),
        'method': request.method,
        'path': request.path,
        'args': dict(request.args),
        'form': dict(request.form),
        'headers': dict(request.headers),
        'session_id': hashlib.md5(f"{request.remote_addr}{request.headers.get('User-Agent', '')}".encode()).hexdigest()[:16]
    }

# HTML Templates
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Portal - Login</title>
    <style>
        body { font-family: Arial; background: #f0f0f0; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 300px; }
        h2 { color: #333; margin-top: 0; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0056b3; }
        .error { color: red; font-size: 14px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>🔐 Admin Portal</h2>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
        </form>
        <p style="font-size: 12px; color: #666; margin-top: 20px;">Default credentials: admin/admin</p>
    </div>
</body>
</html>
"""

ADMIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard</title>
    <style>
        body { font-family: Arial; margin: 0; background: #f5f5f5; }
        .header { background: #007bff; color: white; padding: 20px; }
        .container { padding: 20px; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .btn { padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
        .btn:hover { background: #218838; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎛️ Admin Dashboard</h1>
        <p>Welcome, Administrator</p>
    </div>
    <div class="container">
        <div class="card">
            <h3>Quick Actions</h3>
            <button class="btn" onclick="location.href='/api/users'">View Users</button>
            <button class="btn" onclick="location.href='/api/config'">System Config</button>
            <button class="btn" onclick="location.href='/api/database'">Database</button>
            <button class="btn" onclick="location.href='/api/logs'">View Logs</button>
        </div>
        <div class="card">
            <h3>System Status</h3>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Server Status</td><td>✅ Online</td></tr>
                <tr><td>Database</td><td>✅ Connected</td></tr>
                <tr><td>Active Sessions</td><td>42</td></tr>
                <tr><td>Uptime</td><td>5 days, 3 hours</td></tr>
            </table>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Home page - login form"""
    info = get_client_info()
    log_session({**info, 'action': 'visit_home'})
    return render_template_string(LOGIN_PAGE)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login endpoint - always fails but logs attempts"""
    info = get_client_info()
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        log_session({
            **info,
            'action': 'login_attempt',
            'username': username,
            'password': password,
            'payload_type': 'credentials'
        })
        
        # Fake success for specific credentials to keep attacker engaged
        if username == 'admin' and password == 'admin':
            return render_template_string(ADMIN_PAGE)
        
        return render_template_string(LOGIN_PAGE, error="Invalid credentials")
    
    return render_template_string(LOGIN_PAGE)

@app.route('/admin')
def admin():
    """Admin page - requires 'admin' query param"""
    info = get_client_info()
    
    if request.args.get('token') == 'secret123':
        log_session({**info, 'action': 'admin_access_success'})
        return render_template_string(ADMIN_PAGE)
    
    log_session({**info, 'action': 'admin_access_denied'})
    return jsonify({'error': 'Unauthorized'}), 403

@app.route('/api/users')
def api_users():
    """Fake user API"""
    info = get_client_info()
    log_session({**info, 'action': 'api_users_access'})
    
    return jsonify({
        'users': [
            {'id': 1, 'username': 'admin', 'email': 'admin@company.com', 'role': 'admin'},
            {'id': 2, 'username': 'john_doe', 'email': 'john@company.com', 'role': 'user'},
            {'id': 3, 'username': 'jane_smith', 'email': 'jane@company.com', 'role': 'user'}
        ]
    })

@app.route('/api/config')
def api_config():
    """Fake config API - appears to expose sensitive info"""
    info = get_client_info()
    log_session({**info, 'action': 'api_config_access', 'severity': 'high'})
    
    return jsonify({
        'database': {
            'host': 'db.internal.local',
            'port': 5432,
            'name': 'production_db'
        },
        'api_keys': {
            'stripe': 'sk_test_xxxxxxxxxx',
            'aws': 'AKIA123456789EXAMPLE'
        },
        'debug_mode': True
    })

@app.route('/api/database')
def api_database():
    """Fake database API - detects SQL injection attempts"""
    info = get_client_info()
    query = request.args.get('q', '')
    
    # Detect SQL injection patterns
    sql_patterns = ["'", '"', 'OR', 'SELECT', 'UNION', 'DROP', '--', ';']
    is_sql_injection = any(pattern.lower() in query.lower() for pattern in sql_patterns)
    
    log_session({
        **info,
        'action': 'database_query',
        'query': query,
        'attack_type': 'sql_injection' if is_sql_injection else 'normal',
        'severity': 'critical' if is_sql_injection else 'low'
    })
    
    if is_sql_injection:
        return jsonify({'error': 'Syntax error in SQL query'}), 400
    
    return jsonify({'records': [{'id': 1, 'name': 'Sample Data'}]})

@app.route('/api/logs')
def api_logs():
    """Fake logs endpoint"""
    info = get_client_info()
    log_session({**info, 'action': 'api_logs_access'})
    
    return jsonify({
        'logs': [
            {'timestamp': '2025-10-22 10:30:15', 'level': 'INFO', 'message': 'User login successful'},
            {'timestamp': '2025-10-22 10:28:42', 'level': 'WARNING', 'message': 'Failed login attempt'},
            {'timestamp': '2025-10-22 10:25:33', 'level': 'ERROR', 'message': 'Database connection timeout'}
        ]
    })

@app.route('/api/exec')
def api_exec():
    """Fake command execution endpoint - detects command injection"""
    info = get_client_info()
    cmd = request.args.get('cmd', '')
    
    # Detect command injection patterns
    cmd_patterns = ['&', '|', ';', '`', '$', '>', '<', 'rm ', 'wget ', 'curl ']
    is_cmd_injection = any(pattern in cmd.lower() for pattern in cmd_patterns)
    
    log_session({
        **info,
        'action': 'command_execution',
        'command': cmd,
        'attack_type': 'command_injection' if is_cmd_injection else 'normal',
        'severity': 'critical' if is_cmd_injection else 'low'
    })
    
    return jsonify({'output': 'Command execution disabled', 'status': 'error'})

@app.route('/<path:path>')
def catch_all(path):
    """Catch-all route for path traversal detection"""
    info = get_client_info()
    
    # Detect path traversal attempts
    is_path_traversal = '..' in path or '%2e' in path.lower()
    
    log_session({
        **info,
        'action': 'path_access',
        'requested_path': path,
        'attack_type': 'path_traversal' if is_path_traversal else 'normal',
        'severity': 'high' if is_path_traversal else 'low'
    })
    
    return jsonify({'error': 'Not Found'}), 404

if __name__ == '__main__':
    print("🍯 NeuroHoneypot Web Server Starting...")
    print("📊 Logging sessions to: data/sessions.jsonl")
    print("🌐 Access at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

