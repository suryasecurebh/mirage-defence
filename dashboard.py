"""
NeuroHoneypot - Streamlit Dashboard
Real-time monitoring and visualization
"""
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="NeuroHoneypot Dashboard",
    page_icon="🍯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Cybersecurity Theme CSS
st.markdown("""
<style>
    /* Dark Cyber Security Theme - Professional */
    :root {
        --cyber-bg-primary: #0a0e27;
        --cyber-bg-secondary: #151b3b;
        --cyber-bg-card: #1a1f3a;
        --cyber-accent-blue: #00d4ff;
        --cyber-accent-cyan: #0ff;
        --cyber-accent-purple: #b24bf3;
        --cyber-success: #00ff88;
        --cyber-warning: #ffaa00;
        --cyber-danger: #ff4444;
        --cyber-critical: #ff0066;
        --cyber-text-primary: #e0e6ed;
        --cyber-text-secondary: #8b95a8;
        --cyber-border: #2d3748;
    }
    
    /* Main App Background - Dark */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #151b3b 50%, #0a0e27 100%);
    }
    
    /* Dark Cyber Header */
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, var(--cyber-accent-blue), var(--cyber-accent-cyan), var(--cyber-accent-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Consolas', 'Monaco', monospace;
        letter-spacing: 2px;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    }
    
    .subtitle {
        color: var(--cyber-accent-cyan);
        text-align: center;
        font-size: 0.95rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
        font-family: 'Consolas', monospace;
        letter-spacing: 1px;
        opacity: 0.9;
    }
    
    /* Dark Metric Cards */
    div[data-testid="metric-container"] {
        background: var(--cyber-bg-card);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(0, 212, 255, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        border-color: var(--cyber-accent-blue);
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
        transform: translateY(-2px);
    }
    
    div[data-testid="stMetricValue"] {
        color: var(--cyber-accent-cyan) !important;
        font-size: 2.2rem !important;
        font-weight: 700;
        font-family: 'Consolas', monospace;
    }
    
    div[data-testid="stMetricLabel"] {
        color: var(--cyber-text-secondary) !important;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Consolas', monospace;
    }
    
    /* Dark Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--cyber-bg-secondary);
        border-radius: 10px;
        padding: 8px;
        border: 1px solid var(--cyber-border);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--cyber-text-secondary);
        font-weight: 600;
        font-size: 0.9rem;
        padding: 10px 20px;
        font-family: 'Consolas', monospace;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, rgba(0, 212, 255, 0.2), rgba(11, 255, 255, 0.2));
        border: 1px solid var(--cyber-accent-cyan);
        color: var(--cyber-accent-cyan) !important;
        border-radius: 8px;
    }
    
    /* Dark Buttons */
    .stButton > button {
        background: linear-gradient(90deg, var(--cyber-accent-blue), var(--cyber-accent-cyan));
        color: var(--cyber-bg-primary);
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem;
        font-family: 'Consolas', monospace;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.6);
        transform: scale(1.05);
    }
    
    /* Dark Status Indicators */
    .stSuccess {
        background-color: rgba(0, 255, 136, 0.15);
        border-left: 4px solid var(--cyber-success);
        color: var(--cyber-success) !important;
        padding: 12px;
        border-radius: 4px;
    }
    
    .stWarning {
        background-color: rgba(255, 170, 0, 0.15);
        border-left: 4px solid var(--cyber-warning);
        color: var(--cyber-warning) !important;
        padding: 12px;
        border-radius: 4px;
    }
    
    .stError {
        background-color: rgba(255, 68, 68, 0.15);
        border-left: 4px solid var(--cyber-danger);
        color: var(--cyber-danger) !important;
        padding: 12px;
        border-radius: 4px;
    }
    
    .stInfo {
        background-color: rgba(0, 212, 255, 0.15);
        border-left: 4px solid var(--cyber-accent-blue);
        color: var(--cyber-accent-blue) !important;
        padding: 12px;
        border-radius: 4px;
    }
    
    /* Dark Severity Badges */
    .severity-critical {
        background-color: var(--cyber-critical);
        color: white !important;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        box-shadow: 0 0 15px rgba(255, 0, 102, 0.5);
    }
    
    .severity-high {
        background-color: var(--cyber-danger);
        color: white !important;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        box-shadow: 0 0 15px rgba(255, 68, 68, 0.4);
    }
    
    .severity-medium {
        background-color: var(--cyber-warning);
        color: var(--cyber-bg-primary) !important;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
    }
    
    .severity-low {
        background-color: var(--cyber-success);
        color: var(--cyber-bg-primary) !important;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
    }
    
    /* Dark Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--cyber-bg-primary) 0%, var(--cyber-bg-secondary) 100%);
        border-right: 1px solid var(--cyber-border);
    }
    
    section[data-testid="stSidebar"] * {
        color: var(--cyber-text-primary) !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(90deg, var(--cyber-accent-blue), var(--cyber-accent-cyan));
        color: var(--cyber-bg-primary) !important;
    }
    
    /* Dark Dataframes */
    .dataframe {
        background-color: var(--cyber-bg-card) !important;
        border: 1px solid var(--cyber-border) !important;
        border-radius: 8px;
        color: var(--cyber-text-primary) !important;
    }
    
    .dataframe th {
        background-color: var(--cyber-bg-secondary) !important;
        color: var(--cyber-accent-cyan) !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
        border-bottom: 2px solid var(--cyber-accent-blue) !important;
    }
    
    .dataframe td {
        color: var(--cyber-text-primary) !important;
        border-color: var(--cyber-border) !important;
    }
    
    /* Dark Expanders */
    .streamlit-expanderHeader {
        background-color: var(--cyber-bg-card);
        border: 1px solid var(--cyber-border);
        border-radius: 8px;
        color: var(--cyber-accent-cyan) !important;
        font-weight: 600;
    }
    
    /* Dark Section Headers */
    h1, h2, h3 {
        color: var(--cyber-accent-cyan) !important;
        font-weight: 700;
        font-family: 'Consolas', monospace;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    
    /* Dark Status Badges */
    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Consolas', monospace;
    }
    
    .status-online {
        background-color: rgba(0, 255, 136, 0.2);
        color: var(--cyber-success);
        border: 1px solid var(--cyber-success);
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
    }
    
    .status-warning {
        background-color: rgba(255, 170, 0, 0.2);
        color: var(--cyber-warning);
        border: 1px solid var(--cyber-warning);
    }
    
    .status-offline {
        background-color: rgba(255, 68, 68, 0.2);
        color: var(--cyber-danger);
        border: 1px solid var(--cyber-danger);
    }
    
    /* Dark Dividers */
    hr {
        border: none;
        border-top: 1px solid var(--cyber-border);
        margin: 2rem 0;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.1);
    }
    
    /* Text Colors */
    p, span, label, div {
        color: var(--cyber-text-primary) !important;
    }
</style>
""", unsafe_allow_html=True)

def load_sessions():
    """Load sessions from JSONL file"""
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

def load_actions():
    """Load actions from JSONL file"""
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

def load_cluster_analysis():
    """Load cluster analysis if available"""
    if os.path.exists('data/cluster_analysis.json'):
        with open('data/cluster_analysis.json', 'r') as f:
            return json.load(f)
    return None

def load_alerts():
    """Load alerts from JSONL file"""
    alerts = []
    if os.path.exists('data/alerts.jsonl'):
        with open('data/alerts.jsonl', 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        alerts.append(json.loads(line.strip()))
                    except:
                        pass
    return alerts

def load_rl_policy():
    """Load RL agent policy if available"""
    if os.path.exists('data/rl_policy.json'):
        with open('data/rl_policy.json', 'r') as f:
            return json.load(f)
    return None

def load_anomaly_results():
    """Check if anomaly detector model exists"""
    return os.path.exists('data/anomaly_model.pkl')

# Dark Cyber Header
st.markdown('<div class="main-header">⚡ NEUROHONEYPOT | CYBER DEFENSE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">[ AI-POWERED THREAT INTELLIGENCE & ADAPTIVE RESPONSE ]</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Controls")
auto_refresh = st.sidebar.checkbox("Auto-refresh (5s)", value=True)
show_details = st.sidebar.checkbox("Show detailed logs", value=False)

if st.sidebar.button("🔄 Refresh Now"):
    st.rerun()

if st.sidebar.button("🗑️ Clear Data"):
    if os.path.exists('data/sessions.jsonl'):
        os.remove('data/sessions.jsonl')
    if os.path.exists('data/actions.jsonl'):
        os.remove('data/actions.jsonl')
    if os.path.exists('data/cluster_analysis.json'):
        os.remove('data/cluster_analysis.json')
    st.sidebar.success("Data cleared!")
    time.sleep(1)
    st.rerun()

st.sidebar.markdown("---")

# Load data FIRST (before using it!)
sessions = load_sessions()
actions = load_actions()
cluster_analysis = load_cluster_analysis()
alerts = load_alerts()
rl_policy = load_rl_policy()
has_anomaly_detector = load_anomaly_results()

# NOW we can use the loaded data
st.sidebar.markdown("### 📊 SYSTEM HEALTH")

# System Status Indicators
if sessions and len(sessions) > 0:
    st.sidebar.markdown('<div class="status-badge status-online">● OPERATIONAL</div>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<div class="status-badge status-warning">● STANDBY</div>', unsafe_allow_html=True)

st.sidebar.markdown("")
st.sidebar.markdown("**Service Endpoints:**")
st.sidebar.markdown("```")
st.sidebar.markdown("Honeypot:     :5000")
st.sidebar.markdown("Orchestrator: :5001")
st.sidebar.markdown("Dashboard:    :8501")
st.sidebar.markdown("```")

# Threat Assessment
if sessions:
    critical_count = len([s for s in sessions if s.get('severity') == 'critical'])
    high_count = len([s for s in sessions if s.get('severity') == 'high'])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚠️ THREAT ASSESSMENT")
    
    if critical_count > 0:
        st.sidebar.error(f"🔴 CRITICAL: {critical_count} threats")
    if high_count > 0:
        st.sidebar.warning(f"🟠 HIGH: {high_count} threats")
    
    threat_ratio = (critical_count + high_count) / len(sessions) * 100
    if threat_ratio > 30:
        st.sidebar.error(f"Risk Level: ELEVATED ({threat_ratio:.0f}%)")
    elif threat_ratio > 10:
        st.sidebar.warning(f"Risk Level: MODERATE ({threat_ratio:.0f}%)")
    else:
        st.sidebar.success(f"Risk Level: LOW ({threat_ratio:.0f}%)")

# Metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Total Sessions",
        value=len(sessions),
        delta=f"+{len([s for s in sessions[-10:]])} recent"
    )

with col2:
    unique_ips = len(set(s.get('ip', 'unknown') for s in sessions))
    st.metric(
        label="🌐 Unique IPs",
        value=unique_ips
    )

with col3:
    st.metric(
        label="⚡ Actions Taken",
        value=len(actions)
    )

with col4:
    attack_sessions = [s for s in sessions if s.get('attack_type', 'normal') != 'normal']
    st.metric(
        label="🎯 Attack Attempts",
        value=len(attack_sessions),
        delta=f"{(len(attack_sessions)/max(len(sessions), 1)*100):.1f}%"
    )

# AI/ML Systems Status
st.markdown("### 🤖 AI/ML SYSTEMS STATUS")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if rl_policy:
        st.success("🟢 RL Agent: ACTIVE")
    else:
        st.info("⚪ RL Agent: Inactive")

with col2:
    if has_anomaly_detector:
        st.success("🟢 Neural Network: ACTIVE")
    else:
        st.info("⚪ Neural Network: Inactive")

with col3:
    if cluster_analysis:
        st.success(f"🟢 Clustering: {len(cluster_analysis)} Types")
    else:
        st.info("⚪ Clustering: Inactive")

with col4:
    if alerts:
        critical_alerts = len([a for a in alerts if a.get('severity') == 'critical'])
        if critical_alerts > 0:
            st.error(f"🔴 {len(alerts)} Alerts ({critical_alerts} critical)")
        else:
            st.warning(f"🟡 {len(alerts)} Alerts")
    else:
        st.info("⚪ No Alerts")

st.markdown("---")

# Main content tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Recent Sessions", 
    "⚡ Actions Log", 
    "🤖 ML Clusters", 
    "📊 Analytics",
    "🔔 Alerts",
    "🧠 AI Models"
])

# Tab 1: Recent Sessions
with tab1:
    st.subheader("Recent Attack Sessions")
    
    if sessions:
        # Display recent sessions
        recent_sessions = sessions[-50:][::-1]  # Last 50, reversed
        
        session_data = []
        for session in recent_sessions:
            session_data.append({
                'Time': session.get('timestamp', '')[:19],
                'IP': session.get('ip', 'unknown'),
                'Action': session.get('action', 'unknown'),
                'Attack Type': session.get('attack_type', 'normal'),
                'Severity': session.get('severity', 'low'),
                'Path': session.get('path', '/'),
            })
        
        df = pd.DataFrame(session_data)
        
        # Apply color coding
        def color_severity(val):
            if val == 'critical':
                return 'background-color: #ffcccc'
            elif val == 'high':
                return 'background-color: #ffddcc'
            elif val == 'medium':
                return 'background-color: #ffffcc'
            return ''
        
        styled_df = df.style.applymap(color_severity, subset=['Severity'])
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        if show_details:
            st.subheader("Detailed Session View")
            selected_idx = st.selectbox("Select session", range(len(recent_sessions)), format_func=lambda x: f"Session {x+1}: {recent_sessions[x].get('ip', 'unknown')}")
            st.json(recent_sessions[selected_idx])
    else:
        st.info("No sessions recorded yet. Start the honeypot and attacker to generate data.")

# Tab 2: Actions Log
with tab2:
    st.subheader("Orchestrator Actions")
    
    if actions:
        recent_actions = actions[-50:][::-1]  # Last 50, reversed
        
        action_data = []
        for action in recent_actions:
            action_data.append({
                'Time': action.get('timestamp', '')[:19],
                'Action': action.get('action', 'unknown'),
                'Details': str(action.get('reason', action.get('message', '')))[:50],
                'Status': action.get('status', 'unknown'),
            })
        
        df = pd.DataFrame(action_data)
        st.dataframe(df, use_container_width=True, height=400)
        
        # Action type distribution
        st.subheader("Action Distribution")
        action_types = [a.get('action', 'unknown') for a in actions]
        action_counts = pd.Series(action_types).value_counts()
        st.bar_chart(action_counts)
    else:
        st.info("No actions taken yet. Run the decision engine to start analyzing threats.")

# Tab 3: ML Clusters
with tab3:
    st.subheader("Attack Pattern Clustering")
    
    if cluster_analysis:
        for cluster_name, cluster_info in cluster_analysis.items():
            with st.expander(f"**{cluster_name}**: {cluster_info['type']} ({cluster_info['count']} IPs)", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**IPs in this cluster:**")
                    for ip in cluster_info['ips'][:10]:
                        st.text(f"• {ip}")
                    if len(cluster_info['ips']) > 10:
                        st.text(f"... and {len(cluster_info['ips']) - 10} more")
                
                with col2:
                    st.markdown("**Average Profile:**")
                    features = cluster_info['avg_features']
                    feature_df = pd.DataFrame({
                        'Feature': list(features.keys()),
                        'Value': list(features.values())
                    })
                    feature_df = feature_df[feature_df['Value'] > 0]
                    st.bar_chart(feature_df.set_index('Feature'))
        
        st.info("💡 Clusters are generated using K-means ML algorithm based on attack behavior patterns.")
    else:
        st.info("No cluster analysis available. Run `python ai/feature_cluster.py` to generate clusters.")
        if st.button("Generate Clusters Now"):
            st.warning("Please run: `python ai/feature_cluster.py` from the command line")

# Tab 4: Analytics
with tab4:
    st.subheader("System Analytics")
    
    if sessions:
        # Attack type distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Attack Types Distribution**")
            attack_types = [s.get('attack_type', 'normal') for s in sessions]
            attack_counts = pd.Series(attack_types).value_counts()
            st.bar_chart(attack_counts)
        
        with col2:
            st.markdown("**Severity Levels**")
            severities = [s.get('severity', 'low') for s in sessions]
            severity_counts = pd.Series(severities).value_counts()
            st.bar_chart(severity_counts)
        
        # Timeline
        st.markdown("**Activity Timeline**")
        if len(sessions) > 0:
            timeline_data = []
            for session in sessions:
                try:
                    timestamp = datetime.fromisoformat(session.get('timestamp', ''))
                    timeline_data.append({
                        'timestamp': timestamp,
                        'count': 1
                    })
                except:
                    pass
            
            if timeline_data:
                timeline_df = pd.DataFrame(timeline_data)
                timeline_df = timeline_df.set_index('timestamp')
                timeline_df = timeline_df.resample('1min').sum()
                st.line_chart(timeline_df)
        
        # Top attackers
        st.markdown("**Top Attacking IPs**")
        ip_counts = pd.Series([s.get('ip', 'unknown') for s in sessions]).value_counts().head(10)
        st.bar_chart(ip_counts)
        
    else:
        st.info("No data available for analytics yet.")

# Tab 5: Alerts
with tab5:
    st.subheader("🔔 Security Alerts")
    
    if alerts:
        # Alert summary
        col1, col2, col3, col4 = st.columns(4)
        
        severity_counts = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
        for alert in alerts:
            severity = alert.get('severity', 'low')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        with col1:
            st.metric("🟢 Low", severity_counts['low'])
        with col2:
            st.metric("🟡 Medium", severity_counts['medium'])
        with col3:
            st.metric("🔴 High", severity_counts['high'])
        with col4:
            st.metric("🚨 Critical", severity_counts['critical'])
        
        st.markdown("---")
        
        # Recent alerts
        st.markdown("**Recent Alerts (Most Recent First)**")
        recent_alerts = alerts[-20:][::-1]  # Last 20, reversed
        
        for alert in recent_alerts:
            severity = alert.get('severity', 'low')
            
            # Color coding
            if severity == 'critical':
                st.error(f"**🚨 CRITICAL** - {alert.get('title', 'Alert')}")
            elif severity == 'high':
                st.warning(f"**🔴 HIGH** - {alert.get('title', 'Alert')}")
            elif severity == 'medium':
                st.warning(f"**🟡 MEDIUM** - {alert.get('title', 'Alert')}")
            else:
                st.info(f"**🟢 LOW** - {alert.get('title', 'Alert')}")
            
            with st.expander(f"Details - {alert.get('timestamp', '')[:19]}"):
                st.write(f"**Message:** {alert.get('message', '')}")
                if alert.get('details'):
                    st.json(alert['details'])
        
        # Export alerts
        if st.button("📥 Export Alerts to CSV"):
            st.info("Run: `python export_data.py` to export all data")
    else:
        st.info("No alerts recorded yet.")
        st.markdown("""
        **To generate alerts:**
        1. Run attacks: `python sim_attacker.py full`
        2. Run decision engine: `python decision.py`
        3. Or test alerts: `python alerts.py`
        """)

# Tab 6: AI Models
with tab6:
    st.subheader("🧠 AI/ML Model Status")
    
    # RL Agent
    st.markdown("### 🤖 Reinforcement Learning Agent")
    if rl_policy:
        st.success("✅ Model trained and loaded")
        
        policy = rl_policy.get('policy', {})
        stats = rl_policy.get('stats', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("States Explored", stats.get('states_explored', 0))
            st.metric("Learning Episodes", stats.get('total_learning_episodes', 0))
        
        with col2:
            if policy:
                st.markdown("**Sample Learned Policy:**")
                # Show first 5 states
                sample_states = list(policy.items())[:5]
                for state, action_info in sample_states:
                    st.text(f"State: {state}")
                    st.text(f"  → Best Action: {action_info.get('action')}")
                    st.text(f"  → Q-Value: {action_info.get('q_value', 0):.2f}")
                    st.text("")
        
        if st.button("🔄 Retrain RL Agent"):
            st.info("Run: `python ai/rl_agent.py` to retrain")
    else:
        st.warning("⚠️ RL Agent not trained yet")
        st.markdown("""
        **To train the RL agent:**
        ```bash
        python ai/rl_agent.py
        ```
        
        The agent will:
        - Learn from session data
        - Optimize defensive strategies
        - Save trained model
        """)
        
        if st.button("📚 Learn More About RL Agent"):
            st.info("See NEW_FEATURES.md for details")
    
    st.markdown("---")
    
    # Anomaly Detector
    st.markdown("### 🧠 Neural Network Anomaly Detector")
    if has_anomaly_detector:
        st.success("✅ Anomaly detection model trained")
        
        st.markdown("""
        **Model Details:**
        - Type: Autoencoder Neural Network
        - Features: 12 behavioral metrics
        - Purpose: Detect unusual attack patterns (zero-days)
        """)
        
        if st.button("🔄 Retrain Anomaly Detector"):
            st.info("Run: `python ai/anomaly_detector.py` to retrain")
    else:
        st.warning("⚠️ Anomaly detector not trained yet")
        st.markdown("""
        **To train the anomaly detector:**
        ```bash
        python ai/anomaly_detector.py
        ```
        
        The detector will:
        - Learn normal behavior patterns
        - Identify anomalies
        - Flag zero-day attacks
        """)
    
    st.markdown("---")
    
    # Export functionality
    st.markdown("### 📦 Data Export")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export to CSV"):
            st.info("Run: `python export_data.py csv`")
    
    with col2:
        if st.button("📥 Export to JSON"):
            st.info("Run: `python export_data.py json`")
    
    with col3:
        if st.button("📄 Generate Report"):
            st.info("Run: `python export_data.py report`")
    
    st.markdown("---")
    
    # Training instructions
    st.markdown("### 🎓 Quick Training Guide")
    
    st.code("""
# 1. Generate attack data
python sim_attacker.py full

# 2. Train RL agent
python ai/rl_agent.py

# 3. Train anomaly detector
python ai/anomaly_detector.py

# 4. Run ML clustering
python ai/feature_cluster.py

# 5. Export results
python export_data.py all
    """, language="bash")

# Auto-refresh
if auto_refresh:
    time.sleep(5)
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <small>NeuroHoneypot MVP | AI-Driven Adaptive Deception System | Conference Demo</small>
</div>
""", unsafe_allow_html=True)

