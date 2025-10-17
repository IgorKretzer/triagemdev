#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import httpx

async def teste_simples():
    print("Teste da Integracao")
    print("=" * 30)
    
    # URLs
    sistema_principal = "http://localhost:8000"
    sistema_triagem = "http://localhost:8001"
    
    print(f"Sistema Principal: {sistema_principal}")
    print(f"Sistema Triagem: {sistema_triagem}")
    print()
    
    # Testa sistema principal
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{sistema_principal}/health")
            if response.status_code == 200:
                print("✅ Sistema Principal: Online")
            else:
                print("❌ Sistema Principal: Erro")
                return
    except Exception as e:
        print(f"❌ Sistema Principal: Offline ({e})")
        return
    
    # Testa sistema de triagem
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{sistema_triagem}/health")
            if response.status_code == 200:
                print("✅ Sistema Triagem: Online")
            else:
                print("❌ Sistema Triagem: Erro")
                return
    except Exception as e:
        print(f"❌ Sistema Triagem: Offline ({e})")
        return
    
    # Lista analises recentes
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(f"{sistema_triagem}/api/triagem/sistema-principal/analises-recentes?limite=3")
            
            if response.status_code == 200:
                dados = response.json()
                analises = dados.get('analises', [])
                
                if analises:
                    print(f"✅ {len(analises)} analises encontradas:")
                    for i, analise in enumerate(analises, 1):
                        ticket = analise.get('ticket_numero', 'N/A')
                        modulo = analise.get('modulo_identificado', 'N/A')
                        print(f"   {i}. Ticket {ticket} - {modulo}")
                    
                    # Testa triagem
                    ticket_teste = analises[0].get('ticket_numero')
                    print(f"\n🎯 Testando com ticket: {ticket_teste}")
                    
                    response_triagem = await client.post(f"{sistema_triagem}/api/triagem/ticket/{ticket_teste}")
                    
                    if response_triagem.status_code == 200:
                        resultado = response_triagem.json()
                        print("✅ Triagem executada com sucesso!")
                        print(f"   • Padroes detectados: {len(resultado.get('padroes_encontrados', []))}")
                        print(f"   • Solucoes geradas: {len(resultado.get('solucoes_sugeridas', []))}")
                        print(f"   • Modo Mock: {resultado.get('modo_mock', False)}")
                        print("\n🎉 INTEGRACAO FUNCIONANDO!")
                    else:
                        print(f"❌ Erro na triagem: {response_triagem.status_code}")
                        
                else:
                    print("⚠️  Nenhuma analise encontrada")
                    print("   Execute algumas analises no sistema principal primeiro")
                    
            else:
                print(f"❌ Erro ao buscar analises: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    asyncio.run(teste_simples())
