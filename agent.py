"""Loop do agente: Claude decide quais ferramentas (APIs) chamar."""
import json
import os
from anthropic import Anthropic
from .tools import TOOLS, call_tool

SYSTEM = (
    "Você é um agente de suporte ao cliente educado e objetivo. Responda em português. "
    "Use get_order_status para dúvidas de pedidos. Se não conseguir resolver, "
    "ou o cliente estiver muito insatisfeito, use create_ticket e informe o número."
)

def run_agent(message: str, max_steps: int = 5) -> dict:
    client = Anthropic()
    model = os.getenv("MODEL", "claude-sonnet-5-5")
    messages = [{"role": "user", "content": message}]
    calls = []
    for _ in range(max_steps):
        resp = client.messages.create(
            model=model, max_tokens=1000, system=SYSTEM, tools=TOOLS, messages=messages
        )
        if resp.stop_reason != "tool_use":
            text = "".join(b.text for b in resp.content if b.type == "text")
            return {"reply": text, "tool_calls": calls}
        messages.append({"role": "assistant", "content": resp.content})
        results = []
        for b in resp.content:
            if b.type == "tool_use":
                out = call_tool(b.name, b.input)
                calls.append({"tool": b.name, "input": b.input, "output": out})
                results.append(
                    {"type": "tool_result", "tool_use_id": b.id, "content": json.dumps(out)}
                )
        messages.append({"role": "user", "content": results})
    return {"reply": "Não consegui concluir, um humano vai assumir.", "tool_calls": calls}
