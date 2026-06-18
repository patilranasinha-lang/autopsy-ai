import { 
  Brain, 
  Shield, 
  Upload, 
  FileText,
  TrendingUp,
  Users,
  Clock,
  Database
} from 'lucide-react'
import Card from '../components/Card'
import Button from '../components/Button'
import { Link } from 'react-router-dom'

const Dashboard = () => {
  const stats = [
    { 
      label: 'Total Analyses', 
      value: '24', 
      icon: Brain,
      color: 'text-emerald-600',
      bgColor: 'bg-emerald-100'
    },
    { 
      label: 'Files Uploaded', 
      value: '156', 
      icon: Database,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    { 
      label: 'Reports Generated', 
      value: '18', 
      icon: FileText,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    },
    { 
      label: 'Processing Time', 
      value: '1.2h', 
      icon: Clock,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100'
    }
  ]

  const recentReports = [
    { id: 1, name: 'User Behavior Analysis Q2', date: '2 hours ago', status: 'Completed' },
    { id: 2, name: 'Engagement Metrics', date: 'Yesterday', status: 'Processing' },
    { id: 3, name: 'Retention Study', date: '3 days ago', status: 'Completed' }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Welcome Back!</h1>
          <p className="text-slate-500 mt-1">Here's what's happening with your analyses</p>
        </div>
        <Link to="/upload">
          <Button>
            <Upload size={20} className="mr-2" />
            New Upload
          </Button>
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon
          return (
            <Card key={index} className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-500 font-medium">{stat.label}</p>
                  <p className="text-2xl font-bold text-slate-900 mt-1">{stat.value}</p>
                </div>
                <div className={`w-12 h-12 ${stat.bgColor} rounded-xl flex items-center justify-center ${stat.color}`}>
                  <Icon size={24} />
                </div>
              </div>
            </Card>
          )
        })}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Privacy Notice */}
        <Card className="lg:col-span-2 p-6">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center shrink-0">
              <Shield size={24} />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-slate-900">Privacy-First Processing</h3>
              <p className="text-slate-500 mt-1">
                All your data is processed locally. Nothing leaves your machine without explicit consent.
                Your privacy is our top priority.
              </p>
              <div className="flex gap-2 mt-4">
                <span className="px-3 py-1 bg-emerald-100 text-emerald-700 text-xs font-medium rounded-full">
                  End-to-End Encrypted
                </span>
                <span className="px-3 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded-full">
                  Local Processing
                </span>
              </div>
            </div>
          </div>
        </Card>

        {/* Quick Actions */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <Button className="w-full justify-start" variant="outline">
              <Upload size={20} className="mr-3" />
              Upload Dataset
            </Button>
            <Button className="w-full justify-start" variant="outline">
              <FileText size={20} className="mr-3" />
              View Reports
            </Button>
            <Button className="w-full justify-start" variant="outline">
              <TrendingUp size={20} className="mr-3" />
              Start Analysis
            </Button>
          </div>
        </Card>
      </div>

      {/* Recent Reports */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-slate-900">Recent Reports</h3>
          <Link to="/reports" className="text-sm text-emerald-600 font-medium hover:text-emerald-700">
            View all
          </Link>
        </div>
        <div className="space-y-4">
          {recentReports.map((report) => (
            <div
              key={report.id}
              className="flex items-center justify-between p-4 bg-slate-50 rounded-lg border border-slate-200"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-purple-100 text-purple-600 rounded-lg flex items-center justify-center">
                  <FileText size={20} />
                </div>
                <div>
                  <p className="font-medium text-slate-900">{report.name}</p>
                  <p className="text-sm text-slate-500">{report.date}</p>
                </div>
              </div>
              <span className={`px-3 py-1 text-xs font-medium rounded-full ${
                report.status === 'Completed'
                  ? 'bg-emerald-100 text-emerald-700'
                  : 'bg-yellow-100 text-yellow-700'
              }`}>
                {report.status}
              </span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}

export default Dashboard
