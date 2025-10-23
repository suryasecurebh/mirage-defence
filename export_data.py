"""
NeuroHoneypot - Data Export Utility
Export sessions, actions, and analysis to various formats
"""
import json
import csv
import os
from datetime import datetime
import sys

class DataExporter:
    """Export honeypot data to various formats"""
    
    def __init__(self):
        self.output_dir = 'exports'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_sessions(self):
        """Load all sessions from JSONL"""
        sessions = []
        if os.path.exists('data/sessions.jsonl'):
            with open('data/sessions.jsonl', 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            sessions.append(json.loads(line.strip()))
                        except:
                            pass
        return sessions
    
    def load_actions(self):
        """Load all actions from JSONL"""
        actions = []
        if os.path.exists('data/actions.jsonl'):
            with open('data/actions.jsonl', 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            actions.append(json.loads(line.strip()))
                        except:
                            pass
        return actions
    
    def export_sessions_to_csv(self, filename=None):
        """Export sessions to CSV format"""
        if filename is None:
            filename = f"sessions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        sessions = self.load_sessions()
        
        if not sessions:
            print("⚠️  No sessions to export")
            return None
        
        # Define CSV columns
        fieldnames = [
            'timestamp', 'ip', 'method', 'path', 'action',
            'attack_type', 'severity', 'user_agent', 'session_id'
        ]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            
            for session in sessions:
                writer.writerow(session)
        
        print(f"✅ Exported {len(sessions)} sessions to {filepath}")
        return filepath
    
    def export_actions_to_csv(self, filename=None):
        """Export actions to CSV format"""
        if filename is None:
            filename = f"actions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        actions = self.load_actions()
        
        if not actions:
            print("⚠️  No actions to export")
            return None
        
        fieldnames = ['timestamp', 'action', 'status', 'reason', 'message', 'ip']
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            
            for action in actions:
                # Flatten nested structures
                row = {
                    'timestamp': action.get('timestamp'),
                    'action': action.get('action'),
                    'status': action.get('status'),
                    'reason': action.get('reason', action.get('message', '')),
                    'message': action.get('message', ''),
                    'ip': action.get('ip', '')
                }
                writer.writerow(row)
        
        print(f"✅ Exported {len(actions)} actions to {filepath}")
        return filepath
    
    def export_to_json(self, filename=None):
        """Export complete data to JSON"""
        if filename is None:
            filename = f"complete_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        data = {
            'export_time': datetime.now().isoformat(),
            'sessions': self.load_sessions(),
            'actions': self.load_actions(),
            'statistics': self._generate_stats()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Exported complete data to {filepath}")
        return filepath
    
    def export_summary_report(self, filename=None):
        """Export a human-readable summary report"""
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = os.path.join(self.output_dir, filename)
        sessions = self.load_sessions()
        actions = self.load_actions()
        stats = self._generate_stats()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("NEUROHONEYPOT - SECURITY REPORT\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("SUMMARY\n")
            f.write("-"*70 + "\n")
            f.write(f"Total Sessions: {stats['total_sessions']}\n")
            f.write(f"Unique IPs: {stats['unique_ips']}\n")
            f.write(f"Attack Attempts: {stats['attack_sessions']}\n")
            f.write(f"Actions Taken: {stats['total_actions']}\n\n")
            
            f.write("ATTACK TYPES\n")
            f.write("-"*70 + "\n")
            for attack_type, count in stats['attack_types'].items():
                f.write(f"  {attack_type}: {count}\n")
            f.write("\n")
            
            f.write("SEVERITY DISTRIBUTION\n")
            f.write("-"*70 + "\n")
            for severity, count in stats['severities'].items():
                f.write(f"  {severity.upper()}: {count}\n")
            f.write("\n")
            
            f.write("TOP ATTACKING IPs\n")
            f.write("-"*70 + "\n")
            for ip, count in stats['top_ips'][:10]:
                f.write(f"  {ip}: {count} requests\n")
            f.write("\n")
            
            f.write("DEFENSIVE ACTIONS\n")
            f.write("-"*70 + "\n")
            for action_type, count in stats['action_types'].items():
                f.write(f"  {action_type}: {count}\n")
            f.write("\n")
            
            f.write("RECENT CRITICAL EVENTS\n")
            f.write("-"*70 + "\n")
            critical_sessions = [s for s in sessions if s.get('severity') == 'critical']
            for session in critical_sessions[-5:]:
                f.write(f"  [{session.get('timestamp', '')}] ")
                f.write(f"{session.get('ip', 'unknown')} - ")
                f.write(f"{session.get('attack_type', 'unknown')}\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("End of Report\n")
            f.write("="*70 + "\n")
        
        print(f"✅ Generated summary report: {filepath}")
        return filepath
    
    def _generate_stats(self):
        """Generate statistics from data"""
        sessions = self.load_sessions()
        actions = self.load_actions()
        
        # Attack types
        attack_types = {}
        for session in sessions:
            attack_type = session.get('attack_type', 'normal')
            attack_types[attack_type] = attack_types.get(attack_type, 0) + 1
        
        # Severities
        severities = {}
        for session in sessions:
            severity = session.get('severity', 'low')
            severities[severity] = severities.get(severity, 0) + 1
        
        # Top IPs
        ip_counts = {}
        for session in sessions:
            ip = session.get('ip', 'unknown')
            ip_counts[ip] = ip_counts.get(ip, 0) + 1
        top_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Action types
        action_types = {}
        for action in actions:
            action_type = action.get('action', 'unknown')
            action_types[action_type] = action_types.get(action_type, 0) + 1
        
        return {
            'total_sessions': len(sessions),
            'unique_ips': len(set(s.get('ip') for s in sessions)),
            'attack_sessions': len([s for s in sessions if s.get('attack_type') != 'normal']),
            'total_actions': len(actions),
            'attack_types': attack_types,
            'severities': severities,
            'top_ips': top_ips,
            'action_types': action_types
        }
    
    def export_all(self):
        """Export everything in all formats"""
        print("\n" + "="*60)
        print("📦 Exporting All Data")
        print("="*60 + "\n")
        
        self.export_sessions_to_csv()
        self.export_actions_to_csv()
        self.export_to_json()
        self.export_summary_report()
        
        print("\n" + "="*60)
        print(f"✅ All exports complete! Check the '{self.output_dir}' directory")
        print("="*60)

def main():
    """Main entry point"""
    exporter = DataExporter()
    
    if len(sys.argv) > 1:
        export_type = sys.argv[1].lower()
        
        if export_type == 'csv':
            exporter.export_sessions_to_csv()
            exporter.export_actions_to_csv()
        elif export_type == 'json':
            exporter.export_to_json()
        elif export_type == 'report':
            exporter.export_summary_report()
        elif export_type == 'all':
            exporter.export_all()
        else:
            print(f"Unknown export type: {export_type}")
            print("Usage: python export_data.py [csv|json|report|all]")
    else:
        # Default: export everything
        exporter.export_all()

if __name__ == '__main__':
    main()

