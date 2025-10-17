"""
Serviço de Integração com Sistema Existente (IaChamadoN3)
Busca chamados gerados pelo sistema principal para aplicar triagem
Agora usa Firebase diretamente para melhor performance
"""

import httpx
import os
from typing import Optional, Dict, Any, List
import logging
from firebase_db import FirebaseDatabase

class IntegracaoService:
    def __init__(self):
        # URL do sistema principal (IaChamadoN3) - fallback para HTTP
        self.sistema_principal_url = os.getenv(
            "SISTEMA_PRINCIPAL_URL", 
            "http://localhost:8000"  # URL local do sistema existente
        )
        self.timeout = 30
        
        # Firebase Database para acesso direto
        self.firebase_db = FirebaseDatabase()
        
        # Configuração de log
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def buscar_chamado_por_ticket(self, ticket_numero: str) -> Optional[Dict[str, Any]]:
        """
        Busca o chamado gerado pelo sistema principal usando o número do ticket
        Primeiro tenta Firebase, depois fallback para HTTP
        
        Args:
            ticket_numero: Número do ticket (ex: "12345")
            
        Returns:
            Dicionário com dados do chamado ou None se não encontrado
        """
        try:
            self.logger.info(f"🔍 Buscando chamado para ticket: {ticket_numero}")
            
            # 1. Tenta buscar diretamente do Firebase (mais rápido)
            if self.firebase_db.is_configured():
                self.logger.info("🔥 Buscando no Firebase...")
                dados_firebase = self.firebase_db.buscar_analise_por_ticket(ticket_numero)
                
                if dados_firebase:
                    self.logger.info(f"✅ Chamado encontrado no Firebase para ticket {ticket_numero}")
                    return {
                        'ticket_numero': dados_firebase.get('ticket_numero'),
                        'chamado_gerado': dados_firebase.get('chamado_gerado'),
                        'modulo_identificado': dados_firebase.get('modulo_identificado'),
                        'tipo_identificado': dados_firebase.get('tipo_identificado'),
                        'data_analise': dados_firebase.get('data_analise'),
                        'usuario_nome': dados_firebase.get('usuario_nome'),
                        'cliente_nome': dados_firebase.get('cliente_nome'),
                        'titulo_ticket': dados_firebase.get('titulo_ticket'),
                        'analise_id': dados_firebase.get('id')
                    }
                else:
                    self.logger.info("⚠️ Chamado não encontrado no Firebase, tentando HTTP...")
            
            # 2. Fallback para HTTP (sistema principal)
            self.logger.info("🌐 Buscando via HTTP...")
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Tenta buscar no endpoint de estatísticas recentes
                response = await client.get(f"{self.sistema_principal_url}/api/estatisticas/recentes")
                
                if response.status_code == 200:
                    dados = response.json()
                    analises = dados.get('analises', [])
                    
                    # Procura pela análise do ticket específico
                    for analise in analises:
                        if analise.get('ticket_numero') == str(ticket_numero):
                            self.logger.info(f"✅ Chamado encontrado via HTTP para ticket {ticket_numero}")
                            return {
                                'ticket_numero': analise.get('ticket_numero'),
                                'chamado_gerado': analise.get('chamado_gerado'),
                                'modulo_identificado': analise.get('modulo_identificado'),
                                'tipo_identificado': analise.get('tipo_identificado'),
                                'data_analise': analise.get('data_analise'),
                                'usuario_nome': analise.get('usuario_nome'),
                                'cliente_nome': analise.get('cliente_nome'),
                                'titulo_ticket': analise.get('titulo_ticket'),
                                'analise_id': analise.get('id')
                            }
                
                self.logger.warning(f"⚠️ Chamado não encontrado para ticket: {ticket_numero}")
                return None
                
        except httpx.ConnectError:
            self.logger.error(f"❌ Não foi possível conectar com sistema principal: {self.sistema_principal_url}")
            return None
        except httpx.TimeoutException:
            self.logger.error(f"❌ Timeout ao buscar chamado para ticket: {ticket_numero}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Erro ao buscar chamado: {str(e)}")
            return None
    
    async def verificar_conexao_sistema_principal(self) -> bool:
        """
        Verifica se o sistema principal está acessível
        
        Returns:
            True se acessível, False caso contrário
        """
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"{self.sistema_principal_url}/health")
                return response.status_code == 200
        except:
            return False
    
    async def obter_analises_recentes(self, limite: int = 10) -> list:
        """
        Obtém análises recentes do sistema principal
        Primeiro tenta Firebase, depois fallback para HTTP
        
        Args:
            limite: Número máximo de análises a retornar
            
        Returns:
            Lista de análises recentes
        """
        try:
            self.logger.info(f"📊 Obtendo {limite} análises recentes do sistema principal...")
            
            # 1. Tenta buscar diretamente do Firebase (mais rápido)
            if self.firebase_db.is_configured():
                self.logger.info("🔥 Buscando análises recentes no Firebase...")
                analises_firebase = self.firebase_db.get_analises_recentes_sistema_principal(limite)
                
                if analises_firebase:
                    self.logger.info(f"✅ {len(analises_firebase)} análises obtidas do Firebase")
                    return analises_firebase
                else:
                    self.logger.info("⚠️ Nenhuma análise encontrada no Firebase, tentando HTTP...")
            
            # 2. Fallback para HTTP (sistema principal)
            self.logger.info("🌐 Buscando análises via HTTP...")
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.sistema_principal_url}/api/estatisticas/recentes")
                
                if response.status_code == 200:
                    dados = response.json()
                    analises = dados.get('analises', [])
                    analises_limitadas = analises[:limite]
                    self.logger.info(f"✅ {len(analises_limitadas)} análises obtidas via HTTP")
                    return analises_limitadas
                
                return []
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter análises recentes: {str(e)}")
            return []
    
    async def buscar_por_ticket_alternativo(self, ticket_numero: str) -> Optional[Dict[str, Any]]:
        """
        Método alternativo para buscar chamado por ticket
        Tenta diferentes estratégias de busca
        
        Args:
            ticket_numero: Número do ticket
            
        Returns:
            Dados do chamado ou None
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Estratégia 1: Buscar por período (últimos 30 dias)
                # Isso seria implementado se houvesse um endpoint específico
                
                # Estratégia 2: Buscar em cache local se disponível
                # (implementar cache local se necessário)
                
                # Estratégia 3: Buscar diretamente no banco se tiver acesso
                # (implementar conexão direta ao banco se necessário)
                
                self.logger.info(f"🔍 Tentativa alternativa de busca para ticket: {ticket_numero}")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Erro na busca alternativa: {str(e)}")
            return None

# Instância global do serviço
integracao_service = IntegracaoService()
