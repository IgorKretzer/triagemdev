# 🚀 Guia de Deploy - IACHAMADODEV

## 📋 Pré-requisitos
- Conta no Vercel (frontend)
- Conta no Render (backend)
- Chave da API do Gemini
- Credenciais do Firebase

## 🎨 Frontend (Vercel)

### 1. Conectar repositório no Vercel
- Acesse [vercel.com](https://vercel.com)
- Importe o repositório `IACHAMADODEV`
- O `vercel.json` já está configurado

### 2. Configurar variáveis de ambiente
No dashboard do Vercel, adicione:
```
VITE_API_URL=https://ia-triagem-backend.onrender.com
```

## ⚙️ Backend (Render)

### 1. Conectar repositório no Render
- Acesse [render.com](https://render.com)
- Crie um novo "Web Service"
- Conecte o repositório `IACHAMADODEV`
- Use o arquivo `render.yaml` (já configurado)

### 2. Configurar variáveis de ambiente
No dashboard do Render, adicione:

**Obrigatórias:**
```
GEMINI_API_KEY=sua_chave_gemini_aqui
FIREBASE_PROJECT_ID=ia-chamado-n3
FIREBASE_PRIVATE_KEY_ID=a3664252e2ea35c92e9bf339630e5c8c404f5e9f
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-fbsvc@ia-chamado-n3.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=109385884509299364079
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40ia-chamado-n3.iam.gserviceaccount.com
```

**Firebase Private Key (IMPORTANTE):**
```
FIREBASE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDBFc128PXZEll0
3YxlcBtBSXvdACDawIDFUKX+X5Mh/I11pnIZIDCxOSO9bVB0TpszVw4ZgLirCk/Q
zs/4pSe/jj+3FI55QyJFBcuVQGZQpWdt6tQTE9Iss41QVE/lTdnO3rGVvOUOg+lk
HfxKPr8obcdR6sWxEGQnWeIlVzTQ++k7bIBl7PppXJ4ou+Q+oFg3mTkiCPexO4Xo
l2/9NefNYznQi0jCvNOtDwdgCB0svwpYn8srEM+13jeQzNbrN7wmGVkNOZ7B+yoh
8Iu4TZguxLyVyTKMskk2GeeMH3/uxH9bjyJWe3x8qAFAXzQ0sYyHvooENTxb3GJ9
yO/5OG9BAgMBAAECggEACWWGSafTXGqmBi7k4L1V///+OXEQ4SRz8Z80Tp0X/3eX
eMoct0Y0C/zJRzQ1MYZ9kocbG5xJdb5XyCfT+4ab2N/vuqPME3DJczfql9Jdcv+e
I+gab+09Zyz0q8adveE4wC9FQYNtc9eqJDdzW/689dAAiUqkkxYb2MW+i1D/3rzL
S6S6UpnNQnDTivw/vsaWlI5XK2sMz+qB92ZM6EzfKzQ+K0aGj4KXzY3SW4QBqY0j
Rh6xY2F6Cy8cVUR4HgjVNrxPfnhXEmANJv/R7dj9+6gnqaROfsoDbauECEie7V0Y
GVN58q4ETbHwoY9r+6CDWz/nz6UC9fMSc8wj1JZAswKBgQD1mRovFu/lnrkWtJeD
qBuPvHCv1Cdg5SjpNWl1RwV0f87BbThbavy6n/W9k0H7uGQclY+w6fjPIJfegpIZ
juLz7sTOQD2mKRseaHBMvgdCxSHn7BfTQZkyEHeFlx0XIUjA/b9Us5BcoB2JMxY7
lOAP4JOYbJHgPDVWkNJzUCetTwKBgQDJQ1RClaTgHhPWDuu+kHRBYa4hU03IYKsy
1zu+HbOHDAFRIJ/9x/WFZOwYvBJY0fUFyROcf3+Hhj0/6lE6WSEFjmh83GZWlb5r
xbr61gcLQvITqnLtc05jNO8XiQRPV3oedv7yUaJLDe8gtFdoHnX2aLetOCmR3pJm
ON+0EgiWbwKBgBFmRl+drWNEKnK8WpueNk2pmQYr7ppDwfE7snv3iyBkyZ4UgdCg
NMV3/a3vl9Ygix8nTWXIPbNW6Mt/zp/26odDnDfMf1GdSemOlp4pPFRzqOJIbKuv
0w2j8wPI3+u6lO/vSjXS/uBBC7ajouiXtIQLcglzb6ZGPbUjT3WR8S2rAoGBAKNQ
m0McoxmpznbYzLtqBKw5U09/hZKfvswWk0gGWfOv7jGiw7DvXW/NIThBBLJGTQlQ
zTUk0Jtsdq8yuI8cXAtiL6+CORjxkf9qB/wbSMP+oukKWxALjQQ7o/f5GyI23cVy
0hZX39X/jJeBP5whe59kAgfxlunjLfD9HanFKGrJAoGBAO8shNLi2Jcssf9WIauL
TJ9BbdVC48hNPuu5sS9RN9aK5aTutbN1iR7ciBOOBkfwwsMRqHMLyOdcex+NPlQL
Ji19Fec/G8u8n+z6MmXkRrIDIt8xoZmZhvOU1iXWU6HqYlniwRfI2sv+ewKUqrYf
aBBMTZXrgP0eBWPxX0AmA5CU
-----END PRIVATE KEY-----
```

**Opcionais:**
```
LOG_LEVEL=INFO
DATABASE_PATH=/opt/render/project/src/triagem.db
```

## 🔄 Fluxo de Deploy

### 1. Deploy do Backend (Render)
1. Conecte o repositório no Render
2. Configure as variáveis de ambiente
3. Deploy automático será iniciado
4. Aguarde 3-5 minutos
5. Anote a URL do backend (ex: `https://ia-triagem-backend.onrender.com`)

### 2. Deploy do Frontend (Vercel)
1. Conecte o repositório no Vercel
2. Configure `VITE_API_URL` com a URL do backend do Render
3. Deploy automático será iniciado
4. Aguarde 1-3 minutos
5. Frontend estará disponível na URL do Vercel

## ✅ Teste Pós-Deploy

### 1. Teste do Backend
```bash
curl https://ia-triagem-backend.onrender.com/health
```

### 2. Teste do Frontend
- Acesse a URL do Vercel
- Digite um ticket (ex: 12345)
- Verifique se a triagem funciona

### 3. Teste de Integração
- Digite um ticket que foi analisado no IACHAMADON3
- Verifique se a triagem é feita automaticamente
- Verifique se os dados são salvos no Firebase

## 🚨 Troubleshooting

### Backend não inicia
- Verifique se todas as variáveis de ambiente estão corretas
- Verifique os logs no Render
- Teste localmente primeiro

### Frontend não conecta com backend
- Verifique se `VITE_API_URL` está correto
- Verifique se o backend está rodando
- Verifique CORS no backend

### Firebase não conecta
- Verifique se as credenciais estão corretas
- Verifique se o projeto Firebase existe
- Verifique se as permissões estão corretas

## 📊 Monitoramento

### Render Dashboard
- Logs em tempo real
- Métricas de performance
- Status do serviço

### Vercel Dashboard
- Logs de build
- Métricas de performance
- Status do deploy

### Firebase Console
- Dados das triagens
- Logs de acesso
- Métricas de uso

## 🎯 URLs Finais

Após o deploy:
- **Frontend**: `https://ia-chamados-sponte.vercel.app`
- **Backend**: `https://ia-triagem-backend.onrender.com`
- **Firebase**: `https://console.firebase.google.com/project/ia-chamado-n3`

## 🔗 Integração com IACHAMADON3

O sistema está configurado para:
1. **Ler dados** do Firebase do IACHAMADON3
2. **Fazer triagem** automática
3. **Salvar resultados** no mesmo Firebase
4. **Manter integração** completa entre os sistemas
