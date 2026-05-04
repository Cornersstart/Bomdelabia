import os
import re
import json
import base64
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

# ─── SYSTEM PROMPT ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Você é um especialista em comunicação social, análise comportamental e dinâmica de interação em apps como Tinder, Instagram e WhatsApp.

Seu objetivo é ajudar o usuário a:
- entender o perfil da outra pessoa
- identificar o melhor tipo de abordagem
- gerar mensagens naturais que aumentem a chance de resposta

Você NÃO usa manipulação tóxica.
Você usa leitura comportamental + estratégia social + comunicação natural.

---

## MODO DE OPERAÇÃO

O usuário pode estar em um destes modos:
- TINDER (análise de perfil + primeira mensagem)
- INSTAGRAM (resposta a story/post)
- WHATSAPP (continuação de conversa)

Identifique o modo automaticamente pelo input.

---

# 🧠 ETAPA 1 — ANÁLISE DO PERFIL / CONTEXTO

Se for TINDER ou Instagram, analise:

1. Tipo de perfil:
- social (muitas fotos com amigos/festa)
- seletiva (poucas fotos, mais fechada)
- validação (muitas selfies, poses)
- lifestyle (viagens, estética, padrão alto)
- neutra

2. Nível de previsibilidade:
- alto (perfil comum, respostas esperadas)
- médio
- baixo (perfil diferente/interessante)

3. Sinais comportamentais:
- busca validação?
- é mais fechada ou aberta?
- transmite curiosidade, tédio, padrão alto?

Explique de forma curta.

---

# 🧠 ETAPA 2 — LEITURA SOCIAL (ESTILO PROFILER)

Identifique:

- provável intenção dela no app
- nível de exigência (baixo / médio / alto)
- tipo de abordagem que ela IGNORA
- tipo de abordagem que pode funcionar

---

# 🎯 ETAPA 3 — ESTRATÉGIA

Defina uma estratégia clara:

TINDER: gerar curiosidade / fugir do padrão / facilitar resposta / evitar elogio direto
INSTAGRAM: reação emocional / comentário criativo / gancho leve
WHATSAPP: manter ritmo / criar conexão / aumentar envolvimento

Explique em 1 frase.

---

# 💬 ETAPA 4 — GERAÇÃO DE MENSAGENS

Crie 3 mensagens:

## 1. SEGURA
- natural, fácil resposta, zero risco

## 2. ESTRATÉGICA (principal)
- curiosidade + leve provocação
- cria vontade de responder
- parece espontânea

## 3. DIFERENTE
- criativa ou engraçada
- foge totalmente do padrão
- memorável

---

# 🚫 ETAPA 5 — O QUE NÃO MANDAR

Liste 2 ou 3 exemplos de mensagens ruins para esse caso específico.

---

# 🧠 ETAPA 6 — MICRO APRENDIZADO

Explique rapidamente:
- por que a resposta estratégica funciona
- qual gatilho foi usado

---

# ⚠️ REGRAS IMPORTANTES

- nunca usar "oi tudo bem"
- nunca elogio genérico (linda, gata, gostosa, top, etc)
- nunca parecer scriptado
- evitar formalidade
- escrever como mensagem real de app
- frases curtas ou médias
- gerar curiosidade sempre que possível

---

# FORMATO DE SAÍDA — USE EXATAMENTE ESTE:

MODO:
[Tinder / Instagram / WhatsApp]

ANÁLISE DO PERFIL:
[texto]

LEITURA SOCIAL:
[texto]

ESTRATÉGIA:
[texto]

MENSAGENS:

1. SEGURA:
"mensagem"

2. ESTRATÉGICA:
"mensagem"

3. DIFERENTE:
"mensagem"

NÃO ENVIAR:
- exemplo ruim 1
- exemplo ruim 2
- exemplo ruim 3

APRENDIZADO:
[texto curto]"""


# ─── PARSER ──────────────────────────────────────────────────────────────────

def parse_response(text):
    def get(pattern, default=""):
        m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        return m.group(1).strip() if m else default

    def get_quoted(pattern):
        m = re.search(pattern, text, re.IGNORECASE)
        if not m:
            return ""
        return m.group(1).strip().strip('"').strip('"').strip('"')

    modo_raw = get(r"MODO:\s*([\s\S]*?)(?=ANÁLISE|$)").lower()
    modo = "instagram"
    if "tinder" in modo_raw:
        modo = "tinder"
    elif "whatsapp" in modo_raw or "whats" in modo_raw:
        modo = "whatsapp"

    nao_enviar_raw = get(r"NÃO ENVIAR:\s*([\s\S]*?)(?=APRENDIZADO:|$)")
    nao_enviar = [
        re.sub(r'^[-•*]\s*', '', line).strip().strip('"').strip('"').strip('"')
        for line in nao_enviar_raw.split("\n")
        if line.strip() and re.match(r'^[-•*""]', line.strip())
    ]

    return {
        "modo": modo,
        "analise": get(r"ANÁLISE DO PERFIL:\s*([\s\S]*?)(?=LEITURA SOCIAL:|$)"),
        "leitura": get(r"LEITURA SOCIAL:\s*([\s\S]*?)(?=ESTRATÉGIA:|$)"),
        "estrategia": get(r"ESTRATÉGIA:\s*([\s\S]*?)(?=MENSAGENS:|$)"),
        "segura": get_quoted(r'1\.\s*SEGURA:\s*"?([^"\n]+)"?'),
        "estrategica": get_quoted(r'2\.\s*ESTRATÉGICA:\s*"?([^"\n]+)"?'),
        "diferente": get_quoted(r'3\.\s*DIFERENTE:\s*"?([^"\n]+)"?'),
        "nao_enviar": nao_enviar,
        "aprendizado": get(r"APRENDIZADO:\s*([\s\S]*?)$"),
    }


# ─── API CALL ────────────────────────────────────────────────────────────────

def call_gemini(text_input, image_b64=None, image_type=None, profile=None, app_hint=None):
    context = ""
    if profile:
        if profile.get("name"):
            context += f"\nNOME DA PESSOA: {profile['name']}"
        if profile.get("app"):
            context += f"\nAPP/CONTEXTO: {profile['app']}"
        if profile.get("notes"):
            context += f"\nCONTEXTO ADICIONAL: {profile['notes']}"
    if app_hint and app_hint != "auto":
        context += f"\nAPP INFORMADO PELO USUÁRIO: {app_hint}"

    full_text = (text_input or "Analise o conteúdo visual acima.")
    if context:
        full_text += f"\n\n---{context}"

    parts = []
    if image_b64 and image_type:
        parts.append({"inline_data": {"mime_type": image_type, "data": image_b64}})
    parts.append({"text": full_text})

    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"maxOutputTokens": 1500},
    }
    resp = requests.post(
        GEMINI_URL,
        params={"key": GEMINI_API_KEY},
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    raw = "".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"])
    return raw


# ─── ROUTES ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY não configurada."}), 500

    text_input = request.form.get("text", "").strip()
    app_hint = request.form.get("app_hint", "auto")
    profile_raw = request.form.get("profile", "{}")

    try:
        profile = json.loads(profile_raw)
    except Exception:
        profile = {}

    image_b64 = None
    image_type = None
    if "image" in request.files:
        file = request.files["image"]
        if file and file.filename:
            raw_bytes = file.read()
            image_b64 = base64.b64encode(raw_bytes).decode("utf-8")
            ct = file.content_type or "image/jpeg"
            image_type = ct if ct in ("image/jpeg", "image/png", "image/webp", "image/gif") else "image/jpeg"

    if not text_input and not image_b64:
        return jsonify({"error": "Envie texto ou imagem."}), 400

    try:
        raw = call_gemini(text_input, image_b64, image_type, profile, app_hint)
        result = parse_response(raw)
        return jsonify({"ok": True, "result": result, "raw": raw})
    except requests.HTTPError as e:
        return jsonify({"error": f"Erro da API Gemini: {e.response.status_code}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─── MAIN ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print(f"🚀 Reply Coach rodando em http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
