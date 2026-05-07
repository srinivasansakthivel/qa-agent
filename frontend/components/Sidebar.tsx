import {
  ChartBarIcon,
  DocumentTextIcon,
  PlayIcon,
  CpuChipIcon,
  HomeIcon
} from '@heroicons/react/24/outline'

type ActiveView = 'dashboard' | 'generation' | 'execution' | 'analytics' | 'agents'

interface SidebarProps {
  activeView: ActiveView
  onViewChange: (view: ActiveView) => void
}

const navigation = [
  { name: 'Dashboard', view: 'dashboard' as ActiveView, icon: HomeIcon },
  { name: 'Test Generation', view: 'generation' as ActiveView, icon: DocumentTextIcon },
  { name: 'Test Execution', view: 'execution' as ActiveView, icon: PlayIcon },
  { name: 'Analytics', view: 'analytics' as ActiveView, icon: ChartBarIcon },
  { name: 'AI Agents', view: 'agents' as ActiveView, icon: CpuChipIcon },
]

export default function Sidebar({ activeView, onViewChange }: SidebarProps) {
  return (
    <div className="w-64 bg-white shadow-sm border-r border-gray-200">
      <nav className="mt-8">
        <div className="space-y-1">
          {navigation.map((item) => {
            const isActive = activeView === item.view
            return (
              <button
                key={item.name}
                onClick={() => onViewChange(item.view)}
                className={`w-full flex items-center px-6 py-3 text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <item.icon className="mr-3 h-5 w-5" />
                {item.name}
              </button>
            )
          })}
        </div>
      </nav>
    </div>
  )
}
