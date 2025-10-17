#!/usr/bin/env python3
"""
Teste Rápido do Sistema de Triagem
Executa um teste básico para verificar se tudo está funcionando
"""

import asyncio
import sys
import os
from datetime import datetime

def print_header():
    print("🎯 SISTEMA DE TRIAGEM INTELIGENTE - SPONTE")
    print("=" * 60)
    print(f"⏰ Teste iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

def print_step(step, description):
    print(f"📋 PASSO {step}: {description}")
    print("-" * 40)

async def test_imports():
    """Testa se todas as importações funcionam"""
    print_step(1, "Testando Importações")
    
    try:
        from triagem_service import TriagemService
        from schemas_triagem import TriagemRequest, TriagemResponse
        print("✅ Importações básicas: OK")
        
        # Testa importação opcional do Gemini
        try:
            import google.generativeai as genai
            print("✅ Google Generative AI: OK")
        except ImportError:
            print("⚠️  Google Generative AI: Não instalado (modo MOCK)")
        
        return True
    except Exception as e:
        print(f"❌ Erro nas importações: {e}")
        return False

async def test_base_conhecimento():
    """Testa se a base de conhecimento está carregada"""
    print_step(2, "Testando Base de Conhecimento")
    
    try:
        import json
        
        if not os.path.exists('base_conhecimento_triagem.json'):
            print("❌ Arquivo base_conhecimento_triagem.json não encontrado")
            return False
        
        with open('base_conhecimento_triagem.json', 'r', encoding='utf-8') as f:
            base = json.load(f)
        
        # Verifica estrutura básica
        required_keys = ['padroes_codigo', 'padroes_banco', 'padroes_sistema']
        for key in required_keys:
            if key not in base:
                print(f"❌ Chave '{key}' não encontrada na base de conhecimento")
                return False
        
        # Conta padrões
        total_padroes = 0
        total_padroes += sum(len(categoria) for categoria in base['padroes_codigo'].values())
        total_padroes += len(base['padroes_banco'])
        total_padroes += len(base['padroes_sistema'])
        
        print(f"✅ Base de conhecimento carregada: {total_padroes} padrões")
        print(f"   • Padrões de código: {sum(len(cat) for cat in base['padroes_codigo'].values())}")
        print(f"   • Padrões de banco: {len(base['padroes_banco'])}")
        print(f"   • Padrões de sistema: {len(base['padroes_sistema'])}")
        
        return True
    except Exception as e:
        print(f"❌ Erro na base de conhecimento: {e}")
        return False

async def test_triagem_service():
    """Testa o serviço de triagem"""
    print_step(3, "Testando Serviço de Triagem")
    
    try:
        from triagem_service import TriagemService
        
        # Inicializa o serviço
        service = TriagemService()
        print(f"✅ Serviço inicializado (Modo: {'MOCK' if service.mock_mode else 'IA'})")
        
        # Testa análise com um chamado simples
        chamado_teste = """
        VERSÃO DO SISTEMA EM QUE O PROBLEMA OCORREU:
        R = 2024.1.0
        
        CÓDIGO DA BASE QUE APRESENTA O PROBLEMA:
        R = Base do cliente Teste
        
        JUSTIFICATIVA DA URGÊNCIA:
        R = Erro ao salvar dados
        
        MENU/LOCAL DO SISTEMA EM QUE ACONTECE:
        R = Cadastros > Alunos
        
        BRIEFING:
        R = Erro de constraint violation ao tentar salvar novo aluno no BtnSalvar_Click
        
        EXEMPLOS (OBRIGATÓRIO):
        R = CPF: 123.456.789-00
        
        OBS:
        R = Ticket: #TESTE001
        """
        
        print("🔍 Executando análise de teste...")
        resultado = await service.analisar_chamado(chamado_teste, "CADASTROS")
        
        if resultado['sucesso']:
            print("✅ Análise executada com sucesso")
            print(f"   • Padrões detectados: {len(resultado['padroes_encontrados'])}")
            print(f"   • Soluções geradas: {len(resultado['solucoes_sugeridas'])}")
            
            # Mostra primeiro padrão encontrado
            if resultado['padroes_encontrados']:
                padrao = resultado['padroes_encontrados'][0]
                print(f"   • Primeiro padrão: {padrao['palavra_chave']} ({padrao['tipo']})")
            
            return True
        else:
            print("❌ Falha na análise")
            return False
            
    except Exception as e:
        print(f"❌ Erro no serviço de triagem: {e}")
        return False

async def test_api_endpoints():
    """Testa se os endpoints da API estão funcionando"""
    print_step(4, "Testando Endpoints da API")
    
    try:
        import httpx
        
        # Testa se o servidor está rodando
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get("http://localhost:8001/health")
                
                if response.status_code == 200:
                    print("✅ Servidor API está rodando")
                    health_data = response.json()
                    print(f"   • Status: {health_data.get('status', 'unknown')}")
                    print(f"   • Serviços: {health_data.get('servicos', {})}")
                    return True
                else:
                    print(f"⚠️  Servidor respondeu com status: {response.status_code}")
                    return False
                    
        except httpx.ConnectError:
            print("⚠️  Servidor não está rodando (isso é normal se você não iniciou)")
            print("   Para testar a API, execute: python main_triagem.py")
            return True  # Não é um erro, só não está rodando
            
    except ImportError:
        print("⚠️  httpx não instalado - pulando teste de API")
        return True
    except Exception as e:
        print(f"❌ Erro no teste de API: {e}")
        return False

def print_resumo(resultados):
    """Imprime resumo dos testes"""
    print("\n📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    total_testes = len(resultados)
    testes_ok = sum(1 for r in resultados if r)
    
    print(f"✅ Testes bem-sucedidos: {testes_ok}/{total_testes}")
    
    if testes_ok == total_testes:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("\n🚀 Sistema pronto para uso!")
        print("\n💡 Próximos passos:")
        print("   1. Execute: python main_triagem.py")
        print("   2. Acesse: http://localhost:8001/docs")
        print("   3. Teste: python exemplo_uso.py")
    else:
        print("⚠️  Alguns testes falharam")
        print("\n🔧 Verifique os erros acima e corrija antes de usar")
    
    print(f"\n⏰ Teste concluído em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

async def main():
    """Função principal do teste"""
    print_header()
    
    # Lista de testes
    testes = [
        ("Importações", test_imports),
        ("Base de Conhecimento", test_base_conhecimento),
        ("Serviço de Triagem", test_triagem_service),
        ("Endpoints da API", test_api_endpoints)
    ]
    
    # Executa testes
    resultados = []
    for nome, teste_func in testes:
        try:
            resultado = await teste_func()
            resultados.append(resultado)
        except Exception as e:
            print(f"❌ Erro inesperado no teste '{nome}': {e}")
            resultados.append(False)
        
        print()  # Linha em branco entre testes
    
    # Imprime resumo
    print_resumo(resultados)
    
    # Retorna código de saída
    return 0 if all(resultados) else 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        sys.exit(1)
