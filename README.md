# 🏥 DischargeAI — Multi-Agent FHIR Discharge Coordinator

DischargeAI is an interoperable multi-agent healthcare AI system designed to support safer hospital discharge planning and care transitions.

Built for the Agents Assemble Healthcare AI Hackathon, the platform orchestrates multiple specialized healthcare agents to generate a comprehensive “Discharge Intelligence Plan” from clinical discharge summaries.


# 🚀 Features

## Multi-Agent Healthcare Workflow
The system coordinates specialized AI agents for:

- 💊 Medication reconciliation
- 🚨 Warning sign detection
- 📅 Follow-up coordination
- 📚 Caregiver education
- 🏥 Facility recommendations
- 💳 Insurance guidance
- 📊 Readmission risk assessment
- 🧠 Final discharge plan synthesis

---

# 🧠 Inspiration

This project was inspired by research involving PICU (Pediatric Intensive Care Unit) datasets and healthcare machine learning workflows.

The goal was to explore how interoperable AI systems could support safer discharge coordination, reduce fragmentation, and improve post-hospital care transitions.



# 🏗️ Architecture

```text
Discharge Summary
        ↓
Coordinator Agent
        ↓
7 Specialist Healthcare Agents
        ↓
MCP-Compatible Server
        ↓
Prompt Opinion Integration


# 🔌 Interoperability

DischargeAI includes:

- MCP-compatible endpoints
- SSE transport support
- Prompt Opinion integration
- FHIR-aware healthcare workflows
- External healthcare AI orchestration

The project exposes interoperable healthcare workflow capabilities through a public MCP-compatible endpoint.


# ⚙️ Tech Stack

- Python
- Streamlit
- Groq API
- Llama 3.3 70B
- FastMCP
- FastAPI
- Uvicorn
- HAPI FHIR
- ngrok
- Prompt Opinion
- FHIR R4
- SSE Transport

# 📂 Project Structure

```text
app.py                     # Streamlit frontend
mcp_server.py              # MCP-compatible server
fhir_utils.py              # FHIR patient context loading

base_agent.py              # Base LLM agent
coordinator_agent.py       # Master orchestration agent
medication_agent.py        # Medication analysis
warning_agent.py           # Safety monitoring
followup_agent.py          # Follow-up coordination
education_agent.py         # Caregiver education
facility_agent.py          # Facility recommendations
insurance_agent.py         # Insurance guidance
risk_agent.py              # Readmission risk analysis
```

---

# ▶️ Running Locally

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/dischargeai.git
cd dischargeai
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows
```bash
venv\Scripts\activate
```

### Mac/Linux
```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Add Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_api_key_here
```

---

## 5. Run Streamlit App

```bash
streamlit run app.py
```

---

# 🔌 Running MCP Server

```bash
python mcp_server.py sse 8000
```

Expose publicly with ngrok:

```bash
ngrok http 8000 --host-header=rewrite
```

---

# Groq API
Create an account in Groq and you can get free API from there and paste the API inside the Streamlit App

# 🧪 Sample Workflow

1. Paste hospital discharge summary
2. Coordinator orchestrates healthcare agents
3. Agents analyze medications, risks, follow-up, education, and care transitions
4. Final “Discharge Intelligence Plan” generated
5. MCP-compatible endpoint exposed to Prompt Opinion ecosystem

---

# 📸 Demo

The demo showcases:
- multi-agent healthcare orchestration
- discharge intelligence generation
- MCP-compatible interoperability
- Prompt Opinion integration
- FHIR-aware healthcare workflows

---

# ⚠️ Disclaimer

This project is for research and hackathon demonstration purposes only.

It is not intended for direct clinical deployment or medical decision-making without physician oversight.

---

# 🌟 Future Improvements

- Real EHR integration
- SHARP context propagation
- Stronger hallucination reduction
- Longitudinal patient tracking
- Clinician review workflows
- Expanded post-acute coordination tools

---

# 👨‍💻 Built For

Agents Assemble — The Healthcare AI Endgame Hackathon

Focused on:
- MCP interoperability
- Multi-agent healthcare AI
- FHIR-aware workflows
- Prompt Opinion ecosystem integration
