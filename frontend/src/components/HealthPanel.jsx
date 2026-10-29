import { useState, useEffect } from 'react'
import { Database, Server, Wifi, Activity, RefreshCw, CheckCircle2, AlertCircle } from 'lucide-react'
import axios from 'axios'

const API = '/api/v1'

export default function HealthPanel() {
  const [health, setHealth] = useState(null)
  const [info, setInfo] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const [h, i] = await Promise.all([
          axios.get(`${API}/health`),
          axios.get(`${API}/info`),

  const statusColor = (status) => {
    switch (status) {
      case 'healthy': return 'bg-green-100 text-green-800 border-green-200'
      case 'degraded': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      default: return 'bg-red-100 text-red-800 border-red-200'
    }
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="w-10 h-10 border-4 border-cyan-300 border-t-cyan-600 rounded-full animate-spin mb-4"></div>
        <p className="text-slate-600">Loading health status...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 rounded-2xl p-8 border border-cyan-200/50 shadow-sm">
        <div className="flex items-start gap-4 mb-6">
          <div className="w-12 h-12 bg-cyan-500 rounded-xl flex items-center justify-center text-white shadow-lg shadow-cyan-400/30">
            <Database className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-slate-900 mb-1">System Health</h2>
            <p className="text-slate-600 text-sm">Monitor the status of MorphoSphere services and infrastructure.</p>
          </div>
        </div>
        ])

        <div className="flex items-center gap-4">
          <span className={`px-4 py-2 rounded-lg font-bold text-sm border ${statusColor(health?.status || 'unknown')}`}>
            {health?.status?.toUpperCase() || 'UNKNOWN'}
          </span>
          <button
            onClick={() => window.location.reload()}
            className="bg-slate-900 hover:bg-slate-800 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all"
          >
            <RefreshCw className="w-4 h-4 mr-2" /> Refresh
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <Database className="w-5 h-5 text-slate-500" />
            <h3 className="font-semibold text-slate-900">Neo4j Graph</h3>
          </div>
          <div className={`p-3 rounded-lg ${health?.neo4j ? 'bg-green-50 border-green-100' : 'bg-red-50 border-red-100'} border`}>
            <p className={`text-xs font-bold ${health?.neo4j ? 'text-green-800' : 'text-red-800'}`}>
              {health?.neo4j ? 'Connected' : 'Disconnected'}
            </p>
            <p className="text-[10px] text-slate-500 mt-1">bolt://localhost:7687</p>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <Server className="w-5 h-5 text-slate-500" />
            <h3 className="font-semibold text-slate-900">Qdrant Vectors</h3>
          </div>
          <div className={`p-3 rounded-lg ${health?.qdrant ? 'bg-green-50 border-green-100' : 'bg-red-50 border-red-100'} border`}>
            <p className={`text-xs font-bold ${health?.qdrant ? 'text-green-800' : 'text-red-800'}`}>
              {health?.qdrant ? 'Connected' : 'Disconnected'}
            </p>
            <p className="text-[10px] text-slate-500 mt-1">http://localhost:6333</p>
          </div>

      {info && (
        <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
          <h3 className="font-semibold text-slate-900 mb-4">Application Info</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-slate-500">Name</span>
              <span className="font-medium">{info.name}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Version</span>
              <span className="font-medium">{info.version}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Environment</span>
              <span className="font-medium">{info.environment}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Debug</span>
              <span className="font-medium">{String(info.debug)}</span>
            </div>
          </div>
          <div className="mt-6">
            <h4 className="text-xs font-bold text-slate-500 uppercase mb-2">Features</h4>
            <div className="flex flex-wrap gap-2">
              {Object.entries(info.features).map(([key, enabled]) => (
                <span key={key} className={`px-2.5 py-1 rounded text-xs font-medium border ${
                  enabled ? 'bg-green-50 border-green-100 text-green-800' : 'bg-slate-100 border-slate-200 text-slate-600'
                }`}>
                  {enabled ? '✓' : '✗'} {key.replace(/_/g, ' ')}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
        </div>

        <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <Wifi className="w-5 h-5 text-slate-500" />
            <h3 className="font-semibold text-slate-900">LLM Provider</h3>
          </div>
          <div className="p-3 rounded-lg bg-blue-50 border-blue-100 border">
            <p className="text-xs font-bold text-blue-800">{info?.llm || 'N/A'}</p>
            <p className="text-[10px] text-slate-500 mt-1">Ollama / vLLM compatible</p>
          </div>
        </div>
      </div>
        setHealth(h.data)
        setInfo(i.data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])