import { BeakerIcon } from '@heroicons/react/24/outline'

export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <BeakerIcon className="h-8 w-8 text-blue-600" />
            <h1 className="ml-3 text-xl font-semibold text-gray-900">
              AI-QA-Agent
            </h1>
            <span className="ml-2 text-sm text-gray-500">
              AI-Powered QA Platform
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-sm text-gray-600">
              v1.0.0
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}