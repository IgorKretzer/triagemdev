import React, { useState } from 'react'
import { Ticket, Search, Loader, AlertCircle } from 'lucide-react'

const TicketInput = ({ onBuscarTicket, loading }) => {
  const [ticketNumero, setTicketNumero] = useState('')
  const [erro, setErro] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    setErro('')
    
    if (!ticketNumero.trim()) {
      setErro('Por favor, digite o número do ticket')
      return
    }

    if (!/^\d+$/.test(ticketNumero.trim())) {
      setErro('O número do ticket deve conter apenas números')
      return
    }

    onBuscarTicket(ticketNumero.trim())
  }

  const handleClear = () => {
    setTicketNumero('')
    setErro('')
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit(e)
    }
  }

  return (
    <div className="card fade-in">
      <div className="card-header">
        <h2 className="card-title">
          <Ticket size={24} />
          Análise por Ticket
        </h2>
        <p className="card-subtitle">Digite o número do ticket para buscar e analisar automaticamente</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="form-group">
          <label className="form-label">Número do Ticket:</label>
          <div className="relative">
            <input
              type="text"
              value={ticketNumero}
              onChange={(e) => setTicketNumero(e.target.value)}
              onKeyPress={handleKeyPress}
              className="form-input"
              placeholder="Ex: 1234567"
              disabled={loading}
              autoFocus
            />
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              {loading ? <Loader className="loading" /> : <Search size={20} className="text-secondary" />}
            </div>
          </div>
          {erro && (
            <div className="alert alert-danger mt-2">
              <AlertCircle size={16} />
              {erro}
            </div>
          )}
        </div>

        <div className="flex gap-3 justify-end">
          <button
            type="button"
            onClick={handleClear}
            className="btn btn-secondary"
            disabled={loading}
          >
            Limpar
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !ticketNumero.trim()}
          >
            {loading ? (
              <>
                <Loader className="loading" />
                Buscando...
              </>
            ) : (
              <>
                <Search size={20} />
                Buscar e Analisar
              </>
            )}
          </button>
        </div>
      </form>

      <div className="mt-4 p-3 bg-tertiary rounded-lg">
        <h4 className="mb-2">💡 Como funciona:</h4>
        <ol className="text-sm text-secondary space-y-1">
          <li>1. Digite o número do ticket do Movidesk</li>
          <li>2. O sistema busca o chamado no sistema principal</li>
          <li>3. Analisa automaticamente o conteúdo</li>
          <li>4. Retorna soluções técnicas sugeridas</li>
        </ol>
      </div>

      <div className="mt-3 p-3 bg-info/10 border border-info/20 rounded-lg">
        <h4 className="mb-2 text-info">🔗 Integração:</h4>
        <p className="text-sm text-secondary">
          Este modo se conecta automaticamente com o sistema principal de chamados para 
          recuperar o texto gerado pela IA e fazer a triagem técnica.
        </p>
      </div>
    </div>
  )
}

export default TicketInput