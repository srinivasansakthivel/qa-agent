import { Metadata } from 'next'
import Dashboard from '@/components/Dashboard'

export const metadata: Metadata = {
  title: 'AI-QA-Agent - AI-Powered QA Platform',
  description: 'Autonomous QA testing with AI agents for comprehensive test generation and execution',
}

export default function HomePage() {
  return <Dashboard />
}