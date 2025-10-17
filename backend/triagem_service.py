import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import google.generativeai as genai
import os
from firebase_db import FirebaseDatabase

@dataclass
class SolucaoTriagem:
    tipo: str  # 'codigo', 'sql', 'configuracao', 'debug'
    categoria: str
    prioridade: str  # 'alta', 'media', 'baixa'
    solucao: str
    codigo_sugerido: Optional[str] = None
    script_sql_sugerido: Optional[str] = None
    scripts_sugeridos: Optional[List[str]] = None
    confianca: float = 0.0  # 0.0 a 1.0

class TriagemService:
    def __init__(self):
        self.base_conhecimento = self._carregar_base_conhecimento()
        
        # Inicializa Firebase
        self.firebase_db = FirebaseDatabase()
        
        # Mesma lógica do sistema principal
        api_key = os.getenv("GEMINI_API_KEY", "")
        
        if api_key and api_key != "sua_chave_aqui":
            genai.configure(api_key=api_key)
            # Usando Gemini 2.5 Flash - rápido e estável (mesmo do sistema principal)
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')
            self.mock_mode = False
            print("✅ Gemini API configurada - modo IA ativo")
        else:
            self.mock_mode = True
            print("⚠️  Gemini API não configurada - usando modo MOCK para triagem")
            print("💡 Configure GEMINI_API_KEY no arquivo .env para usar a IA real")
        
        # Status do Firebase
        if self.firebase_db.is_configured():
            print("✅ Firebase configurado - triagens serão salvas")
        else:
            print("⚠️  Firebase não configurado - triagens não serão salvas")
    
    def _carregar_base_conhecimento(self) -> Dict[str, Any]:
        """Carrega a base de conhecimento de padrões"""
        try:
            with open('base_conhecimento_triagem.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Arquivo base_conhecimento_triagem.json não encontrado")
            return {}
        except Exception as e:
            print(f"❌ Erro ao carregar base de conhecimento: {e}")
            return {}
    
    def salvar_triagem_firebase(
        self, 
        ticket_numero: str, 
        chamado_texto: str, 
        modulo: Optional[str], 
        resultado: Dict[str, Any],
        analise_id_original: Optional[str] = None,
        usuario: Optional[str] = None
    ) -> str:
        """Salva a triagem no Firebase"""
        if not self.firebase_db.is_configured():
            return "mock_triagem_id"
        
        return self.firebase_db.registrar_triagem(
            ticket_numero=ticket_numero,
            chamado_texto=chamado_texto,
            modulo=modulo,
            resultado_triagem=resultado,
            analise_id_original=analise_id_original,
            usuario=usuario
        )
    
    async def analisar_chamado(self, chamado_texto: str, modulo: str = None) -> Dict[str, Any]:
        """
        Analisa um chamado e retorna sugestões de triagem
        
        Args:
            chamado_texto: Texto do chamado gerado
            modulo: Módulo identificado (opcional)
            
        Returns:
            Dicionário com análise de triagem e soluções sugeridas
        """
        # 1. Análise por padrões (regras)
        padroes_encontrados = self._analisar_padroes(chamado_texto)
        
        # 2. Análise por IA (se disponível)
        if not self.mock_mode:
            analise_ia = await self._analisar_com_ia(chamado_texto, modulo, padroes_encontrados)
        else:
            analise_ia = self._gerar_analise_mock(chamado_texto, modulo)
        
        # 3. Combinar resultados
        resultado = {
            "sucesso": True,
            "padroes_encontrados": padroes_encontrados,
            "analise_ia": analise_ia,
            "solucoes_sugeridas": self._gerar_solucoes_consolidadas(padroes_encontrados, analise_ia),
            "resumo": self._gerar_resumo_triagem(padroes_encontrados, analise_ia),
            "modo_mock": self.mock_mode
        }
        
        return resultado
    
    def _analisar_padroes(self, texto: str) -> List[Dict[str, Any]]:
        """Analisa o texto buscando padrões conhecidos"""
        padroes_encontrados = []
        texto_lower = texto.lower()
        
        # Analisar padrões de código VB.NET
        for padrao_id, config in self.base_conhecimento.get("padroes_codigo", {}).get("vb_net", {}).items():
            for palavra_chave in config["palavras_chave"]:
                if palavra_chave.lower() in texto_lower:
                    padroes_encontrados.append({
                        "tipo": "codigo_vb",
                        "padrao_id": padrao_id,
                        "palavra_chave": palavra_chave,
                        "config": config,
                        "confianca": 0.8  # Alta confiança para match exato
                    })
                    break
        
        # Analisar padrões ASP.NET
        for padrao_id, config in self.base_conhecimento.get("padroes_codigo", {}).get("asp_net", {}).items():
            for palavra_chave in config["palavras_chave"]:
                if palavra_chave.lower() in texto_lower:
                    padroes_encontrados.append({
                        "tipo": "codigo_asp",
                        "padrao_id": padrao_id,
                        "palavra_chave": palavra_chave,
                        "config": config,
                        "confianca": 0.8
                    })
                    break
        
        # Analisar padrões de banco
        for padrao_id, config in self.base_conhecimento.get("padroes_banco", {}).items():
            for palavra_chave in config["palavras_chave"]:
                if palavra_chave.lower() in texto_lower:
                    padroes_encontrados.append({
                        "tipo": "banco",
                        "padrao_id": padrao_id,
                        "palavra_chave": palavra_chave,
                        "config": config,
                        "confianca": 0.8
                    })
                    break
        
        # Analisar padrões de sistema
        for padrao_id, config in self.base_conhecimento.get("padroes_sistema", {}).items():
            for palavra_chave in config["palavras_chave"]:
                if palavra_chave.lower() in texto_lower:
                    padroes_encontrados.append({
                        "tipo": "sistema",
                        "padrao_id": padrao_id,
                        "palavra_chave": palavra_chave,
                        "config": config,
                        "confianca": 0.8
                    })
                    break
        
        return padroes_encontrados
    
    async def _analisar_com_ia(self, texto: str, modulo: str, padroes: List[Dict]) -> Dict[str, Any]:
        """Analisa o chamado usando IA para sugestões mais avançadas"""
        
        prompt = self._montar_prompt_triagem(texto, modulo, padroes)
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_resposta_ia_triagem(response.text)
        except Exception as e:
            print(f"❌ Erro ao chamar IA para triagem: {e}")
            return {"erro": str(e)}
    
    def _montar_prompt_triagem(self, texto: str, modulo: str, padroes: List[Dict]) -> str:
        """Monta o prompt especializado para triagem"""
        
        padroes_str = ""
        for padrao in padroes:
            padroes_str += f"- {padrao['tipo']}: {padrao['palavra_chave']}\n"
        
        prompt = f"""
Você é um especialista em suporte técnico do sistema SPONTE (VB.NET + ASP.NET + SQL Server).

=== CHAMADO PARA TRIAGEM ===

MÓDULO: {modulo or 'Não identificado'}

TEXTO DO CHAMADO:
{texto}

=== PADRÕES DETECTADOS ===
{padroes_str or 'Nenhum padrão específico detectado'}

=== SUA TAREFA ===

Analise este chamado e forneça uma triagem técnica detalhada. Retorne APENAS um JSON válido:

{{
  "tipo_problema": "codigo|banco|configuracao|performance|outro",
  "categoria_detalhada": "descrição específica da categoria",
  "diagnostico": "análise técnica do problema",
  "solucao_sugerida": "passos para resolução",
  "codigo_exemplo": "código VB.NET de exemplo (se aplicável)",
  "script_sql": "script SQL de exemplo (se aplicável)",
  "prioridade": "alta|media|baixa",
  "tempo_estimado": "tempo estimado para resolução",
  "recursos_necessarios": ["lista", "de", "recursos"],
  "observacoes": "observações adicionais importantes"
}}

=== CONTEXTO TÉCNICO ===

Sistema SPONTE:
- Backend: VB.NET com ASP.NET Web Forms
- Frontend: HTML, CSS, Bootstrap, AJAX
- Banco: SQL Server
- Arquitetura: Code-behind com eventos (BtnSalvar_Click, BtnExcluir_Click)
- Servidor: AWS

Erros comuns:
- Constraint violations em operações CRUD
- Timeouts em consultas pesadas
- Problemas de ViewState/PostBack
- Erros de permissão/perfil
- Configurações de banco incorretas

IMPORTANTE: Retorne APENAS o JSON, sem texto adicional.
"""
        return prompt
    
    def _parse_resposta_ia_triagem(self, resposta: str) -> Dict[str, Any]:
        """Parse da resposta da IA para triagem"""
        try:
            # Limpa markdown se houver
            resposta_limpa = resposta.strip()
            if resposta_limpa.startswith('```json'):
                resposta_limpa = resposta_limpa[7:]
            if resposta_limpa.startswith('```'):
                resposta_limpa = resposta_limpa[3:]
            if resposta_limpa.endswith('```'):
                resposta_limpa = resposta_limpa[:-3]
            
            resposta_limpa = resposta_limpa.strip()
            
            return json.loads(resposta_limpa)
            
        except Exception as e:
            print(f"❌ Erro ao fazer parse da resposta IA: {e}")
            return {"erro": "Erro ao processar análise da IA"}
    
    def _gerar_analise_mock(self, texto: str, modulo: str) -> Dict[str, Any]:
        """Gera análise mockada para demonstração"""
        return {
            "tipo_problema": "codigo",
            "categoria_detalhada": "Erro de validação em operação CRUD",
            "diagnostico": "Problema detectado em operação de banco de dados com possível violação de constraint",
            "solucao_sugerida": "Verificar validações de dados e constraints do banco antes de executar operação",
            "codigo_exemplo": "Try\n    ' Validação de dados\n    If String.IsNullOrEmpty(campo) Then Throw New ArgumentException(\"Campo obrigatório\")\n    ' Operação de banco\nCatch ex As Exception\n    Throw New Exception($\"Erro na operação: {ex.Message}\")\nEnd Try",
            "script_sql": "SELECT * FROM tabela WHERE campo = 'valor'",
            "prioridade": "alta",
            "tempo_estimado": "1-2 horas",
            "recursos_necessarios": ["Desenvolvedor VB.NET", "Acesso ao banco de dados"],
            "observacoes": "Esta é uma análise mockada. Configure a API do Gemini para análises mais precisas."
        }
    
    def _gerar_solucoes_consolidadas(self, padroes: List[Dict], analise_ia: Dict) -> List[SolucaoTriagem]:
        """Consolida soluções dos padrões e análise da IA"""
        solucoes = []
        
        # Adicionar soluções dos padrões detectados
        for padrao in padroes:
            config = padrao["config"]
            solucao = SolucaoTriagem(
                tipo=config["solucao_tipo"],
                categoria=config["categoria"],
                prioridade=config["prioridade"],
                solucao=config["solucao"],
                codigo_sugerido=config.get("codigo_sugerido"),
                script_sql_sugerido=config.get("script_sql_sugerido"),
                scripts_sugeridos=config.get("scripts_sugeridos"),
                confianca=padrao["confianca"]
            )
            solucoes.append(solucao)
        
        # Adicionar solução da IA (se disponível e válida)
        if analise_ia and "erro" not in analise_ia:
            solucao_ia = SolucaoTriagem(
                tipo=analise_ia.get("tipo_problema", "outro"),
                categoria=analise_ia.get("categoria_detalhada", "Análise IA"),
                prioridade=analise_ia.get("prioridade", "media"),
                solucao=analise_ia.get("solucao_sugerida", ""),
                codigo_sugerido=analise_ia.get("codigo_exemplo"),
                script_sql_sugerido=analise_ia.get("script_sql"),
                confianca=0.7  # Confiança média para IA
            )
            solucoes.append(solucao_ia)
        
        return solucoes
    
    def _gerar_resumo_triagem(self, padroes: List[Dict], analise_ia: Dict) -> Dict[str, Any]:
        """Gera resumo da triagem"""
        total_padroes = len(padroes)
        tem_analise_ia = analise_ia and "erro" not in analise_ia
        
        # Contar por categoria
        categorias = {}
        for padrao in padroes:
            cat = padrao["config"]["categoria"]
            categorias[cat] = categorias.get(cat, 0) + 1
        
        # Prioridade geral
        prioridades = [p["config"]["prioridade"] for p in padroes]
        prioridade_geral = "alta" if "alta" in prioridades else ("media" if "media" in prioridades else "baixa")
        
        return {
            "total_padroes_detectados": total_padroes,
            "tem_analise_ia": tem_analise_ia,
            "categorias_afetadas": list(categorias.keys()),
            "prioridade_geral": prioridade_geral,
            "resumo": f"Detectados {total_padroes} padrões conhecidos" + (" + análise de IA" if tem_analise_ia else "")
        }

# Função para converter SolucaoTriagem para dict (para serialização JSON)
def solucao_para_dict(solucao: SolucaoTriagem) -> Dict[str, Any]:
    return {
        "tipo": solucao.tipo,
        "categoria": solucao.categoria,
        "prioridade": solucao.prioridade,
        "solucao": solucao.solucao,
        "codigo_sugerido": solucao.codigo_sugerido,
        "script_sql_sugerido": solucao.script_sql_sugerido,
        "scripts_sugeridos": solucao.scripts_sugeridos,
        "confianca": solucao.confianca
    }
