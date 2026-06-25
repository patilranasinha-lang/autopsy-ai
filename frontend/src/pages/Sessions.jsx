import { useState, useEffect } from 'react';
import axios from 'axios';
import { RefreshCw, AlertCircle } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import SessionMetrics from '../components/widgets/SessionMetrics';
import SessionTimeline from '../components/widgets/SessionTimeline';
import ActivityDistribution from '../components/widgets/ActivityDistribution';

const Sessions = () => {
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState(null);
  const [summary, setSummary] = useState(null);
  const [sessions, setSessions] = useState([]);

  const fetchSessionData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};

      const [summaryRes, sessionsRes] = await Promise.all([
        axios.get('/api/sessions/summary', { headers }),
        axios.get('/api/sessions?per_page=50', { headers }) // get up to 50 for timeline
      ]);

      setSummary(summaryRes.data);
      setSessions(sessionsRes.data.sessions);
    } catch (err) {
      console.error('Error fetching session data:', err);
      setError('Failed to load session data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSessionData();
  }, []);

  const handleGenerateSessions = async () => {
    try {
      setGenerating(true);
      const token = localStorage.getItem('token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      await axios.post('/api/sessions/generate', {}, { headers });
      await fetchSessionData();
    } catch (err) {
      console.error('Error generating sessions:', err);
      alert('Failed to generate sessions');
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full min-h-[400px]">
        <div className="w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
        <AlertCircle className="text-red-600 mt-0.5" size={24} />
        <div>
          <h3 className="font-semibold text-red-800">Error Loading Sessions</h3>
          <p className="text-red-700 mt-1">{error}</p>
          <Button onClick={fetchSessionData} variant="outline" className="mt-4">Retry</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Session Analytics</h1>
          <p className="text-slate-500 mt-1">Behavioral intelligence blocks detected from your events</p>
        </div>
        <Button onClick={handleGenerateSessions} disabled={generating}>
          {generating ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
          ) : (
            <RefreshCw size={20} className="mr-2" />
          )}
          {generating ? 'Processing...' : 'Run Detection Engine'}
        </Button>
      </div>

      <SessionMetrics summary={summary} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2 p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Session Timeline</h3>
          <SessionTimeline sessions={sessions} />
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Session Distribution</h3>
          <ActivityDistribution data={summary?.session_distribution || {}} />
        </Card>
      </div>
    </div>
  );
};

export default Sessions;
