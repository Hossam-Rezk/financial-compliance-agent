import { useState } from 'react'
import { Search, Loader } from 'lucide-react'

interface Props {
  projectId: string
  onReportGenerated: (report: any) => void
}

export default function AnalyzeSection({ projectId, onReportGenerated }: Props) {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAnalyze = async () => {
    if (!query.trim()) return
    
    setLoading(true)
    setError('')
    
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/nlp/analyze/${projectId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, top_k: 5 })
      })
      
      const data = await res.json()
      if (!res.ok) throw new Error(data.message || 'Analysis failed')
      
      onReportGenerated(data.report)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="glass-panel flex-col gap-4" style={{ padding: '2rem' }}>
      <h3>Generate Compliance Report</h3>
      <p style={{ color: 'var(--text-secondary)' }}>
        Ask a specific question or request a general compliance audit against the rule set.
      </p>
      
      <div className="flex gap-4">
        <input 
          type="text" 
          className="input-field" 
          placeholder="e.g. Does this document violate any data privacy rules?" 
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
          disabled={loading}
        />
        <button 
          className="btn btn-primary" 
          onClick={handleAnalyze}
          disabled={loading || !query.trim()}
        >
          {loading ? <Loader className="animate-spin" size={18} /> : <Search size={18} />}
          {loading ? 'Analyzing (Takes 1-2m)...' : 'Analyze'}
        </button>
      </div>
      
      {error && <p style={{ color: 'var(--danger)' }}>{error}</p>}
    </div>
  )
}
