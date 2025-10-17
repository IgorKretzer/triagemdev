import React, { useState } from 'react'
import { AlertCircle, CheckCircle, Ticket, FileText } from 'lucide-react'
import TriagemInput from '../components/TriagemInput'
import TicketInput from '../components/TicketInput'
import TriagemResult from '../components/TriagemResult'
import { triagemAPI, utils } from '../services/api'

const HomePage = () => {
  const [resultado, setResultado] = useState(null)
  const [loading, setLoading] = useState(false)
  const [erro, setErro] = useState('')
  const [modo, setModo] = useState('ticket') // 'ticket' ou 'texto'

  const handleAnalisar = async (chamadoTexto, modulo) => {
    setLoading(true)
    setErro('')
    setResultado(null)

    try {
      console.log('🔍 Iniciando análise de triagem...')
      const resultado = await triagemAPI.analisarChamado(chamadoTexto, modulo)
      
      console.log('✅ Triagem concluída:', resultado)
      setResultado(resultado)
      
    } catch (error) {
      console.error('❌ Erro na triagem:', error)
      
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

  const handleBuscarTicket = async (ticketNumero) => {
    setLoading(true)
    setErro('')
    setResultado(null)

    try {
      console.log(`🎫 Buscando ticket: ${ticketNumero}`)
      const resultado = await triagemAPI.triagemPorTicket(ticketNumero)
      
      console.log('✅ Triagem por ticket concluída:', resultado)
      setResultado(resultado)
      
    } catch (error) {
      console.error('❌ Erro na triagem por ticket:', error)
      
      let mensagemErro = 'Erro desconhecido'
      
      if (error.response?.status === 404) {
        mensagemErro = `Ticket ${ticketNumero} não encontrado no sistema principal. Verifique se o ticket foi analisado no sistema de chamados.`
      } else if (utils.isConnectionError(error)) {
        mensagemErro = 'Não foi possível conectar com o sistema principal. Verifique se ambos os sistemas estão rodando.'
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

  const handleFeedback = async (triagemId, feedback) => {
    try {
      console.log('📝 Enviando feedback...')
      await triagemAPI.registrarFeedback(triagemId, feedback)
      console.log('✅ Feedback enviado')
    } catch (error) {
      console.error('❌ Erro ao enviar feedback:', error)
      // Não mostra erro para o usuário, apenas loga
    }
  }

  return (
    <div className="home-page fade-in">
      <div className="card text-center mb-4">
        <div className="card-header">
          <h1 className="card-title">🎯 Sistema de Triagem IA</h1>
          <p className="card-subtitle">Análise inteligente de chamados para correções automáticas</p>
        </div>
      </div>

      <div className="card mb-4">
        <div className="card-header">
          <h2 className="card-title">Escolha o modo de análise:</h2>
        </div>
        <div className="flex gap-3 justify-center">
          <button 
            className={`btn ${modo === 'ticket' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setModo('ticket')}
          >
            <Ticket size={20} />
            Por Ticket
          </button>
          <button 
            className={`btn ${modo === 'texto' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setModo('texto')}
          >
            <FileText size={20} />
            Por Texto
          </button>
        </div>
      </div>

      {modo === 'ticket' ? (
        <TicketInput 
          onBuscarTicket={handleBuscarTicket}
          loading={loading}
        />
      ) : (
        <TriagemInput 
          onAnalisar={handleAnalisar}
          loading={loading}
        />
      )}

      {resultado && (
        <div className="card slide-in">
          <div className="card-header">
            <h2 className="card-title">📊 Resultado da Análise</h2>
          </div>
          
          <div className="flex justify-between items-center mb-3">
            <span className="text-secondary">Ticket: {resultado.ticket_numero}</span>
            <span className={`btn btn-sm ${resultado.status.toLowerCase() === 'sucesso' ? 'btn-success' : 'btn-warning'}`}>
              {resultado.status}
            </span>
          </div>
          
          {resultado.chamado_original && (
            <div className="mb-4">
              <h3 className="mb-2">📋 Chamado Original:</h3>
              <div className="bg-tertiary p-3 rounded-lg">
                <p>{resultado.chamado_original}</p>
              </div>
            </div>
          )}
          
          <div className="grid grid-2 gap-4">
            <div>
              <h3 className="mb-2">⚠️ Problemas Identificados:</h3>
              <div className="space-y-2">
                {resultado.problemas_identificados?.map((problema, index) => (
                  <div key={index} className="alert alert-warning">
                    <strong>{problema.tipo}:</strong> {problema.descricao}
                  </div>
                ))}
              </div>
            </div>
            
            <div>
              <h3 className="mb-2">💡 Soluções Sugeridas:</h3>
              <div className="space-y-3">
                {resultado.solucoes_sugeridas?.map((solucao, index) => (
                  <div key={index} className="alert alert-info">
                    <strong>{solucao.tipo}:</strong>
                    <pre className="mt-2 p-2 bg-tertiary rounded text-sm overflow-x-auto">{solucao.codigo}</pre>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          <div className="text-center mt-4">
            <button onClick={() => handleFeedback(resultado.id, 'positivo')} className="btn btn-primary">
              👍 Avaliar Resultado
            </button>
          </div>
        </div>
      )}

      {erro && (
        <div className="alert alert-danger">
          <h3>❌ Erro</h3>
          <p>{erro}</p>
        </div>
      )}
    </div>
  )
}

export default HomePage