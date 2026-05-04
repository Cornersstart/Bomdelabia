# Reply Coach V3 — Python/Flask

App de análise comportamental e geração de mensagens para Tinder, Instagram e WhatsApp.

---

## ⚡ Rodar localmente

```bash
# 1. Clone o projeto
git clone https://github.com/cornersstart/bomdelabia
cd bomdelabia

# 2. Crie o ambiente virtual
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure a API key
cp .env.example .env
# Edite o .env e coloque sua ANTHROPIC_API_KEY

# 5. Rode
GEMINI_API_KEY=AIza... python app.py

# Acesse: http://localhost:5000
```

---

## 🐳 Deploy no Render (como você já usa)

1. Suba o projeto no GitHub
2. No Render → New Web Service → conecte o repo
3. Runtime: **Docker**
4. Em **Environment Variables** adicione:
   - `GEMINI_API_KEY` = sua chave
5. Deploy → pronto

---

## 📁 Estrutura

```
├── app.py              # Backend Flask + chamada Anthropic
├── requirements.txt
├── Dockerfile
├── render.yaml
├── .env.example
└── templates/
    └── index.html      # Frontend completo (HTML/CSS/JS)
```

---

## 🔑 Como pegar a GEMINI_API_KEY

1. Acesse https://aistudio.google.com/app/apikey
2. Create API Key
3. Cole no `.env` ou na variável de ambiente do Render
