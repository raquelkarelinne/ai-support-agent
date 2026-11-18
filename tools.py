"""Integrações REST que o agente pode chamar."""
import os
import httpx

ORDERS_API_URL = lambda: os.getenv("ORDERS_API_URL", "http://localhost:8000/mock")

TOOLS = [
    {
        "name": "get_order_status",
        "description": "Consulta status, transportadora e previsão de entrega de um pedido pelo ID.",
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"],
        },
    },
    {
        "name": "create_ticket",
        "description": "Abre um ticket para a equipe humana quando o problema não pode ser resolvido pelo agente.",
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "priority": {"type": "string", "enum": ["low", "medium", "high"]},
            },
            "required": ["summary", "priority"],
        },
    },
]

def get_order_status(order_id: str) -> dict:
    r = httpx.get(f"{ORDERS_API_URL()}/orders/{order_id}", timeout=10)
    if r.status_code == 404:
        return {"error": "Pedido não encontrado"}
    r.raise_for_status()
    return r.json()

def create_ticket(summary: str, priority: str) -> dict:
    token, repo = os.getenv("GITHUB_TOKEN"), os.getenv("GITHUB_REPO")
    if not token or not repo:  # dry-run
        return {"ticket": "DRY-RUN-001", "summary": summary, "priority": priority}
    r = httpx.post(
        f"https://api.github.com/repos/{repo}/issues",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
        json={"title": f"[{priority.upper()}] {summary[:80]}", "body": summary, "labels": ["support"]},
        timeout=10,
    )
    r.raise_for_status()
    return {"ticket": r.json()["html_url"]}

def call_tool(name: str, args: dict) -> dict:
    try:
        return {"get_order_status": get_order_status, "create_ticket": create_ticket}[name](**args)
    except Exception as e:  # o agente recebe o erro e pode se recuperar
        return {"error": str(e)}
