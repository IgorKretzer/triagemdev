import React, { useState } from 'react'
import { FileText, Send, Loader } from 'lucide-react'

const TriagemInput = ({ onAnalisar, loading }) => {
  const [chamadoTexto, setChamadoTexto] = useState('')
  const [modulo, setModulo] = useState('')

  const modulosSponte = [
    'CADASTROS',
    'PEDAGÓGICO', 
    'FINANCEIRO',
    'RELATÓRIOS',
    'GERENCIAL',
    'UTILITÁRIOS'
  ]

  const handleSubmit = (e) => {
    e.preventDefault()
    if (chamadoTexto.trim() && modulo) {
      onAnalisar(chamadoTexto.trim(), modulo)
    }
  }

  const handleClear = () => {
    setChamadoTexto('')
    setModulo('')
  }

  return (
    <div className="card fade-in">
      <div className="card-header">
        <h2 className="card-title">
          <FileText size={24} />
          Análise por Texto
        </h2>
        <p className="card-subtitle">Cole o texto do chamado para análise automática</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="form-group">
          <label className="form-label">Módulo Sponte:</label>
          <select 
            value={modulo}
            onChange={(e) => setModulo(e.target.value)}
            className="form-input"
            required
            disabled={loading}
          >
            <option value="">Selecione um módulo</option>
            {modulosSponte.map(mod => (
              <option key={mod} value={mod}>{mod}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Texto do Chamado:</label>
          <textarea
            value={chamadoTexto}
            onChange={(e) => setChamadoTexto(e.target.value)}
            className="form-textarea"
            placeholder="Cole aqui o texto completo do chamado que você deseja analisar..."
            rows={8}
            required
            disabled={loading}
          />
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
            disabled={loading || !chamadoTexto.trim() || !modulo}
          >
            {loading ? (
              <>
                <Loader className="loading" />
                Analisando...
              </>
            ) : (
              <>
                <Send size={20} />
                Analisar Chamado
              </>
            )}
          </button>
        </div>
      </form>

      <div className="mt-4 p-3 bg-tertiary rounded-lg">
        <h4 className="mb-2">💡 Dica:</h4>
        <p className="text-sm text-secondary">
          Para melhores resultados, inclua o texto completo do chamado, incluindo mensagens de erro, 
          descrição do problema e contexto da situação.
        </p>
      </div>
    </div>
  )
}

export default TriagemInput