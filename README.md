# 🚀 IACHAMADODEV - Sistema de Triagem Automática

Sistema de triagem automática de chamados técnicos integrado com IA (Gemini) e Firebase.

## ✨ Features

- **Triagem Automática**: Análise inteligente de chamados com IA
- **Integração Firebase**: Conecta com sistema IACHAMADON3
- **Frontend Moderno**: React + Vite
- **Backend Robusto**: FastAPI + Python
- **Análise de Padrões**: Detecção automática de problemas conhecidos
- **Classificação Inteligente**: Categorização automática de chamados

## 🏗️ Arquitetura

```
Frontend (Vercel) → Backend (Render) → Firebase (IACHAMADON3)
```

## 🚀 Deploy

- **Frontend**: [Vercel](https://vercel.com)
- **Backend**: [Render](https://render.com)
- **Database**: Firebase Firestore

## 📋 Pré-requisitos

- Node.js 18+
- Python 3.10+
- Chave API Gemini
- Credenciais Firebase

## 🛠️ Desenvolvimento Local

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main_triagem:app --host 0.0.0.0 --port 8001
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📖 Documentação

Para instruções detalhadas de deploy, consulte [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md).

## 🔗 Integração

Este sistema se integra com o **IACHAMADON3** através do Firebase, permitindo:
- Leitura de análises existentes
- Triagem automática de tickets
- Armazenamento de resultados
- Feedback e estatísticas

## 📄 Licença

MIT License
