import React, { useState, useEffect } from 'react'
import { 
  BarChart3, 
  TrendingUp, 
  Clock, 
  Target, 
  AlertTriangle,
  CheckCircle,
  RefreshCw
} from 'lucide-react'
import { triagemAPI, utils } from '../services/api'

const DashboardPage = () => {
  const [estatisticas, setEstatisticas] = useState(null)
  const [historico, setHistorico] = useState(null)
  const [loading, setLoading] = useState(true)
  const [erro, setErro] = useState('')
  const [periodo, setPeriodo] = useState(7)

  const carregarDados = async () => {
    setLoading(true)
    setErro('')

    try {
      console.log('📊 Carregando dados do dashboard...')
      
      const [statsResponse, historicoResponse] = await Promise.all([
        triagemAPI.obterEstatisticas(periodo),
        triagemAPI.obterHistorico(1, 10)
      ])
      
      setEstatisticas(statsResponse)
      setHistorico(historicoResponse)
      
      console.log('✅ Dados carregados:', { statsResponse, historicoResponse })
      
    } catch (error) {
      console.error('❌ Erro ao carregar dados:', error)
      
      let mensagemErro = 'Erro desconhecido'
      
      if (utils.isConnectionError(error)) {
        mensagemErro = 'Servidor não está respondendo. Verifique se o backend está rodando.'
      } else if (utils.isServerError(error)) {
        mensagemErro = 'Erro interno do servidor. Tente novamente em alguns minutos.'
      } else {
        mensagemErro = utils.formatarErro(error)
      }
      
      setErro(mensagemErro)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    carregarDados()
  }, [periodo])

  const formatarData = (data) => {
    return new Date(data).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getCorPrioridade = (prioridade) => {
    switch (prioridade?.toLowerCase()) {
      case 'alta':
        return '#ef4444'
      case 'media':
        return '#f59e0b'
      case 'baixa':
        return '#10b981'
      default:
        return '#6b7280'
    }
  }

  const getIconPrioridade = (prioridade) => {
    switch (prioridade?.toLowerCase()) {
      case 'alta':
        return <AlertTriangle size={16} style={{ color: '#ef4444' }} />
      case 'media':
        return <Clock size={16} style={{ color: '#f59e0b' }} />
      case 'baixa':
        return <CheckCircle size={16} style={{ color: '#10b981' }} />
      default:
        return <Target size={16} />
    }
  }

  return (
    <div>
      {/* Header da Página */}
      <div className="flex justify-between items-center mb-3">
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: '700', marginBottom: '0.5rem' }}>
            📊 Dashboard de Triagem
          </h1>
          <p style={{ color: '#64748b', fontSize: '1.1rem' }}>
            Estatísticas e métricas do sistema de triagem
          </p>
        </div>
        
        <div className="flex gap-2">
          <select
            className="form-select"
            value={periodo}
            onChange={(e) => setPeriodo(parseInt(e.target.value))}
            style={{ width: 'auto', minWidth: '120px' }}
          >
            <option value={1}>Último dia</option>
            <option value={7}>Última semana</option>
            <option value={30}>Último mês</option>
            <option value={90}>Últimos 3 meses</option>
          </select>
          
          <button
            onClick={carregarDados}
            className="btn btn-secondary"
            disabled={loading}
          >
            <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
            Atualizar
          </button>
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          Carregando dados...
        </div>
      )}

      {/* Erro */}
      {erro && (
        <div className="card mb-3" style={{ borderColor: '#ef4444', backgroundColor: '#fef2f2' }}>
          <div className="flex items-center gap-2" style={{ color: '#dc2626' }}>
            <AlertTriangle size={20} />
            <strong>Erro:</strong> {erro}
          </div>
        </div>
      )}

      {/* Estatísticas Gerais */}
      {estatisticas && (
        <div className="card mb-3">
          <div className="card-header">
            <h3 className="card-title">📈 Resumo Geral ({estatisticas.periodo})</h3>
          </div>
          
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-number">
                {estatisticas.resumo_geral?.total_triagens_periodo || 0}
              </div>
              <div className="stat-label">Total de Triagens</div>
            </div>
            
            <div className="stat-card">
              <div className="stat-number">
                {estatisticas.resumo_geral?.media_triagens_dia?.toFixed(1) || '0.0'}
              </div>
              <div className="stat-label">Média por Dia</div>
            </div>
            
            <div className="stat-card">
              <div className="stat-number">
                {((estatisticas.resumo_geral?.taxa_sucesso || 0) * 100).toFixed(1)}%
              </div>
              <div className="stat-label">Taxa de Sucesso</div>
            </div>
            
            <div className="stat-card">
              <div className="stat-number">
                {estatisticas.resumo_geral?.categoria_mais_comum || 'N/A'}
              </div>
              <div className="stat-label">Categoria Mais Comum</div>
            </div>
          </div>
        </div>
      )}

      {/* Estatísticas Diárias */}
      {estatisticas && estatisticas.estatisticas && (
        <div className="card mb-3">
          <div className="card-header">
            <h3 className="card-title">📅 Estatísticas Diárias</h3>
          </div>
          
          <div className="overflow-x-auto">
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #e2e8f0' }}>
                  <th style={{ padding: '0.75rem', textAlign: 'left' }}>Data</th>
                  <th style={{ padding: '0.75rem', textAlign: 'center' }}>Triagens</th>
                  <th style={{ padding: '0.75rem', textAlign: 'center' }}>Com Solução</th>
                  <th style={{ padding: '0.75rem', textAlign: 'center' }}>Tempo Médio</th>
                  <th style={{ padding: '0.75rem', textAlign: 'center' }}>Prioridades</th>
                </tr>
              </thead>
              <tbody>
                {estatisticas.estatisticas.slice(0, 7).map((stat, index) => (
                  <tr key={index} style={{ borderBottom: '1px solid #f1f5f9' }}>
                    <td style={{ padding: '0.75rem' }}>
                      {new Date(stat.data).toLocaleDateString('pt-BR')}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                      {stat.total_triagens}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                      {stat.triagens_com_solucao}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                      {stat.tempo_medio_processamento?.toFixed(0)}ms
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                      <div className="flex gap-1 justify-center">
                        {Object.entries(stat.prioridades || {}).map(([prioridade, count]) => (
                          <span
                            key={prioridade}
                            className="result-badge badge-info"
                            style={{ fontSize: '0.7rem' }}
                          >
                            {prioridade}: {count}
                          </span>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Histórico Recente */}
      {historico && (
        <div className="card mb-3">
          <div className="card-header">
            <h3 className="card-title">🕒 Histórico Recente</h3>
            <span className="result-badge badge-info">
              {historico.total} total
            </span>
          </div>
          
          <div className="overflow-x-auto">
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #e2e8f0' }}>
                  <th style={{ padding: '0.75rem', textAlign: 'left' }}>Data</th>
                  <th style={{ padding: '0.75rem', textAlign: 'left' }}>Módulo</th>
                  <th style={{ padding: '0.75rem', textAlign: 'center' }}>Padrões</th>
                  <th style={{ padding: '0.75rem', textAlign: 'center' }}>Soluções</th>
                  <th style={{ padding: '0.75rem', textAlign: 'center' }}>Prioridade</th>
                  <th style={{ padding: '0.75rem', textAlign: 'center' }}>Feedback</th>
                </tr>
              </thead>
              <tbody>
                {historico.triagens.map((triagem, index) => (
                  <tr key={index} style={{ borderBottom: '1px solid #f1f5f9' }}>
                    <td style={{ padding: '0.75rem' }}>
                      {formatarData(triagem.data_triagem)}
                    </td>
                    <td style={{ padding: '0.75rem' }}>
                      {triagem.modulo || 'Não informado'}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                      {triagem.total_padroes}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                      {triagem.solucoes_geradas}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                      <div className="flex items-center justify-center gap-1">
                        {getIconPrioridade(triagem.prioridade_geral)}
                        <span style={{ color: getCorPrioridade(triagem.prioridade_geral) }}>
                          {triagem.prioridade_geral?.toUpperCase()}
                        </span>
                      </div>
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                      {triagem.teve_feedback ? (
                        <CheckCircle size={16} style={{ color: '#10b981' }} />
                      ) : (
                        <span style={{ color: '#6b7280' }}>-</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Informações Adicionais */}
      <div className="grid grid-2">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">📊 Categorias Mais Comuns</h3>
          </div>
          
          {estatisticas?.estatisticas?.[0]?.categorias_mais_comuns ? (
            <div>
              {estatisticas.estatisticas[0].categorias_mais_comuns.map((cat, index) => (
                <div key={index} className="flex justify-between items-center mb-2">
                  <span>{cat.categoria}</span>
                  <span className="result-badge badge-info">{cat.count}</span>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: '#6b7280' }}>Nenhum dado disponível</p>
          )}
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">🎯 Tipos de Problema</h3>
          </div>
          
          {estatisticas?.estatisticas?.[0]?.tipos_problema ? (
            <div>
              {Object.entries(estatisticas.estatisticas[0].tipos_problema).map(([tipo, count]) => (
                <div key={tipo} className="flex justify-between items-center mb-2">
                  <span>{tipo}</span>
                  <span className="result-badge badge-info">{count}</span>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: '#6b7280' }}>Nenhum dado disponível</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default DashboardPage
