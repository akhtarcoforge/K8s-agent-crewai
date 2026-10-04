import os
import sys
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

# ==============================================================================
# 🛡️ ENTERPRISE AIR-GAPPED & COMPLIANCE CONFIGURATION
# ==============================================================================
# Disable CrewAI's default telemetry outbound network pathways to home servers
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

# Verify the local Python Kubernetes SDK client package is available
try:
    from kubernetes import client, config
except ImportError:
    print("[Error] Missing 'kubernetes' SDK library. Please execute: pip install kubernetes")
    sys.exit(1)

# Connect CrewAI core to your local Llama 3.2 engine running on your Mac via Ollama
local_llm = LLM(
    model="ollama/llama3.2:3b",
    base_url="http://localhost:11434"
)

# Configure the local vector embedding manager to run 100% offline via Ollama
local_embedder = {
    "provider": "ollama",
    "config": {
        "model": "llama3.2:3b",
        "base_url": "http://localhost:11434"
    }
}

# ==============================================================================
# 🔌 LIVE INFRASTRUCTURE INTEGRATION TOOL
# ==============================================================================
@tool("Kubernetes Cluster Inspector")
def inspect_k8s_cluster(pod_name: str) -> str:
    """Connects to the active cluster configuration control plane and extracts live container logs."""
    print(f"\n⚡ [LIVE INFRASTRUCTURE ACTION] Connecting to Kube-API. Fetching logs for pod: {pod_name}...")
    try:
        # Load local cluster authentication context parameters automatically from ~/.kube/config
        config.load_kube_config()
        v1 = client.CoreV1Api()

        # Programmatically pull raw container logs out of the default cluster namespace
        # We limit the read to the final 40 lines to stay well within local LLM text windows
        pod_logs = v1.read_namespaced_pod_log(name=pod_name, namespace="default", tail_lines=40)
        return f"AUTHENTIC REAL-TIME CLUSTER TELEMETRY FOR POD '{pod_name}':\n{pod_logs}"
    except Exception as e:
        return f"[Tool Error] Unable to securely query live cluster parameters: {str(e)}. Ensure minikube is active and pod exists."

# ==============================================================================
# 🤖 AUTONOMOUS AGENT ROLE DEFINTIONS
# ==============================================================================
sre_lead_agent = Agent(
    role="Principal Site Reliability Engineer (SRE)",
    goal="Inspect cluster infrastructure components, trace runtime system failures, and isolate core software dependencies.",
    backstory="You are an expert Kubernetes engineer. You utilize secure, read-only diagnostic tools to inspect log files, extract error flags, and isolate exact infrastructure faults.",
    tools=[inspect_k8s_cluster],
    llm=local_llm,
    verbose=True
)

incident_commander_agent = Agent(
    role="DevOps Incident Commander",
    goal="Synthesize technical log matrices into clean, highly structured, 3-step incident response playbooks for human engineers.",
    backstory="You are a senior DevOps architect. Your job is to take raw container logs and technical telemetry summaries provided by the SRE team and translate them into direct, clear restoration procedures.",
    llm=local_llm,
    verbose=True
)

# ==============================================================================
# 📋 TASK ASSIGNMENTS
# ==============================================================================
triage_task = Task(
    description="Analyze the health status of the active container pod 'auth-service-v2'. Invoke the Kubernetes Cluster Inspector tool to extract its live terminal error signature.",
    expected_output="Raw log strings extracted straight from the active container runtime configuration space.",
    agent=sre_lead_agent
)

playbook_generation_task = Task(
    description="Review the live log telemetry gathered. Synthesize a pristine, structured markdown playbook detailing: 1. What failed, 2. The exact root cause, and 3. The precise command line syntax required to fix it.",
    expected_output="A clean markdown incident report document mapping out immediate copy-paste mitigation steps.",
    agent=incident_commander_agent
)

# ==============================================================================
# 🚀 ORCHESTRATION & RUN LOOPS
# ==============================================================================
devops_crew = Crew(
    agents=[sre_lead_agent, incident_commander_agent],
    tasks=[triage_task, playbook_generation_task],
    process=Process.sequential,  # Sequential mode forces the SRE to hand off its findings to the Commander
    embedder=local_embedder       # Forces all semantic embeddings to stay offline on your Mac
)

if __name__ == "__main__":
    print("🚀 Initializing Autonomous Air-Gapped K8s Triage Framework...")
    result = devops_crew.kickoff()
    print("\n==================================================================")
    print("  🏆 LIVE AUTONOMOUS AGENT INCIDENT PLAYBOOK GENERATED           ")
    print("==================================================================")
    print(result)
    print("==================================================================")
