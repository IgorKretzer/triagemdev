"""
Exemplo de Uso da Integração entre Sistemas
Demonstra como usar o sistema de triagem com tickets do sistema principal
"""

import asyncio
import httpx
import json
from datetime import datetime

async def exemplo_integracao_completa():
    """Exemplo completo da integração entre os sistemas"""
    
    print("🔗 INTEGRAÇÃO ENTRE SISTEMAS - EXEMPLO COMPLETO")
    print("=" * 60)
    
    # URLs dos sistemas
    sistema_principal_url = "http://localhost:8000"  # IaChamadoN3
    sistema_triagem_url = "http://localhost:8001"    # Sistema de Triagem
    
    print(f"📋 Sistema Principal: {sistema_principal_url}")
    print(f"🎯 Sistema Triagem: {sistema_triagem_url}")
    print()
    
    # ============================================
    # PASSO 1: VERIFICAR CONECTIVIDADE
    # ============================================
    
    print("🔍 PASSO 1: Verificando conectividade dos sistemas")
    print("-" * 50)
    
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            # Verifica sistema principal
            response = await client.get(f"{sistema_principal_url}/health")
            if response.status_code == 200:
                print("✅ Sistema Principal: Online")
            else:
                print("❌ Sistema Principal: Erro")
                return
        except:
            print("❌ Sistema Principal: Offline")
            return
        
        try:
            # Verifica sistema de triagem
            response = await client.get(f"{sistema_triagem_url}/health")
            if response.status_code == 200:
                print("✅ Sistema Triagem: Online")
            else:
                print("❌ Sistema Triagem: Erro")
                return
        except:
            print("❌ Sistema Triagem: Offline")
            return
    
    # ============================================
    # PASSO 2: LISTAR ANÁLISES RECENTES
    # ============================================
    
    print("\n📊 PASSO 2: Listando análises recentes do sistema principal")
    print("-" * 50)
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(f"{sistema_triagem_url}/api/triagem/sistema-principal/analises-recentes?limite=5")
            
            if response.status_code == 200:
                dados = response.json()
                analises = dados.get('analises', [])
                
                print(f"✅ {len(analises)} análises encontradas:")
                
                for i, analise in enumerate(analises, 1):
                    ticket = analise.get('ticket_numero', 'N/A')
                    modulo = analise.get('modulo_identificado', 'N/A')
                    data = analise.get('data_analise', 'N/A')
                    print(f"   {i}. Ticket {ticket} - {modulo} - {data}")
                
                if not analises:
                    print("⚠️  Nenhuma análise encontrada no sistema principal")
                    print("   Execute algumas análises no sistema principal primeiro")
                    return
                
                # Usa o primeiro ticket para exemplo
                ticket_exemplo = analises[0].get('ticket_numero')
                print(f"\n🎯 Usando ticket {ticket_exemplo} para exemplo")
                
            else:
                print(f"❌ Erro ao buscar análises: {response.status_code}")
                return
                
    except Exception as e:
        print(f"❌ Erro ao conectar com sistema de triagem: {e}")
        return
    
    # ============================================
    # PASSO 3: TRIAGEM POR TICKET
    # ============================================
    
    print(f"\n🎯 PASSO 3: Executando triagem para ticket {ticket_exemplo}")
    print("-" * 50)
    
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(f"{sistema_triagem_url}/api/triagem/ticket/{ticket_exemplo}")
            
            if response.status_code == 200:
                resultado = response.json()
                
                print("✅ Triagem executada com sucesso!")
                print(f"   • Ticket: {resultado.get('ticket_numero')}")
                print(f"   • Análise ID: {resultado.get('analise_id_original')}")
                print(f"   • Padrões detectados: {len(resultado.get('padroes_encontrados', []))}")
                print(f"   • Soluções geradas: {len(resultado.get('solucoes_sugeridas', []))}")
                print(f"   • Modo Mock: {resultado.get('modo_mock', False)}")
                
                # Mostra informações de integração
                integracao = resultado.get('integracao', {})
                if integracao:
                    print(f"\n🔗 Informações de Integração:")
                    print(f"   • Sistema origem: {integracao.get('sistema_origem')}")
                    print(f"   • Data original: {integracao.get('data_chamado_original')}")
                    print(f"   • Usuário original: {integracao.get('usuario_original')}")
                    print(f"   • Cliente original: {integracao.get('cliente_original')}")
                
                # Mostra soluções sugeridas
                solucoes = resultado.get('solucoes_sugeridas', [])
                if solucoes:
                    print(f"\n💡 Soluções Sugeridas:")
                    for i, sol in enumerate(solucoes, 1):
                        print(f"   {i}. [{sol.get('prioridade', 'N/A').upper()}] {sol.get('categoria', 'N/A')}")
                        print(f"      Solução: {sol.get('solucao', 'N/A')[:100]}...")
                        if sol.get('codigo_sugerido'):
                            print(f"      Código: {sol.get('codigo_sugerido', '')[:50]}...")
                
                # Salva resultado em arquivo
                with open(f'triagem_ticket_{ticket_exemplo}.json', 'w', encoding='utf-8') as f:
                    json.dump(resultado, f, indent=2, ensure_ascii=False)
                
                print(f"\n💾 Resultado salvo em: triagem_ticket_{ticket_exemplo}.json")
                
            else:
                print(f"❌ Erro na triagem: {response.status_code}")
                print(f"   Resposta: {response.text}")
                
    except Exception as e:
        print(f"❌ Erro ao executar triagem: {e}")
        return
    
    # ============================================
    # PASSO 4: TESTE DE BUSCA DIRETA
    # ============================================
    
    print(f"\n🔍 PASSO 4: Testando busca direta do chamado")
    print("-" * 50)
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(f"{sistema_triagem_url}/api/triagem/buscar-chamado/{ticket_exemplo}")
            
            if response.status_code == 200:
                dados = response.json()
                chamado = dados.get('dados_chamado', {})
                
                print("✅ Chamado encontrado diretamente:")
                print(f"   • Ticket: {chamado.get('ticket_numero')}")
                print(f"   • Módulo: {chamado.get('modulo_identificado')}")
                print(f"   • Tipo: {chamado.get('tipo_identificado')}")
                print(f"   • Data: {chamado.get('data_analise')}")
                print(f"   • Texto do chamado: {len(chamado.get('chamado_gerado', ''))} caracteres")
                
            else:
                print(f"❌ Erro na busca: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Erro na busca direta: {e}")
    
    print("\n🎉 EXEMPLO DE INTEGRAÇÃO CONCLUÍDO!")
    print("=" * 60)
    print("✅ Sistema funcionando corretamente")
    print("✅ Integração entre sistemas operacional")
    print("✅ Triagem automática por ticket funcionando")

async def exemplo_api_rest():
    """Exemplo de uso via API REST"""
    print("\n🌐 EXEMPLO DE USO VIA API REST")
    print("=" * 60)
    
    sistema_triagem_url = "http://localhost:8001"
    
    # Exemplo de triagem por ticket
    payload_ticket = {
        "ticket_numero": "12345"
    }
    
    print("📋 Exemplo de chamada para triagem por ticket:")
    print(f"curl -X POST {sistema_triagem_url}/api/triagem/ticket/12345")
    
    print("\n📋 Exemplo de busca de chamado:")
    print(f"curl -X GET {sistema_triagem_url}/api/triagem/buscar-chamado/12345")
    
    print("\n📋 Exemplo de verificação de status:")
    print(f"curl -X GET {sistema_triagem_url}/api/triagem/sistema-principal/status")
    
    print("\n📋 Exemplo de análises recentes:")
    print(f"curl -X GET {sistema_triagem_url}/api/triagem/sistema-principal/analises-recentes")

async def exemplo_frontend():
    """Exemplo de uso no frontend"""
    print("\n🎨 EXEMPLO DE USO NO FRONTEND")
    print("=" * 60)
    
    print("1. Acesse: http://localhost:3000")
    print("2. Clique em 'Por Ticket'")
    print("3. Digite o número do ticket (ex: 12345)")
    print("4. Clique em 'Buscar e Triar'")
    print("5. Veja as soluções sugeridas automaticamente")
    
    print("\n🔄 Fluxo completo:")
    print("   Ticket → Sistema Principal → Busca Chamado → Triagem → Soluções")

if __name__ == "__main__":
    print("🚀 Iniciando exemplos de integração...")
    
    # Executa exemplo principal
    asyncio.run(exemplo_integracao_completa())
    
    # Executa exemplos adicionais
    asyncio.run(exemplo_api_rest())
    asyncio.run(exemplo_frontend())
    
    print("\n✨ Exemplos concluídos!")
    print("\n💡 Para usar em produção:")
    print("   1. Configure SISTEMA_PRINCIPAL_URL no .env")
    print("   2. Deploy ambos os sistemas")
    print("   3. Configure URLs de produção")
