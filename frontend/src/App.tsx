import { useState } from 'react'
import { ShieldCheck, UploadCloud, MessageSquare, FileText } from 'lucide-react'
import UploadSection from './components/UploadSection'
import AnalyzeSection from './components/AnalyzeSection'
import ReportView from './components/ReportView'
import Chatbot from './components/Chatbot'

function App() {
  const [projectId, setProjectId] = useState<string | null>(null)
  const [report, setReport] = useState<any>(null)
  const [activeTab, setActiveTab] = useState<'upload' | 'analyze' | 'chat'>('upload')

  return (
    <div className="container flex-col gap-6">
      <header className="flex items-center justify-between glass-panel" style={{ padding: '20px', marginBottom: '2rem' }}>
        <div className="flex items-center gap-4">
          <ShieldCheck size={32} color="var(--accent-primary)" />
          <div>
            <h1 style={{ fontSize: '1.5rem', margin: 0 }}>Financial Compliance Agent</h1>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>AI-Powered RAG Compliance Pipeline</p>
          </div>
        </div>
        {projectId && (
          <div className="flex items-center gap-2" style={{ background: 'var(--bg-tertiary)', padding: '8px 16px', borderRadius: 'var(--radius-sm)' }}>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-tertiary)' }}>Active Project:</span>
            <span style={{ fontWeight: 600, color: 'var(--accent-primary)' }}>{projectId}</span>
          </div>
        )}
      </header>

      <div className="flex gap-4" style={{ marginBottom: '2rem' }}>
        <button 
          className={`btn ${activeTab === 'upload' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setActiveTab('upload')}
        >
          <UploadCloud size={18} /> Upload Data
        </button>
        <button 
          className={`btn ${activeTab === 'analyze' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setActiveTab('analyze')}
          disabled={!projectId}
        >
          <FileText size={18} /> Generate Report
        </button>
        <button 
          className={`btn ${activeTab === 'chat' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setActiveTab('chat')}
          disabled={!projectId}
        >
          <MessageSquare size={18} /> Chat Assistant
        </button>
      </div>

      <main className="animate-fade-in">
        {activeTab === 'upload' && (
          <UploadSection onProjectCreated={(id) => { setProjectId(id); setActiveTab('analyze'); }} />
        )}
        
        {activeTab === 'analyze' && (
          <div className="flex-col gap-6">
            <AnalyzeSection projectId={projectId!} onReportGenerated={setReport} />
            {report && <ReportView report={report} />}
          </div>
        )}

        {activeTab === 'chat' && (
          <Chatbot projectId={projectId!} />
        )}
      </main>
    </div>
  )
}

export default App
