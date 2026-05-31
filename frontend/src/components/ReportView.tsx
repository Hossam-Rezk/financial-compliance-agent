import { useState } from 'react'
import { AlertTriangle, Info, ShieldAlert, ChevronDown, ChevronUp } from 'lucide-react'

interface Props {
  report: any
}

export default function ReportView({ report }: Props) {
  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'Critical': return 'var(--danger)'
      case 'High': return 'var(--warning)'
      case 'Medium': return 'var(--info)'
      case 'Low': return 'var(--success)'
      default: return 'var(--text-secondary)'
    }
  }

  const getRiskIcon = (risk: string) => {
    switch (risk) {
      case 'Critical': return <ShieldAlert size={24} color="var(--danger)" />
      case 'High': return <AlertTriangle size={24} color="var(--warning)" />
      case 'Medium': return <Info size={24} color="var(--info)" />
      default: return <Info size={24} color="var(--text-secondary)" />
    }
  }

  return (
    <div className="animate-fade-in flex-col gap-6">
      <div className="flex gap-6">
        <div className="glass-panel flex-col justify-center items-center gap-2" style={{ padding: '2rem', flex: 1 }}>
          <h3 style={{ color: 'var(--text-secondary)' }}>Overall Risk</h3>
          <div className="flex items-center gap-2">
            {getRiskIcon(report.overall_risk)}
            <span style={{ fontSize: '2rem', fontWeight: 700, color: getRiskColor(report.overall_risk) }}>
              {report.overall_risk}
            </span>
          </div>
        </div>

        <div className="glass-panel flex-col gap-4" style={{ padding: '2rem', flex: 2 }}>
          <h3 style={{ color: 'var(--text-secondary)' }}>Executive Summary</h3>
          <p style={{ lineHeight: 1.6 }}>{report.executive_summary}</p>
        </div>
      </div>

      <div className="glass-panel flex-col gap-4" style={{ padding: '2rem' }}>
        <div className="flex justify-between items-center border-b" style={{ paddingBottom: '1rem', borderBottom: '1px solid var(--glass-border)' }}>
          <h3>Findings ({report.total_findings})</h3>
          <div className="flex gap-4">
            <span style={{ color: 'var(--danger)' }}>Critical: {report.severity_summary.Critical}</span>
            <span style={{ color: 'var(--warning)' }}>High: {report.severity_summary.High}</span>
            <span style={{ color: 'var(--info)' }}>Medium: {report.severity_summary.Medium}</span>
            <span style={{ color: 'var(--success)' }}>Low: {report.severity_summary.Low}</span>
          </div>
        </div>

        <div className="flex-col gap-4" style={{ marginTop: '1rem' }}>
          {report.findings.length === 0 ? (
            <div className="flex-col items-center gap-2" style={{ padding: '3rem', color: 'var(--text-tertiary)' }}>
              <ShieldAlert size={48} />
              <p>No violations found.</p>
            </div>
          ) : (
            report.findings.map((finding: any, idx: number) => (
              <FindingCard key={idx} finding={finding} color={getRiskColor(finding.severity)} />
            ))
          )}
        </div>
      </div>
    </div>
  )
}

function FindingCard({ finding, color }: { finding: any, color: string }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div className="glass-card" style={{ overflow: 'hidden' }}>
      <div 
        className="flex justify-between items-center" 
        style={{ padding: '1.5rem', cursor: 'pointer', borderLeft: `4px solid ${color}` }}
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex-col gap-2" style={{ flex: 1 }}>
          <div className="flex items-center gap-4">
            <span style={{ background: color, color: '#000', padding: '2px 8px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 600 }}>
              {finding.severity}
            </span>
            <h4 style={{ margin: 0 }}>{finding.rule}</h4>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>{finding.rationale}</p>
        </div>
        <div>
          {expanded ? <ChevronUp /> : <ChevronDown />}
        </div>
      </div>
      
      {expanded && (
        <div style={{ padding: '1.5rem', background: 'rgba(0,0,0,0.2)', borderTop: '1px solid var(--glass-border)' }}>
          <h5 style={{ color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>Document Excerpt (Chunk {finding.chunk_order})</h5>
          <p style={{ fontFamily: 'monospace', fontSize: '0.85rem', color: 'var(--text-primary)', whiteSpace: 'pre-wrap', lineHeight: 1.5 }}>
            {finding.chunk_text}
          </p>
          
          <h5 style={{ color: 'var(--text-secondary)', marginTop: '1rem', marginBottom: '0.5rem' }}>AI Finding</h5>
          <p style={{ fontSize: '0.9rem' }}>{finding.finding}</p>
        </div>
      )}
    </div>
  )
}
