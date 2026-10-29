import { useState, useEffect } from 'react'
import { Activity, RefreshCw, NodeGraph } from 'lucide-react'
import axios from 'axios'

const API = '/api/v1'

export default function GraphView() {
  const [graph, setGraph] = useState(null)
  const [loading, setLoading] = useState(false)
  const [limit, setLimit] = useState(100)

  const loadGraph = async () => {
    setLoading(true)
    try {
      const res = await axios.get(`${API}/graph/visualize`, { params: { limit } })
      setGraph(res.data)
    } catch (err) {
      console.error(err)
    } finally {

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 rounded-2xl p-8 border border-cyan-200/50 shadow-sm">
        <div className="flex items-start gap-4 mb-6">
          <div className="w-12 h-12 bg-cyan-500 rounded-xl flex items-center justify-center text-white shadow-lg shadow-cyan-400/30">
            <NodeGraph className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-slate-900 mb-1">Structural Graph Visualization</h2>
            <p className="text-slate-600 text-sm">
              Explore the Abstract Syntax Graph - nodes represent code elements, edges represent relationships
              (calls, imports, extends, implements, contains).
            </p>
          </div>
        </div>
      setLoading(false)
    }
  }

  useEffect(() => {
    loadGraph()
  }, [limit])

        <div className="flex items-center gap-4">
          <label className="text-sm font-medium text-slate-700">Max Nodes</label>
          <input
            type="number"
            value={limit}
            onChange={e => setLimit(parseInt(e.target.value) || 100)}
            min={10} max={1000}
            className="w-24 rounded-xl border border-slate-300 px-3 py-2 focus:ring-2 focus:ring-cyan-500 outline-none font-mono text-sm"
          />
          <button
            onClick={loadGraph}
            disabled={loading}
            className="bg-slate-900 hover:bg-slate-800 disabled:bg-slate-400 text-white px-6 py-2.5 rounded-xl font-bold transition-all"
          >
            <RefreshCw className="w-4 h-4 mr-2" /> Refresh Graph
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 min-h-[600px]">
        {loading ? (
          <div className="flex flex-col items-center justify-center h-full">
            <div className="w-8 h-8 border-4 border-cyan-300 border-t-cyan-600 rounded-full animate-spin mb-4"></div>
            <p className="text-slate-600">Loading graph data...</p>
          </div>
        ) : graph ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-slate-900">Graph Overview</h3>
                <p className="text-xs text-slate-500 mt-1">
                  {graph.node_count} nodes • {graph.edge_count} edges
                </p>
              </div>
              <div className="flex gap-2 text-xs text-slate-500">
                <span className="bg-blue-50 px-2 py-1 rounded text-blue-700">Nodes: {graph.node_count}</span>
                <span className="bg-green-50 px-2 py-1 rounded text-green-700">Edges: {graph.edge_count}</span>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-200">
                    <th className="pb-3 text-xs font-bold text-slate-500 uppercase">ID</th>
                    <th className="pb-3 text-xs font-bold text-slate-500 uppercase">Label</th>
                    <th className="pb-3 text-xs font-bold text-slate-500 uppercase">Type</th>
                    <th className="pb-3 text-xs font-bold text-slate-500 uppercase">File</th>
                    <th className="pb-3 text-xs font-bold text-slate-500 uppercase">Line</th>
                  </tr>
                </thead>
                <tbody>
                  {graph.nodes.map((node, i) => (
                    <tr key={i} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                      <td className="py-3 text-xs font-mono text-slate-600">{node.id.slice(0, 8)}...</td>
                      <td className="py-3 text-xs font-medium text-slate-900">{node.label}</td>
                      <td className="py-3 text-xs font-mono text-slate-500">{node.node_type}</td>
                      <td className="py-3 text-xs font-mono text-slate-400 truncate max-w-xs">{node.file_path}</td>
                      <td className="py-3 text-xs font-mono text-slate-500">{node.start_line}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {graph.nodes.length > 0 && (
              <div className="mt-6 p-4 rounded-lg border border-slate-200 bg-slate-50">
                <h4 className="text-sm font-semibold text-slate-700 mb-2">Sample Edges</h4>
                <div className="space-y-2">
                  {graph.edges.slice(0, 10).map((edge, i) => (
                    <div key={i} className="flex items-center gap-3 p-2 bg-white rounded border border-slate-100">
                      <span className="text-[10px] font-mono text-slate-400 w-16">{edge.source.slice(0, 8)}...</span>
                      <span className="bg-cyan-100 text-cyan-800 text-[10px] px-2 py-0.5 rounded font-bold uppercase">{edge.label}</span>
                      <span className="text-[10px] font-mono text-slate-400 w-16">{edge.target.slice(0, 8)}...</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-slate-500">
            <Activity className="w-12 h-12 opacity-20 mb-4" />
            <p>No graph data available. Ingest some code first.</p>
          </div>
        )}
      </div>
    </div>
  )
}