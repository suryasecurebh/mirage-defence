# 🍯 NeuroHoneypot - AI-Driven Adaptive Deception System

**Conference Demo MVP - Windows-Friendly**

An intelligent cybersecurity honeypot that uses AI/ML to detect, analyze, and adaptively respond to cyber attacks in real-time.

---

## 🎯 Overview

NeuroHoneypot is an adaptive deception system that:
- **Attracts** attackers with a fake vulnerable web application
- **Learns** from attack patterns using machine learning
- **Adapts** defensive strategies dynamically based on threat analysis
- **Visualizes** everything in real-time through an interactive dashboard

### System Components

1. **Flask Web Honeypot** (`honeypot.py`) - Fake vulnerable application that logs all interactions
2. **Orchestrator API** (`orchestrator.py`) - Executes defensive actions (blocking, rate limiting, decoys)
3. **Decision Engine** (`decision.py`) - Rule-based intelligence that analyzes threats and triggers responses
4. **ML Clustering** (`ai/feature_cluster.py`) - K-means clustering to classify attacker types
5. **Streamlit Dashboard** (`dashboard.py`) - Real-time monitoring and visualization
6. **Simulated Attacker** (`sim_attacker.py`) - Generates realistic attack traffic for demos

---

## 🚀 Quick Start (Windows)

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**
   ```bash
   cd C:\Users\surya\Desktop\mvp
   ```

2. **Create a virtual environment (recommended)**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

### Running the System

You have two options:

#### Option A: Automated Start (Recommended)
Run everything with one command:
```powershell
.\run_all.bat
```

#### Option B: Manual Start (For Testing Individual Components)

Open **4 separate PowerShell terminals** and run:

**Terminal 1 - Honeypot:**
```powershell
python honeypot.py
```
*Runs on http://localhost:5000*

**Terminal 2 - Orchestrator:**
```powershell
python orchestrator.py
```
*Runs on http://localhost:5001*

**Terminal 3 - Dashboard:**
```powershell
streamlit run dashboard.py
```
*Opens automatically at http://localhost:8501*

**Terminal 4 - Attacker (for demo):**
```powershell
python sim_attacker.py full
```
*Generates attack traffic*

---

## 🎬 Demo Workflow

Follow these steps for your conference presentation:

### 1. Start the System
```powershell
# Start all components
.\run_all.bat
```

Wait for all services to start (about 10-15 seconds).

### 2. Show the Dashboard
Open your browser to: http://localhost:8501

This is your main presentation view showing:
- Real-time session logs
- Attack detection
- System responses
- ML clustering results

### 3. Generate Attack Traffic
In a new terminal:
```powershell
# Run a complete attack scenario
python sim_attacker.py full

# Or try different scenarios:
python sim_attacker.py quick          # Quick demo
python sim_attacker.py brute_force    # Focus on login attacks
python sim_attacker.py sql_only       # Focus on SQL injection
```

### 4. Analyze Threats
Run the decision engine to analyze and respond:
```powershell
python decision.py
```

Watch the dashboard show:
- ✅ Blocked IPs
- ⚡ Rate limiting applied
- 🎯 Decoys deployed

### 5. View ML Clustering
Generate and view attack pattern clusters:
```powershell
python ai/feature_cluster.py
```

Then check the "ML Clusters" tab in the dashboard.

---

## 📊 Dashboard Features

### Real-Time Metrics
- Total sessions captured
- Unique attacker IPs
- Defensive actions taken
- Attack attempt percentage

### Session Log
- Live feed of all honeypot interactions
- Color-coded by severity
- Attack type detection
- Detailed request information

### Actions Log
- Real-time defensive actions
- IP blocking events
- Rate limiting applied
- Decoy deployments

### ML Clusters
- Attacker classification:
  - 🎯 Sophisticated Attackers
  - 💉 SQL Injection Specialists
  - 🔐 Brute Force Attackers
  - 🔍 Scanners/Reconnaissance
  - And more...

### Analytics
- Attack type distribution
- Severity level charts
- Activity timeline
- Top attacking IPs

---

## 🎯 Attack Scenarios

### Full Attack Scenario (Recommended for Demo)
```powershell
python sim_attacker.py full
```
**Demonstrates:**
- Reconnaissance scanning
- Brute force login attempts
- SQL injection attacks
- Command injection attempts
- Path traversal attacks
- Sensitive data access

**Duration:** ~60-90 seconds

### Quick Demo
```powershell
python sim_attacker.py quick
```
**Demonstrates:** Basic reconnaissance + SQL injection + brute force

**Duration:** ~30 seconds

### Specialized Scenarios
```powershell
# SQL Injection only
python sim_attacker.py sql_only

# Brute force only
python sim_attacker.py brute_force
```

---

## 🧠 How It Works

### 1. Attack Detection Flow
```
Attacker → Honeypot (logs) → Decision Engine → Threat Analysis → Orchestrator → Action
```

### 2. Machine Learning Pipeline
```
Sessions → Feature Extraction → K-means Clustering → Attacker Classification
```

### 3. Decision Rules

| Threat Score | Actions Taken |
|-------------|---------------|
| 80+ (Critical) | ❌ Block IP immediately + Alert |
| 50-79 (High) | ⏱️ Rate limit + Deploy decoys + Alert |
| 30-49 (Medium) | 📊 Monitor + Log + Alert |
| <30 (Low) | 📝 Log only |

### 4. Attack Type Detection

- **SQL Injection**: Detects `'`, `OR`, `UNION`, `SELECT`, etc.
- **Command Injection**: Detects `;`, `|`, `&&`, `wget`, etc.
- **Path Traversal**: Detects `../`, `..\\`, `%2e`, etc.
- **Brute Force**: Tracks failed login attempts per IP

---

## 📁 Project Structure

```
mvp/
├── honeypot.py              # Flask web honeypot (port 5000)
├── orchestrator.py          # Defense orchestrator API (port 5001)
├── decision.py              # Rule-based decision engine
├── sim_attacker.py          # Simulated attacker for demo
├── dashboard.py             # Streamlit dashboard (port 8501)
├── ai/
│   └── feature_cluster.py   # ML clustering analysis
├── data/
│   ├── sessions.jsonl       # Attack logs (auto-generated)
│   ├── actions.jsonl        # System actions (auto-generated)
│   └── cluster_analysis.json # ML results (auto-generated)
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── run_all.bat             # Windows batch script
└── start_component.bat     # Component starter helper
```

---

## 🔧 Advanced Usage

### Continuous Monitoring Mode
Run the decision engine in continuous mode:
```powershell
python decision.py --continuous
```
*Analyzes threats every 30 seconds automatically*

### Custom Cluster Count
Specify number of clusters for ML analysis:
```powershell
python ai/feature_cluster.py 5
```
*Creates 5 clusters instead of default 3*

### Clear All Data
```powershell
del data\sessions.jsonl
del data\actions.jsonl
del data\cluster_analysis.json
```
Or use the "Clear Data" button in the dashboard.

### API Testing
Test orchestrator API directly:
```powershell
# Block an IP
curl -X POST http://localhost:5001/action/block_ip -H "Content-Type: application/json" -d "{\"ip\": \"192.168.1.100\", \"reason\": \"Manual block\"}"

# Check system state
curl http://localhost:5001/state

# View recent actions
curl http://localhost:5001/actions/recent
```

---

## 🎤 Presentation Tips

### Opening (30 seconds)
> "NeuroHoneypot is an AI-driven deception system that doesn't just log attacks—it learns from them and adapts its defenses in real-time."

### Demo Flow (3-5 minutes)

1. **Show Clean Dashboard** (10s)
   - "Here's our system before any attacks..."

2. **Launch Attack** (15s)
   - "Now I'll simulate a sophisticated attacker..."
   - Run: `python sim_attacker.py full`

3. **Show Real-Time Detection** (30s)
   - Watch dashboard fill with sessions
   - Point out attack type detection
   - Highlight severity levels

4. **Trigger Decision Engine** (30s)
   - Run: `python decision.py`
   - Show IP blocking
   - Show decoy deployment
   - Highlight automated responses

5. **Show ML Clustering** (60s)
   - Run: `python ai/feature_cluster.py`
   - Go to "ML Clusters" tab
   - Explain attacker classification
   - Show behavior patterns

6. **Highlight Analytics** (30s)
   - Show attack distribution charts
   - Timeline visualization
   - Top attackers

### Key Talking Points

✅ **Real-time threat detection** - No human intervention needed
✅ **Machine learning classification** - Identifies attacker types automatically
✅ **Adaptive responses** - Different actions for different threats
✅ **Complete visibility** - Everything logged and visualized
✅ **Extensible design** - Easy to add RL, neural networks, more ML models

---

## 🐛 Troubleshooting

### "Address already in use" Error
```powershell
# Kill processes on ports
netstat -ano | findstr :5000
netstat -ano | findstr :5001
netstat -ano | findstr :8501

# Then kill the PID
taskkill /PID <PID> /F
```

### "No sessions to analyze"
Make sure:
1. Honeypot is running
2. Attacker has been run
3. `data/sessions.jsonl` exists

### Dashboard Not Updating
Click the "🔄 Refresh Now" button or enable "Auto-refresh" in sidebar

### Import Errors
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Virtual Environment Issues
```powershell
# Deactivate and recreate
deactivate
rmdir /s venv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📈 Future Enhancements

This MVP is designed for extensibility. Planned additions:

- 🤖 **Reinforcement Learning** - Train agents to optimize defensive strategies
- 🧠 **Neural Networks** - Deep learning for anomaly detection
- 🔗 **Docker Integration** - Containerized deployment
- 🌐 **Multi-Protocol Support** - SSH, FTP, Database honeypots
- 📡 **Threat Intelligence** - Integration with external threat feeds
- 🎯 **Advanced Decoys** - Dynamic service emulation
- 📊 **Historical Analysis** - Long-term pattern recognition

---

## 📄 License

This is a demo/MVP project for conference submission. Feel free to extend and adapt for your needs.

---

## 🙋 Support

For questions or issues during your conference demo:

1. Check this README troubleshooting section
2. Verify all services are running with `run_all.bat`
3. Check logs in each terminal window
4. Clear data and restart if needed

---

## 🎓 Technical Details

### Technologies Used
- **Backend**: Flask (Python web framework)
- **ML/AI**: scikit-learn (K-means clustering)
- **Data Processing**: pandas, numpy
- **Visualization**: Streamlit
- **Data Storage**: JSONL (JSON Lines format)

### Performance
- Handles 100+ sessions/minute
- Real-time analysis < 1 second
- Dashboard refresh every 5 seconds
- Clustering analysis < 5 seconds for 1000 sessions

### Security Note
⚠️ **This is a honeypot/demo system** - do NOT use credentials or data from this system in production. All "sensitive" information displayed is fake and for demonstration purposes only.

---

**Built for Conference Demo | 3-Day MVP Sprint | October 2025**

Good luck with your presentation! 🚀

#   m i r a g e - d e f e n c e  
 #   m i r a g e - d e f e n c e  
 #   m i r a g e - d e f e n c e  
 