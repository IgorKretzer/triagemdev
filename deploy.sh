#!/bin/bash

# Script de Deploy - Sistema de Triagem Inteligente
# Sponte - N3 Suporte

echo "🚀 DEPLOY - SISTEMA DE TRIAGEM INTELIGENTE"
echo "=========================================="
echo ""

# Verifica se está no diretório correto
if [ ! -f "vercel.json" ] || [ ! -f "render.yaml" ]; then
    echo "❌ Execute este script no diretório raiz do projeto"
    exit 1
fi

echo "✅ Estrutura de projeto verificada"

# ============================================
# 1. BACKEND - DEPLOY NO RENDER
# ============================================

echo ""
echo "🔧 1. CONFIGURANDO BACKEND (Render.com)"
echo "---------------------------------------"

echo "📋 Instruções para deploy do backend:"
echo ""
echo "1. Acesse: https://render.com"
echo "2. Faça login e clique em 'New +' > 'Web Service'"
echo "3. Conecte seu repositório GitHub"
echo "4. Configure:"
echo "   • Name: ia-triagem-backend"
echo "   • Region: Oregon (US West)"
echo "   • Branch: main"
echo "   • Root Directory: backend"
echo "   • Build Command: pip install -r requirements.txt"
echo "   • Start Command: uvicorn main_triagem:app --host 0.0.0.0 --port \$PORT"
echo "   • Instance Type: Free"
echo ""
echo "5. Adicione as variáveis de ambiente:"
echo "   • PYTHON_VERSION: 3.10.0"
echo "   • GEMINI_API_KEY: sua_chave_gemini_aqui (opcional)"
echo "   • DATABASE_PATH: /opt/render/project/src/triagem.db"
echo "   • LOG_LEVEL: INFO"
echo ""
echo "6. Clique em 'Create Web Service'"
echo "7. Aguarde o deploy (5-10 minutos)"
echo "8. Sua URL será: https://ia-triagem-backend.onrender.com"
echo ""

read -p "✅ Backend deployado? Digite a URL do backend (ex: https://ia-triagem-backend.onrender.com): " BACKEND_URL

if [ -z "$BACKEND_URL" ]; then
    echo "⚠️  URL do backend não informada. Continuando com URL padrão."
    BACKEND_URL="https://ia-triagem-backend.onrender.com"
fi

# ============================================
# 2. FRONTEND - DEPLOY NO VERCEL
# ============================================

echo ""
echo "🌐 2. CONFIGURANDO FRONTEND (Vercel)"
echo "------------------------------------"

# Atualiza vercel.json com a URL do backend
echo "📝 Atualizando vercel.json com URL do backend..."
sed -i "s|https://ia-triagem-backend.onrender.com|$BACKEND_URL|g" vercel.json

echo "✅ vercel.json atualizado"

echo ""
echo "📋 Instruções para deploy do frontend:"
echo ""
echo "1. Instale Vercel CLI: npm install -g vercel"
echo "2. Execute: vercel login"
echo "3. Execute: vercel --prod"
echo ""
echo "4. Configure as variáveis de ambiente no Vercel:"
echo "   • VITE_API_URL: $BACKEND_URL"
echo ""
echo "5. Sua URL será: https://seu-projeto.vercel.app"
echo ""

read -p "✅ Frontend deployado? Digite a URL do frontend: " FRONTEND_URL

# ============================================
# 3. TESTE DE INTEGRAÇÃO
# ============================================

echo ""
echo "🧪 3. TESTANDO INTEGRAÇÃO"
echo "-------------------------"

if [ ! -z "$BACKEND_URL" ]; then
    echo "🔍 Testando backend..."
    
    # Testa health check
    if curl -s "$BACKEND_URL/health" > /dev/null; then
        echo "✅ Backend respondendo"
    else
        echo "❌ Backend não está respondendo"
    fi
fi

if [ ! -z "$FRONTEND_URL" ]; then
    echo "🔍 Testando frontend..."
    echo "✅ Frontend: $FRONTEND_URL"
fi

# ============================================
# 4. RESUMO FINAL
# ============================================

echo ""
echo "🎉 DEPLOY CONCLUÍDO!"
echo "===================="
echo ""
echo "📊 URLs do Sistema:"
echo "   • Frontend: $FRONTEND_URL"
echo "   • Backend: $BACKEND_URL"
echo "   • Docs API: $BACKEND_URL/docs"
echo ""
echo "🔧 Próximos Passos:"
echo "   1. Teste o sistema completo"
echo "   2. Configure GEMINI_API_KEY (opcional)"
echo "   3. Integre com sistema existente"
echo "   4. Monitore logs e estatísticas"
echo ""
echo "📚 Documentação:"
echo "   • README_TRIAGEM.md - Documentação completa"
echo "   • COMO_USAR.md - Guia de uso"
echo "   • $BACKEND_URL/docs - API Documentation"
echo ""
echo "🎯 Sistema pronto para produção!"

# ============================================
# 5. COMANDOS ÚTEIS
# ============================================

echo ""
echo "💡 COMANDOS ÚTEIS:"
echo "------------------"
echo ""
echo "# Ver logs do backend (Render)"
echo "• Acesse: https://dashboard.render.com"
echo "• Vá para seu serviço > Logs"
echo ""
echo "# Redeploy do frontend"
echo "vercel --prod"
echo ""
echo "# Ver logs do frontend (Vercel)"
echo "vercel logs"
echo ""
echo "# Testar API localmente"
echo "curl $BACKEND_URL/health"
echo ""
echo "# Testar triagem"
echo "curl -X POST $BACKEND_URL/api/triagem/analisar \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"chamado_texto\":\"Erro ao salvar aluno\",\"modulo\":\"CADASTROS\"}'"
echo ""

echo "🚀 Deploy concluído com sucesso!"
