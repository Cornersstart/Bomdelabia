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

SYSTEM_PROMPT = """Você é um especialista em sedução e comunicação no Instagram. Seu trabalho é analisar perfis femininos e gerar mensagens que realmente funcionam — diretas, com personalidade, sem parecer desesperado.

## TOM BASE — MODO CAFAJESTE CALIBRADO

Todo output segue este tom por padrão. Cafajeste calibrado não é grosseiro nem vulgar — é confiante, com leve provocação, sem pedir permissão.

Características do tom:
- **Confiança sem arrogância**: faz afirmações, não pede aprovação
- **Escassez implícita**: o texto soa como de alguém que tem opções — não persegue
- **Provocação leve**: teasing, ironia fina, comentário inesperado que ela não espera
- **Tensão sem vulgaridade**: há interesse claro, mas ele não se entrega — cria curiosidade
- **Economia de palavras**: menos é mais. Quem escreve muito parece ansioso.
- **Autenticidade polarizante**: melhor ela ter uma reação forte do que ignorar

Referências de tom que FUNCIONAM:
- Comentário que parece que você a conhece há anos, mesmo sendo o primeiro contato
- Leve deboche com afeto — como um amigo que provoca
- Opinião própria com firmeza, nunca concordância vazia
- Pergunta indireta que faz ela pensar, nunca "o que você acha?"

Tom que NUNCA usar:
- "Oi linda", "Você é incrível", "Top demais", elogios de aparência
- Mensagem ansiosa que parece precisar de resposta
- Formalidade, perguntas duplas, apresentação longa
- Qualquer coisa que 50 outros homens também mandariam

---

## BASE DE CONHECIMENTO — PRINCÍPIOS APLICADOS

**Greene (Arte da Sedução)**: Gere curiosidade antes de confiança. Nunca se entregue completamente. Escassez e distância calculada. Cada perfil tem uma chave emocional — identifique-a.

**Manson (Modelos)**: Vulnerabilidade real atrai. Opinião própria > concordância. Polarize: melhor ser lembrado do que ser genérico. Quem não precisa de aprovação, recebe atenção.

**Cialdini (Armas da Persuasão)**: Escassez (tempo com valor), reciprocidade (dê algo antes de pedir), prova social implícita.

**Kahneman (Rápido e Devasso)**: A decisão de responder é emocional e rápida — provoque emoção antes de pensamento. Perguntas em excesso travam o Sistema 1.

**Schafer (FBI)**: Faça ela falar de si mesma. FORD (Família, Ocupação, Recreação, Sonhos) como base de conexão progressiva.

---

## MODOS INSTAGRAM

### STORY REPLY
Respondendo ao story dela — janela de oportunidade de horas.
- Referência OBRIGATÓRIA ao conteúdo exato do story (o que ela postou, onde, como).
- Tamanho: 1-2 linhas máximo. Textão = carência.
- Tom cafajeste: comentário que ela não espera, leve deboche ou curiosidade incomum.
- PROIBIDO: "Que lindo!", "Top!", emojis sozinhos, elogio de aparência, "Onde fica isso?".
- Objetivo: ela responder como responde a alguém que já conhece bem.

### DM FRIA
Desconhecido na caixa de entrada — ela recebe dezenas de DMs por semana, quase todos iguais.
- Referência ULTRA-ESPECÍFICA ao perfil (bio exata, post específico, legenda, destaque, nicho).
- Estrutura: [gancho do perfil dela] → [algo sobre você em 1 frase] → [abertura].
- Limite rígido: 2-3 linhas. Uma frase forte > um parágrafo fraco.
- Tom: confiante, levemente provocador, como se você tivesse algo a oferecer — não a pedir.
- PROIBIDO: "posso te conhecer?", elogio físico, "você tem namorado?", textão, pressão.
- Objetivo: ela querer saber quem você é antes de responder.

### PERFIL COMPLETO
Análise total para montar a estratégia de entrada.
- Analise tudo: bio, fotos, destaques, legendas, frequência, estilo visual, interações.
- Identifique nicho: fitness / lifestyle / fashion / viagem / trabalho / misto.
- Diferencie persona projetada (o que ela quer parecer) da persona real (o que transparece).
- Mapeie o tipo de homem que ela tende a responder:
  * Tom das legendas: intelectual, casual, emocional, irônico?
  * Conteúdo: vaidade vs. propósito, social vs. introspectiva?
  * Pistas de parceiro ou ausência?
- ESTRATÉGIA deve incluir plano de 3 passos PRÉ-mensagem: o que fazer antes de entrar na DM (engajar story, curtir posts recentes, comentar algo específico) + timing ideal.
- Defina ponto de entrada: story reply / comentário em post / DM direta.

---

## HISTÓRICO DA CONVERSA

Se fornecido:
- Analise ritmo, tom e profundidade do histórico
- Identifique o que ela demonstrou interesse ou resistência
- Note o que foi ignorado — são os sinais mais importantes
- As mensagens geradas são continuação natural — nunca nova abordagem
- Nunca repita perguntas. Avance a conexão.

---

# ETAPA 1 — ANÁLISE DO PERFIL

1. Tipo de perfil: social / seletiva / validação / lifestyle / neutra
2. Previsibilidade: alta / média / baixa
3. Sinais comportamentais: busca validação? aberta ou fechada? padrão exigente?
4. Qual gatilho psicológico é mais relevante para ela?

5. DESCRIÇÃO FÍSICA (obrigatório quando houver foto):
- Biótipo: magra / curvilínea / atlética / cheia
- Rosto e cabelo: traços, cor, comprimento, tipo
- Linguagem corporal: postura, expressão, olhar
- Estilo e vibe: roupas, cores, cuidado com aparência
- Nível de atratividade: alto / médio (objetivo, sem julgamento)

---

# ETAPA 2 — LEITURA SOCIAL

- Intenção dela no Instagram
- Nível de exigência: baixo / médio / alto
- Tipo de abordagem que ela IGNORA
- Tipo de abordagem que pode funcionar
- Princípio psicológico mais relevante

---

# ETAPA 3 — ESTRATÉGIA

Estágio atual da conversa:
- PRIMEIRO_CONTATO: nunca conversaram
- AQUECENDO: já há troca, ainda superficial
- CONEXÃO: conversa fluindo, interesse mútuo
- ENCONTRO: conexão forte, hora de propor

Defina a estratégia com tom cafajeste calibrado. Explique em 1 frase o princípio usado.

---

# ETAPA 4 — MENSAGENS

Gere 3 mensagens com tom cafajeste calibrado:

## 1. SEGURA
- Confiante, abre conversa sem risco, naturalidade total
- Rapport genuíno, sem elogio vazio

## 2. ESTRATÉGICA (principal)
- Provocação leve + curiosidade + tensão sutil
- Parece espontânea, nunca roteirizada
- Ela vai querer responder sem saber exatamente por quê

## 3. DIFERENTE
- Inesperada, criativa, com humor ou deboche inteligente
- Memorável — ela vai lembrar de você

---

# ETAPA 5 — O QUE NÃO MANDAR

2-3 exemplos ruins específicos para esse perfil, com explicação curta do porquê falham.

---

# ETAPA 6 — MICRO APRENDIZADO

Por que a mensagem estratégica funciona? Qual gatilho foi ativado?

---

# REGRAS ABSOLUTAS

- Zero elogio genérico de aparência
- Zero "oi tudo bem" ou variações
- Zero textão ansioso
- Zero pergunta dupla
- Escrever como mensagem real, não como redação
- Frases curtas — cada palavra tem que ganhar seu lugar
- Único para esse perfil específico — nunca copy-paste

---

# FORMATO DE SAÍDA — EXATO:

MODO:
Instagram

ANÁLISE DO PERFIL:
[texto]

DESCRIÇÃO FÍSICA:
[descrição — ou "N/A" se sem foto]

LEITURA SOCIAL:
[texto]

ESTRATÉGIA:
[texto]

ESTÁGIO: [PRIMEIRO_CONTATO / AQUECENDO / CONEXÃO / ENCONTRO]

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


# ─── INSTAGRAM MODE LABELS ───────────────────────────────────────────────────

IG_MODE_LABELS = {
    "story-reply":     "STORY REPLY — respondendo ao story dela",
    "dm-fria":         "DM FRIA — primeiro contato, ela nao conhece o usuario",
    "perfil-completo": "PERFIL COMPLETO — analise total do perfil Instagram",
}

# ─── PARSER ──────────────────────────────────────────────────────────────────

def parse_response(text):
    QUOTES = '"""\''

    def strip_md(s):
        s = re.sub(r'\*\*(.+?)\*\*', r'\1', s, flags=re.DOTALL)
        s = re.sub(r'\*(.+?)\*',     r'\1', s, flags=re.DOTALL)
        # remove trailing markdown separators/headers that bleed into fields
        s = re.sub(r'\s*\n\s*-{3,}\s*\n?\s*#{0,2}\s*$', '', s)
        s = re.sub(r'\s*-{3,}\s*$', '', s)
        s = re.sub(r'\s*#{1,3}\s*$', '', s)
        return s.strip()

    def get(pattern, default=""):
        m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        return strip_md(m.group(1)) if m else default

    def get_msg(label_re):
        # Handles: "msg", **"msg"**, "**msg**", **msg**
        m = re.search(
            rf'{label_re}\s*\n?\s*\*{{0,2}}\s*[{QUOTES}]?(.*?)[{QUOTES}]?\s*\*{{0,2}}\s*(?:\n|$)',
            text, re.IGNORECASE
        )
        if not m:
            return ""
        return strip_md(m.group(1)).strip(QUOTES).strip()

    modo_raw = get(r"MODO:\s*([\s\S]*?)(?=ANÁLISE|$)").lower()
    modo = "instagram"
    if "tinder" in modo_raw:
        modo = "tinder"
    elif "whatsapp" in modo_raw or "whats" in modo_raw:
        modo = "whatsapp"

    nao_enviar_raw = get(r"NÃO ENVIAR:\s*([\s\S]*?)(?=APRENDIZADO:|$)")
    nao_enviar = [
        strip_md(re.sub(r'^[-•*]\s*', '', line)).strip(QUOTES).strip()
        for line in nao_enviar_raw.split("\n")
        if line.strip() and re.match(r'^[-•*""*]', line.strip())
    ]

    estagio_m = re.search(r"ESTÁGIO:\s*\[?([^\n\[\]]+)\]?", text, re.IGNORECASE)
    estagio_raw = estagio_m.group(1).strip().upper() if estagio_m else ""
    estagio = ""
    if estagio_raw:
        if "PRIMEIRO" in estagio_raw or "CONTATO" in estagio_raw:
            estagio = "PRIMEIRO_CONTATO"
        elif "AQUEC" in estagio_raw:
            estagio = "AQUECENDO"
        elif "CONEX" in estagio_raw:
            estagio = "CONEXAO"
        elif "ENCONTR" in estagio_raw:
            estagio = "ENCONTRO"
        else:
            estagio = estagio_raw

    desc_raw = get(r"DESCRIÇÃO FÍSICA:\s*([\s\S]*?)(?=LEITURA SOCIAL:|$)")
    descricao_fisica = "" if desc_raw.strip().upper() in ("N/A", "N/A.", "") else desc_raw

    return {
        "modo": modo,
        "analise":         get(r"ANÁLISE DO PERFIL:\s*([\s\S]*?)(?=DESCRIÇÃO FÍSICA:|LEITURA SOCIAL:|$)"),
        "descricao_fisica": descricao_fisica,
        "leitura":         get(r"LEITURA SOCIAL:\s*([\s\S]*?)(?=ESTRATÉGIA:|$)"),
        "estrategia":      get(r"ESTRATÉGIA:\s*([\s\S]*?)(?=ESTÁGIO:|MENSAGENS:|$)"),
        "estagio":         estagio,
        "segura":          get_msg(r'1\.\s*SEGURA:'),
        "estrategica":     get_msg(r'2\.\s*ESTRATÉGICA:'),
        "diferente":       get_msg(r'3\.\s*DIFERENTE:'),
        "nao_enviar":      nao_enviar,
        "aprendizado":     get(r"APRENDIZADO:\s*([\s\S]*?)$"),
    }


# ─── API CALL ────────────────────────────────────────────────────────────────

def call_anthropic(text_input, images=None, profile=None, app_hint=None, memory_mode=None, ig_knows_me=None, conversation_history=None, ig_mode=None):
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

    if app_hint == "instagram" and ig_mode and ig_mode in IG_MODE_LABELS:
        context_parts.append(f"MODO INSTAGRAM: {IG_MODE_LABELS[ig_mode]}")
    elif app_hint == "instagram" and ig_knows_me is not None:
        label = "ELA_ME_CONHECE — ela já sabe quem é o usuário" if ig_knows_me else "ELA_NAO_ME_CONHECE — abordagem completamente fria"
        context_parts.append(f"INSTAGRAM: {label}")

    if conversation_history:
        context_parts.append(f"HISTÓRICO DA CONVERSA:\n{conversation_history}")

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
            "max_tokens": 2400,
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
    ig_mode = request.form.get("ig_mode", "").strip()
    profile_raw = request.form.get("profile", "{}")
    conversation_history = request.form.get("conversation_history", "").strip()

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
        raw = call_anthropic(text_input, images, profile, app_hint, memory_mode, ig_knows_me, conversation_history, ig_mode)
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
