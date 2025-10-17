import json
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, List, Any
from google.cloud.firestore import FieldFilter
from firebase_config import firebase_config

class FirebaseDatabase:
    def __init__(self):
        self.db = firebase_config.db
        
        # Nomes das coleções no Firestore
        self.COLLECTIONS = {
            'triagens': 'triagens',  # Coleção específica para triagens
            'analises': 'analises',  # Coleção do sistema principal (para leitura)
            'feedbacks_triagem': 'feedbacks_triagem',  # Feedbacks específicos de triagem
            'estatisticas_triagem': 'estatisticas_triagem'  # Estatísticas de triagem
        }
    
    def is_configured(self) -> bool:
        """Verifica se o Firebase está configurado"""
        return self.db is not None
    
    # ==================== TRIAGENS ====================
    
    def registrar_triagem(
        self,
        ticket_numero: str,
        chamado_texto: str,
        modulo: Optional[str],
        resultado_triagem: Dict[str, Any],
        analise_id_original: Optional[str] = None,
        usuario: Optional[str] = None
    ) -> str:
        """Registra uma triagem completa"""
        if not self.is_configured():
            print("⚠️  Firebase não configurado - triagem não será salva")
            return "mock_id"
        
        doc_ref = self.db.collection(self.COLLECTIONS['triagens']).document()
        
        now = datetime.now(timezone.utc)
        data = {
            'ticket_numero': ticket_numero,
            'analise_id_original': analise_id_original,
            'chamado_texto': chamado_texto,
            'modulo_identificado': modulo,
            'usuario_nome': usuario,
            'padroes_encontrados': resultado_triagem.get('padroes_encontrados', []),
            'analise_ia': resultado_triagem.get('analise_ia', {}),
            'solucoes_sugeridas': resultado_triagem.get('solucoes_sugeridas', []),
            'resumo': resultado_triagem.get('resumo', {}),
            'modo_mock': resultado_triagem.get('modo_mock', False),
            'tempo_processamento_ms': resultado_triagem.get('tempo_processamento_ms', 0),
            'foi_utilizada': False,
            'data_triagem': now,
            'created_at': now,
            'updated_at': now
        }
        
        doc_ref.set(data)
        print(f"✅ Triagem salva no Firebase: {doc_ref.id}")
        return doc_ref.id
    
    def marcar_triagem_como_utilizada(self, triagem_id: str):
        """Marca que a triagem foi utilizada pelo suporte"""
        if not self.is_configured():
            return
        
        doc_ref = self.db.collection(self.COLLECTIONS['triagens']).document(triagem_id)
        doc_ref.update({
            'foi_utilizada': True,
            'updated_at': datetime.now(timezone.utc)
        })
    
    def get_triagem_por_id(self, triagem_id: str) -> Optional[Dict]:
        """Busca uma triagem por ID"""
        if not self.is_configured():
            return None
        
        doc_ref = self.db.collection(self.COLLECTIONS['triagens']).document(triagem_id)
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            # Converter timestamps para string para compatibilidade
            if 'data_triagem' in data and hasattr(data['data_triagem'], 'isoformat'):
                data['data_triagem'] = data['data_triagem'].isoformat()
            if 'created_at' in data and hasattr(data['created_at'], 'isoformat'):
                data['created_at'] = data['created_at'].isoformat()
            if 'updated_at' in data and hasattr(data['updated_at'], 'isoformat'):
                data['updated_at'] = data['updated_at'].isoformat()
            return data
        return None
    
    def get_triagens_por_ticket(self, ticket_numero: str) -> List[Dict]:
        """Busca todas as triagens de um ticket específico"""
        if not self.is_configured():
            return []
        
        query = self.db.collection(self.COLLECTIONS['triagens']).where(
            'ticket_numero', '==', ticket_numero
        )
        
        triagens = []
        for doc in query.stream():
            data = doc.to_dict()
            # Converter timestamps
            if 'data_triagem' in data and hasattr(data['data_triagem'], 'isoformat'):
                data['data_triagem'] = data['data_triagem'].isoformat()
            
            triagens.append({
                'id': doc.id,
                'ticket_numero': data.get('ticket_numero'),
                'modulo_identificado': data.get('modulo_identificado'),
                'data_triagem': data.get('data_triagem'),
                'foi_utilizada': data.get('foi_utilizada', False),
                'resumo': data.get('resumo', {})
            })
        
        # Ordena localmente por data (mais recente primeiro)
        triagens.sort(key=lambda x: x.get('data_triagem', ''), reverse=True)
        
        return triagens
    
    # ==================== INTEGRAÇÃO COM SISTEMA PRINCIPAL ====================
    
    def buscar_analise_por_ticket(self, ticket_numero: str) -> Optional[Dict]:
        """Busca uma análise do sistema principal por número do ticket"""
        if not self.is_configured():
            return None
        
        # Busca na coleção 'analises' do sistema principal (sem ordenação para evitar problemas de índice)
        query = self.db.collection(self.COLLECTIONS['analises']).where(
            'ticket_numero', '==', ticket_numero
        )
        
        docs = list(query.stream())
        if docs:
            # Ordena localmente por data (mais recente primeiro)
            docs.sort(key=lambda doc: doc.to_dict().get('data_analise', ''), reverse=True)
            doc = docs[0]
            data = doc.to_dict()
            
            # Converter timestamps
            if 'data_analise' in data and hasattr(data['data_analise'], 'isoformat'):
                data['data_analise'] = data['data_analise'].isoformat()
            
            return {
                'id': doc.id,
                'ticket_numero': data.get('ticket_numero'),
                'chamado_gerado': data.get('chamado_gerado'),
                'modulo_identificado': data.get('modulo_identificado'),
                'usuario_nome': data.get('usuario_nome'),
                'cliente_nome': data.get('cliente_nome'),
                'data_analise': data.get('data_analise'),
                'tipo_identificado': data.get('tipo_identificado')
            }
        
        return None
    
    def get_analises_recentes_sistema_principal(self, limite: int = 10) -> List[Dict]:
        """Retorna análises recentes do sistema principal"""
        if not self.is_configured():
            return []
        
        query = self.db.collection(self.COLLECTIONS['analises']).order_by(
            'data_analise', direction='DESCENDING'
        ).limit(limite)
        
        analises = []
        for doc in query.stream():
            data = doc.to_dict()
            # Converter timestamps
            if 'data_analise' in data and hasattr(data['data_analise'], 'isoformat'):
                data['data_analise'] = data['data_analise'].isoformat()
            
            analises.append({
                'id': doc.id,
                'ticket_numero': data.get('ticket_numero', ''),
                'usuario_nome': data.get('usuario_nome'),
                'data_analise': data.get('data_analise', ''),
                'tipo_identificado': data.get('tipo_identificado'),
                'modulo_identificado': data.get('modulo_identificado'),
                'chamado_gerado': data.get('chamado_gerado'),
                'foi_copiado': data.get('foi_copiado', False)
            })
        
        return analises
    
    # ==================== FEEDBACKS DE TRIAGEM ====================
    
    def registrar_feedback_triagem(
        self,
        triagem_id: str,
        foi_util: bool,
        nota: Optional[int] = None,
        comentario: Optional[str] = None,
        solucao_utilizada: Optional[str] = None
    ) -> str:
        """Registra feedback específico de triagem"""
        if not self.is_configured():
            return "mock_feedback_id"
        
        doc_ref = self.db.collection(self.COLLECTIONS['feedbacks_triagem']).document()
        
        now = datetime.now(timezone.utc)
        data = {
            'triagem_id': triagem_id,
            'foi_util': foi_util,
            'nota': nota,
            'comentario': comentario,
            'solucao_utilizada': solucao_utilizada,
            'data_feedback': now,
            'created_at': now,
            'updated_at': now
        }
        
        doc_ref.set(data)
        return doc_ref.id
    
    # ==================== ESTATÍSTICAS DE TRIAGEM ====================
    
    def get_estatisticas_triagem(self, dias: int = 7) -> Dict[str, Any]:
        """Retorna estatísticas das triagens"""
        if not self.is_configured():
            return {
                'total_triagens': 0,
                'triagens_utilizadas': 0,
                'taxa_utilizacao': 0,
                'modulos_mais_triados': [],
                'tempo_medio_ms': 0,
                'periodo_dias': dias
            }
        
        # Busca todas as triagens (sem filtro de data para evitar problemas de índice)
        triagens_query = self.db.collection(self.COLLECTIONS['triagens'])
        all_triagens = list(triagens_query.stream())
        
        # Filtra por data localmente
        data_inicio = datetime.now(timezone.utc) - timedelta(days=dias)
        triagens_recentes = []
        
        for doc in all_triagens:
            data = doc.to_dict()
            data_triagem = data.get('data_triagem')
            if data_triagem and data_triagem >= data_inicio:
                triagens_recentes.append((doc, data))
        
        total_triagens = len(triagens_recentes)
        
        # Conta triagens utilizadas
        triagens_utilizadas = sum(1 for _, data in triagens_recentes if data.get('foi_utilizada', False))
        
        # Taxa de utilização
        taxa_utilizacao = (triagens_utilizadas / total_triagens * 100) if total_triagens > 0 else 0
        
        # Módulos mais triados
        modulos_count = {}
        tempo_total = 0
        count_tempo = 0
        
        for _, data in triagens_recentes:
            modulo = data.get('modulo_identificado')
            if modulo and modulo.strip():
                modulos_count[modulo] = modulos_count.get(modulo, 0) + 1
            
            tempo = data.get('tempo_processamento_ms', 0)
            if tempo > 0:
                tempo_total += tempo
                count_tempo += 1
        
        # Ordena e pega os top 5
        modulos_sorted = sorted(modulos_count.items(), key=lambda x: x[1], reverse=True)[:5]
        modulos = [{'modulo': modulo, 'total': total} for modulo, total in modulos_sorted]
        
        tempo_medio = tempo_total / count_tempo if count_tempo > 0 else 0
        
        return {
            'total_triagens': total_triagens,
            'triagens_utilizadas': triagens_utilizadas,
            'taxa_utilizacao': round(taxa_utilizacao, 1),
            'modulos_mais_triados': modulos,
            'tempo_medio_ms': round(tempo_medio, 2),
            'periodo_dias': dias
        }
    
    def get_triagens_recentes(self, limite: int = 10) -> List[Dict]:
        """Retorna triagens mais recentes"""
        if not self.is_configured():
            return []
        
        query = self.db.collection(self.COLLECTIONS['triagens']).order_by(
            'data_triagem', direction='DESCENDING'
        ).limit(limite)
        
        triagens = []
        for doc in query.stream():
            data = doc.to_dict()
            # Converter timestamps
            if 'data_triagem' in data and hasattr(data['data_triagem'], 'isoformat'):
                data['data_triagem'] = data['data_triagem'].isoformat()
            
            triagens.append({
                'id': doc.id,
                'ticket_numero': data.get('ticket_numero', ''),
                'modulo_identificado': data.get('modulo_identificado'),
                'data_triagem': data.get('data_triagem', ''),
                'foi_utilizada': data.get('foi_utilizada', False),
                'resumo': data.get('resumo', {})
            })
        
        return triagens
