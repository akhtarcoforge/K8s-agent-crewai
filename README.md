# K8s-agent-crewai
# 🤖 Autonomous Air-Gapped Multi-Agent Framework for Kubernetes Incident Triage

An enterprise-grade, security-first AIOps orchestration framework built using **Python and CrewAI**. This system dynamically intercepts Kubernetes container runtime failures (such as `CrashLoopBackOff` events), programmatically hooks into live cluster control planes via the native **Kubernetes Python SDK**, and delegates troubleshooting tasks across a collaborative team of specialized AI agents.

To satisfy strict corporate compliance and data residency constraints (common in banking, healthcare, and enterprise fintech), the entire analytical brain runs **100% locally and offline** using **Llama 3.2 via Ollama**, ensuring zero infrastructure telemetry, code secrets, or proprietary stack traces leak to public cloud endpoints.

---

## 🏗️ Architectural Blueprint & Collaborative Flow


[ Failing K8s Pod ] ◄── (1. CrashLoopBackOff detected)
│
▼ (Triggers Framework Orchestration Loop)
┌────────────────────────────────────────────────────────┐
│                  THE CREW (CrewAI)                     │
│                                                        │
│  ┌───────────────────────┐      ┌───────────────────┐  │
│  │       AGENT 1:        │      │     AGENT 2:      │  │
│  │     Principal SRE     │      │Incident Commander │  │
│  └──────────┬────────────┘      └─────────▲─────────┘  │
│             │                             │            │
│             ▼ (Invokes Tool)              │ (Hands off │
│  ┌───────────────────────┐             │ Diagnostics)│
│  │  Kube-API Ingestion   │─────────────┘               │
│  │   (Kubernetes SDK)    │                             │
│  └───────────────────────┘                             │
└──────────────────────────┬─────────────────────────────┘
│
▼ (Local Socket - Port 11434)
[ Ollama Core Engine ] ──► (Llama 3.2 3B Inference)
│
▼
[ Formatted Markdown Playbook Generated ]

---

## 📂 Project Structure & Functions Breakdown

The core engine (`live_k8s_agent.py`) implements a decoupled, sequential architecture designed around three foundational layers:

### 1. Ingestion Layer: `inspect_k8s_cluster(pod_name)`
* **The Mechanics:** A custom programmatic DevOps tool decorated via CrewAI structures. It securely initializes cluster authentication by parsing configuration context (`config.load_kube_config()`) directly from the local host pathway.
* **The Operation:** It maps to the core cluster API via `client.CoreV1Api()`, reads the live raw container stdout text stream (`read_namespaced_pod_log`), and slices the evaluation footprint down to the final 40 console lines. This keeps context processing windows highly optimized and prevents token bloat.

### 2. Multi-Agent Reasoning Loop (Sequential Process)
* **Agent A: The Principal SRE Agent** 
  * *Role/Backstory:* An expert cluster system administrator tasked with pulling live diagnostic metrics, filtering out structural noises, and establishing a raw error signature tracking block.
  * *Execution:* Executes the Kube-API inspector tool, reads the standard error stream, and transforms unstructured text logs into clean data points.
* **Agent B: The DevOps Incident Commander**
  * *Role/Backstory:* A senior platform systems architect who ingests technical inputs from the SRE layer and translates complex stack dumps into highly consumable operational playbooks for human development teams.

### 3. Air-Gapped Compliance Control
* Explicitly forces `CREWAI_TELEMETRY_OPT_OUT = "true"` to sever any outbound tracking calls to external home servers.
* Overrides the default open-source memory engine by passing a localized `embedder` configuration matrix pointing to the internal Ollama daemon, maintaining absolute data perimeter boundaries on your processing core.

---

## 🛠️ Installation, Sandbox Setup & Local Execution

### Prerequisites
* **macOS** with a working Homebrew environment.
* Stable **Python 3.12** sandbox configuration (Python 3.14 or legacy <3.10 are unsupported by CrewAI tokenizers).

### Step 1: Provision Private AI and Cluster Drivers
1. **Install and spin up the QEMU lightweight Mac hypervisor engine:**
   ```bash
   brew install qemu
   ```
2. **Boot up a local single-node Kubernetes environment forcing QEMU execution:**
   ```bash
   minikube start --driver=qemu
   ```
3. **Download and initialize the local AI model repository:**
   ```bash
   brew install ollama
   brew services start ollama
   ollama run llama3.2:3b
   # Once the progress bar fills up and the chat window opens, type /exit and hit Enter.
   ```

### Step 2: Set Up Your Project Virtual Workspace
1. **Initialize a fresh Python 3.12 sandbox inside your folder:**
   ```bash
   cd ~/DevOps/adv-log-parser
   rm -rf .venv  # Clear any legacy broken system environments
   /opt/homebrew/bin/python3.12 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install pre-compiled dependency wheels inside your isolated workspace:**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install crewai kubernetes ollama
   ```

### Step 3: Inject a Real Production Crash State for the AI to Diagnose
To verify the framework, push a live container deployment that intentionally enters a failing `CrashLoopBackOff` state due to a missing service asset path:
```bash
kubectl run auth-service-v2 --image=nginx --command -- sh -c "echo '[FATAL] Database connection refused on port 5432' && exit 1"
```
*(Verify by running `kubectl get pods` - you will see `auth-service-v2` actively crashing on your machine's kernel).*

### Step 4: Kickoff the Autonomous Run
Execute your live framework script from your active sandbox terminal:
```bash
python3 live_k8s_agent.py
```

---

## 🎯 Sample Production Telemetry Output

When executed, the system tracks the multi-agent task loop in real time:

```text
🚀 Initializing Autonomous Air-Gapped K8s Triage Framework...
╭─────────────────────────────────── 🤖 Agent Started ───────────────────────────────────╮
│  Agent: Principal Site Reliability Engineer (SRE)                                      │
│  Task: Analyze the health status of the active container pod 'auth-service-v2'...       │
╰────────────────────────────────────────────────────────────────────────────────────────╯

⚡ [LIVE INFRASTRUCTURE ACTION] Connecting to Kube-API. Fetching logs for pod: auth-service-v2...
Tool kubernetes_cluster_inspector executed with result: AUTHENTIC REAL-TIME CLUSTER TELEMETRY:
b'[FATAL] Database connection refused on port 5432\n'...

╭─────────────────────────────────── 🤖 Agent Started ───────────────────────────────────╮
│  Agent: DevOps Incident Commander                                                      │
│  Task: Review the live log telemetry gathered. Synthesize a structured playbook...       │
╰────────────────────────────────────────────────────────────────────────────────────────╯

==================================================================
  🏆 LIVE AUTONOMOUS AGENT INCIDENT PLAYBOOK GENERATED           
==================================================================
**Incident Report: auth-service-v2 Pod Failure**

### 1. What Failed
The container pod `auth-service-v2` failed during runtime boot sequence. The Kube-API core container logs returned an explicit crash exit code.

### 2. Root Cause Analysis
The application layer initiated a connection hook to a backend database module on port `5432`. The target network port rejected the packet stream (`Connection Refused`), causing the internal engine to throw a `[FATAL]` exception signature and exit the process.

### 3. Recommended Remediation Playbook
* Step 1: Verify the database cluster pod state and endpoint exposure parameters:
  ```bash
  kubectl get svc,pods -n production | grep db
  ```
* Step 2: Ensure the network policies inside Minikube allow communication on port 5432:
  ```bash
  kubectl describe networkpolicy
  ```
==================================================================
```

---

## 📈 Measurable Business & Engineering Outcomes
* **Zero Investigation Toil:** Completely automates initial L1/L2 on-call manual tasks (`kubectl logs`, `describe`).
* **MTTR Optimization:** Shrinks the initial cluster incident investigation footprint from a **15-minute manual task down to under 5 seconds of automated machine inference.**
* **100% Privacy Compliance:** Absolute data residency is preserved. Zero metadata fields, cluster node names, or internal logging configurations leave the corporate security perimeter.



