# 🤖 AI Support Agent

Agente de suporte ao cliente com IA (Claude) que **integra sistemas via APIs REST** usando *tool use*:

- 📦 Consulta o status de pedidos (API REST de pedidos)
- 🎫 Escala para humanos abrindo issues via **GitHub REST API**

```
Cliente → POST /chat → FastAPI → Claude ⇄ Tools (REST) → resposta
                                          ├─ GET  /orders/{id}
                                          └─ POST api.github.com/repos/{repo}/issues
```

## Rodando

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencha ANTHROPIC_API_KEY
uvicorn app.main:app --reload
```

## Testando

```bash
curl -X POST localhost:8000/chat -H "Content-Type: application/json" \
  -d '{"message": "Cadê meu pedido 1003? Já está atrasado!"}'
```

A resposta traz `reply` e `tool_calls` (mostra quais APIs o agente chamou).
Docs interativas: http://localhost:8000/docs · Testes: `pytest`

## Próximos passos
- Trocar a API mock por um e-commerce/ERP real
- Adicionar memória de conversa e autenticação
- Integrar Slack/WhatsApp como canal de entrada
- Dockerfile + deploy (Render/Railway)
