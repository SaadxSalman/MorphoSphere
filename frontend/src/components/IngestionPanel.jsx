import { useState } from 'react'
import { FileText, Folder, Play, Terminal, CheckCircle, AlertCircle } from 'lucide-react'
import axios from 'axios'

const API = '/api/v1'

export default function IngestionPanel() {
  const [filePath, setFilePath] = useState('')
  const [dirPath, setDirPath] = useState('')
  const [extensions, setExtensions] = useState('py,js,ts,go,rs,java,cpp,md')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleIngestFile = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await axios.post(`${API}/ingest/file`, null, {
        params: { file_path: filePath },
      })
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleIngestDirectory = async (e) => {
    e.preventDefault()
    setLoading(true)

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 rounded-2xl p-8 border border-cyan-200/50 shadow-sm">
        <div className="flex items-start gap-4 mb-6">
          <div className="w-12 h-12 bg-cyan-500 rounded-xl flex items-center justify-center text-white shadow-lg shadow-cyan-400/30">
            <Folder className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-slate-900 mb-1">Multi-Modal Ingestion</h2>
            <p className="text-slate-600 text-sm">
              Parse source code and documentation into Abstract Syntax Graphs (ASGs), extract structural motifs,
              and index them in Neo4j and Qdrant for hybrid retrieval.
            </p>
          </div>
        </div>
    setError(null)
    setResult(null)
    try {
      const res = await axios.post(`${API}/ingest/directory`, null, {

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <FileText className="w-5 h-5 text-cyan-600" /> Ingest Single File
            </h3>
            <form onSubmit={handleIngestFile} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">File Path</label>
                <input
                  type="text"
                  value={filePath}
                  onChange={e => setFilePath(e.target.value)}
                  placeholder="/path/to/your/code.py"
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 outline-none font-mono text-sm"
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-slate-900 hover:bg-slate-800 disabled:bg-slate-400 text-white font-bold py-3 rounded-xl transition-all"
              >
                <Play className="w-4 h-4 mr-2" /> Ingest File
              </button>
            </form>
          </div>

          <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Folder className="w-5 h-5 text-cyan-600" /> Ingest Directory
            </h3>
            <form onSubmit={handleIngestDirectory} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Directory Path</label>
                <input
                  type="text"
                  value={dirPath}
                  onChange={e => setDirPath(e.target.value)}
                  placeholder="/path/to/your/project"
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 outline-none font-mono text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Extensions</label>
                <input
                  type="text"
                  value={extensions}
                  onChange={e => setExtensions(e.target.value)}
                  placeholder="py,js,ts,go,rs"

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-6">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 mt-0.5" />
            <div>
              <h3 className="font-semibold text-red-900">Ingestion Error</h3>
              <p className="text-red-700 text-sm mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      {result && (
        <div className="bg-green-50 border border-green-200 rounded-xl p-6">
          <div className="flex items-start gap-3">
            <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
            <div>
              <h3 className="font-semibold text-green-900">Ingestion Complete</h3>
              <p className="text-green-700 text-sm mt-1">{result.filename}</p>
            </div>
          </div>
          <div className="mt-4 grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white p-4 rounded-lg border border-slate-200">
              <p className="text-xs text-slate-500 uppercase font-bold">Nodes</p>
              <p className="text-xl font-bold text-slate-900">{result.node_count}</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-slate-200">
              <p className="text-xs text-slate-500 uppercase font-bold">Edges</p>
              <p className="text-xl font-bold text-slate-900">{result.edge_count}</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-slate-200">
              <p className="text-xs text-slate-500 uppercase font-bold">Motifs</p>
              <p className="text-xl font-bold text-slate-900">{result.motif_count}</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-slate-200">
              <p className="text-xs text-slate-500 uppercase font-bold">Size</p>
              <p className="text-xl font-bold text-slate-900">{result.size_bytes} bytes</p>
            </div>
          </div>
          <div className="mt-4 bg-slate-100 p-3 rounded-lg text-xs font-mono text-slate-600">
            <p><span className="font-bold">ID:</span> {result.document_id}</p>
            <p><span className="font-bold">Type:</span> {result.document_type}</p>
            <p><span className="font-bold">Language:</span> {result.language}</p>
            <p><span className="font-bold">Checksum:</span> {result.checksum}</p>
          </div>
        </div>
      )}

      {loading && (
        <div className="flex justify-center py-8">
          <div className="w-8 h-8 border-4 border-cyan-300 border-t-cyan-600 rounded-full animate-spin"></div>
        </div>
      )}
    </div>
  )
}
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 outline-none font-mono text-sm"
                />
                <p className="text-xs text-slate-500 mt-1">Comma-separated file extensions</p>
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-cyan-600 hover:bg-cyan-700 disabled:bg-cyan-400 text-white font-bold py-3 rounded-xl transition-all shadow-lg shadow-cyan-500/30"
              >
                <Play className="w-4 h-4 mr-2" /> Ingest Directory
              </button>
            </form>
          </div>
        </div>
      </div>
        params: { directory_path: dirPath, extensions },
      })
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }
  const [error, setError] = useState(null)