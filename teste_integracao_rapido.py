#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Rapido da Integracao
Verifica se voce consegue buscar chamados do sistema principal
"""

import asyncio
import httpx
import json

async def teste_rapido():
    """Teste rápido da integração"""
    
    print("🧪 TESTE RÁPIDO DA INTEGRAÇÃO")
    print("=" * 50)
    
    # URLs
    sistema_principal = "http://localhost:8000"  # IaChamadoN3
    sistema_triagem = "http://localhost:8001"    # Triagem
    
    print(f"📋 Sistema Principal: {sistema_principal}")
    print(f"🎯 Sistema Triagem: {sistema_triagem}")
    print()
    
    # 1. Verificar se sistemas estão rodando
    print("🔍 Verificando sistemas...")
    
    sistemas_ok = True
    
    # Testa sistema principal
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{sistema_principal}/health")
            if response.status_code == 200:
                print("✅ Sistema Principal: Online")
            else:
                print("❌ Sistema Principal: Erro")
                sistemas_ok = False
    except:
        print("❌ Sistema Principal: Offline")
        sistemas_ok = False
    
    # Testa sistema de triagem
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{sistema_triagem}/health")
            if response.status_code == 200:
                print("✅ Sistema Triagem: Online")
            else:
                print("❌ Sistema Triagem: Erro")
                sistemas_ok = False
    except:
        print("❌ Sistema Triagem: Offline")
        sistemas_ok = False
    
    if not sistemas_ok:
        print("\n⚠️  Sistemas não estão rodando!")
        print("Execute:")
        print("  # Terminal 1: Sistema Principal")
        print("  cd /home/eduardo/Desktop/IaChamadoN3")
        print("  python -m uvicorn app.main:app --port 8000")
        print()
        print("  # Terminal 2: Sistema Triagem")  
        print("  cd /home/eduardo/Desktop/IaChamadoDev")
        print("  python backend/main_triagem.py")
        return
    
    # 2. Listar análises recentes
    print("\n📊 Buscando análises recentes...")
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(f"{sistema_triagem}/api/triagem/sistema-principal/analises-recentes?limite=3")
            
            if response.status_code == 200:
                dados = response.json()
                analises = dados.get('analises', [])
                
                if analises:
                    print(f"✅ {len(analises)} análises encontradas:")
                    for i, analise in enumerate(analises, 1):
                        ticket = analise.get('ticket_numero', 'N/A')
                        modulo = analise.get('modulo_identificado', 'N/A')
                        data = analise.get('data_analise', 'N/A')[:10]  # Só a data
                        print(f"   {i}. Ticket {ticket} - {modulo} - {data}")
                    
                    # Testa com o primeiro ticket
                    ticket_teste = analises[0].get('ticket_numero')
                    print(f"\n🎯 Testando com ticket: {ticket_teste}")
                    
                    # 3. Teste de triagem
                    print(f"🤖 Executando triagem...")
                    response_triagem = await client.post(f"{sistema_triagem}/api/triagem/ticket/{ticket_teste}")
                    
                    if response_triagem.status_code == 200:
                        resultado = response_triagem.json()
                        print("✅ Triagem executada com sucesso!")
                        print(f"   • Padrões detectados: {len(resultado.get('padroes_encontrados', []))}")
                        print(f"   • Soluções geradas: {len(resultado.get('solucoes_sugeridas', []))}")
                        print(f"   • Modo Mock: {resultado.get('modo_mock', False)}")
                        
                        # Mostra primeira solução se houver
                        solucoes = resultado.get('solucoes_sugeridas', [])
                        if solucoes:
                            sol = solucoes[0]
                            print(f"\n💡 Primeira solução:")
                            print(f"   • Categoria: {sol.get('categoria', 'N/A')}")
                            print(f"   • Prioridade: {sol.get('prioridade', 'N/A')}")
                            print(f"   • Solução: {sol.get('solucao', 'N/A')[:100]}...")
                        
                        print(f"\n🎉 INTEGRAÇÃO FUNCIONANDO PERFEITAMENTE!")
                        print("✅ Sistema principal conectado")
                        print("✅ Sistema de triagem conectado") 
                        print("✅ Busca de chamados funcionando")
                        print("✅ Triagem automática funcionando")
                        
                    else:
                        print(f"❌ Erro na triagem: {response_triagem.status_code}")
                        print(f"   Resposta: {response_triagem.text}")
                        
                else:
                    print("⚠️  Nenhuma análise encontrada no sistema principal")
                    print("   Execute algumas análises no sistema principal primeiro")
                    
            else:
                print(f"❌ Erro ao buscar análises: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n" + "=" * 50)
    print("💡 Para usar no frontend:")
    print("   1. Acesse: http://localhost:3000 (sistema triagem)")
    print("   2. Clique em 'Por Ticket'")
    print("   3. Digite um número de ticket")
    print("   4. Veja a triagem automática!")

if __name__ == "__main__":
    asyncio.run(teste_rapido())
