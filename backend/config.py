import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Configurações do sistema de triagem"""
    
    # API do Google Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Configuração do servidor
    PORT = int(os.getenv("PORT", 8001))
    HOST = os.getenv("HOST", "0.0.0.0")
    
    # Sistema principal (IaChamadoN3)
    SISTEMA_PRINCIPAL_URL = os.getenv("SISTEMA_PRINCIPAL_URL", "http://localhost:8000")
    
    # Logs
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def is_gemini_configured(cls):
        """Verifica se a API do Gemini está configurada"""
        return bool(cls.GEMINI_API_KEY and cls.GEMINI_API_KEY != "sua_chave_aqui")
    
    @classmethod
    def get_status(cls):
        """Retorna status da configuração"""
        return {
            "gemini_configured": cls.is_gemini_configured(),
            "sistema_principal_url": cls.SISTEMA_PRINCIPAL_URL,
            "port": cls.PORT,
            "host": cls.HOST
        }



