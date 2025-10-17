# -*- coding: utf-8 -*-
import firebase_admin
from firebase_admin import credentials, firestore
import os
from typing import Optional
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class FirebaseConfig:
    _instance = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseConfig, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialize_firebase()
            self._initialized = True
    
    def _initialize_firebase(self):
        """Inicializa o Firebase Admin SDK"""
        try:
            # Verifica se já existe uma app do Firebase
            if not firebase_admin._apps:
                # Opção 1: Usar variável de ambiente com path do arquivo de credenciais
                credentials_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
                
                if credentials_path and os.path.exists(credentials_path):
                    # Usar arquivo de credenciais
                    cred = credentials.Certificate(credentials_path)
                    firebase_admin.initialize_app(cred)
                else:
                    # Opção 2: Usar variáveis de ambiente (para deploy em produção)
                    firebase_config = {
                        "type": os.getenv('FIREBASE_TYPE', 'service_account'),
                        "project_id": os.getenv('FIREBASE_PROJECT_ID'),
                        "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
                        "private_key": os.getenv('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n'),
                        "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
                        "client_id": os.getenv('FIREBASE_CLIENT_ID'),
                        "auth_uri": os.getenv('FIREBASE_AUTH_URI', 'https://accounts.google.com/o/oauth2/auth'),
                        "token_uri": os.getenv('FIREBASE_TOKEN_URI', 'https://oauth2.googleapis.com/token'),
                        "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
                        "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL')
                    }
                    
                    # Verifica se as variáveis essenciais estão presentes
                    required_vars = ['project_id', 'private_key', 'client_email']
                    if all(firebase_config.get(var) for var in required_vars):
                        cred = credentials.Certificate(firebase_config)
                        firebase_admin.initialize_app(cred)
                    else:
                        print("⚠️  Firebase não configurado - usando modo local")
                        missing_vars = [var for var in required_vars if not firebase_config.get(var)]
                        print(f"Variáveis faltando: {missing_vars}")
                        self._db = None
                        return
            
            self._db = firestore.client()
            print("✅ Firebase configurado com sucesso!")
            
        except Exception as e:
            print(f"⚠️  Erro ao inicializar Firebase: {e}")
            print("💡 Configure as variáveis do Firebase no arquivo .env")
            self._db = None
    
    @property
    def db(self):
        """Retorna a instância do Firestore"""
        if self._db is None:
            self._initialize_firebase()
        return self._db
    
    def is_configured(self) -> bool:
        """Verifica se o Firebase está configurado"""
        return self._db is not None

# Instância global do Firebase
firebase_config = FirebaseConfig()
