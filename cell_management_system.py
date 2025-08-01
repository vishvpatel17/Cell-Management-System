import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import random
import time
from datetime import datetime, timedelta
import json

# Set page configuration
st.set_page_config(
    page_title="Battery Cell Management System",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Professional Dark Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Base text color - changed to light gray for better visibility */
    body, .main, .stApp, .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown ol, .stMarkdown ul {
        color: #e0e0e0 !important;
    }
    
    /* Make metric values more visible */
    .stMetricValue, .stMetricLabel {
        color: #ffffff !important;
    }
    
    /* Make sidebar text more visible */
    .css-1d391kg, .css-1d391kg p, .css-1d391kg li {
        color: #e0e0e0 !important;
    }
    
    /* Make tab content text visible */
    .stTabs [role="tabpanel"] {
        color: #e0e0e0 !important;
    }
    
    /* Make input labels visible */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: #e0e0e0 !important;
    }
    
    /* Make table text visible */
    .stDataFrame, .stDataFrame td, .stDataFrame th {
        color: #e0e0e0 !important;
    }
    
    /* Keep the rest of your existing CSS below */
    .main {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 50%, #0c0c0c 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 50%, #0c0c0c 100%);
    }
    
    /* ... (keep all your existing CSS rules below this point) ... */
</style>
""", unsafe_allow_html=True)

# Professional Dark Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 50%, #0c0c0c 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 50%, #0c0c0c 100%);
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Professional Cards */
    .metric-card {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #333;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 150, 255, 0.2);
        border-color: #0096ff;
    }
    
    .task-card {
        background: linear-gradient(145deg, #1a2332, #243447);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #00d4ff;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .task-card:hover {
        transform: translateX(5px);
        box-shadow: 0 12px 40px rgba(0, 212, 255, 0.2);
    }
    
    /* Status Cards */
    .status-good { 
        background: linear-gradient(145deg, #1a332a, #2d5a42);
        border-left: 4px solid #00ff88;
    }
    .status-warning { 
        background: linear-gradient(145deg, #332a1a, #5a4d2d);
        border-left: 4px solid #ffaa00;
    }
    .status-critical { 
        background: linear-gradient(145deg, #331a1a, #5a2d2d);
        border-left: 4px solid #ff4444;
    }
    
    /* Header Styling */
    h1 {
        background: linear-gradient(90deg, #00d4ff, #0096ff, #0066cc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        font-size: 3rem;
    }
    
    h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a1a, #0c0c0c);
        border-right: 1px solid #333;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #0096ff, #00d4ff);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 150, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 150, 255, 0.4);
    }
    
    /* Metrics */
    .stMetric {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #333;
    }
    
    .stMetric > div {
        color: #ffffff !important;
    }
    
    .stMetric [data-testid="metric-container"] {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #333;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #1a1a1a;
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #888;
        border-radius: 8px;
        margin: 0 0.25rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #0096ff, #00d4ff);
        color: white;
    }
    
    /* Input fields */
    .stSelectbox > div > div {
        background: #2a2a2a;
        border: 1px solid #444;
        color: #ffffff;
    }
    
    .stNumberInput > div > div > input {
        background: #2a2a2a;
        border: 1px solid #444;
        color: #ffffff;
    }
    
    .stTextInput > div > div > input {
        background: #2a2a2a;
        border: 1px solid #444;
        color: #ffffff;
    }
    
    /* Professional glow effects */
    .glow-text {
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #0096ff, #00d4ff);
        border-radius: 4px;
    }
    
    /* Alert styles */
    .alert-success {
        background: linear-gradient(145deg, #1a332a, #2d5a42);
        border-left: 4px solid #00ff88;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: linear-gradient(145deg, #332a1a, #5a4d2d);
        border-left: 4px solid #ffaa00;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .alert-danger {
        background: linear-gradient(145deg, #331a1a, #5a2d2d);
        border-left: 4px solid #ff4444;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cells_data' not in st.session_state:
    st.session_state.cells_data = {}
if 'tasks_data' not in st.session_state:
    st.session_state.tasks_data = {}
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'system_health' not in st.session_state:
    st.session_state.system_health = 100

def generate_cell_data(cell_type, cell_id):
    """Generate cell data based on type with enhanced parameters"""
    base_specs = {
        "lfp": {"voltage": 3.2, "min_v": 2.8, "max_v": 3.6, "capacity_base": 100},
        "li-ion": {"voltage": 3.6, "min_v": 3.2, "max_v": 4.0, "capacity_base": 120},
        "lithium": {"voltage": 3.7, "min_v": 3.0, "max_v": 4.2, "capacity_base": 110}
    }
    
    specs = base_specs.get(cell_type, base_specs["li-ion"])
    
    voltage = specs["voltage"] + random.uniform(-0.2, 0.2)
    current = round(random.uniform(-8, 8), 2)
    temp = round(random.uniform(25, 40), 1)
    capacity = round(specs["capacity_base"] + random.uniform(-20, 20), 2)
    soc = round(random.uniform(20, 95), 1)
    cycles = random.randint(50, 500)
    health = round(100 - (cycles / 10), 1)
    
    return {
        "id": cell_id,
        "type": cell_type,
        "voltage": voltage,
        "current": current,
        "temp": temp,
        "capacity": capacity,
        "min_voltage": specs["min_v"],
        "max_voltage": specs["max_v"],
        "soc": soc,
        "cycles": cycles,
        "health": health,
        "status": get_cell_status(voltage, temp, specs["min_v"], specs["max_v"]),
        "timestamp": datetime.now(),
        "efficiency": round(random.uniform(85, 98), 1),
        "internal_resistance": round(random.uniform(0.01, 0.05), 3)
    }

def get_cell_status(voltage, temp, min_voltage, max_voltage):
    """Enhanced cell status determination"""
    if voltage < min_voltage * 1.05 or temp > 38 or voltage > max_voltage * 0.98:
        return "Critical"
    elif voltage < min_voltage * 1.15 or temp > 32:
        return "Warning"
    else:
        return "Good"

def calculate_system_health():
    """Calculate overall system health"""
    if not st.session_state.cells_data:
        return 100
    
    cells = list(st.session_state.cells_data.values())
    total_health = sum(cell['health'] for cell in cells)
    avg_health = total_health / len(cells)
    
    # Adjust for critical cells
    critical_count = sum(1 for cell in cells if cell['status'] == 'Critical')
    health_penalty = critical_count * 10
    
    return max(0, min(100, avg_health - health_penalty))

def create_advanced_3d_visualization():
    """Enhanced 3D visualization with professional styling"""
    if not st.session_state.cells_data:
        return None
    
    cells = list(st.session_state.cells_data.values())
    
    fig = go.Figure()
    
    # Color mapping with professional palette
    colors = {
        'lfp': '#00ff88', 
        'li-ion': '#ff6b6b', 
        'lithium': '#4ecdc4'
    }
    
    # Create battery pack layout (grid formation)
    grid_size = int(np.ceil(np.sqrt(len(cells))))
    
    for i, cell in enumerate(cells):
        x_pos = i % grid_size
        y_pos = i // grid_size
        z_pos = cell['voltage'] * 10  # Scale for better visualization
        
        # Size based on capacity and health
        marker_size = (cell['capacity'] / 10) * (cell['health'] / 100)
        
        # Opacity based on status
        opacity = 0.9 if cell['status'] == 'Good' else 0.7 if cell['status'] == 'Warning' else 0.5
        
        fig.add_trace(go.Scatter3d(
            x=[x_pos],
            y=[y_pos],
            z=[z_pos],
            mode='markers+text',
            marker=dict(
                size=marker_size,
                color=colors.get(cell['type'], '#888888'),
                opacity=opacity,
                line=dict(width=2, color='white'),
                symbol='circle'
            ),
            text=f"Cell {cell['id']}",
            textposition="top center",
            name=f"Cell {cell['id']} ({cell['type']})",
            hovertemplate=f"""
            <b>Cell {cell['id']}</b><br>
            Type: {cell['type']}<br>
            Voltage: {cell['voltage']:.2f}V<br>
            Current: {cell['current']:.2f}A<br>
            Temperature: {cell['temp']:.1f}°C<br>
            SOC: {cell['soc']:.1f}%<br>
            Health: {cell['health']:.1f}%<br>
            Status: {cell['status']}<br>
            <extra></extra>
            """
        ))
    
    # Add battery pack outline
    outline_x = [-0.5, grid_size-0.5, grid_size-0.5, -0.5, -0.5]
    outline_y = [-0.5, -0.5, grid_size-0.5, grid_size-0.5, -0.5]
    outline_z = [0, 0, 0, 0, 0]
    
    fig.add_trace(go.Scatter3d(
        x=outline_x, y=outline_y, z=outline_z,
        mode='lines',
        line=dict(color='cyan', width=5),
        name='Battery Pack Outline',
        showlegend=False
    ))
    
    fig.update_layout(
        title={
            'text': "🔋 3D Battery Pack Visualization",
            'x': 0.5,
            'font': {'size': 24, 'color': 'white'}
        },
        scene=dict(
            xaxis=dict(title="X Position", backgroundcolor="black", gridcolor="gray"),
            yaxis=dict(title="Y Position", backgroundcolor="black", gridcolor="gray"),
            zaxis=dict(title="Voltage Scale", backgroundcolor="black", gridcolor="gray"),
            bgcolor="black",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="white"),
        height=700,
        margin=dict(l=0, r=0, t=60, b=0)
    )
    
    return fig

def create_professional_dashboard():
    """Enhanced dashboard with professional metrics"""
    if not st.session_state.cells_data:
        return None
    
    cells = list(st.session_state.cells_data.values())
    
    # Create advanced subplots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            "📊 Voltage Distribution", "🌡️ Temperature vs Health",
            "⚡ Current Flow Analysis", "🔄 SOC Distribution",
            "🔋 Capacity vs Cycles", "⚠️ System Status Overview"
        ),
        specs=[
            [{"type": "bar"}, {"type": "scatter"}],
            [{"type": "scatter"}, {"type": "histogram"}],
            [{"type": "scatter"}, {"type": "pie"}]
        ],
        vertical_spacing=0.1,
        horizontal_spacing=0.1
    )
    
    # Enhanced visualizations
    cell_ids = [f"Cell {cell['id']}" for cell in cells]
    voltages = [cell['voltage'] for cell in cells]
    temps = [cell['temp'] for cell in cells]
    healths = [cell['health'] for cell in cells]
    currents = [cell['current'] for cell in cells]
    socs = [cell['soc'] for cell in cells]
    capacities = [cell['capacity'] for cell in cells]
    cycles = [cell['cycles'] for cell in cells]
    
    # 1. Voltage distribution with color coding
    colors_voltage = ['#00ff88' if v > 3.5 else '#ffaa00' if v > 3.2 else '#ff4444' for v in voltages]
    fig.add_trace(
        go.Bar(x=cell_ids, y=voltages, name="Voltage", marker_color=colors_voltage),
        row=1, col=1
    )
    
    # 2. Temperature vs Health scatter
    fig.add_trace(
        go.Scatter(
            x=temps, y=healths, mode="markers+text",
            text=cell_ids, textposition="top center",
            marker=dict(size=12, color=socs, colorscale="Viridis", showscale=True),
            name="Temp vs Health"
        ),
        row=1, col=2
    )
    
    # 3. Current flow analysis
    colors_current = ['#00ff88' if c > 0 else '#ff4444' for c in currents]
    fig.add_trace(
        go.Scatter(
            x=list(range(len(currents))), y=currents,
            mode="markers+lines",
            marker=dict(size=10, color=colors_current),
            name="Current Flow"
        ),
        row=2, col=1
    )
    
    # 4. SOC histogram
    fig.add_trace(
        go.Histogram(x=socs, nbinsx=10, name="SOC Distribution", marker_color="#00d4ff"),
        row=2, col=2
    )
    
    # 5. Capacity vs Cycles
    fig.add_trace(
        go.Scatter(
            x=cycles, y=capacities, mode="markers",
            marker=dict(size=healths, sizemode="diameter", sizeref=2, 
                       color=healths, colorscale="RdYlGn", showscale=True),
            name="Capacity vs Cycles"
        ),
        row=3, col=1
    )
    
    # 6. Status pie chart
    status_counts = {}
    for cell in cells:
        status = cell['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    colors_status = ['#00ff88', '#ffaa00', '#ff4444']
    fig.add_trace(
        go.Pie(
            labels=list(status_counts.keys()), 
            values=list(status_counts.values()),
            marker_colors=colors_status,
            name="Status Distribution"
        ),
        row=3, col=2
    )
    
    fig.update_layout(
        height=1000,
        showlegend=True,
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="white", size=12),
        title={
            'text': "📈 Advanced Performance Dashboard",
            'x': 0.5,
            'font': {'size': 20, 'color': 'white'}
        }
    )
    
    return fig

def create_real_time_monitor():
    """Create real-time monitoring chart"""
    if not st.session_state.historical_data:
        return None
    
    df = pd.DataFrame(st.session_state.historical_data)
    
    fig = go.Figure()
    
    for cell_id in df['cell_id'].unique():
        cell_data = df[df['cell_id'] == cell_id].tail(50)  # Last 50 points
        
        fig.add_trace(go.Scatter(
            x=cell_data['timestamp'],
            y=cell_data['voltage'],
            mode='lines+markers',
            name=f'Cell {cell_id}',
            line=dict(width=3),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title="⚡ Real-time Voltage Monitoring",
        xaxis_title="Time",
        yaxis_title="Voltage (V)",
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="white"),
        height=400,
        showlegend=True
    )
    
    return fig

def generate_system_report():
    """Generate comprehensive system report"""
    if not st.session_state.cells_data:
        return "No data available for report generation."
    
    cells = list(st.session_state.cells_data.values())
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_cells": len(cells),
        "system_health": calculate_system_health(),
        "status_distribution": {},
        "avg_metrics": {
            "voltage": round(sum(c['voltage'] for c in cells) / len(cells), 2),
            "temperature": round(sum(c['temp'] for c in cells) / len(cells), 1),
            "soc": round(sum(c['soc'] for c in cells) / len(cells), 1),
            "health": round(sum(c['health'] for c in cells) / len(cells), 1)
        },
        "critical_cells": [c['id'] for c in cells if c['status'] == 'Critical'],
        "recommendations": []
    }
    
    # Status distribution
    for cell in cells:
        status = cell['status']
        report["status_distribution"][status] = report["status_distribution"].get(status, 0) + 1
    
    # Generate recommendations
    if report["critical_cells"]:
        report["recommendations"].append("🚨 Immediate attention required for critical cells")
    if report["avg_metrics"]["temperature"] > 35:
        report["recommendations"].append("🌡️ Consider cooling system activation")
    if report["avg_metrics"]["soc"] < 30:
        report["recommendations"].append("🔋 Battery pack requires charging")
    if report["system_health"] < 80:
        report["recommendations"].append("⚠️ System maintenance recommended")
    
    return json.dumps(report, indent=2)

def simulate_real_time_data():
    """Enhanced real-time simulation"""
    if st.session_state.simulation_running and st.session_state.cells_data:
        new_alerts = []
        
        for cell_key in st.session_state.cells_data:
            cell = st.session_state.cells_data[cell_key]
            
            # More realistic simulation
            cell['voltage'] += random.uniform(-0.05, 0.05)
            cell['current'] += random.uniform(-0.3, 0.3)
            cell['temp'] += random.uniform(-0.5, 0.5)
            cell['soc'] += random.uniform(-1, 1)
            
            # Capacity degradation over time
            if random.random() < 0.01:  # 1% chance per update
                cell['capacity'] *= 0.999
                cell['health'] = max(0, cell['health'] - 0.1)
            
            # Keep within realistic bounds
            cell['voltage'] = max(cell['min_voltage'], min(cell['max_voltage'], cell['voltage']))
            cell['temp'] = max(20, min(50, cell['temp']))
            cell['soc'] = max(0, min(100, cell['soc']))
            
            # Update status and check for alerts
            old_status = cell['status']
            cell['status'] = get_cell_status(cell['voltage'], cell['temp'], 
                                           cell['min_voltage'], cell['max_voltage'])
            
            # Generate alerts for status changes
            if old_status != cell['status'] and cell['status'] in ['Warning', 'Critical']:
                new_alerts.append(f"Cell {cell['id']}: Status changed to {cell['status']}")
            
            cell['timestamp'] = datetime.now()
        
        # Update system health
        st.session_state.system_health = calculate_system_health()
        
        # Store alerts
        st.session_state.alerts.extend(new_alerts)
        if len(st.session_state.alerts) > 10:  # Keep only last 10 alerts
            st.session_state.alerts = st.session_state.alerts[-10:]
        
        # Store historical data
        timestamp = datetime.now()
        for cell_key, cell in st.session_state.cells_data.items():
            st.session_state.historical_data.append({
                'timestamp': timestamp,
                'cell_id': cell['id'],
                'voltage': cell['voltage'],
                'current': cell['current'],
                'temp': cell['temp'],
                'soc': cell['soc'],
                'health': cell['health']
            })
        
        # Limit historical data
        if len(st.session_state.historical_data) > len(st.session_state.cells_data) * 100:
            st.session_state.historical_data = st.session_state.historical_data[-len(st.session_state.cells_data) * 50:]

# Main App Layout
st.markdown('<h1 class="glow-text">🔋 Advanced Battery Management System</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #888; font-size: 1.2rem;">Professional-grade monitoring and analysis platform</p>', unsafe_allow_html=True)

# Sidebar for controls
with st.sidebar:
    st.markdown("### 🔧 System Controls")
    
    # System Status Indicator
    health = st.session_state.system_health
    health_color = "#00ff88" if health > 80 else "#ffaa00" if health > 60 else "#ff4444"
    st.markdown(f"""
    <div class="metric-card">
        <h4>🏥 System Health</h4>
        <div style="font-size: 2rem; color: {health_color}; font-weight: bold;">{health:.1f}%</div>
        <div class="pulse" style="width: 100%; height: 8px; background: {health_color}; border-radius: 4px; margin-top: 0.5rem;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Alerts Panel
    if st.session_state.alerts:
        st.markdown("### 🚨 Recent Alerts")
        for alert in st.session_state.alerts[-3:]:  # Show last 3 alerts
            st.markdown(f'<div class="alert-warning">{alert}</div>', unsafe_allow_html=True)
    
    # Cell Configuration
    with st.expander("🔋 Cell Configuration", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            num_cells = st.number_input("Cells to add:", min_value=1, max_value=20, value=1)
        with col2:
            cell_type = st.selectbox("Type:", ["lfp", "li-ion", "lithium"])
        
        if st.button("🚀 Generate Cells", type="primary", use_container_width=True):
            for i in range(num_cells):
                cell_id = len(st.session_state.cells_data) + 1
                cell_key = f"cell_{cell_id}_{cell_type}"
                st.session_state.cells_data[cell_key] = generate_cell_data(cell_type, cell_id)
            st.success(f"✅ Added {num_cells} {cell_type.upper()} cell(s)")
            st.rerun()
    
    # Advanced Task Configuration
    with st.expander("⚙️ Task Management", expanded=False):
        task_type = st.selectbox("Task type:", ["CC_CV", "IDLE", "CC_CD", "PULSE_TEST"])
        task_name = st.text_input("Task name:", value=f"Task_{len(st.session_state.tasks_data)+1}")
        
        if task_type == "CC_CV":
            col1, col2 = st.columns(2)
            with col1:
                cc_value = st.number_input("CC (A):", value=5.0)
                cv_voltage = st.number_input("CV (V):", value=4.0)
            with col2:
                current = st.number_input("Current (A):", value=2.0)
                duration = st.number_input("Duration (min):", value=60)
            
            priority = st.selectbox("Priority:", ["Low", "Medium", "High", "Critical"])
            
            task_data = {
                "task_type": task_type,
                "cc_value": cc_value,
                "cv_voltage": cv_voltage,
                "current": current,
                "duration_minutes": duration,
                "priority": priority,
                "created": datetime.now().isoformat()
            }
        
        elif task_type == "PULSE_TEST":
            pulse_current = st.number_input("Pulse Current (A):", value=10.0)
            pulse_duration = st.number_input("Pulse Duration (s):", value=10)
            rest_duration = st.number_input("Rest Duration (s):", value=30)
            cycles = st.number_input("Cycles:", value=5)
            
            task_data = {
                "task_type": task_type,
                "pulse_current": pulse_current,
                "pulse_duration": pulse_duration,
                "rest_duration": rest_duration,
                "cycles": cycles,
                "created": datetime.now().isoformat()
            }
        
        elif task_type == "IDLE":
            duration = st.number_input("Duration (min):", value=30)
            task_data = {
                "task_type": task_type,
                "duration_minutes": duration,
                "created": datetime.now().isoformat()
            }
        
        elif task_type == "CC_CD":
            col1, col2 = st.columns(2)
            with col1:
                cc_value = st.number_input("CC (A):", value=5.0)
                voltage = st.number_input("Voltage (V):", value=3.6)
            with col2:
                capacity = st.number_input("Capacity:", value=100.0)
                duration = st.number_input("Duration (min):", value=60)
            
            task_data = {
                "task_type": task_type,
                "cc_value": cc_value,
                "voltage": voltage,
                "capacity": capacity,
                "duration_minutes": duration,
                "created": datetime.now().isoformat()
            }
        
        if st.button("📋 Add Task", use_container_width=True):
            st.session_state.tasks_data[task_name] = task_data
            st.success(f"✅ Task '{task_name}' added successfully")
    
    # Simulation Controls
    st.markdown("### 🎮 Simulation Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start", type="primary", use_container_width=True):
            st.session_state.simulation_running = True
            st.success("🟢 Simulation started")
    
    with col2:
        if st.button("⏹️ Stop", use_container_width=True):
            st.session_state.simulation_running = False
            st.info("🔴 Simulation stopped")
    
    # Advanced Controls
    if st.button("📊 Generate Report", use_container_width=True):
        report = generate_system_report()
        st.download_button(
            label="💾 Download System Report",
            data=report,
            file_name=f"battery_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    if st.button("🗑️ Clear All Data", use_container_width=True):
        st.session_state.cells_data = {}
        st.session_state.tasks_data = {}
        st.session_state.historical_data = []
        st.session_state.alerts = []
        st.session_state.simulation_running = False
        st.session_state.system_health = 100
        st.success("🧹 All data cleared!")
        st.rerun()

# Main content area
if st.session_state.cells_data:
    # Real-time simulation
    if st.session_state.simulation_running:
        simulate_real_time_data()
        time.sleep(0.5)  # Slower updates for better visualization
        st.rerun()
    
    # Enhanced metrics overview
    st.markdown("### 📊 System Overview")
    
    cells = list(st.session_state.cells_data.values())
    total_cells = len(cells)
    avg_voltage = sum(cell['voltage'] for cell in cells) / total_cells if total_cells > 0 else 0
    avg_temp = sum(cell['temp'] for cell in cells) / total_cells if total_cells > 0 else 0
    avg_soc = sum(cell['soc'] for cell in cells) / total_cells if total_cells > 0 else 0
    critical_cells = sum(1 for cell in cells if cell['status'] == 'Critical')
    total_capacity = sum(cell['capacity'] for cell in cells)
    avg_health = sum(cell['health'] for cell in cells) / total_cells if total_cells > 0 else 0
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric(
            label="🔋 Total Cells",
            value=total_cells,
            delta=None
        )
    
    with col2:
        voltage_delta = avg_voltage - 3.6 if avg_voltage else 0
        st.metric(
            label="⚡ Avg Voltage",
            value=f"{avg_voltage:.2f}V",
            delta=f"{voltage_delta:+.2f}V"
        )
    
    with col3:
        temp_delta = avg_temp - 30 if avg_temp else 0
        st.metric(
            label="🌡️ Avg Temperature",
            value=f"{avg_temp:.1f}°C",
            delta=f"{temp_delta:+.1f}°C"
        )
    
    with col4:
        st.metric(
            label="🔄 Avg SOC",
            value=f"{avg_soc:.1f}%",
            delta=f"{avg_soc - 50:+.1f}%" if avg_soc else None
        )
    
    with col5:
        st.metric(
            label="⚠️ Critical Cells",
            value=critical_cells,
            delta=f"-{critical_cells}" if critical_cells > 0 else "All Good"
        )
    
    with col6:
        st.metric(
            label="💪 Avg Health",
            value=f"{avg_health:.1f}%",
            delta=f"{avg_health - 90:+.1f}%" if avg_health else None
        )
    
    # Enhanced tabs with professional layout
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔋 Cell Monitor", "🎯 3D Visualization", "📈 Analytics Dashboard", 
        "📊 Real-time Monitor", "📋 Task Manager"
    ])
    
    with tab1:
        st.markdown("### 🔋 Advanced Cell Status Monitor")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status:", ["All", "Good", "Warning", "Critical"])
        with col2:
            type_filter = st.selectbox("Filter by Type:", ["All", "lfp", "li-ion", "lithium"])
        with col3:
            sort_by = st.selectbox("Sort by:", ["ID", "Voltage", "Temperature", "SOC", "Health"])
        
        # Filter and sort cells
        filtered_cells = []
        for cell_key, cell in st.session_state.cells_data.items():
            if status_filter == "All" or cell['status'] == status_filter:
                if type_filter == "All" or cell['type'] == type_filter:
                    filtered_cells.append((cell_key, cell))
        
        if sort_by == "ID":
            filtered_cells.sort(key=lambda x: x[1]['id'])
        elif sort_by == "Voltage":
            filtered_cells.sort(key=lambda x: x[1]['voltage'], reverse=True)
        elif sort_by == "Temperature":
            filtered_cells.sort(key=lambda x: x[1]['temp'], reverse=True)
        elif sort_by == "SOC":
            filtered_cells.sort(key=lambda x: x[1]['soc'], reverse=True)
        elif sort_by == "Health":
            filtered_cells.sort(key=lambda x: x[1]['health'], reverse=True)
        
        # Display cell cards in grid
        cols = st.columns(3)
        for i, (cell_key, cell) in enumerate(filtered_cells):
            with cols[i % 3]:
                status_colors = {
                    "Good": "#00ff88",
                    "Warning": "#ffaa00",
                    "Critical": "#ff4444"
                }
                
                status_classes = {
                    "Good": "status-good",
                    "Warning": "status-warning", 
                    "Critical": "status-critical"
                }
                
                status_color = status_colors.get(cell['status'], "#888888")
                status_class = status_classes.get(cell['status'], "")
                
                # Enhanced cell card with more metrics
                st.markdown(f"""
                <div class="metric-card {status_class}">
                    <h4>🔋 Cell {cell['id']} ({cell['type'].upper()})</h4>
                    <div style="color: {status_color}; font-weight: bold; font-size: 1.1rem;">
                        Status: {cell['status']}
                    </div>
                    <hr style="margin: 0.5rem 0; border-color: #333;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                        <div><strong>⚡ Voltage:</strong><br>{cell['voltage']:.2f}V</div>
                        <div><strong>🔄 Current:</strong><br>{cell['current']:.2f}A</div>
                        <div><strong>🌡️ Temp:</strong><br>{cell['temp']:.1f}°C</div>
                        <div><strong>🔋 SOC:</strong><br>{cell['soc']:.1f}%</div>
                        <div><strong>💪 Health:</strong><br>{cell['health']:.1f}%</div>
                        <div><strong>🔄 Cycles:</strong><br>{cell['cycles']}</div>
                        <div><strong>📏 Capacity:</strong><br>{cell['capacity']:.1f}Ah</div>
                        <div><strong>⚙️ Efficiency:</strong><br>{cell['efficiency']:.1f}%</div>
                    </div>
                    <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #888;">
                        Internal R: {cell['internal_resistance']:.3f}Ω<br>
                        Last Update: {cell['timestamp'].strftime('%H:%M:%S')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🎯 3D Battery Pack Visualization")
        fig_3d = create_advanced_3d_visualization()
        if fig_3d:
            st.plotly_chart(fig_3d, use_container_width=True)
            
            # 3D Controls
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔄 Rotate View"):
                    st.info("Use mouse to rotate the 3D view")
            with col2:
                if st.button("🔍 Zoom Fit"):
                    st.info("Double-click to auto-fit view")
            with col3:
                if st.button("📷 Screenshot"):
                    st.info("Right-click → Save image")
        else:
            st.info("🔋 Add cells to see 3D visualization")
    
    with tab3:
        st.markdown("### 📈 Advanced Analytics Dashboard")
        fig_dashboard = create_professional_dashboard()
        if fig_dashboard:
            st.plotly_chart(fig_dashboard, use_container_width=True)
            
            # Additional analytics
            st.markdown("#### 🔍 Detailed Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Energy analysis
                total_energy = sum(cell['voltage'] * abs(cell['current']) for cell in cells)
                avg_efficiency = sum(cell['efficiency'] for cell in cells) / len(cells)
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>⚡ Energy Analysis</h4>
                    <p><strong>Total Power:</strong> {total_energy:.2f}W</p>
                    <p><strong>Avg Efficiency:</strong> {avg_efficiency:.1f}%</p>
                    <p><strong>Total Capacity:</strong> {total_capacity:.1f}Ah</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Performance metrics
                max_temp = max(cell['temp'] for cell in cells)
                min_voltage = min(cell['voltage'] for cell in cells)
                voltage_variance = np.var([cell['voltage'] for cell in cells])
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📊 Performance Metrics</h4>
                    <p><strong>Max Temperature:</strong> {max_temp:.1f}°C</p>
                    <p><strong>Min Voltage:</strong> {min_voltage:.2f}V</p>
                    <p><strong>Voltage Variance:</strong> {voltage_variance:.4f}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 📊 Real-time System Monitor")
        
        # Real-time charts
        if st.session_state.historical_data:
            fig_realtime = create_real_time_monitor()
            if fig_realtime:
                st.plotly_chart(fig_realtime, use_container_width=True)
            
            # Live data table
            st.markdown("#### 📋 Live Data Stream")
            df_recent = pd.DataFrame(st.session_state.historical_data).tail(20)
            st.dataframe(
                df_recent.style.format({
                    'voltage': '{:.2f}V',
                    'current': '{:.2f}A', 
                    'temp': '{:.1f}°C',
                    'soc': '{:.1f}%',
                    'health': '{:.1f}%'
                }),
                use_container_width=True
            )
        else:
            st.info("📈 Start simulation to see real-time data")
    
    with tab5:
        st.markdown("### 📋 Advanced Task Manager")
        
        if st.session_state.tasks_data:
            # Task overview
            st.markdown("#### 📊 Task Overview")
            
            for task_name, task_data in st.session_state.tasks_data.items():
                priority_colors = {
                    "Low": "#888888",
                    "Medium": "#ffaa00",
                    "High": "#ff6b6b",
                    "Critical": "#ff4444"
                }
                
                priority_color = priority_colors.get(task_data.get('priority', 'Medium'), "#888888")
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="task-card">
                        <h4>📋 {task_name}</h4>
                        <div style="color: {priority_color}; font-weight: bold;">
                            Priority: {task_data.get('priority', 'Medium')}
                        </div>
                        <p><strong>Type:</strong> {task_data['task_type']}</p>
                        <p><strong>Created:</strong> {task_data.get('created', 'Unknown')}</p>
                        <details>
                            <summary>View Details</summary>
                            <pre style="background: #1a1a1a; padding: 1rem; border-radius: 5px; margin-top: 0.5rem;">
{json.dumps(task_data, indent=2)}
                            </pre>
                        </details>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{task_name}"):
                        del st.session_state.tasks_data[task_name]
                        st.rerun()
                    
                    if st.button(f"▶️ Execute", key=f"execute_{task_name}"):
                        st.success(f"Executing task: {task_name}")
        else:
            st.info("📋 No tasks configured. Add tasks using the sidebar.")
            
            # Task templates
            st.markdown("#### 📝 Quick Task Templates")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔋 Quick Charge", use_container_width=True):
                    template_task = {
                        "task_type": "CC_CV",
                        "cc_value": 5.0,
                        "cv_voltage": 4.0,
                        "current": 3.0,
                        "duration_minutes": 30,
                        "priority": "High",
                        "created": datetime.now().isoformat()
                    }
                    st.session_state.tasks_data["Quick_Charge"] = template_task
                    st.rerun()
            
            with col2:
                if st.button("🧪 Health Check", use_container_width=True):
                    template_task = {
                        "task_type": "PULSE_TEST",
                        "pulse_current": 10.0,
                        "pulse_duration": 5,
                        "rest_duration": 15,
                        "cycles": 3,
                        "created": datetime.now().isoformat()
                    }
                    st.session_state.tasks_data["Health_Check"] = template_task
                    st.rerun()
            
            with col3:
                if st.button("😴 Rest Mode", use_container_width=True):
                    template_task = {
                        "task_type": "IDLE",
                        "duration_minutes": 60,
                        "created": datetime.now().isoformat()
                    }
                    st.session_state.tasks_data["Rest_Mode"] = template_task
                    st.rerun()

else:
    st.info("🔋 No battery cells configured. Add cells using the sidebar controls to get started.")

# Professional footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #888;">
    <p><strong>🔋 Advanced Battery Cell Management System</strong></p>
    <p>Built with ❤️ using Streamlit • Plotly • Professional Engineering Standards</p>
    <p style="font-size: 0.9rem;">© 2024 Battery Management Solutions | Version 2.0 Professional</p>
</div>
""", unsafe_allow_html=True)