import streamlit as st
from datetime import datetime
import threading
import time


st.set_page_config(
    page_title="Agent Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State Initialization ---
if "agent_status" not in st.session_state:
    st.session_state.agent_status = {
        "Listener": "idle",
        "Planner": "idle",
        "Executor": "idle",
    }

if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = {
        "Listener": [],
        "Planner": [],
        "Executor": [],
    }

# --- UI ---
st.title("🧠 Agent Dashboard")

st.sidebar.header("Controls")

selected_agent = st.sidebar.selectbox(
    "Select Agent",
    ["Listener", "Planner", "Executor"]
)

col1, col2 = st.sidebar.columns(2)

with col1:
    start_clicked = st.button("▶ Start")

with col2:
    stop_clicked = st.button("⏹ Stop")

# --- Actions ---
timestamp = datetime.now().strftime("%H:%M:%S")

if start_clicked:
    st.session_state.agent_status[selected_agent] = "running"
    st.session_state.agent_logs[selected_agent].append(
        f"[{timestamp}] Agent started"
    )

if stop_clicked:
    st.session_state.agent_status[selected_agent] = "stopped"
    st.session_state.agent_logs[selected_agent].append(
        f"[{timestamp}] Agent stopped"
    )

# --- Status & Logs ---
st.subheader("Agent Status & Logs")

for agent, status in st.session_state.agent_status.items():
    with st.expander(f"{agent} — {status.upper()}"):
        logs = st.session_state.agent_logs[agent]
        if logs:
            for line in logs[-10:]:
                st.text(line)
        else:
            st.text("No logs yet.")

# --- Agent Worker --- #
def agent_worker(agent_name):
    while st.session_state.agent_status[agent_name] == "running":
        timestamp = time.strftime("%H:%M:%S")
        st.session_state.agent_logs[agent_name].append(
            f"[{timestamp}] {agent_name} heartbeat"
        )
        time.sleep(2)  # simulate work
if "agent_threads" not in st.session_state:
    st.session_state.agent_threads = {}

if start_clicked:
    if st.session_state.agent_status[selected_agent] != "running":
        st.session_state.agent_status[selected_agent] = "running"
        st.session_state.agent_logs[selected_agent].append(
            f"[{timestamp}] Agent started"
        )

        thread = threading.Thread(
            target=agent_worker,
            args=(selected_agent,),
            daemon=True
        )
        st.session_state.agent_threads[selected_agent] = thread
        thread.start()
if stop_clicked:
    if st.session_state.agent_status[selected_agent] == "running":
        st.session_state.agent_status[selected_agent] = "stopped"
        st.session_state.agent_logs[selected_agent].append(
            f"[{timestamp}] Agent stopped"
        )

auto_refresh = st.sidebar.checkbox("Live updates", value=True)

if auto_refresh:
    time.sleep(0.5)
    st.rerun()

