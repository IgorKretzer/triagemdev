"""
Exemplo de uso do Sistema de Triagem Inteligente
Demonstra como usar o sistema para analisar chamados
"""

import asyncio
import json
from triagem_service import TriagemService

async def exemplo_triagem():
    """Exemplo completo de uso do sistema de triagem"""
    
    print("🔍 Sistema de Triagem Inteligente - Exemplo de Uso")
    print("=" * 60)
    
    # Inicializa o serviço
    triagem_service = TriagemService()
    
    # Exemplo 1: Chamado com erro de salvar (VB.NET)
    print("\n📋 EXEMPLO 1: Erro ao Salvar")
    print("-" * 40)
    
    chamado_salvar = """
    VERSÃO DO SISTEMA EM QUE O PROBLEMA OCORREU:
    R = 2024.1.0
    
    CÓDIGO DA BASE QUE APRESENTA O PROBLEMA:
    R = Base do cliente ABC Escola
    
    JUSTIFICATIVA DA URGÊNCIA:
    R = Não consegue salvar dados de alunos - sistema crítico
    
    MENU/LOCAL DO SISTEMA EM QUE ACONTECE:
    R = Cadastros > Alunos > Novo Aluno
    
    BRIEFING:
    R = Cliente relata que ao tentar salvar um novo aluno, o sistema apresenta erro "Constraint violation" 
    e não permite o salvamento. O erro ocorre especificamente no BtnSalvar_Click após preencher todos 
    os campos obrigatórios.
    
    EXEMPLOS (OBRIGATÓRIO):
    R = CPF: 123.456.789-00, Nome: João Silva, Data Nascimento: 15/03/2010
    
    OBS:
    R = Cliente: ABC Escola, Ticket: #12345
    """
    
    resultado1 = await triagem_service.analisar_chamado(chamado_salvar, "CADASTROS")
    print_resultado(resultado1)
    
    # Exemplo 2: Chamado com erro de banco
    print("\n📋 EXEMPLO 2: Erro de Banco de Dados")
    print("-" * 40)
    
    chamado_banco = """
    VERSÃO DO SISTEMA EM QUE O PROBLEMA OCORREU:
    R = 2024.1.0
    
    CÓDIGO DA BASE QUE APRESENTA O PROBLEMA:
    R = Base do cliente XYZ Colégio
    
    JUSTIFICATIVA DA URGÊNCIA:
    R = Erro de timeout em consulta - sistema lento
    
    MENU/LOCAL DO SISTEMA EM QUE ACONTECE:
    R = Relatórios > Acadêmicos > Lista de Alunos
    
    BRIEFING:
    R = Ao tentar gerar relatório de lista de alunos, o sistema apresenta "Query timeout" após 30 segundos. 
    A consulta parece estar demorando muito para executar.
    
    EXEMPLOS (OBRIGATÓRIO):
    R = Filtros: Todas as turmas, Período: Ano letivo 2024
    
    OBS:
    R = Cliente: XYZ Colégio, Ticket: #12346
    """
    
    resultado2 = await triagem_service.analisar_chamado(chamado_banco, "RELATÓRIOS")
    print_resultado(resultado2)
    
    # Exemplo 3: Chamado com erro de AJAX
    print("\n📋 EXEMPLO 3: Erro AJAX")
    print("-" * 40)
    
    chamado_ajax = """
    VERSÃO DO SISTEMA EM QUE O PROBLEMA OCORREU:
    R = 2024.1.0
    
    CÓDIGO DA BASE QUE APRESENTA O PROBLEMA:
    R = Base do cliente DEF Instituto
    
    JUSTIFICATIVA DA URGÊNCIA:
    R = Erro 500 em operação AJAX - funcionalidade quebrada
    
    MENU/LOCAL DO SISTEMA EM QUE ACONTECE:
    R = Financeiro > Boletos > Gerar Boletos
    
    BRIEFING:
    R = Ao tentar gerar boletos em lote, o sistema apresenta "Internal Server Error" via AJAX. 
    O erro ocorre quando clica no botão "Gerar Todos" que faz uma chamada AJAX para o WebMethod.
    
    EXEMPLOS (OBRIGATÓRIO):
    R = 150 boletos para gerar, Vencimento: 05/02/2024
    
    OBS:
    R = Cliente: DEF Instituto, Ticket: #12347
    """
    
    resultado3 = await triagem_service.analisar_chamado(chamado_ajax, "FINANCEIRO")
    print_resultado(resultado3)
    
    # Exemplo 4: Chamado sem padrão específico
    print("\n📋 EXEMPLO 4: Chamado Genérico")
    print("-" * 40)
    
    chamado_generico = """
    VERSÃO DO SISTEMA EM QUE O PROBLEMA OCORREU:
    R = 2024.1.0
    
    CÓDIGO DA BASE QUE APRESENTA O PROBLEMA:
    R = Base do cliente GHI Escola
    
    JUSTIFICATIVA DA URGÊNCIA:
    R = Dúvida sobre funcionalidade
    
    MENU/LOCAL DO SISTEMA EM QUE ACONTECE:
    R = Pedagógico > Notas > Lançamento
    
    BRIEFING:
    R = Cliente tem dúvida sobre como configurar os pesos das avaliações no sistema.
    
    EXEMPLOS (OBRIGATÓRIO):
    R = Avaliação 1: peso 3, Avaliação 2: peso 2, Avaliação 3: peso 5
    
    OBS:
    R = Cliente: GHI Escola, Ticket: #12348
    """
    
    resultado4 = await triagem_service.analisar_chamado(chamado_generico, "PEDAGÓGICO")
    print_resultado(resultado4)

def print_resultado(resultado):
    """Imprime o resultado da triagem de forma formatada"""
    
    print(f"✅ Sucesso: {resultado['sucesso']}")
    print(f"🎯 Modo Mock: {resultado['modo_mock']}")
    
    # Padrões encontrados
    padroes = resultado['padroes_encontrados']
    print(f"\n🔍 Padrões Detectados ({len(padroes)}):")
    for padrao in padroes:
        print(f"  • {padrao['tipo']}: {padrao['palavra_chave']} (confiança: {padrao['confianca']})")
    
    # Análise da IA
    analise_ia = resultado['analise_ia']
    if analise_ia and 'erro' not in analise_ia:
        print(f"\n🤖 Análise IA:")
        print(f"  • Tipo: {analise_ia.get('tipo_problema', 'N/A')}")
        print(f"  • Categoria: {analise_ia.get('categoria_detalhada', 'N/A')}")
        print(f"  • Prioridade: {analise_ia.get('prioridade', 'N/A')}")
        print(f"  • Tempo estimado: {analise_ia.get('tempo_estimado', 'N/A')}")
    
    # Soluções sugeridas
    solucoes = resultado['solucoes_sugeridas']
    print(f"\n💡 Soluções Sugeridas ({len(solucoes)}):")
    for i, sol in enumerate(solucoes, 1):
        print(f"  {i}. [{sol.prioridade.upper()}] {sol.categoria}")
        print(f"     Tipo: {sol.tipo}")
        print(f"     Solução: {sol.solucao}")
        if sol.codigo_sugerido:
            print(f"     Código: {sol.codigo_sugerido[:100]}...")
        if sol.script_sql_sugerido:
            print(f"     SQL: {sol.script_sql_sugerido[:100]}...")
        print(f"     Confiança: {sol.confianca:.1%}")
        print()
    
    # Resumo
    resumo = resultado['resumo']
    print(f"📊 Resumo:")
    print(f"  • {resumo['resumo']}")
    print(f"  • Prioridade geral: {resumo['prioridade_geral'].upper()}")
    print(f"  • Categorias: {', '.join(resumo['categorias_afetadas'])}")

async def exemplo_api_rest():
    """Exemplo de como usar via API REST"""
    print("\n🌐 EXEMPLO DE USO VIA API REST")
    print("=" * 60)
    
    import httpx
    
    # URL base (ajuste conforme necessário)
    base_url = "http://localhost:8001"
    
    # Exemplo de chamada para triagem
    payload = {
        "chamado_texto": """
        VERSÃO DO SISTEMA EM QUE O PROBLEMA OCORREU:
        R = 2024.1.0
        
        CÓDIGO DA BASE QUE APRESENTA O PROBLEMA:
        R = Base do cliente ABC Escola
        
        JUSTIFICATIVA DA URGÊNCIA:
        R = Erro ao salvar dados de alunos
        
        MENU/LOCAL DO SISTEMA EM QUE ACONTECE:
        R = Cadastros > Alunos
        
        BRIEFING:
        R = Erro de constraint violation ao tentar salvar novo aluno
        
        EXEMPLOS (OBRIGATÓRIO):
        R = CPF: 123.456.789-00
        
        OBS:
        R = Ticket: #12345
        """,
        "modulo": "CADASTROS"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{base_url}/api/triagem/analisar", json=payload)
            
            if response.status_code == 200:
                resultado = response.json()
                print("✅ Resposta da API:")
                print(json.dumps(resultado, indent=2, ensure_ascii=False))
            else:
                print(f"❌ Erro na API: {response.status_code}")
                print(response.text)
                
    except Exception as e:
        print(f"❌ Erro ao chamar API: {e}")
        print("💡 Certifique-se de que o servidor está rodando em http://localhost:8001")

if __name__ == "__main__":
    print("🚀 Iniciando exemplos do Sistema de Triagem...")
    
    # Executa exemplo direto
    asyncio.run(exemplo_triagem())
    
    # Executa exemplo via API (descomente se o servidor estiver rodando)
    # asyncio.run(exemplo_api_rest())
    
    print("\n✨ Exemplos concluídos!")
