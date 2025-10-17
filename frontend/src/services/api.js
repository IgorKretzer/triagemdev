import axios from 'axios'

// Configuração base da API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para logs
api.interceptors.request.use(
  (config) => {
    console.log(`🌐 API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('❌ API Request Error:', error)
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// ============================================
// API DE TRIAGEM
// ============================================

export const triagemAPI = {
  // Analisar chamado
  async analisarChamado(chamadoTexto, modulo = null) {
    const response = await api.post('/api/triagem/analisar', {
      chamado_texto: chamadoTexto,
      modulo: modulo
    })
    return response.data
  },

  // Registrar feedback
  async registrarFeedback(triagemId, feedback) {
    const response = await api.post('/api/triagem/feedback', {
      triagem_id: triagemId,
      ...feedback
    })
    return response.data
  },

  // Obter estatísticas
  async obterEstatisticas(dias = 7, categoria = null) {
    const params = new URLSearchParams()
    if (dias) params.append('dias', dias)
    if (categoria) params.append('categoria', categoria)
    
    const response = await api.get(`/api/triagem/estatisticas?${params}`)
    return response.data
  },

  // Obter histórico
  async obterHistorico(pagina = 1, porPagina = 20, modulo = null) {
    const params = new URLSearchParams()
    params.append('pagina', pagina)
    params.append('por_pagina', porPagina)
    if (modulo) params.append('modulo', modulo)
    
    const response = await api.get(`/api/triagem/historico?${params}`)
    return response.data
  },

  // Listar padrões
  async listarPadroes() {
    const response = await api.get('/api/triagem/padroes')
    return response.data
  },

  // Obter base de conhecimento
  async obterBaseConhecimento() {
    const response = await api.get('/api/triagem/base-conhecimento')
    return response.data
  },

  // Health check
  async healthCheck() {
    const response = await api.get('/health')
    return response.data
  },

  // ============================================
  // INTEGRAÇÃO COM SISTEMA PRINCIPAL
  // ============================================

  // Triagem por ticket (busca no sistema principal)
  async triagemPorTicket(ticketNumero) {
    const response = await api.post(`/api/triagem/ticket/${ticketNumero}`)
    return response.data
  },

  // Buscar chamado no sistema principal
  async buscarChamadoSistemaPrincipal(ticketNumero) {
    const response = await api.get(`/api/triagem/buscar-chamado/${ticketNumero}`)
    return response.data
  },

  // Verificar status do sistema principal
  async verificarStatusSistemaPrincipal() {
    const response = await api.get('/api/triagem/sistema-principal/status')
    return response.data
  },

  // Obter análises recentes do sistema principal
  async obterAnalisesRecentesSistemaPrincipal(limite = 10) {
    const response = await api.get(`/api/triagem/sistema-principal/analises-recentes?limite=${limite}`)
    return response.data
  }
}

// ============================================
// API DE INTEGRAÇÃO (Sistema Existente)
// ============================================

export const integracaoAPI = {
  // Triagem após análise do sistema existente
  async triagemAposAnalise(analiseId, chamadoTexto, modulo, ticketNumero) {
    const response = await api.post('/api/integracao/triagem-chamado', {
      analise_id: analiseId,
      chamado_texto: chamadoTexto,
      modulo: modulo,
      ticket_numero: ticketNumero
    })
    return response.data
  }
}

// ============================================
// UTILITÁRIOS
// ============================================

export const utils = {
  // Formatar erro da API
  formatarErro(error) {
    if (error.response?.data?.detail) {
      return error.response.data.detail
    }
    if (error.response?.data?.message) {
      return error.response.data.message
    }
    if (error.message) {
      return error.message
    }
    return 'Erro desconhecido'
  },

  // Verificar se é erro de conexão
  isConnectionError(error) {
    return error.code === 'ECONNREFUSED' || 
           error.message.includes('Network Error') ||
           error.message.includes('timeout')
  },

  // Verificar se é erro de servidor
  isServerError(error) {
    return error.response?.status >= 500
  },

  // Verificar se é erro de cliente
  isClientError(error) {
    return error.response?.status >= 400 && error.response?.status < 500
  }
}

export default api
