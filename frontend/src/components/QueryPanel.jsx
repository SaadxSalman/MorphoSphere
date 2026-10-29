import { useState, useEffect } from 'react'
import { Search, Copy, Terminal, Bot, Zap, Clock, FileText } from 'lucide-react'
import axios from 'axios'

const API = '/api/v1'

export default function QueryPanel() {
  const [query, setQuery] = useState('')
  const [intent, setIntent] = useState('')
  const [topK, setTopK] = useState(10)
  const [agentic, setAgentic] = useState(true)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleIntentSuggest = async (e) => {
    const q = e.target.value
    if (q.length < 3) {
      setIntentSuggestions(null)
      return
    }
    try {
      const res = await axios.get(`${API}/query/intent-suggestions`, { params: { q } })
      setIntentSuggestions(res.data)
    } catch (err) {
      // silent
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 rounded-2xl p-8 border border-cyan-200/50 shadow-sm">
        <div className="flex items-start gap-4 mb-6">
          <div className="w-12 h-12 bg-cyan-500 rounded-xl flex items-center justify-center text-white shadow-lg shadow-cyan-400/30">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-slate-900 mb-1">Structural Query Engine</h2>
            <p className="text-slate-600 text-sm">Ask questions about your codebase's architecture, dependencies, and design patterns.</p>
          </div>
        </div>
    setLoading(true)
    setError(null)
    try {
      const res = await axios.post(`${API}/query`, {
        query,
        intent: intent || undefined,
        top_k: topK,
        enable_agentic_correction: agentic,

        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="col-span-2">
            <label className="block text-sm font-medium text-slate-700 mb-2">Query</label>
            <textarea
              value={query}
              onChange={e => { setQuery(e.target.value); handleIntentSuggest(e) }}
              className="w-full min-h-[100px] rounded-xl border border-slate-300 p-4 focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 outline-none transition-all font-mono text-sm"
              placeholder="e.g. How does the authentication flow connect to the database layer? Show me the factory pattern implementations..."
            />
          </div>
      })
      setResults(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }
          </div>
          <div className="flex flex-col gap-3">
            <label className="text-sm font-medium text-slate-700">Intent</label>
            <select
              value={intent}
              onChange={e => setIntent(e.target.value)}
              className="rounded-xl border border-slate-300 px-4 py-3 focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 outline-none bg-white"
            >
              <option value="">Auto-detect</option>
              <option value="behavioral_flow">Behavioral Flow</option>
              <option value="structural_bug">Structural Bug</option>
              <option value="architectural_relationship">Architectural Relationship</option>
              <option value="code_search">Code Search</option>
              <option value="documentation_lookup">Documentation Lookup</option>
            </select>
          </div>
          <div className="flex flex-col gap-3">
            <label className="text-sm font-medium text-slate-700">Top K</label>
            <input
              type="number"
              value={topK}
              onChange={e => setTopK(parseInt(e.target.value) || 10)}
              min={1} max={50}
              className="rounded-xl border border-slate-300 px-4 py-3 focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 outline-none bg-white"
            />
          </div>
          <div className="flex items-end gap-3">
            <label className="flex items-center gap-2 text-sm font-medium text-slate-700 cursor-pointer select-none">
              <input

        {intentSuggestions && (
          <div className="mt-4 p-4 bg-slate-50 rounded-xl border border-slate-200">
            <div className="flex items-center gap-2 mb-2">
              <Search className="w-4 h-4 text-slate-500" />
              <span className="text-sm font-medium text-slate-700">Intent detected:</span>
            </div>
            <div className="flex gap-2">
              <span className="px-3 py-1 bg-cyan-100 text-cyan-800 rounded-full text-xs font-semibold">
                {intentSuggestions.intent}
              </span>
              <span className="px-3 py-1 bg-slate-200 text-slate-700 rounded-full text-xs">
                Confidence: {(intentSuggestions.confidence * 100).toFixed(0)}%
              </span>
              {intentSuggestions.structural_hints.length > 0 && (
                <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                  Hints: {intentSuggestions.structural_hints.slice(0, 3).join(', ')}
                </span>
              )}

      {loading && (
        <div className="flex justify-center py-8">
          <div className="flex flex-col items-center gap-3">
            <div className="w-8 h-8 border-4 border-cyan-300 border-t-cyan-600 rounded-full animate-spin"></div>
            <p className="text-slate-600 text-sm">Analyzing structural patterns...</p>
          </div>
        </div>
      )}

      {results && (
        <div className="grid gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-cyan-600" />
                <h3 className="font-semibold text-slate-900">Results</h3>
              </div>
              <div className="flex gap-2 text-xs text-slate-500">
                <span className="bg-slate-100 px-2 py-1 rounded">Intent: {results.intent}</span>
                <span className="bg-blue-50 px-2 py-1 rounded text-blue-700">Passes: {results.agentic_passes}</span>
                <span className="bg-green-50 px-2 py-1 rounded text-green-700">{results.processing_time_ms.toFixed(0)}ms</span>
              </div>
            </div>

            <div className="bg-slate-50 rounded-xl p-4 mb-6 border border-slate-100">
              <h4 className="text-sm font-semibold text-slate-700 mb-2">Generated Answer</h4>
              <div className="prose prose-sm text-slate-800 whitespace-pre-wrap font-mono text-sm">
                {results.generated_answer}
              </div>
              <button
                onClick={() => {
                  navigator.clipboard.writeText(results.generated_answer)
                }}
                className="mt-3 text-xs text-cyan-600 hover:text-cyan-800 underline flex items-center gap-1"
              >
                <Copy className="w-3 h-3" /> Copy Answer
              </button>
            </div>

            <div className="mb-6">
              <h4 className="text-sm font-semibold text-slate-700 mb-3">Retrieved Context ({results.results.length})</h4>
              <div className="space-y-3">
                {results.results.map((r, i) => (
                  <div key={i} className="p-3 rounded-lg border border-slate-200 bg-slate-50/50">
                    <div className="flex items-start gap-3">
                      <div className="bg-cyan-100 text-cyan-800 rounded p-2 flex-shrink-0">
                        <FileText className="w-4 h-4" />
                      </div>
                      <div className="flex-1">
                        <div className="flex justify-between mb-1">
                          <span className="text-xs font-bold text-slate-600 uppercase tracking-wider">
                            {r.metadata?.node_type || 'node'}
                          </span>
                          <span className="text-[10px] bg-slate-200 px-2 py-0.5 rounded text-slate-500 font-mono">
                            Score: {r.fused_score?.toFixed(3) || 0}
                          </span>
                        </div>
                        <p className="text-sm text-slate-700 font-mono mb-1">{r.name || 'Untitled'}</p>
                        <p className="text-xs text-slate-500 font-mono">
                          {r.metadata?.file_path || 'unknown'}:{r.metadata?.start_line || ''}
                        </p>
                        <div className="mt-2 p-2 bg-white rounded border border-slate-100 text-xs text-slate-600 font-mono overflow-x-auto">
                          {r.content?.slice(0, 300)}...
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {results.graph_context && results.graph_context.length > 0 && (
              <div className="mt-6 p-4 rounded-xl border border-blue-100 bg-blue-50">
                <h4 className="text-sm font-semibold text-blue-900 mb-2">Graph Context</h4>
                <p className="text-xs text-blue-700 mb-3">
                  {results.graph_context.length} neighboring nodes found in the structural graph.
                </p>
                <div className="flex gap-2 flex-wrap">
                  {results.graph_context.slice(0, 10).map((n, i) => (
                    <span key={i} className="px-2 py-1 bg-white text-blue-800 rounded text-xs border border-blue-200">
                      {n.name || 'node'}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-6">
          <div className="flex items-start gap-3">
            <Terminal className="w-5 h-5 text-red-600 mt-0.5" />
            <div>
              <h3 className="font-semibold text-red-900">Query Error</h3>
              <p className="text-red-700 text-sm mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}
                type="checkbox"
                checked={agentic}
                onChange={e => setAgentic(e.target.checked)}
                className="rounded border-slate-300 text-cyan-600 focus:ring-cyan-500"
              />
              Agentic Self-Correction
            </label>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-cyan-600 hover:bg-cyan-700 disabled:bg-cyan-300 text-white font-bold py-4 rounded-xl shadow-lg shadow-cyan-500/30 transition-all transform active:scale-[0.98] flex items-center justify-center gap-2"
            >
              <Zap className="w-5 h-5" /> Analyze Structure
            </button>
          </div>
        </form>
  const [intentSuggestions, setIntentSuggestions] = useState(null)