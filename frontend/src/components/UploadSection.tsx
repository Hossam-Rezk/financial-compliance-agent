import { useState, useRef } from 'react'
import { Upload, File, Loader, CheckCircle2 } from 'lucide-react'

interface Props {
  onProjectCreated: (projectId: string) => void
}

export default function UploadSection({ onProjectCreated }: Props) {
  const [file, setFile] = useState<File | null>(null)
  const [projectId, setProjectId] = useState<string>('')
  const [status, setStatus] = useState<'idle' | 'uploading' | 'processing' | 'success' | 'error'>('idle')
  const [errorMsg, setErrorMsg] = useState<string>('')
  
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0])
    }
  }

  const generateProjectId = () => {
    return 'proj_' + Math.random().toString(36).substring(2, 9)
  }

  const handleUploadAndProcess = async () => {
    if (!file) return
    
    let currentProjectId = projectId
    if (!currentProjectId) {
      currentProjectId = generateProjectId()
      setProjectId(currentProjectId)
    }

    try {
      setStatus('uploading')
      setErrorMsg('')
      
      const formData = new FormData()
      formData.append('file', file)
      
      const uploadRes = await fetch(`http://127.0.0.1:8000/api/v1/data/upload/${currentProjectId}`, {
        method: 'POST',
        body: formData,
      })
      
      if (!uploadRes.ok) throw new Error('Upload failed')
      const uploadData = await uploadRes.json()
      
      setStatus('processing')
      
      const processRes = await fetch(`http://127.0.0.1:8000/api/v1/data/process/${currentProjectId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          file_name: uploadData.file_name,
          chunk_size: 1000,
          overlap_size: 200
        })
      })
      
      if (!processRes.ok) throw new Error('Processing failed')
      
      setStatus('success')
      setTimeout(() => {
        onProjectCreated(currentProjectId)
      }, 1500)
      
    } catch (err: any) {
      setStatus('error')
      setErrorMsg(err.message || 'An error occurred')
    }
  }

  return (
    <div className="glass-panel flex-col items-center gap-6" style={{ padding: '3rem', maxWidth: '600px', margin: '0 auto' }}>
      <div className="flex-col items-center gap-2">
        <h2>Upload Document</h2>
        <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
          Upload your financial documents (PDF/TXT) to begin the compliance analysis process.
        </p>
      </div>

      <div 
        className="glass-card flex-col items-center justify-center pulse-animation" 
        style={{ width: '100%', padding: '3rem', borderStyle: 'dashed', cursor: 'pointer' }}
        onClick={() => fileInputRef.current?.click()}
      >
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileChange} 
          style={{ display: 'none' }} 
          accept=".pdf,.txt"
        />
        {file ? (
          <div className="flex-col items-center gap-2">
            <File size={48} color="var(--accent-primary)" />
            <span style={{ fontWeight: 500 }}>{file.name}</span>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)' }}>{(file.size / 1024 / 1024).toFixed(2)} MB</span>
          </div>
        ) : (
          <div className="flex-col items-center gap-2" style={{ color: 'var(--text-secondary)' }}>
            <Upload size={48} />
            <span>Click to browse or drag and drop</span>
          </div>
        )}
      </div>

      <div style={{ width: '100%' }}>
        <input 
          type="text" 
          className="input-field" 
          placeholder="Custom Project ID (optional)" 
          value={projectId}
          onChange={(e) => setProjectId(e.target.value)}
          disabled={status !== 'idle' && status !== 'error'}
        />
      </div>

      <button 
        className="btn btn-primary" 
        style={{ width: '100%', padding: '1rem' }}
        onClick={handleUploadAndProcess}
        disabled={!file || (status !== 'idle' && status !== 'error')}
      >
        {status === 'idle' && 'Upload & Process'}
        {status === 'uploading' && <><Loader className="animate-spin" size={18} /> Uploading...</>}
        {status === 'processing' && <><Loader className="animate-spin" size={18} /> Chunking & Embedding...</>}
        {status === 'success' && <><CheckCircle2 size={18} /> Complete!</>}
        {status === 'error' && 'Retry'}
      </button>

      {errorMsg && (
        <div style={{ color: 'var(--danger)', fontSize: '0.9rem', textAlign: 'center' }}>
          {errorMsg}
        </div>
      )}
    </div>
  )
}
