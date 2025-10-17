import React, { useState } from 'react'
import { 
  CheckCircle, 
  AlertTriangle, 
  Info, 
  Copy, 
  ThumbsUp, 
  ThumbsDown,
  Clock,
  Target,
  Code,
  Database
} from 'lucide-react'

const TriagemResult = ({ resultado, onFeedback, loading = false }) => {
  const [feedbackEnviado, setFeedbackEnviado] = useState(false)
  const [feedback, setFeedback] = useState({
    solucao_util: null,
    comentario: '',
    nota: 5
  })

  if (!resultado) return null

  const { 
    padroes_encontrados = [], 
    analise_ia = {}, 
    solucoes_sugeridas = [], 
    resumo = {},
    modo_mock = false,
    tempo_processamento_ms = 0
  } = resultado

  const copiarTexto = (texto) => {
    navigator.clipboard.writeText(texto)
    // Aqui você pode adicionar uma notificação de sucesso
  }

  const enviarFeedback = (util) => {
    setFeedback({ ...feedback, solucao_util: util })
    
    if (onFeedback && resultado.triagem_id) {
      onFeedback(resultado.triagem_id, {
        ...feedback,
        solucao_util: util
      })
      setFeedbackEnviado(true)
    }
  }

  const getPrioridadeIcon = (prioridade) => {
    switch (prioridade?.toLowerCase()) {
      case 'alta':
        return <AlertTriangle size={16} style={{ color: '#ef4444' }} />
      case 'media':
        return <Info size={16} style={{ color: '#f59e0b' }} />
      case 'baixa':
        return <CheckCircle size={16} style={{ color: '#10b981' }} />
      default:
        return <Info size={16} />
    }
  }

  const getPrioridadeClass = (prioridade) => {
    switch (prioridade?.toLowerCase()) {
      case 'alta':
        return 'prioridade-alta'
      case 'media':
        return 'prioridade-media'
      case 'baixa':
        return 'prioridade-baixa'
      default:
        return 'prioridade-media'
    }
  }

  return (
    <div className="result-container">
      {/* Resumo da Triagem */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">📊 Resumo da Triagem</h3>
            <p className="card-subtitle">
              {resumo.resumo || 'Análise concluída com sucesso'}
            </p>
          </div>
          <div className="flex gap-2">
            {modo_mock && (
              <span className="result-badge badge-warning">
                Modo Demonstração
              </span>
            )}
            <span className={`result-badge badge-${resumo.prioridade_geral === 'alta' ? 'error' : 'info'}`}>
              {resumo.prioridade_geral?.toUpperCase() || 'MEDIA'}
            </span>
          </div>
        </div>

        <div className="grid grid-3">
          <div className="stat-card">
            <div className="stat-number">{padroes_encontrados.length}</div>
            <div className="stat-label">Padrões Detectados</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{solucoes_sugeridas.length}</div>
            <div className="stat-label">Soluções Geradas</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{tempo_processamento_ms}ms</div>
            <div className="stat-label">Tempo de Processamento</div>
          </div>
        </div>
      </div>

      {/* Padrões Detectados */}
      {padroes_encontrados.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">🔍 Padrões Detectados</h3>
          </div>
          <div className="grid grid-2">
            {padroes_encontrados.map((padrao, index) => (
              <div key={index} className="solucao-item">
                <div className="solucao-header">
                  <span className="solucao-categoria">
                    {padrao.tipo?.replace('_', ' ').toUpperCase()}
                  </span>
                  <span className="result-badge badge-info">
                    {(padrao.confianca * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="solucao-descricao">
                  <strong>Palavra-chave:</strong> "{padrao.palavra_chave}"
                </div>
                <div className="solucao-descricao">
                  <strong>Padrão:</strong> {padrao.padrao_id}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Análise da IA */}
      {analise_ia && !analise_ia.erro && (
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">🤖 Análise Inteligente</h3>
          </div>
          
          {analise_ia.tipo_problema && (
            <div className="mb-2">
              <strong>Tipo de Problema:</strong> {analise_ia.tipo_problema}
            </div>
          )}
          
          {analise_ia.categoria_detalhada && (
            <div className="mb-2">
              <strong>Categoria:</strong> {analise_ia.categoria_detalhada}
            </div>
          )}
          
          {analise_ia.diagnostico && (
            <div className="mb-2">
              <strong>Diagnóstico:</strong> {analise_ia.diagnostico}
            </div>
          )}
          
          {analise_ia.tempo_estimado && (
            <div className="mb-2 flex items-center">
              <Clock size={16} style={{ marginRight: '8px' }} />
              <strong>Tempo estimado:</strong> {analise_ia.tempo_estimado}
            </div>
          )}
          
          {analise_ia.recursos_necessarios && (
            <div className="mb-2">
              <strong>Recursos necessários:</strong> {analise_ia.recursos_necessarios.join(', ')}
            </div>
          )}
          
          {analise_ia.observacoes && (
            <div className="mb-2">
              <strong>Observações:</strong> {analise_ia.observacoes}
            </div>
          )}
        </div>
      )}

      {/* Soluções Sugeridas */}
      {solucoes_sugeridas.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">💡 Soluções Sugeridas</h3>
            <span className="result-badge badge-success">
              {solucoes_sugeridas.length} solução(ões)
            </span>
          </div>

          {solucoes_sugeridas.map((solucao, index) => (
            <div key={index} className="solucao-item">
              <div className="solucao-header">
                <span className="solucao-categoria">
                  {solucao.categoria}
                </span>
                <div className="flex items-center gap-2">
                  <span className={`solucao-prioridade ${getPrioridadeClass(solucao.prioridade)}`}>
                    {getPrioridadeIcon(solucao.prioridade)}
                    {solucao.prioridade?.toUpperCase()}
                  </span>
                  <span className="result-badge badge-info">
                    {(solucao.confianca * 100).toFixed(0)}%
                  </span>
                </div>
              </div>

              <div className="solucao-descricao">
                {solucao.solucao}
              </div>

              {solucao.codigo_sugerido && (
                <div className="mb-2">
                  <div className="flex items-center justify-between mb-1">
                    <strong className="flex items-center">
                      <Code size={16} style={{ marginRight: '8px' }} />
                      Código Sugerido:
                    </strong>
                    <button
                      onClick={() => copiarTexto(solucao.codigo_sugerido)}
                      className="btn btn-secondary"
                      style={{ padding: '0.25rem 0.5rem', fontSize: '0.8rem' }}
                    >
                      <Copy size={14} />
                      Copiar
                    </button>
                  </div>
                  <pre className="solucao-codigo">
                    {solucao.codigo_sugerido}
                  </pre>
                </div>
              )}

              {solucao.script_sql_sugerido && (
                <div className="mb-2">
                  <div className="flex items-center justify-between mb-1">
                    <strong className="flex items-center">
                      <Database size={16} style={{ marginRight: '8px' }} />
                      Script SQL:
                    </strong>
                    <button
                      onClick={() => copiarTexto(solucao.script_sql_sugerido)}
                      className="btn btn-secondary"
                      style={{ padding: '0.25rem 0.5rem', fontSize: '0.8rem' }}
                    >
                      <Copy size={14} />
                      Copiar
                    </button>
                  </div>
                  <pre className="solucao-sql">
                    {solucao.script_sql_sugerido}
                  </pre>
                </div>
              )}

              {solucao.scripts_sugeridos && solucao.scripts_sugeridos.length > 0 && (
                <div className="mb-2">
                  <strong className="flex items-center mb-1">
                    <Database size={16} style={{ marginRight: '8px' }} />
                    Scripts SQL Adicionais:
                  </strong>
                  {solucao.scripts_sugeridos.map((script, scriptIndex) => (
                    <div key={scriptIndex} className="mb-1">
                      <div className="flex items-center justify-between">
                        <small>Script {scriptIndex + 1}:</small>
                        <button
                          onClick={() => copiarTexto(script)}
                          className="btn btn-secondary"
                          style={{ padding: '0.25rem 0.5rem', fontSize: '0.8rem' }}
                        >
                          <Copy size={14} />
                          Copiar
                        </button>
                      </div>
                      <pre className="solucao-sql" style={{ fontSize: '0.8rem' }}>
                        {script}
                      </pre>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Feedback */}
      {resultado.triagem_id && !feedbackEnviado && (
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">👍 Feedback</h3>
            <p className="card-subtitle">
              Ajude-nos a melhorar a qualidade das triagens
            </p>
          </div>
          
          <div className="flex gap-2">
            <button
              onClick={() => enviarFeedback(true)}
              className="btn btn-success"
              disabled={loading}
            >
              <ThumbsUp size={16} />
              Útil
            </button>
            <button
              onClick={() => enviarFeedback(false)}
              className="btn btn-danger"
              disabled={loading}
            >
              <ThumbsDown size={16} />
              Não Útil
            </button>
          </div>
        </div>
      )}

      {feedbackEnviado && (
        <div className="card">
          <div className="text-center">
            <CheckCircle size={32} style={{ color: '#10b981', marginBottom: '1rem' }} />
            <h3>Obrigado pelo feedback!</h3>
            <p>Sua avaliação nos ajuda a melhorar o sistema.</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default TriagemResult
