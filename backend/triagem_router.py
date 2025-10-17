from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import time
import json
import os
from datetime import datetime, timedelta

from schemas_triagem import (
    TriagemRequest,
    TriagemResponse,
    FeedbackTriagemRequest,
    FeedbackTriagemResponse,
    EstatisticasTriagemResponse,
    HistoricoTriagemResponse,
    AtualizarBaseConhecimentoRequest,
    AtualizarBaseConhecimentoResponse,
    SolucaoSugerida,
    PadraoDetectado,
    AnaliseIA,
    ResumoTriagem,
    EstatisticaTriagem,
    TriagemHistorico
)
from triagem_service import TriagemService, solucao_para_dict
from integracao_service import integracao_service

router = APIRouter(prefix="/api/triagem", tags=["Triagem"])

# Inicializa serviços
triagem_service = TriagemService()

# ============================================
# ENDPOINTS DE TRIAGEM
# ============================================

@router.post("/analisar", response_model=TriagemResponse)
async def analisar_triagem(request: TriagemRequest):
    """
    Analisa um chamado e retorna sugestões de triagem técnica
    """
    try:
        inicio = time.time()
        
        print(f"🔍 Iniciando triagem para módulo: {request.modulo}")
        
        # Executa análise de triagem
        resultado = await triagem_service.analisar_chamado(
            chamado_texto=request.chamado_texto,
            modulo=request.modulo
        )
        
        # Calcula tempo de processamento
        fim = time.time()
        tempo_ms = int((fim - inicio) * 1000)
        
        # Converte soluções para dict
        solucoes_dict = [solucao_para_dict(sol) for sol in resultado["solucoes_sugeridas"]]
        
        # Converte padrões para dict
        padroes_dict = [
            {
                "tipo": p["tipo"],
                "padrao_id": p["padrao_id"],
                "palavra_chave": p["palavra_chave"],
                "confianca": p["confianca"]
            }
            for p in resultado["padroes_encontrados"]
        ]
        
        # Converte análise IA para dict
        analise_ia_dict = resultado["analise_ia"]
        
        # Converte resumo para dict
        resumo_dict = resultado["resumo"]
        
        print(f"✅ Triagem concluída em {tempo_ms}ms - {len(solucoes_dict)} soluções geradas")
        
        return TriagemResponse(
            sucesso=True,
            triagem_id=None,  # TODO: Implementar salvamento no banco
            padroes_encontrados=padroes_dict,
            analise_ia=analise_ia_dict,
            solucoes_sugeridas=solucoes_dict,
            resumo=resumo_dict,
            modo_mock=resultado["modo_mock"],
            tempo_processamento_ms=tempo_ms,
            mensagem="Triagem realizada com sucesso"
        )
        
    except Exception as e:
        print(f"❌ Erro na triagem: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro na triagem: {str(e)}")

@router.post("/feedback", response_model=FeedbackTriagemResponse)
async def registrar_feedback_triagem(request: FeedbackTriagemRequest):
    """
    Registra feedback sobre uma triagem realizada
    """
    try:
        # TODO: Implementar salvamento do feedback no banco
        feedback_id = 1  # Placeholder
        
        print(f"📝 Feedback registrado para triagem {request.triagem_id}: {'👍' if request.solucao_util else '👎'}")
        
        return FeedbackTriagemResponse(
            sucesso=True,
            feedback_id=feedback_id,
            mensagem="Feedback registrado com sucesso"
        )
        
    except Exception as e:
        print(f"❌ Erro ao registrar feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao registrar feedback: {str(e)}")

# ============================================
# ENDPOINTS DE ESTATÍSTICAS
# ============================================

@router.get("/estatisticas", response_model=EstatisticasTriagemResponse)
async def obter_estatisticas_triagem(
    dias: int = Query(7, description="Número de dias para consultar"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoria específica")
):
    """
    Obtém estatísticas de triagem do período
    """
    try:
        # TODO: Implementar consulta real no banco
        # Por enquanto, retorna dados mockados
        
        estatisticas_mock = []
        for i in range(dias):
            data = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            estatistica = EstatisticaTriagem(
                data=data,
                total_triagens=10 + i,
                triagens_com_solucao=8 + i,
                tipos_problema={
                    "codigo": 5 + i,
                    "banco": 3 + i,
                    "configuracao": 2 + i
                },
                categorias_mais_comuns=[
                    {"categoria": "Validação/Dados", "count": 4 + i},
                    {"categoria": "Integridade Referencial", "count": 3 + i},
                    {"categoria": "Performance", "count": 2 + i}
                ],
                prioridades={
                    "alta": 3 + i,
                    "media": 4 + i,
                    "baixa": 3 + i
                },
                tempo_medio_processamento=1500.0 + (i * 100)
            )
            estatisticas_mock.append(estatistica)
        
        resumo_geral = {
            "total_triagens_periodo": sum(s.total_triagens for s in estatisticas_mock),
            "media_triagens_dia": sum(s.total_triagens for s in estatisticas_mock) / dias,
            "taxa_sucesso": sum(s.triagens_com_solucao for s in estatisticas_mock) / sum(s.total_triagens for s in estatisticas_mock),
            "categoria_mais_comum": "Validação/Dados"
        }
        
        return EstatisticasTriagemResponse(
            sucesso=True,
            periodo=f"Últimos {dias} dias",
            estatisticas=estatisticas_mock,
            resumo_geral=resumo_geral
        )
        
    except Exception as e:
        print(f"❌ Erro ao obter estatísticas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}")

@router.get("/historico", response_model=HistoricoTriagemResponse)
async def obter_historico_triagem(
    pagina: int = Query(1, description="Página (começa em 1)"),
    por_pagina: int = Query(20, description="Registros por página"),
    modulo: Optional[str] = Query(None, description="Filtrar por módulo")
):
    """
    Obtém histórico de triagens realizadas
    """
    try:
        # TODO: Implementar consulta real no banco
        # Por enquanto, retorna dados mockados
        
        historico_mock = []
        for i in range(min(por_pagina, 20)):  # Limita a 20 registros mockados
            triagem = TriagemHistorico(
                id=1000 + i,
                data_triagem=datetime.now() - timedelta(hours=i * 2),
                modulo="CADASTROS" if i % 3 == 0 else "FINANCEIRO" if i % 3 == 1 else "PEDAGÓGICO",
                total_padroes=2 + (i % 4),
                prioridade_geral="alta" if i % 4 == 0 else "media",
                solucoes_geradas=1 + (i % 3),
                teve_feedback=i % 5 == 0
            )
            historico_mock.append(triagem)
        
        return HistoricoTriagemResponse(
            sucesso=True,
            triagens=historico_mock,
            total=len(historico_mock),
            pagina=pagina,
            por_pagina=por_pagina
        )
        
    except Exception as e:
        print(f"❌ Erro ao obter histórico: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter histórico: {str(e)}")

# ============================================
# ENDPOINTS DE CONFIGURAÇÃO
# ============================================

@router.post("/configurar-base", response_model=AtualizarBaseConhecimentoResponse)
async def atualizar_base_conhecimento(request: AtualizarBaseConhecimentoRequest):
    """
    Atualiza a base de conhecimento de padrões
    """
    try:
        # TODO: Implementar atualização real da base de conhecimento
        # Por enquanto, apenas simula a atualização
        
        padroes_atualizados = 0
        if request.padroes_codigo:
            padroes_atualizados += sum(len(categoria) for categoria in request.padroes_codigo.values())
        if request.padroes_banco:
            padroes_atualizados += len(request.padroes_banco)
        if request.padroes_sistema:
            padroes_atualizados += len(request.padroes_sistema)
        
        print(f"📝 Base de conhecimento atualizada: {padroes_atualizados} padrões")
        
        return AtualizarBaseConhecimentoResponse(
            sucesso=True,
            padroes_atualizados=padroes_atualizados,
            mensagem=f"Base de conhecimento atualizada com {padroes_atualizados} padrões"
        )
        
    except Exception as e:
        print(f"❌ Erro ao atualizar base: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar base: {str(e)}")

@router.get("/base-conhecimento")
async def obter_base_conhecimento():
    """
    Obtém a base de conhecimento atual
    """
    try:
        # Retorna a base de conhecimento atual
        with open('base_conhecimento_triagem.json', 'r', encoding='utf-8') as f:
            base = json.load(f)
        
        return {
            "sucesso": True,
            "base_conhecimento": base,
            "total_padroes": (
                sum(len(categoria) for categoria in base.get("padroes_codigo", {}).values()) +
                len(base.get("padroes_banco", {})) +
                len(base.get("padroes_sistema", {}))
            )
        }
        
    except Exception as e:
        print(f"❌ Erro ao obter base: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter base: {str(e)}")

# ============================================
# ENDPOINTS AUXILIARES
# ============================================

@router.get("/health")
async def health_check():
    """
    Health check do serviço de triagem
    """
    api_key = os.getenv("GEMINI_API_KEY", "")
    gemini_configured = bool(api_key and api_key != "sua_chave_aqui")
    
    return {
        "status": "ok",
        "servico": "triagem",
        "versao": "1.0.0",
        "modo_mock": triagem_service.mock_mode,
        "gemini_configured": gemini_configured,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/config")
async def configuracao_sistema():
    """
    Retorna informações sobre a configuração do sistema
    """
    api_key = os.getenv("GEMINI_API_KEY", "")
    gemini_configured = bool(api_key and api_key != "sua_chave_aqui")
    
    return {
        "gemini_api": {
            "configurada": gemini_configured,
            "modelo": "gemini-2.5-flash" if gemini_configured else None,
            "modo_atual": "IA Real" if gemini_configured else "Mock"
        },
        "sistema_principal": {
            "url": "http://localhost:8000",
            "status": "configurado"
        },
        "instrucoes": {
            "configurar_gemini": "1. Obtenha uma chave API em https://makersuite.google.com/app/apikey\n2. Crie um arquivo .env na pasta backend/\n3. Adicione: GEMINI_API_KEY=sua_chave_aqui\n4. Reinicie o servidor"
        } if not gemini_configured else {}
    }

@router.get("/padroes")
async def listar_padroes_disponiveis():
    """
    Lista todos os padrões disponíveis na base de conhecimento
    """
    try:
        padroes = []
        
        # Padrões de código VB.NET
        for padrao_id, config in triagem_service.base_conhecimento.get("padroes_codigo", {}).get("vb_net", {}).items():
            padroes.append({
                "tipo": "codigo_vb",
                "id": padrao_id,
                "categoria": config["categoria"],
                "prioridade": config["prioridade"],
                "palavras_chave": config["palavras_chave"]
            })
        
        # Padrões ASP.NET
        for padrao_id, config in triagem_service.base_conhecimento.get("padroes_codigo", {}).get("asp_net", {}).items():
            padroes.append({
                "tipo": "codigo_asp",
                "id": padrao_id,
                "categoria": config["categoria"],
                "prioridade": config["prioridade"],
                "palavras_chave": config["palavras_chave"]
            })
        
        # Padrões de banco
        for padrao_id, config in triagem_service.base_conhecimento.get("padroes_banco", {}).items():
            padroes.append({
                "tipo": "banco",
                "id": padrao_id,
                "categoria": config["categoria"],
                "prioridade": config["prioridade"],
                "palavras_chave": config["palavras_chave"]
            })
        
        # Padrões de sistema
        for padrao_id, config in triagem_service.base_conhecimento.get("padroes_sistema", {}).items():
            padroes.append({
                "tipo": "sistema",
                "id": padrao_id,
                "categoria": config["categoria"],
                "prioridade": config["prioridade"],
                "palavras_chave": config["palavras_chave"]
            })
        
        return {
            "sucesso": True,
            "total_padroes": len(padroes),
            "padroes": padroes
        }
        
    except Exception as e:
        print(f"❌ Erro ao listar padrões: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar padrões: {str(e)}")

# ============================================
# ENDPOINTS DE INTEGRAÇÃO COM SISTEMA EXISTENTE
# ============================================

@router.post("/ticket/{ticket_numero}")
async def triagem_por_ticket(ticket_numero: str):
    """
    Recebe um número de ticket e faz triagem automática do chamado gerado pelo sistema principal
    """
    try:
        print(f"🎯 Iniciando triagem por ticket: {ticket_numero}")
        
        # 1. Busca o chamado no sistema principal
        print(f"🔍 Buscando chamado no sistema principal...")
        dados_chamado = await integracao_service.buscar_chamado_por_ticket(ticket_numero)
        
        if not dados_chamado:
            raise HTTPException(
                status_code=404, 
                detail=f"Chamado não encontrado para o ticket {ticket_numero}. Verifique se o ticket foi analisado no sistema principal."
            )
        
        # 2. Extrai informações do chamado
        chamado_texto = dados_chamado.get('chamado_gerado', '')
        modulo = dados_chamado.get('modulo_identificado')
        analise_id = dados_chamado.get('analise_id')
        
        if not chamado_texto:
            raise HTTPException(
                status_code=400,
                detail="Chamado encontrado mas sem texto gerado"
            )
        
        print(f"✅ Chamado encontrado (ID: {analise_id}, Módulo: {modulo})")
        
        # 3. Executa a triagem
        print(f"🤖 Executando triagem...")
        resultado = await triagem_service.analisar_chamado(chamado_texto, modulo)
        
        # 4. Adiciona informações de integração ao resultado
        resultado['integracao'] = {
            'ticket_numero': ticket_numero,
            'analise_id_original': analise_id,
            'sistema_origem': 'IaChamadoN3',
            'data_chamado_original': dados_chamado.get('data_analise'),
            'usuario_original': dados_chamado.get('usuario_nome'),
            'cliente_original': dados_chamado.get('cliente_nome')
        }
        
        # 5. Converte soluções para dict
        solucoes_dict = [solucao_para_dict(sol) for sol in resultado["solucoes_sugeridas"]]
        
        # 6. Converte padrões para dict
        padroes_dict = [
            {
                "tipo": p["tipo"],
                "padrao_id": p["padrao_id"],
                "palavra_chave": p["palavra_chave"],
                "confianca": p["confianca"]
            }
            for p in resultado["padroes_encontrados"]
        ]
        
        print(f"✅ Triagem concluída para ticket {ticket_numero}")
        
        return {
            "sucesso": True,
            "ticket_numero": ticket_numero,
            "analise_id_original": analise_id,
            "padroes_encontrados": padroes_dict,
            "analise_ia": resultado["analise_ia"],
            "solucoes_sugeridas": solucoes_dict,
            "resumo": resultado["resumo"],
            "modo_mock": resultado["modo_mock"],
            "integracao": resultado["integracao"],
            "mensagem": f"Triagem realizada com sucesso para ticket {ticket_numero}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro na triagem por ticket: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro na triagem: {str(e)}")

@router.get("/buscar-chamado/{ticket_numero}")
async def buscar_chamado_sistema_principal(ticket_numero: str):
    """
    Busca apenas os dados do chamado no sistema principal (sem fazer triagem)
    """
    try:
        print(f"🔍 Buscando chamado para ticket: {ticket_numero}")
        
        dados_chamado = await integracao_service.buscar_chamado_por_ticket(ticket_numero)
        
        if not dados_chamado:
            raise HTTPException(
                status_code=404,
                detail=f"Chamado não encontrado para o ticket {ticket_numero}"
            )
        
        return {
            "sucesso": True,
            "ticket_numero": ticket_numero,
            "dados_chamado": dados_chamado,
            "mensagem": "Chamado encontrado com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao buscar chamado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar chamado: {str(e)}")

@router.get("/sistema-principal/status")
async def verificar_status_sistema_principal():
    """
    Verifica se o sistema principal está acessível
    """
    try:
        status = await integracao_service.verificar_conexao_sistema_principal()
        
        return {
            "sucesso": True,
            "sistema_principal_online": status,
            "url_sistema_principal": integracao_service.sistema_principal_url,
            "mensagem": "Sistema principal online" if status else "Sistema principal offline"
        }
        
    except Exception as e:
        print(f"❌ Erro ao verificar status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao verificar status: {str(e)}")

@router.get("/sistema-principal/analises-recentes")
async def obter_analises_recentes_sistema_principal(limite: int = Query(10, description="Número de análises a retornar")):
    """
    Obtém análises recentes do sistema principal
    """
    try:
        analises = await integracao_service.obter_analises_recentes(limite)
        
        return {
            "sucesso": True,
            "total_analises": len(analises),
            "analises": analises,
            "mensagem": f"{len(analises)} análises encontradas"
        }
        
    except Exception as e:
        print(f"❌ Erro ao obter análises recentes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter análises: {str(e)}")
