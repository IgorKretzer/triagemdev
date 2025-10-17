"""
Sistema de Triagem Inteligente para Chamados Sponte
Integração com o sistema existente de análise de tickets
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from datetime import datetime
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Importa os routers
from triagem_router import router as triagem_router

# Cria a aplicação FastAPI
app = FastAPI(
    title="Sistema de Triagem - Sponte",
    description="Sistema inteligente de triagem técnica para chamados do sistema Sponte",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra os routers
app.include_router(triagem_router)

# ============================================
# ENDPOINTS PRINCIPAIS
# ============================================

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "mensagem": "Sistema de Triagem Inteligente - Sponte",
        "versao": "1.0.0",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "triagem": "/api/triagem/analisar",
            "feedback": "/api/triagem/feedback",
            "estatisticas": "/api/triagem/estatisticas",
            "historico": "/api/triagem/historico",
            "documentacao": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check geral"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "servicos": {
            "triagem": "online",
            "base_conhecimento": "carregada",
            "ia": "disponivel" if os.getenv("GEMINI_API_KEY") else "mock"
        }
    }

# ============================================
# ENDPOINTS DE INTEGRAÇÃO COM SISTEMA EXISTENTE
# ============================================

@app.post("/api/integracao/triagem-chamado")
async def triagem_apos_analise(
    analise_id: int,
    chamado_texto: str,
    modulo: str = None,
    ticket_numero: str = None
):
    """
    Endpoint para integrar com o sistema existente
    Recebe o resultado da análise e aplica triagem
    """
    try:
        from triagem_service import TriagemService
        
        triagem_service = TriagemService()
        resultado = await triagem_service.analisar_chamado(chamado_texto, modulo)
        
        # Aqui você pode salvar no banco junto com o analise_id
        # TODO: Implementar salvamento integrado
        
        return {
            "sucesso": True,
            "analise_id": analise_id,
            "ticket_numero": ticket_numero,
            "triagem": resultado,
            "integracao": "sucesso"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na integração: {str(e)}")

# ============================================
# CONFIGURAÇÃO E INICIALIZAÇÃO
# ============================================

@app.on_event("startup")
async def startup_event():
    """Evento de inicialização"""
    print("🚀 Iniciando Sistema de Triagem Inteligente...")
    
    # Verifica se a base de conhecimento existe
    if not os.path.exists("base_conhecimento_triagem.json"):
        print("⚠️  Base de conhecimento não encontrada!")
    else:
        print("✅ Base de conhecimento carregada")
    
    # Verifica API do Gemini
    if os.getenv("GEMINI_API_KEY"):
        print("✅ API do Gemini configurada")
    else:
        print("⚠️  API do Gemini não configurada - modo MOCK ativo")
    
    print("🎯 Sistema pronto para triagem!")

if __name__ == "__main__":
    # Configuração para desenvolvimento
    uvicorn.run(
        "main_triagem:app",
        host="0.0.0.0",
        port=8001,  # Porta diferente do sistema principal
        reload=True,
        log_level="info"
    )
