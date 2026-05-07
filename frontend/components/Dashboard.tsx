'use client'

import { useState } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Header from '@/components/Header'
import Sidebar from '@/components/Sidebar'
import TestGenerationPanel from '@/components/TestGenerationPanel'
import TestExecutionPanel from '@/components/TestExecutionPanel'
import AnalyticsDashboard from '@/components/AnalyticsDashboard'
import AgentPanel from '@/components/AgentPanel'

const queryClient = new QueryClient()

type ActiveView = 'dashboard' | 'generation' | 'execution' | 'analytics' | 'agents'

export default function Dashboard() {
  const [activeView, setActiveView] = useState<ActiveView>('dashboard')

  const renderActiveView = () => {
    switch (activeView) {
      case 'generation':
        return <TestGenerationPanel />
      case 'execution':
        return <TestExecutionPanel />
      case 'analytics':
        return <AnalyticsDashboard />
      case 'agents':
        return <AgentPanel />
      default:
        return <AnalyticsDashboard />
    }
  }

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="flex">
          <Sidebar activeView={activeView} onViewChange={setActiveView} />
          <main className="flex-1 p-6">
            {renderActiveView()}
          </main>
        </div>
      </div>
    </QueryClientProvider>
  )
}