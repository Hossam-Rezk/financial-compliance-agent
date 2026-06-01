import { useState, useRef, useEffect } from 'react'
import { Send, User, Bot, Loader } from 'lucide-react'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface Props {
  projectId: string
}

export default function Chatbot({ projectId }: Props) {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I am your compliance assistant. Ask me anything about the uploaded project.' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMsg: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/nlp/chat/${projectId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          query: userMsg.content,
          chat_history: messages.filter(m => m.role !== 'assistant' || m.content !== 'Hello! I am your compliance assistant. Ask me anything about the uploaded project.') 
        })
      })

      const data = await res.json()
      if (!res.ok) throw new Error(data.message || 'Failed to fetch response')

      setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
    } catch (err: any) {
      setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${err.message}` }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="glass-panel flex-col" style={{ height: '600px', overflow: 'hidden' }}>
      <div style={{ padding: '1rem 1.5rem', borderBottom: '1px solid var(--glass-border)', background: 'rgba(0,0,0,0.3)' }}>
        <h3 style={{ margin: 0 }}>Compliance Assistant</h3>
      </div>

      <div className="flex-col gap-4" style={{ flex: 1, overflowY: 'auto', padding: '1.5rem' }}>
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}>
            {msg.role === 'assistant' && (
              <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--bg-tertiary)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Bot size={18} color="var(--accent-primary)" />
              </div>
            )}
            <div style={{ 
              maxWidth: '75%', 
              padding: '12px 16px', 
              borderRadius: 'var(--radius-md)',
              background: msg.role === 'user' ? 'var(--accent-primary)' : 'var(--bg-tertiary)',
              color: msg.role === 'user' ? '#fff' : 'var(--text-primary)',
              lineHeight: 1.5
            }}>
              {msg.content}
            </div>
            {msg.role === 'user' && (
              <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--accent-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <User size={18} color="#fff" />
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex gap-3">
            <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--bg-tertiary)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Bot size={18} color="var(--accent-primary)" />
            </div>
            <div style={{ padding: '12px 16px', borderRadius: 'var(--radius-md)', background: 'var(--bg-tertiary)' }}>
              <Loader className="animate-spin" size={18} />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div style={{ padding: '1rem', borderTop: '1px solid var(--glass-border)', background: 'rgba(0,0,0,0.3)' }}>
        <div className="flex gap-2">
          <input 
            type="text" 
            className="input-field" 
            placeholder="Ask a question..." 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            disabled={loading}
          />
          <button 
            className="btn btn-primary" 
            style={{ padding: '0 20px' }}
            onClick={handleSend}
            disabled={loading || !input.trim()}
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  )
}
