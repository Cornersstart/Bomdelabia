import os
import re
import json
import base64
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"

# ─── SYSTEM PROMPT ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Você é um especialista em comunicação social, análise comportamental e psicologia aplicada à interação em apps de relacionamento e redes sociais.

## BASE DE CONHECIMENTO — PRINCÍPIOS PSICOLÓGICOS

Sua análise integra os seguintes princípios, aplicados de forma prática:

**Sedução e mistério** (Greene — A Arte da Sedução): Gere curiosidade antes de confiança. Nunca se entregue completamente. Use escassez e distância calculada. Cada pessoa tem uma chave emocional diferente — identifique-a.

**Rapport acelerado** (Schafer — Manual de Persuasão do FBI): Espelhe o vocabulário dela. Valide emocionalmente antes de avançar. FORD: Família, Ocupação, Recreação, Sonhos — pergunte sobre o que ela vive.

**Não-necessidade e autenticidade** (Manson — Modelos): Vulnerabilidade real atrai, performática repele. Opinião própria > concordância vazia. Polarize: melhor ser lembrado que ser genérico.

**Gatilhos de influência** (Cialdini — As Armas da Persuasão): Reciprocidade (dê algo antes de pedir), escassez (implique que seu tempo tem valor), afinidade genuína (encontre o ponto em comum real).

**Decisão emocional** (Kahneman — Rápido e Devasso): A decisão de responder é emocional, rápida e inconsciente (Sistema 1). Provoque emoção antes de pensamento. Perguntas em excesso acionam defesas racionais (Sistema 2).

**Loop de engajamento** (Duhigg — O Poder do Hábito): Sua mensagem é o gatilho. Responder deve parecer natural e recompensador, não obrigatório.

**Inteligência emocional** (Goleman): Leia o estado emocional do contexto antes de escolher o tom. Story melancólico ≠ abordagem engraçada.

**Humanidade genuína** (Carnegie / Rosenberg): Faça ela se sentir vista e compreendida. Observe sem julgar. Curiosidade genuína sempre supera elogios vazios.

---

## MODO DE OPERAÇÃO

- TINDER (análise de perfil + primeira mensagem)
- INSTAGRAM (resposta a story / post / DM)
- WHATSAPP (continuação de conversa)

Identifique o modo automaticamente pelo input, ou use o informado.

---

## CONTEXTO DA CONVERSA (MEMÓRIA)

PRIMEIRO_CONTATO: Nunca conversaram. Objetivo único: provocar curiosidade. Seja curto, específico, imprevisível. Evite qualquer coisa que pareça script ou copy-paste.

EM_ANDAMENTO: Já há conversa estabelecida. Mantenha o ritmo, aprofunde a conexão progressivamente, crie antecipação para o próximo contato.

REAQUECENDO: Ficaram sem falar por um tempo. Reentrar com leveza e naturalidade, sem mencionar o sumiço diretamente. Use humor ou contexto externo como gancho.

---

## CONTEXTO DO INSTAGRAM

ELA_ME_CONHECE: Ela já sabe quem é o usuário. Pode ser mais direto e natural. Pode referenciar algo compartilhado entre os dois. A missão não é se apresentar, é aprofundar.

ELA_NAO_ME_CONHECE: Abordagem completamente fria. Uma frase deve capturar atenção. Referência específica ao conteúdo/perfil dela. Nunca elogio genérico. Objetivo: ela querer saber quem é esse.

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
- qual gatilho psicológico é mais relevante para esse perfil?

Explique de forma curta.

---

# 🧠 ETAPA 2 — LEITURA SOCIAL (ESTILO PROFILER)

Identifique:
- provável intenção dela no app
- nível de exigência (baixo / médio / alto)
- tipo de abordagem que ela IGNORA
- tipo de abordagem que pode funcionar
- qual princípio psicológico aplicar (cite qual dos livros base é mais relevante)

---

# 🎯 ETAPA 3 — ESTRATÉGIA

Defina uma estratégia clara considerando o modo de memória e o app:

TINDER: gerar curiosidade / fugir do padrão / facilitar resposta / evitar elogio direto
INSTAGRAM (não me conhece): capturar atenção em 1-2 frases / referência específica / sem elogio genérico
INSTAGRAM (me conhece): naturalidade / referência compartilhada / aprofundar conexão
WHATSAPP: manter ritmo / criar conexão / aumentar envolvimento

Explique em 1 frase qual princípio psicológico está sendo usado.

---

# 💬 ETAPA 4 — GERAÇÃO DE MENSAGENS

Crie 3 mensagens adaptadas ao contexto de memória e ao app:

## 1. SEGURA
- natural, fácil resposta, zero risco
- usa rapport e humanidade genuína

## 2. ESTRATÉGICA (principal)
- curiosidade + leve provocação ou vulnerabilidade real
- cria vontade de responder
- parece espontânea, nunca roteirizada
- usa o gatilho psicológico identificado

## 3. DIFERENTE
- criativa, engraçada ou completamente inesperada
- foge totalmente do padrão
- memorável — ela vai pensar "quem é esse?"

---

# 🚫 ETAPA 5 — O QUE NÃO MANDAR

Liste 2 ou 3 exemplos de mensagens ruins para esse caso específico.

---

# 🧠 ETAPA 6 — MICRO APRENDIZADO

Explique rapidamente:
- por que a mensagem estratégica funciona
- qual gatilho psicológico foi usado (mencione o conceito ou livro se relevante)

---

# ⚠️ REGRAS IMPORTANTES

- nunca usar "oi tudo bem"
- nunca elogio genérico (linda, gata, gostosa, top, etc)
- nunca parecer scriptado ou copy-paste
- evitar formalidade
- escrever como mensagem real de app
- frases curtas ou médias
- cada mensagem deve ser única para esse perfil específico

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
    QUOTES = '”“”\''

    def strip_md(s):
        s = re.sub(r'\*\*(.+?)\*\*', r'\1', s, flags=re.DOTALL)
        s = re.sub(r'\*(.+?)\*',     r'\1', s, flags=re.DOTALL)
        # remove trailing markdown separators/headers that bleed into fields
        s = re.sub(r'\s*\n\s*-{3,}\s*\n?\s*#{0,2}\s*$', '', s)
        s = re.sub(r'\s*-{3,}\s*$', '', s)
        s = re.sub(r'\s*#{1,3}\s*$', '', s)
        return s.strip()

    def get(pattern, default=””):
        m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        return strip_md(m.group(1)) if m else default

    def get_msg(label_re):
        # Handles: “msg”, **”msg”**, “**msg**”, **msg**
        m = re.search(
            rf'{label_re}\s*\n?\s*\*{{0,2}}\s*[{QUOTES}]?(.*?)[{QUOTES}]?\s*\*{{0,2}}\s*(?:\n|$)',
            text, re.IGNORECASE
        )
        if not m:
            return “”
        return strip_md(m.group(1)).strip(QUOTES).strip()

    modo_raw = get(r”MODO:\s*([\s\S]*?)(?=ANÁLISE|$)”).lower()
    modo = “instagram”
    if “tinder” in modo_raw:
        modo = “tinder”
    elif “whatsapp” in modo_raw or “whats” in modo_raw:
        modo = “whatsapp”

    nao_enviar_raw = get(r”NÃO ENVIAR:\s*([\s\S]*?)(?=APRENDIZADO:|$)”)
    nao_enviar = [
        strip_md(re.sub(r'^[-•*]\s*', '', line)).strip(QUOTES).strip()
        for line in nao_enviar_raw.split(“\n”)
        if line.strip() and re.match(r'^[-•*“”*]', line.strip())
    ]

    return {
        “modo”: modo,
        “analise”:    get(r”ANÁLISE DO PERFIL:\s*([\s\S]*?)(?=LEITURA SOCIAL:|$)”),
        “leitura”:    get(r”LEITURA SOCIAL:\s*([\s\S]*?)(?=ESTRATÉGIA:|$)”),
        “estrategia”: get(r”ESTRATÉGIA:\s*([\s\S]*?)(?=MENSAGENS:|$)”),
        “segura”:      get_msg(r'1\.\s*SEGURA:'),
        “estrategica”: get_msg(r'2\.\s*ESTRATÉGICA:'),
        “diferente”:   get_msg(r'3\.\s*DIFERENTE:'),
        “nao_enviar”: nao_enviar,
        “aprendizado”: get(r”APRENDIZADO:\s*([\s\S]*?)$”),
    }


# ─── API CALL ────────────────────────────────────────────────────────────────

def call_anthropic(text_input, images=None, profile=None, app_hint=None, memory_mode=None, ig_knows_me=None):
    context_parts = []

    if profile:
        if profile.get("name"):
            context_parts.append(f"NOME DA PESSOA: {profile['name']}")
        if profile.get("app"):
            context_parts.append(f"APP/CONTEXTO: {profile['app']}")
        if profile.get("notes"):
            context_parts.append(f"CONTEXTO ADICIONAL: {profile['notes']}")

    if app_hint and app_hint != "auto":
        context_parts.append(f"APP INFORMADO: {app_hint.upper()}")

    memory_labels = {
        "primeiro-contato": "PRIMEIRO_CONTATO — nunca conversaram antes",
        "em-andamento": "EM_ANDAMENTO — já há conversa estabelecida",
        "reaquecendo": "REAQUECENDO — ficaram sem falar por um tempo",
    }
    if memory_mode and memory_mode in memory_labels:
        context_parts.append(f"MEMÓRIA: {memory_labels[memory_mode]}")

    if app_hint == "instagram" and ig_knows_me is not None:
        label = "ELA_ME_CONHECE — ela já sabe quem é o usuário" if ig_knows_me else "ELA_NAO_ME_CONHECE — abordagem completamente fria"
        context_parts.append(f"INSTAGRAM: {label}")

    full_text = text_input or "Analise o conteúdo visual acima."
    if context_parts:
        full_text += "\n\n---\n" + "\n".join(context_parts)

    user_content = []
    for img_b64, img_type in (images or []):
        user_content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": img_type, "data": img_b64},
        })
    user_content.append({"type": "text", "text": full_text})

    resp = requests.post(
        ANTHROPIC_URL,
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
        },
        json={
            "model": "claude-opus-4-5",
            "max_tokens": 1800,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": user_content}],
        },
        timeout=90,
    )
    resp.raise_for_status()
    data = resp.json()
    return "".join(b.get("text", "") for b in data.get("content", []))


# ─── ROUTES ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "ANTHROPIC_API_KEY não configurada."}), 500

    text_input = request.form.get("text", "").strip()
    app_hint = request.form.get("app_hint", "auto")
    memory_mode = request.form.get("memory_mode", "primeiro-contato")
    ig_knows_me_raw = request.form.get("ig_knows_me", "")
    ig_knows_me = (ig_knows_me_raw.lower() == "true") if ig_knows_me_raw else None
    profile_raw = request.form.get("profile", "{}")

    try:
        profile = json.loads(profile_raw)
    except Exception:
        profile = {}

    images = []
    for file in request.files.getlist("images"):
        if file and file.filename:
            raw_bytes = file.read()
            img_b64 = base64.b64encode(raw_bytes).decode("utf-8")
            ct = file.content_type or "image/jpeg"
            img_type = ct if ct in ("image/jpeg", "image/png", "image/webp", "image/gif") else "image/jpeg"
            images.append((img_b64, img_type))

    if not text_input and not images:
        return jsonify({"error": "Envie texto ou imagem."}), 400

    try:
        raw = call_anthropic(text_input, images, profile, app_hint, memory_mode, ig_knows_me)
        result = parse_response(raw)
        return jsonify({"ok": True, "result": result, "raw": raw})
    except requests.HTTPError as e:
        return jsonify({"error": f"Erro da API Anthropic: {e.response.status_code}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─── MAIN ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print(f"🚀 Reply Coach rodando em http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
