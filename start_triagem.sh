#!/bin/bash

# Script de Inicialização do Sistema de Triagem Inteligente
# Sponte - N3 Suporte

echo "🎯 SISTEMA DE TRIAGEM INTELIGENTE - SPONTE"
echo "=========================================="
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale Python 3.10+ primeiro."
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Verifica se pip está instalado
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip não encontrado. Instale pip primeiro."
    exit 1
fi

echo "✅ pip encontrado"

# Cria ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativa ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instala dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt

# Executa teste rápido
echo ""
echo "🧪 Executando teste rápido..."
python teste_rapido.py

# Pergunta se quer iniciar o servidor
echo ""
read -p "🚀 Deseja iniciar o servidor de triagem? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌐 Iniciando servidor..."
    echo "   URL: http://localhost:8001"
    echo "   Docs: http://localhost:8001/docs"
    echo ""
    echo "⏹️  Para parar: Ctrl+C"
    echo ""
    
    python main_triagem.py
else
    echo "👋 Para iniciar manualmente:"
    echo "   source venv/bin/activate"
    echo "   python main_triagem.py"
fi
