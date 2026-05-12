# mcp_server.py  —  MCP Server for Prompt Opinion Platform
"""
Run modes:
  python mcp_server.py          → stdio (Claude Desktop)
  python mcp_server.py sse 8000 → HTTP/SSE (Prompt Opinion)

Then: ngrok http 8000
Register the ngrok HTTPS URL on Prompt Opinion as an MCP Server.
"""
import os, sys, json
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP(
    name="discharge-planning-coordinator",
    instructions="""You are DischargeAI — a Discharge Planning Coordinator powered by 7 specialist AI agents.
You orchestrate: Medication, Warning Signs, Follow-Up, Caregiver Education, Facility Finder, Insurance, and Risk agents.
SHARP context: patient_id, fhir_base_url, fhir_token are auto-injected from the EHR session by Prompt Opinion.""",
)


@mcp.tool()
def run_discharge_plan(
    discharge_note: str,
    patient_id:     str = "",
    fhir_base_url:  str = "https://hapi.fhir.org/baseR4",
    fhir_token:     str = "",
    insurance_type: str = "Medicare",
) -> str:
    """
    Run the full 7-agent Discharge Planning pipeline.
    Returns a complete Discharge Intelligence Plan.
    SHARP context: patient_id, fhir_base_url, fhir_token from EHR session.
    """
    from agents.coordinator_agent import DischargePlanningCoordinator

    ctx = {}
    if patient_id:
        try:
            from fhir_utils import build_patient_context
            ctx = build_patient_context(patient_id, fhir_base_url, fhir_token or None)
        except Exception as e:
            ctx = {"fhir_error": str(e), "patient_id": patient_id}

    coordinator = DischargePlanningCoordinator()
    results = coordinator.run(discharge_note=discharge_note,
                              patient_context=ctx, insurance_type=insurance_type)

    return json.dumps({
        "metadata":   results.get("metadata", {}),
        "final_plan": results.get("final_plan", ""),
        "risk":       results.get("risk", ""),
        "warnings":   results.get("warnings", ""),
        "medications":results.get("medications", ""),
    }, indent=2)


@mcp.tool()
def get_fhir_patient(
    patient_id:    str,
    fhir_base_url: str = "https://hapi.fhir.org/baseR4",
    fhir_token:    str = "",
) -> str:
    """
    Fetch patient summary from a FHIR R4 server.
    Returns demographics, conditions, medications, allergies.
    SHARP context: patient_id, fhir_base_url, fhir_token.
    """
    from fhir_utils import build_patient_context
    try:
        ctx = build_patient_context(patient_id, fhir_base_url, fhir_token or None)
        return json.dumps(ctx, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "patient_id": patient_id})


@mcp.tool()
def assess_risk(
    discharge_note: str,
    patient_id:     str = "",
    fhir_base_url:  str = "https://hapi.fhir.org/baseR4",
    fhir_token:     str = "",
) -> str:
    """
    Assess 30-day hospital readmission risk using the LACE index.
    Returns risk level, contributing factors, and mitigation strategies.
    SHARP context: patient_id, fhir_base_url, fhir_token.
    """
    from agents.risk_agent import RiskAgent
    ctx = {}
    if patient_id:
        try:
            from fhir_utils import build_patient_context
            ctx = build_patient_context(patient_id, fhir_base_url, fhir_token or None)
        except Exception:
            pass
    agent = RiskAgent()
    result = agent.analyze(discharge_note, patient_context=ctx)
    return json.dumps({"risk_assessment": result, "patient_id": patient_id}, indent=2)


if __name__ == "__main__":
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    port      = int(sys.argv[2]) if len(sys.argv) > 2 else int(os.getenv("MCP_SERVER_PORT","8000"))

    print("╔═══════════════════════════════════════════════════════╗")
    print("║   🏥  DischargeAI — MCP Server for Prompt Opinion    ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print(f"  Transport : {transport}")
    if transport == "sse":
        print(f"  Port      : {port}")
        print(f"  SSE URL   : http://0.0.0.0:{port}/sse")
        print()
        print("  Next steps:")
        print(f"    ngrok http {port}")
        print("    Copy HTTPS URL → Prompt Opinion → MCP Servers → Add New")
        print()
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")
