import { useState } from 'react'
import { Layout, Dashboard, Database, Zap, Brain, Activity, Terminal, Settings, HelpCircle, Play, Copy, Plus } from 'lucide-react'
import QueryPanel from './components/QueryPanel'
import GraphView from './components/GraphView'
import IngestionPanel from './components/IngestionPanel'
import HealthPanel from './components/HealthPanel'

export default function App() {
  const [activeTab, setActiveTab] = useState('query')

  const tabs = [
    { id: 'query', label: 'Query', icon: Zap },
    { id: 'ingest', label: 'Ingest', icon: Plus },
    { id: 'graph', label: 'Graph', icon: Activity },
    { id: 'health', label: 'Health', icon: Dashboard },
    { id: 'settings', label: 'Settings', icon: Settings },
  ]

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {/* Header */}
      <header className="bg-slate-900 text-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/30">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">MorphoSphere</h1>
              <p className="text-xs text-cyan-300">Topological & Structural Pattern Engine</p>
            </div>
          </div>
          <div className="flex gap-2">
            <a href="/docs" target="_blank" rel="noopener noreferrer" className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm font-medium transition-colors border border-slate-700">
              API Docs
            </a>
            <a href="https://github.com/SaadxSalman/MorphoSphere" target="_blank" rel="noopener noreferrer" className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm font-medium transition-colors border border-slate-700">
              GitHub
            </a>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 bg-slate-900 text-white hidden md:flex flex-col">
          <nav className="flex-1 py-6 space-y-1 px-4">
            {tabs.map((tab) => {
              const Icon = tab.icon
              const isActive = activeTab === tab.id
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-cyan-600/20 text-cyan-300 border border-cyan-500/50'
                      : 'hover:bg-slate-800 text-slate-400'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  {tab.label}
                </button>
              )
            })}
          </nav>
          <div className="p-4 border-t border-slate-800">
            <p className="text-xs text-slate-500 mb-2">v1.0.0</p>
            <p className="text-xs text-slate-500">Structural Pattern Recognition</p>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6 md:p-8">
          {activeTab === 'query' && <QueryPanel />}
          {activeTab === 'ingest' && <IngestionPanel />}
          {activeTab === 'graph' && <GraphView />}
          {activeTab === 'health' && <HealthPanel />}
          {activeTab === 'settings' && (
            <div className="bg-white rounded-xl shadow p-6">
              <h2 className="text-lg font-semibold mb-4">Settings</h2>
              <p className="text-slate-500 text-sm">Configuration managed via .env file</p>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}