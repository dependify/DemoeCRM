const { useState, useEffect, useCallback } = React;

// API Configuration
const API_URL = '/api';

// Enums
const ConvertStage = {
    NEW: 'new',
    IN_FOLLOWUP: 'in_followup',
    IN_CLASSES: 'in_classes',
    IN_HOUSE_FELLOWSHIP: 'in_house_fellowship',
    ESTABLISHED: 'established',
    HANDED_OVER: 'handed_over',
    INACTIVE: 'inactive'
};

// Utility Functions
const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('en-NG', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
    });
};

const formatPhone = (phone) => {
    if (!phone) return '-';
    if (phone.length === 11) {
        return `${phone.slice(0, 4)} ${phone.slice(4, 7)} ${phone.slice(7)}`;
    }
    return phone;
};

const getHealthScoreClass = (score) => {
    if (score >= 80) return 'score-excellent';
    if (score >= 60) return 'score-good';
    if (score >= 40) return 'score-fair';
    return 'score-poor';
};

const getStageColor = (stage) => {
    const colors = {
        new: 'bg-orange-100 text-orange-800',
        in_followup: 'bg-green-100 text-green-800',
        in_classes: 'bg-blue-100 text-blue-800',
        in_house_fellowship: 'bg-purple-100 text-purple-800',
        established: 'bg-teal-100 text-teal-800',
        handed_over: 'bg-gray-100 text-gray-800',
        inactive: 'bg-red-100 text-red-800'
    };
    return colors[stage] || 'bg-gray-100';
};

const getStageLabel = (stage) => {
    const labels = {
        new: 'New',
        in_followup: 'In Follow-up',
        in_classes: 'In Classes',
        in_house_fellowship: 'In House Fellowship',
        established: 'Established',
        handed_over: 'Handed Over',
        inactive: 'Inactive'
    };
    return labels[stage] || stage;
};

// API Helper
const api = {
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('token');
        const url = `${API_URL}${endpoint}`;
        
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` })
            },
            ...options
        };
        
        if (config.body && typeof config.body === 'object') {
            config.body = JSON.stringify(config.body);
        }
        
        const response = await fetch(url, config);
        
        if (response.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.reload();
            return;
        }
        
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || `HTTP ${response.status}`);
        }
        
        return response.json();
    },
    
    get(endpoint) { return this.request(endpoint, { method: 'GET' }); },
    post(endpoint, body) { return this.request(endpoint, { method: 'POST', body }); },
    patch(endpoint, body) { return this.request(endpoint, { method: 'PATCH', body }); },
    delete(endpoint) { return this.request(endpoint, { method: 'DELETE' }); }
};

// Login Component
function Login({ onLogin }) {
    const [email, setEmail] = useState('admin@dependifygospel.demo');
    const [password, setPassword] = useState('Demo@2025');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        
        try {
            const data = await api.post('/auth/login', { email, password });
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            onLogin(data.user);
        } catch (err) {
            setError(err.message || 'Login failed');
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-amber-50 to-orange-50">
            <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md">
                <div className="text-center mb-8">
                    <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-4">
                        <i className="fas fa-church text-white text-2xl"></i>
                    </div>
                    <h1 className="text-2xl font-bold text-gray-800">Dependify Gospel Centre</h1>
                    <p className="text-gray-500">Evangelism CRM - Demo</p>
                </div>
                
                {error && (
                    <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">
                        <i className="fas fa-exclamation-circle mr-2"></i>{error}
                    </div>
                )}
                
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                            required
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-primary text-white py-2 rounded-lg hover:bg-primary-dark transition-colors disabled:opacity-50"
                    >
                        {loading ? (
                            <span><i className="fas fa-spinner fa-spin mr-2"></i>Logging in...</span>
                        ) : (
                            'Sign In'
                        )}
                    </button>
                </form>
                
                <div className="mt-6 p-4 bg-amber-50 rounded-lg text-sm text-gray-600">
                    <p className="font-medium mb-1">Demo Credentials:</p>
                    <p>Email: admin@dependifygospel.demo</p>
                    <p>Password: Demo@2025</p>
                </div>
            </div>
        </div>
    );
}

// Sidebar Component
function Sidebar({ activeTab, setActiveTab, user }) {
    const menuItems = [
        { id: 'dashboard', icon: 'fa-home', label: 'Dashboard' },
        { id: 'converts', icon: 'fa-users', label: 'Converts' },
        { id: 'alerts', icon: 'fa-bell', label: 'Alerts' },
        { id: 'voice-agent', icon: 'fa-phone-alt', label: 'Voice Agent' },
        { id: 'analytics', icon: 'fa-chart-bar', label: 'Analytics' },
    ];
    
    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.reload();
    };
    
    return (
        <div className="w-64 bg-white shadow-lg h-screen fixed left-0 top-0 flex flex-col">
            <div className="p-6 border-b">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center">
                        <i className="fas fa-church text-white"></i>
                    </div>
                    <div>
                        <h2 className="font-bold text-gray-800">Dependify Gospel</h2>
                        <p className="text-xs text-gray-500">Evangelism CRM</p>
                    </div>
                </div>
            </div>
            
            <nav className="flex-1 p-4">
                <ul className="space-y-2">
                    {menuItems.map(item => (
                        <li key={item.id}>
                            <button
                                onClick={() => setActiveTab(item.id)}
                                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                                    activeTab === item.id 
                                        ? 'bg-amber-50 text-primary' 
                                        : 'text-gray-600 hover:bg-gray-50'
                                }`}
                            >
                                <i className={`fas ${item.icon} w-5`}></i>
                                <span>{item.label}</span>
                            </button>
                        </li>
                    ))}
                </ul>
            </nav>
            
            <div className="p-4 border-t">
                <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                        <i className="fas fa-user text-gray-500"></i>
                    </div>
                    <div className="flex-1 min-w-0">
                        <p className="font-medium text-gray-800 truncate">{user?.name}</p>
                        <p className="text-xs text-gray-500 truncate">{user?.email}</p>
                    </div>
                </div>
                <button
                    onClick={handleLogout}
                    className="w-full flex items-center justify-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                    <i className="fas fa-sign-out-alt"></i>
                    <span>Logout</span>
                </button>
            </div>
        </div>
    );
}

// Dashboard Component
function Dashboard() {
    const [stats, setStats] = useState(null);
    const [stageDist, setStageDist] = useState({});
    const [recentActivity, setRecentActivity] = useState([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        loadDashboard();
    }, []);
    
    const loadDashboard = async () => {
        try {
            const [statsData, stageData, activityData] = await Promise.all([
                api.get('/dashboard/stats'),
                api.get('/dashboard/stage-distribution'),
                api.get('/dashboard/recent-activity')
            ]);
            setStats(statsData);
            setStageDist(stageData);
            setRecentActivity(activityData);
        } catch (err) {
            console.error('Error loading dashboard:', err);
        } finally {
            setLoading(false);
        }
    };
    
    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <i className="fas fa-spinner fa-spin text-3xl text-primary"></i>
            </div>
        );
    }
    
    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
            
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white rounded-xl shadow-sm p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-500 text-sm">Total Converts</p>
                            <p className="text-3xl font-bold text-gray-800">{stats?.total_converts || 0}</p>
                        </div>
                        <div className="w-12 h-12 bg-blue-50 rounded-lg flex items-center justify-center">
                            <i className="fas fa-users text-blue-500 text-xl"></i>
                        </div>
                    </div>
                    <p className="text-green-500 text-sm mt-2">
                        <i className="fas fa-arrow-up mr-1"></i>
                        {stats?.new_this_month || 0} new this month
                    </p>
                </div>
                
                <div className="bg-white rounded-xl shadow-sm p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-500 text-sm">At Risk</p>
                            <p className="text-3xl font-bold text-red-600">{stats?.at_risk || 0}</p>
                        </div>
                        <div className="w-12 h-12 bg-red-50 rounded-lg flex items-center justify-center">
                            <i className="fas fa-exclamation-triangle text-red-500 text-xl"></i>
                        </div>
                    </div>
                    <p className="text-gray-400 text-sm mt-2">Need immediate attention</p>
                </div>
                
                <div className="bg-white rounded-xl shadow-sm p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-500 text-sm">Avg Health Score</p>
                            <p className="text-3xl font-bold text-gray-800">{stats?.average_health_score || 0}</p>
                        </div>
                        <div className="w-12 h-12 bg-green-50 rounded-lg flex items-center justify-center">
                            <i className="fas fa-heartbeat text-green-500 text-xl"></i>
                        </div>
                    </div>
                    <p className="text-gray-400 text-sm mt-2">Out of 100 points</p>
                </div>
                
                <div className="bg-white rounded-xl shadow-sm p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-500 text-sm">Open Alerts</p>
                            <p className="text-3xl font-bold text-orange-600">{stats?.open_alerts || 0}</p>
                        </div>
                        <div className="w-12 h-12 bg-orange-50 rounded-lg flex items-center justify-center">
                            <i className="fas fa-bell text-orange-500 text-xl"></i>
                        </div>
                    </div>
                    <p className="text-gray-400 text-sm mt-2">Awaiting action</p>
                </div>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Stage Distribution */}
                <div className="bg-white rounded-xl shadow-sm p-6">
                    <h3 className="font-bold text-gray-800 mb-4">Converts by Stage</h3>
                    <div className="space-y-3">
                        {Object.entries(stageDist).map(([stage, count]) => (
                            <div key={stage} className="flex items-center">
                                <span className="w-32 text-sm text-gray-600 capitalize">
                                    {getStageLabel(stage)}
                                </span>
                                <div className="flex-1 mx-3">
                                    <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                                        <div 
                                            className="h-full bg-primary rounded-full transition-all"
                                            style={{ 
                                                width: `${(count / (stats?.total_converts || 1)) * 100}%` 
                                            }}
                                        ></div>
                                    </div>
                                </div>
                                <span className="w-10 text-sm font-medium text-gray-800">{count}</span>
                            </div>
                        ))}
                    </div>
                </div>
                
                {/* Recent Activity */}
                <div className="bg-white rounded-xl shadow-sm p-6">
                    <h3 className="font-bold text-gray-800 mb-4">Recent Activity</h3>
                    <div className="space-y-4 max-h-80 overflow-y-auto">
                        {recentActivity.map((activity, index) => (
                            <div key={index} className="flex items-start gap-3">
                                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                                    activity.type === 'voice_call' 
                                        ? 'bg-purple-50 text-purple-500' 
                                        : 'bg-blue-50 text-blue-500'
                                }`}>
                                    <i className={`fas ${
                                        activity.type === 'voice_call' ? 'fa-phone' : 'fa-user-plus'
                                    } text-sm`}></i>
                                </div>
                                <div className="flex-1">
                                    <p className="text-sm text-gray-800">{activity.message}</p>
                                    <p className="text-xs text-gray-400">
                                        {formatDate(activity.timestamp)}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

// Converts Component
function Converts() {
    const [converts, setConverts] = useState([]);
    const [search, setSearch] = useState('');
    const [stageFilter, setStageFilter] = useState('');
    const [loading, setLoading] = useState(true);
    const [selectedConvert, setSelectedConvert] = useState(null);
    const [viewMode, setViewMode] = useState('list');
    
    useEffect(() => {
        loadConverts();
    }, []);
    
    const loadConverts = async () => {
        try {
            const params = new URLSearchParams();
            if (stageFilter) params.append('stage', stageFilter);
            if (search) params.append('search', search);
            
            const data = await api.get(`/converts?${params.toString()}`);
            setConverts(data);
        } catch (err) {
            console.error('Error loading converts:', err);
        } finally {
            setLoading(false);
        }
    };
    
    const handleSearch = (e) => {
        e.preventDefault();
        loadConverts();
    };
    
    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <i className="fas fa-spinner fa-spin text-3xl text-primary"></i>
            </div>
        );
    }
    
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold text-gray-800">Converts</h1>
                <div className="flex gap-3">
                    <div className="flex bg-gray-100 rounded-lg p-1">
                        <button
                            onClick={() => setViewMode('list')}
                            className={`px-4 py-2 rounded-md transition-colors ${viewMode === 'list' ? 'bg-white text-gray-800 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
                        >
                            <i className="fas fa-list mr-2"></i>List
                        </button>
                        <button
                            onClick={() => setViewMode('kanban')}
                            className={`px-4 py-2 rounded-md transition-colors ${viewMode === 'kanban' ? 'bg-white text-gray-800 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
                        >
                            <i className="fas fa-columns mr-2"></i>Kanban
                        </button>
                    </div>
                    <button className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary-dark transition-colors">
                        <i className="fas fa-plus mr-2"></i>Add Convert
                    </button>
                </div>
            </div>
            
            {/* Filters */}
            <form onSubmit={handleSearch} className="flex gap-4">
                <div className="flex-1 relative">
                    <i className="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
                    <input
                        type="text"
                        placeholder="Search by name or phone..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500"
                    />
                </div>
                <select
                    value={stageFilter}
                    onChange={(e) => setStageFilter(e.target.value)}
                    className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500"
                >
                    <option value="">All Stages</option>
                    {Object.values(ConvertStage).map(stage => (
                        <option key={stage} value={stage}>{getStageLabel(stage)}</option>
                    ))}
                </select>
                <button type="submit" className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200">
                    <i className="fas fa-filter mr-2"></i>Filter
                </button>
            </form>
            
            {/* Kanban View */}
            {viewMode === 'kanban' && (
                <div className="flex gap-4 overflow-x-auto pb-4 kanban-container">
                    {[
                        {id: 'new', label: 'New', color: 'bg-orange-500', bg: 'bg-orange-50'},
                        {id: 'in_followup', label: 'In Follow-up', color: 'bg-yellow-500', bg: 'bg-yellow-50'},
                        {id: 'in_classes', label: 'In Classes', color: 'bg-blue-500', bg: 'bg-blue-50'},
                        {id: 'in_house_fellowship', label: 'House Fellowship', color: 'bg-purple-500', bg: 'bg-purple-50'},
                        {id: 'established', label: 'Established', color: 'bg-green-500', bg: 'bg-green-50'},
                        {id: 'inactive', label: 'Inactive', color: 'bg-gray-500', bg: 'bg-gray-50'}
                    ].map(col => {
                        const colConverts = converts.filter(c => c.stage === col.id);
                        return (
                            <div key={col.id} className={`flex-shrink-0 w-72 ${col.bg} rounded-xl`}>
                                <div className={`${col.color} text-white px-4 py-3 rounded-t-xl flex justify-between items-center`}>
                                    <span className="font-semibold">{col.label}</span>
                                    <span className="bg-white/20 px-2 py-1 rounded-full text-sm">{colConverts.length}</span>
                                </div>
                                <div className="p-3 space-y-3">
                                    {colConverts.map(convert => (
                                        <div key={convert.id} onClick={() => setSelectedConvert(convert)} className="bg-white rounded-lg p-3 shadow-sm cursor-pointer hover:shadow-md">
                                            <div className="flex items-center gap-2 mb-2">
                                                <div className="w-8 h-8 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
                                                    {convert.first_name[0]}{convert.last_name[0]}
                                                </div>
                                                <div className="flex-1 min-w-0">
                                                    <p className="font-medium text-gray-800 text-sm truncate">{convert.first_name} {convert.last_name}</p>
                                                    <p className="text-xs text-gray-500">{formatPhone(convert.phone)}</p>
                                                </div>
                                                <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${getHealthScoreClass(convert.health_score || 0)}`}>
                                                    {convert.health_score || '-'}
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                    {colConverts.length === 0 && (
                                        <div className="text-center py-8 text-gray-400">
                                            <p className="text-sm">No converts</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
            
            {/* List View */}
            {viewMode === 'list' && (
            <div className="bg-white rounded-xl shadow-sm overflow-hidden">
            <div className="bg-white rounded-xl shadow-sm overflow-hidden">
                <table className="w-full">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Convert</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Contact</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Stage</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Health</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                        {converts.map(convert => (
                            <tr key={convert.id} className="hover:bg-gray-50">
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center text-white font-medium">
                                            {convert.first_name[0]}{convert.last_name[0]}
                                        </div>
                                        <div>
                                            <p className="font-medium text-gray-800">
                                                {convert.first_name} {convert.last_name}
                                            </p>
                                            <p className="text-sm text-gray-500">{convert.occupation || '-'}</p>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4">
                                    <p className="text-sm text-gray-800">{formatPhone(convert.phone)}</p>
                                    <p className="text-sm text-gray-500">{convert.city || '-'}</p>
                                </td>
                                <td className="px-6 py-4">
                                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStageColor(convert.stage)}`}>
                                        {getStageLabel(convert.stage)}
                                    </span>
                                </td>
                                <td className="px-6 py-4">
                                    <div className={`health-score-ring ${getHealthScoreClass(convert.health_score || 0)}`}>
                                        {convert.health_score || '-'}
                                    </div>
                                </td>
                                <td className="px-6 py-4">
                                    <div className="flex gap-2">
                                        <button 
                                            onClick={() => setSelectedConvert(convert)}
                                            className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg"
                                            title="View Details"
                                        >
                                            <i className="fas fa-eye"></i>
                                        </button>
                                        <button className="p-2 text-green-600 hover:bg-green-50 rounded-lg" title="Call">
                                            <i className="fas fa-phone"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            )}
            
            {/* Convert Detail Modal */}
            {selectedConvert && (
                <ConvertModal 
                    convert={selectedConvert} 
                    onClose={() => setSelectedConvert(null)} 
                />
            )}
        </div>
    );
}

// Convert Modal Component
function ConvertModal({ convert, onClose }) {
    const [healthScore, setHealthScore] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        loadHealthScore();
    }, []);
    
    const loadHealthScore = async () => {
        try {
            const data = await api.get(`/health-scores/${convert.id}`);
            setHealthScore(data);
        } catch (err) {
            console.error('Error loading health score:', err);
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto fade-in">
                <div className="p-6 border-b flex items-center justify-between">
                    <h2 className="text-xl font-bold text-gray-800">Convert Details</h2>
                    <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
                        <i className="fas fa-times text-xl"></i>
                    </button>
                </div>
                
                <div className="p-6 space-y-6">
                    {/* Header Info */}
                    <div className="flex items-center gap-4">
                        <div className="w-20 h-20 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                            {convert.first_name[0]}{convert.last_name[0]}
                        </div>
                        <div>
                            <h3 className="text-xl font-bold text-gray-800">
                                {convert.first_name} {convert.last_name}
                            </h3>
                            <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium mt-1 ${getStageColor(convert.stage)}`}>
                                {getStageLabel(convert.stage)}
                            </span>
                        </div>
                        <div className="ml-auto">
                            <div className={`health-score-ring ${getHealthScoreClass(convert.health_score || 0)}`}>
                                {convert.health_score || '-'}
                            </div>
                        </div>
                    </div>
                    
                    {/* Contact Info */}
                    <div className="grid grid-cols-2 gap-4">
                        <div className="p-4 bg-gray-50 rounded-lg">
                            <p className="text-sm text-gray-500">Phone</p>
                            <p className="font-medium text-gray-800">{formatPhone(convert.phone)}</p>
                        </div>
                        <div className="p-4 bg-gray-50 rounded-lg">
                            <p className="text-sm text-gray-500">Email</p>
                            <p className="font-medium text-gray-800">{convert.email || '-'}</p>
                        </div>
                        <div className="p-4 bg-gray-50 rounded-lg">
                            <p className="text-sm text-gray-500">Location</p>
                            <p className="font-medium text-gray-800">{convert.city || '-'}, {convert.state || '-'}</p>
                        </div>
                        <div className="p-4 bg-gray-50 rounded-lg">
                            <p className="text-sm text-gray-500">Occupation</p>
                            <p className="font-medium text-gray-800">{convert.occupation || '-'}</p>
                        </div>
                    </div>
                    
                    {/* Health Score Factors */}
                    {healthScore && healthScore.factors && (
                        <div>
                            <h4 className="font-semibold text-gray-800 mb-3">Health Score Factors</h4>
                            <div className="grid grid-cols-2 gap-4">
                                {Object.entries(healthScore.factors).map(([key, value]) => (
                                    <div key={key} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                        <span className="text-sm text-gray-600 capitalize">
                                            {key.replace(/_/g, ' ')}
                                        </span>
                                        <div className="flex items-center gap-2">
                                            <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                                                <div 
                                                    className="h-full bg-primary rounded-full"
                                                    style={{ width: `${value}%` }}
                                                ></div>
                                            </div>
                                            <span className="text-sm font-medium w-8">{value}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                    
                    {/* Notes */}
                    {convert.notes && (
                        <div>
                            <h4 className="font-semibold text-gray-800 mb-2">Notes</h4>
                            <p className="text-gray-600 p-4 bg-amber-50 rounded-lg">{convert.notes}</p>
                        </div>
                    )}
                </div>
                
                <div className="p-6 border-t flex justify-end gap-3">
                    <button onClick={onClose} className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg">
                        Close
                    </button>
                    <button className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark">
                        <i className="fas fa-phone mr-2"></i>Call Now
                    </button>
                </div>
            </div>
        </div>
    );
}

// Alerts Component
function Alerts() {
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('');
    
    useEffect(() => {
        loadAlerts();
    }, []);
    
    const loadAlerts = async () => {
        try {
            const params = filter ? `?status=${filter}` : '';
            const data = await api.get(`/alerts${params}`);
            setAlerts(data);
        } catch (err) {
            console.error('Error loading alerts:', err);
        } finally {
            setLoading(false);
        }
    };
    
    const handleUpdateStatus = async (alertId, newStatus) => {
        try {
            await api.patch(`/alerts/${alertId}`, { status: newStatus });
            loadAlerts();
        } catch (err) {
            console.error('Error updating alert:', err);
        }
    };
    
    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <i className="fas fa-spinner fa-spin text-3xl text-primary"></i>
            </div>
        );
    }
    
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold text-gray-800">Alerts</h1>
                <select 
                    value={filter}
                    onChange={(e) => { setFilter(e.target.value); loadAlerts(); }}
                    className="px-4 py-2 border border-gray-300 rounded-lg"
                >
                    <option value="">All Status</option>
                    <option value="open">Open</option>
                    <option value="acknowledged">Acknowledged</option>
                    <option value="in_progress">In Progress</option>
                    <option value="resolved">Resolved</option>
                </select>
            </div>
            
            <div className="space-y-4">
                {alerts.map(alert => (
                    <div key={alert.id} className={`bg-white rounded-xl shadow-sm p-6 alert-${alert.severity}`}>
                        <div className="flex items-start justify-between">
                            <div className="flex-1">
                                <div className="flex items-center gap-3 mb-2">
                                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                                        alert.severity === 'high' ? 'bg-red-100 text-red-700' :
                                        alert.severity === 'medium' ? 'bg-orange-100 text-orange-700' :
                                        'bg-green-100 text-green-700'
                                    }`}>
                                        {alert.severity.toUpperCase()}
                                    </span>
                                    <span className={`px-3 py-1 rounded-full text-xs ${
                                        alert.status === 'open' ? 'bg-blue-100 text-blue-700' :
                                        alert.status === 'resolved' ? 'bg-green-100 text-green-700' :
                                        'bg-gray-100 text-gray-700'
                                    }`}>
                                        {alert.status.replace('_', ' ')}
                                    </span>
                                </div>
                                <h3 className="font-semibold text-gray-800">{alert.title}</h3>
                                <p className="text-gray-600 text-sm mt-1">{alert.description}</p>
                                <p className="text-gray-500 text-sm mt-2">
                                    <i className="fas fa-user mr-1"></i>
                                    {alert.convert_name}
                                    {alert.convert_phone && (
                                        <span className="ml-3">
                                            <i className="fas fa-phone mr-1"></i>
                                            {formatPhone(alert.convert_phone)}
                                        </span>
                                    )}
                                </p>
                            </div>
                            <div className="flex gap-2">
                                {alert.status === 'open' && (
                                    <button 
                                        onClick={() => handleUpdateStatus(alert.id, 'acknowledged')}
                                        className="px-3 py-1 bg-blue-50 text-blue-600 rounded-lg text-sm hover:bg-blue-100"
                                    >
                                        Acknowledge
                                    </button>
                                )}
                                {alert.status !== 'resolved' && (
                                    <button 
                                        onClick={() => handleUpdateStatus(alert.id, 'resolved')}
                                        className="px-3 py-1 bg-green-50 text-green-600 rounded-lg text-sm hover:bg-green-100"
                                    >
                                        Resolve
                                    </button>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
                
                {alerts.length === 0 && (
                    <div className="text-center py-12 text-gray-500">
                        <i className="fas fa-check-circle text-4xl mb-3 text-green-500"></i>
                        <p>No alerts found</p>
                    </div>
                )}
            </div>
        </div>
    );
}

// Voice Agent Component
function VoiceAgent() {
    const [calls, setCalls] = useState([]);
    const [scripts, setScripts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('calls');
    const [selectedCall, setSelectedCall] = useState(null);
    
    useEffect(() => {
        loadData();
    }, []);
    
    const loadData = async () => {
        try {
            const [callsData, scriptsData] = await Promise.all([
                api.get('/voice-agent/calls'),
                api.get('/voice-agent/scripts')
            ]);
            setCalls(callsData);
            setScripts(scriptsData);
        } catch (err) {
            console.error('Error loading voice agent data:', err);
        } finally {
            setLoading(false);
        }
    };
    
    const handleSimulateCall = async (callId) => {
        try {
            const result = await api.post(`/voice-agent/calls/${callId}/simulate`, {});
            setSelectedCall(result.call);
            loadData();
        } catch (err) {
            console.error('Error simulating call:', err);
        }
    };
    
    const getStatusColor = (status) => {
        const colors = {
            completed: 'bg-green-100 text-green-700',
            scheduled: 'bg-blue-100 text-blue-700',
            in_progress: 'bg-yellow-100 text-yellow-700',
            failed: 'bg-red-100 text-red-700',
            no_answer: 'bg-gray-100 text-gray-700'
        };
        return colors[status] || 'bg-gray-100';
    };
    
    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <i className="fas fa-spinner fa-spin text-3xl text-primary"></i>
            </div>
        );
    }
    
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-3">
                        <i className="fas fa-robot text-primary"></i>
                        Voice Agent
                    </h1>
                    <p className="text-gray-500">AI-powered voice calling for convert follow-up</p>
                </div>
                <div className="flex items-center gap-2 bg-green-50 text-green-700 px-4 py-2 rounded-lg">
                    <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                    <span className="font-medium">Agent Active</span>
                </div>
            </div>
            
            {/* Tabs */}
            <div className="flex gap-4 border-b">
                {['calls', 'scripts'].map(tab => (
                    <button
                        key={tab}
                        onClick={() => setActiveTab(tab)}
                        className={`px-4 py-3 font-medium capitalize transition-colors ${
                            activeTab === tab 
                                ? 'text-primary border-b-2 border-primary' 
                                : 'text-gray-500 hover:text-gray-700'
                        }`}
                    >
                        {tab}
                    </button>
                ))}
            </div>
            
            {/* Calls Tab */}
            {activeTab === 'calls' && (
                <div className="space-y-4">
                    {calls.map(call => (
                        <div key={call.id} className="bg-white rounded-xl shadow-sm p-6">
                            <div className="flex items-start justify-between">
                                <div className="flex-1">
                                    <div className="flex items-center gap-3 mb-2">
                                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(call.status)}`}>
                                            {call.status.replace('_', ' ')}
                                        </span>
                                        {call.outcome && (
                                            <span className="text-sm text-gray-500">
                                                Outcome: <span className="font-medium capitalize">{call.outcome}</span>
                                            </span>
                                        )}
                                    </div>
                                    <h3 className="font-semibold text-lg text-gray-800">{call.convert_name}</h3>
                                    <p className="text-gray-500">
                                        <i className="fas fa-phone mr-2"></i>
                                        {formatPhone(call.convert_phone)}
                                    </p>
                                    {call.duration_seconds && (
                                        <p className="text-sm text-gray-400 mt-1">
                                            <i className="fas fa-clock mr-1"></i>
                                            Duration: {Math.round(call.duration_seconds / 60)} minutes
                                        </p>
                                    )}
                                </div>
                                <div className="flex flex-col gap-2">
                                    {call.status === 'scheduled' && (
                                        <button
                                            onClick={() => handleSimulateCall(call.id)}
                                            className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark"
                                        >
                                            <i className="fas fa-play mr-2"></i>Simulate Call
                                        </button>
                                    )}
                                    <button
                                        onClick={() => setSelectedCall(call)}
                                        className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                                    >
                                        View Details
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                    
                    {calls.length === 0 && (
                        <div className="text-center py-12 text-gray-500">
                            <i className="fas fa-phone-slash text-4xl mb-3"></i>
                            <p>No voice calls found</p>
                        </div>
                    )}
                </div>
            )}
            
            {/* Scripts Tab */}
            {activeTab === 'scripts' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {scripts.map(script => (
                        <div key={script.id} className="bg-white rounded-xl shadow-sm p-6">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="font-semibold text-gray-800">{script.name}</h3>
                                <span className="text-xs text-gray-500 capitalize">{script.purpose}</span>
                            </div>
                            <p className="text-gray-600 text-sm p-4 bg-gray-50 rounded-lg">
                                &quot;{script.content}&quot;
                            </p>
                        </div>
                    ))}
                </div>
            )}
            
            {/* Call Detail Modal */}
            {selectedCall && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto fade-in">
                        <div className="p-6 border-b flex items-center justify-between">
                            <h2 className="text-xl font-bold text-gray-800">Call Details</h2>
                            <button onClick={() => setSelectedCall(null)} className="text-gray-400 hover:text-gray-600">
                                <i className="fas fa-times text-xl"></i>
                            </button>
                        </div>
                        
                        <div className="p-6 space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="p-4 bg-gray-50 rounded-lg">
                                    <p className="text-sm text-gray-500">Convert</p>
                                    <p className="font-medium text-gray-800">{selectedCall.convert_name}</p>
                                </div>
                                <div className="p-4 bg-gray-50 rounded-lg">
                                    <p className="text-sm text-gray-500">Phone</p>
                                    <p className="font-medium text-gray-800">{formatPhone(selectedCall.convert_phone)}</p>
                                </div>
                                <div className="p-4 bg-gray-50 rounded-lg">
                                    <p className="text-sm text-gray-500">Status</p>
                                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium capitalize ${getStatusColor(selectedCall.status)}`}>
                                        {selectedCall.status.replace('_', ' ')}
                                    </span>
                                </div>
                                <div className="p-4 bg-gray-50 rounded-lg">
                                    <p className="text-sm text-gray-500">Duration</p>
                                    <p className="font-medium text-gray-800">
                                        {selectedCall.duration_seconds 
                                            ? `${Math.round(selectedCall.duration_seconds / 60)} minutes` 
                                            : '-'}
                                    </p>
                                </div>
                            </div>
                            
                            {selectedCall.transcript && (
                                <div>
                                    <h4 className="font-semibold text-gray-800 mb-3">Transcript</h4>
                                    <div className="p-4 bg-gray-50 rounded-lg text-gray-600 text-sm">
                                        {selectedCall.transcript}
                                    </div>
                                </div>
                            )}
                            
                            {selectedCall.notes && (
                                <div>
                                    <h4 className="font-semibold text-gray-800 mb-2">Notes</h4>
                                    <p className="p-4 bg-amber-50 rounded-lg text-gray-600">{selectedCall.notes}</p>
                                </div>
                            )}
                        </div>
                        
                        <div className="p-6 border-t flex justify-end">
                            <button onClick={() => setSelectedCall(null)} className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg">
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

// Analytics Component
function Analytics() {
    const [convertAnalytics, setConvertAnalytics] = useState(null);
    const [voiceAnalytics, setVoiceAnalytics] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        loadAnalytics();
    }, []);
    
    const loadAnalytics = async () => {
        try {
            const [convertData, voiceData] = await Promise.all([
                api.get('/analytics/converts'),
                api.get('/analytics/voice-calls')
            ]);
            setConvertAnalytics(convertData);
            setVoiceAnalytics(voiceData);
        } catch (err) {
            console.error('Error loading analytics:', err);
        } finally {
            setLoading(false);
        }
    };
    
    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <i className="fas fa-spinner fa-spin text-3xl text-primary"></i>
            </div>
        );
    }
    
    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-800">Analytics</h1>
            
            {/* Voice Call Analytics */}
            <div className="bg-white rounded-xl shadow-sm p-6">
                <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
                    <i className="fas fa-phone-alt text-primary"></i>
                    Voice Call Analytics
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                        <p className="text-3xl font-bold text-gray-800">{voiceAnalytics?.total_calls || 0}</p>
                        <p className="text-sm text-gray-500">Total Calls</p>
                    </div>
                    <div className="text-center p-4 bg-green-50 rounded-lg">
                        <p className="text-3xl font-bold text-green-600">{voiceAnalytics?.completed || 0}</p>
                        <p className="text-sm text-gray-500">Completed</p>
                    </div>
                    <div className="text-center p-4 bg-blue-50 rounded-lg">
                        <p className="text-3xl font-bold text-blue-600">{voiceAnalytics?.success_rate || 0}%</p>
                        <p className="text-sm text-gray-500">Success Rate</p>
                    </div>
                    <div className="text-center p-4 bg-purple-50 rounded-lg">
                        <p className="text-3xl font-bold text-purple-600">
                            {Math.round((voiceAnalytics?.average_duration_seconds || 0) / 60)}
                        </p>
                        <p className="text-sm text-gray-500">Avg Duration (min)</p>
                    </div>
                </div>
            </div>
            
            {/* Convert Analytics */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white rounded-xl shadow-sm p-6">
                    <h3 className="font-bold text-gray-800 mb-4">Converts by Source</h3>
                    <div className="space-y-3">
                        {convertAnalytics?.by_source && Object.entries(convertAnalytics.by_source).map(([source, count]) => (
                            <div key={source} className="flex items-center">
                                <span className="w-24 text-sm text-gray-600 capitalize">{source}</span>
                                <div className="flex-1 mx-3">
                                    <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                                        <div 
                                            className="h-full bg-secondary rounded-full"
                                            style={{ width: `${(count / (convertAnalytics?.total || 1)) * 100}%` }}
                                        ></div>
                                    </div>
                                </div>
                                <span className="w-10 text-sm font-medium text-gray-800">{count}</span>
                            </div>
                        ))}
                    </div>
                </div>
                
                <div className="bg-white rounded-xl shadow-sm p-6">
                    <h3 className="font-bold text-gray-800 mb-4">Monthly Trend</h3>
                    <div className="space-y-3">
                        {convertAnalytics?.monthly_trend && Object.entries(convertAnalytics.monthly_trend)
                            .sort()
                            .map(([month, count]) => (
                            <div key={month} className="flex items-center">
                                <span className="w-20 text-sm text-gray-600">{month}</span>
                                <div className="flex-1 mx-3">
                                    <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                                        <div 
                                            className="h-full bg-primary rounded-full"
                                            style={{ width: `${(count / 50) * 100}%` }}
                                        ></div>
                                    </div>
                                </div>
                                <span className="w-10 text-sm font-medium text-gray-800">{count}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

// Main App Component
function App() {
    const [user, setUser] = useState(null);
    const [activeTab, setActiveTab] = useState('dashboard');
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        // Small delay to ensure localStorage is ready and prevent flash
        const timer = setTimeout(() => {
            const savedUser = localStorage.getItem('user');
            const token = localStorage.getItem('token');
            // Only set user if both user data AND token exist
            if (savedUser && token) {
                try {
                    setUser(JSON.parse(savedUser));
                } catch (e) {
                    // Invalid JSON in localStorage, clear it
                    localStorage.removeItem('user');
                    localStorage.removeItem('token');
                }
            }
            setLoading(false);
        }, 100);
        
        return () => clearTimeout(timer);
    }, []);
    
    const handleLogin = (userData) => {
        setUser(userData);
    };
    
    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-50">
                <div className="text-center">
                    <i className="fas fa-spinner fa-spin text-4xl text-primary mb-4"></i>
                    <p className="text-gray-600">Loading...</p>
                </div>
            </div>
        );
    }
    
    if (!user) {
        return <Login onLogin={handleLogin} />;
    }
    
    const renderContent = () => {
        switch (activeTab) {
            case 'dashboard': return <Dashboard />;
            case 'converts': return <Converts />;
            case 'alerts': return <Alerts />;
            case 'voice-agent': return <VoiceAgent />;
            case 'analytics': return <Analytics />;
            default: return <Dashboard />;
        }
    };
    
    return (
        <div className="min-h-screen bg-gray-50">
            <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} user={user} />
            <main className="ml-64 p-8">
                {renderContent()}
            </main>
        </div>
    );
}

// Mount the app
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
