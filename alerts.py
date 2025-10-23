"""
NeuroHoneypot - Alert System
Console and file-based alerting for critical threats
Can be extended with email/Slack integration
"""
import json
import os
from datetime import datetime
from colorama import init, Fore, Back, Style

# Initialize colorama for Windows color support
init(autoreset=True)

class AlertSystem:
    """
    Multi-channel alert system for security events
    """
    
    def __init__(self, alert_file='data/alerts.jsonl'):
        self.alert_file = alert_file
        os.makedirs('data', exist_ok=True)
        self.alert_count = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
    
    def send_alert(self, severity, title, message, details=None):
        """
        Send an alert through multiple channels
        
        Args:
            severity: 'low', 'medium', 'high', or 'critical'
            title: Short alert title
            message: Detailed message
            details: Optional dictionary with additional context
        """
        alert_data = {
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'title': title,
            'message': message,
            'details': details or {}
        }
        
        # Console alert
        self._console_alert(alert_data)
        
        # File alert
        self._file_alert(alert_data)
        
        # Count alerts
        self.alert_count[severity] = self.alert_count.get(severity, 0) + 1
        
        return alert_data
    
    def _console_alert(self, alert_data):
        """Print colored alert to console"""
        severity = alert_data['severity']
        
        # Color mapping
        colors = {
            'low': Fore.GREEN,
            'medium': Fore.YELLOW,
            'high': Fore.RED,
            'critical': Fore.WHITE + Back.RED
        }
        
        icons = {
            'low': '📗',
            'medium': '📙',
            'high': '📕',
            'critical': '🚨'
        }
        
        color = colors.get(severity, Fore.WHITE)
        icon = icons.get(severity, '📢')
        
        print(f"\n{color}{icon} ALERT [{severity.upper()}] {icon}{Style.RESET_ALL}")
        print(f"{color}{'='*60}{Style.RESET_ALL}")
        print(f"{color}Title: {alert_data['title']}{Style.RESET_ALL}")
        print(f"{color}Message: {alert_data['message']}{Style.RESET_ALL}")
        print(f"{color}Time: {alert_data['timestamp']}{Style.RESET_ALL}")
        
        if alert_data['details']:
            print(f"{color}Details:{Style.RESET_ALL}")
            for key, value in alert_data['details'].items():
                print(f"{color}  • {key}: {value}{Style.RESET_ALL}")
        
        print(f"{color}{'='*60}{Style.RESET_ALL}\n")
    
    def _file_alert(self, alert_data):
        """Log alert to file"""
        with open(self.alert_file, 'a') as f:
            f.write(json.dumps(alert_data) + '\n')
    
    def _email_alert(self, alert_data):
        """
        Send email alert (placeholder for future implementation)
        
        To implement:
        import smtplib
        from email.mime.text import MIMEText
        
        # Configure SMTP settings
        # Send email
        """
        pass
    
    def _slack_alert(self, alert_data):
        """
        Send Slack alert (placeholder for future implementation)
        
        To implement:
        import requests
        webhook_url = 'YOUR_SLACK_WEBHOOK_URL'
        requests.post(webhook_url, json={'text': alert_data['message']})
        """
        pass
    
    def get_recent_alerts(self, count=50):
        """Get recent alerts from file"""
        if not os.path.exists(self.alert_file):
            return []
        
        alerts = []
        with open(self.alert_file, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        alerts.append(json.loads(line.strip()))
                    except:
                        pass
        
        return alerts[-count:]
    
    def get_alert_stats(self):
        """Get alert statistics"""
        return {
            'total': sum(self.alert_count.values()),
            'by_severity': self.alert_count,
            'recent_count': len(self.get_recent_alerts(10))
        }
    
    def clear_alerts(self):
        """Clear all alerts"""
        if os.path.exists(self.alert_file):
            os.remove(self.alert_file)
        self.alert_count = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}

# Global alert instance
alert_system = AlertSystem()

# Convenience functions
def alert_low(title, message, details=None):
    """Send low severity alert"""
    return alert_system.send_alert('low', title, message, details)

def alert_medium(title, message, details=None):
    """Send medium severity alert"""
    return alert_system.send_alert('medium', title, message, details)

def alert_high(title, message, details=None):
    """Send high severity alert"""
    return alert_system.send_alert('high', title, message, details)

def alert_critical(title, message, details=None):
    """Send critical severity alert"""
    return alert_system.send_alert('critical', title, message, details)

def main():
    """Demo the alert system"""
    print("🔔 Alert System Demo\n")
    
    # Test different severity levels
    alert_low(
        "Low Priority Event",
        "Normal traffic detected from known IP",
        {'ip': '192.168.1.100', 'requests': 5}
    )
    
    alert_medium(
        "Suspicious Activity",
        "Multiple failed login attempts detected",
        {'ip': '203.0.113.42', 'attempts': 5, 'username': 'admin'}
    )
    
    alert_high(
        "SQL Injection Detected",
        "SQL injection attempt from external IP",
        {'ip': '198.51.100.33', 'payload': "' OR '1'='1", 'endpoint': '/api/database'}
    )
    
    alert_critical(
        "CRITICAL: System Breach Attempt",
        "Multiple attack vectors detected - possible coordinated attack",
        {
            'ip': '172.16.5.20',
            'attack_types': ['sql_injection', 'command_injection', 'path_traversal'],
            'threat_score': 95,
            'action_taken': 'IP blocked immediately'
        }
    )
    
    print("\n📊 Alert Statistics:")
    stats = alert_system.get_alert_stats()
    print(f"Total alerts: {stats['total']}")
    print(f"By severity: {stats['by_severity']}")

if __name__ == '__main__':
    main()

