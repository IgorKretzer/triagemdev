from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# ============================================
# SCHEMAS PARA TRIAGEM DE CHAMADOS
# ============================================

class TriagemRequest(BaseModel):
    """Request para análise de triagem"""
    chamado_texto: str = Field(..., description="Texto completo do chamado gerado")
    modulo: Optional[str] = Field(None, description="Módulo identificado no chamado")
    analise_id: Optional[int] = Field(None, description="ID da análise original (opcional)")

class SolucaoSugerida(BaseModel):
    """Modelo para solução sugerida"""
    tipo: str = Field(..., description="Tipo da solução: codigo, sql, configuracao, debug")
    categoria: str = Field(..., description="Categoria do problema")
    prioridade: str = Field(..., description="Prioridade: alta, media, baixa")
    solucao: str = Field(..., description="Descrição da solução")
    codigo_sugerido: Optional[str] = Field(None, description="Código de exemplo")
    script_sql_sugerido: Optional[str] = Field(None, description="Script SQL sugerido")
    scripts_sugeridos: Optional[List[str]] = Field(None, description="Lista de scripts SQL")
    confianca: float = Field(0.0, description="Nível de confiança (0.0 a 1.0)")

class PadraoDetectado(BaseModel):
    """Modelo para padrão detectado"""
    tipo: str = Field(..., description="Tipo do padrão: codigo_vb, codigo_asp, banco, sistema")
    padrao_id: str = Field(..., description="ID do padrão na base de conhecimento")
    palavra_chave: str = Field(..., description="Palavra-chave que foi encontrada")
    confianca: float = Field(0.0, description="Nível de confiança do match")

class AnaliseIA(BaseModel):
    """Modelo para análise da IA"""
    tipo_problema: Optional[str] = Field(None, description="Tipo do problema identificado")
    categoria_detalhada: Optional[str] = Field(None, description="Categoria detalhada")
    diagnostico: Optional[str] = Field(None, description="Diagnóstico técnico")
    solucao_sugerida: Optional[str] = Field(None, description="Sugestão de solução")
    codigo_exemplo: Optional[str] = Field(None, description="Código de exemplo")
    script_sql: Optional[str] = Field(None, description="Script SQL de exemplo")
    prioridade: Optional[str] = Field(None, description="Prioridade estimada")
    tempo_estimado: Optional[str] = Field(None, description="Tempo estimado para resolução")
    recursos_necessarios: Optional[List[str]] = Field(None, description="Recursos necessários")
    observacoes: Optional[str] = Field(None, description="Observações adicionais")
    erro: Optional[str] = Field(None, description="Mensagem de erro se houver")

class ResumoTriagem(BaseModel):
    """Modelo para resumo da triagem"""
    total_padroes_detectados: int = Field(..., description="Total de padrões detectados")
    tem_analise_ia: bool = Field(..., description="Se tem análise da IA disponível")
    categorias_afetadas: List[str] = Field(..., description="Categorias de problemas afetadas")
    prioridade_geral: str = Field(..., description="Prioridade geral da triagem")
    resumo: str = Field(..., description="Resumo textual da triagem")

class TriagemResponse(BaseModel):
    """Response da análise de triagem"""
    sucesso: bool = Field(..., description="Se a triagem foi bem-sucedida")
    triagem_id: Optional[int] = Field(None, description="ID da triagem salva no banco")
    padroes_encontrados: List[PadraoDetectado] = Field(..., description="Padrões detectados no texto")
    analise_ia: AnaliseIA = Field(..., description="Análise realizada pela IA")
    solucoes_sugeridas: List[SolucaoSugerida] = Field(..., description="Soluções sugeridas")
    resumo: ResumoTriagem = Field(..., description="Resumo da triagem")
    modo_mock: bool = Field(..., description="Se está em modo mock")
    tempo_processamento_ms: Optional[int] = Field(None, description="Tempo de processamento")
    mensagem: str = Field(..., description="Mensagem de status")

# ============================================
# SCHEMAS PARA FEEDBACK DE TRIAGEM
# ============================================

class FeedbackTriagemRequest(BaseModel):
    """Request para feedback da triagem"""
    triagem_id: int = Field(..., description="ID da triagem")
    solucao_util: bool = Field(..., description="Se a solução foi útil")
    solucao_usada: Optional[str] = Field(None, description="Qual solução foi utilizada")
    tempo_resolucao: Optional[str] = Field(None, description="Tempo real de resolução")
    comentario: Optional[str] = Field(None, description="Comentário sobre a triagem")
    nota: Optional[int] = Field(None, ge=1, le=5, description="Nota de 1 a 5")

class FeedbackTriagemResponse(BaseModel):
    """Response do feedback"""
    sucesso: bool = Field(..., description="Se o feedback foi registrado")
    feedback_id: int = Field(..., description="ID do feedback registrado")
    mensagem: str = Field(..., description="Mensagem de confirmação")

# ============================================
# SCHEMAS PARA ESTATÍSTICAS DE TRIAGEM
# ============================================

class EstatisticaTriagem(BaseModel):
    """Estatística de triagem"""
    data: str = Field(..., description="Data da estatística")
    total_triagens: int = Field(..., description="Total de triagens no dia")
    triagens_com_solucao: int = Field(..., description="Triagens que geraram soluções")
    tipos_problema: Dict[str, int] = Field(..., description="Contagem por tipo de problema")
    categorias_mais_comuns: List[Dict[str, Any]] = Field(..., description="Categorias mais comuns")
    prioridades: Dict[str, int] = Field(..., description="Distribuição de prioridades")
    tempo_medio_processamento: float = Field(..., description="Tempo médio de processamento")

class EstatisticasTriagemResponse(BaseModel):
    """Response das estatísticas"""
    sucesso: bool = Field(..., description="Se a consulta foi bem-sucedida")
    periodo: str = Field(..., description="Período consultado")
    estatisticas: List[EstatisticaTriagem] = Field(..., description="Lista de estatísticas")
    resumo_geral: Dict[str, Any] = Field(..., description="Resumo geral do período")

# ============================================
# SCHEMAS PARA HISTÓRICO DE TRIAGEM
# ============================================

class TriagemHistorico(BaseModel):
    """Item do histórico de triagem"""
    id: int = Field(..., description="ID da triagem")
    data_triagem: datetime = Field(..., description="Data da triagem")
    modulo: Optional[str] = Field(None, description="Módulo analisado")
    total_padroes: int = Field(..., description="Total de padrões detectados")
    prioridade_geral: str = Field(..., description="Prioridade geral")
    solucoes_geradas: int = Field(..., description="Número de soluções geradas")
    teve_feedback: bool = Field(..., description="Se teve feedback registrado")

class HistoricoTriagemResponse(BaseModel):
    """Response do histórico"""
    sucesso: bool = Field(..., description="Se a consulta foi bem-sucedida")
    triagens: List[TriagemHistorico] = Field(..., description="Lista de triagens")
    total: int = Field(..., description="Total de registros")
    pagina: int = Field(..., description="Página atual")
    por_pagina: int = Field(..., description="Registros por página")

# ============================================
# SCHEMAS PARA CONFIGURAÇÃO DE BASE DE CONHECIMENTO
# ============================================

class ConfiguracaoPadrao(BaseModel):
    """Configuração de um padrão"""
    palavras_chave: List[str] = Field(..., description="Palavras-chave do padrão")
    solucao_tipo: str = Field(..., description="Tipo da solução")
    categoria: str = Field(..., description="Categoria do padrão")
    prioridade: str = Field(..., description="Prioridade")
    solucao: str = Field(..., description="Descrição da solução")
    codigo_sugerido: Optional[str] = Field(None, description="Código sugerido")
    script_sql_sugerido: Optional[str] = Field(None, description="Script SQL sugerido")
    scripts_sugeridos: Optional[List[str]] = Field(None, description="Scripts SQL sugeridos")

class AtualizarBaseConhecimentoRequest(BaseModel):
    """Request para atualizar base de conhecimento"""
    padroes_codigo: Optional[Dict[str, Dict[str, ConfiguracaoPadrao]]] = Field(None, description="Padrões de código")
    padroes_banco: Optional[Dict[str, ConfiguracaoPadrao]] = Field(None, description="Padrões de banco")
    padroes_sistema: Optional[Dict[str, ConfiguracaoPadrao]] = Field(None, description="Padrões de sistema")

class AtualizarBaseConhecimentoResponse(BaseModel):
    """Response da atualização"""
    sucesso: bool = Field(..., description="Se a atualização foi bem-sucedida")
    padroes_atualizados: int = Field(..., description="Número de padrões atualizados")
    mensagem: str = Field(..., description="Mensagem de confirmação")
