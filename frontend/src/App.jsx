import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Monitoring from './pages/Monitoring';
import RouteOptimizer from './pages/RouteOptimizer';
import Simulator from './pages/Simulator';
import SignalAdvisory from './pages/SignalAdvisory';
import { networkAPI } from './api/client';

export default function App() {
  const [networkSummary, setNetworkSummary] = useState(null);

  const fetchSummary = async () => {
    try {
      const res = await networkAPI.getGraph();
      setNetworkSummary(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchSummary();
    const interval = setInterval(fetchSummary, 6000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <div className="app-container">
        <Sidebar />
        <div className="main-content">
          <Navbar networkSummary={networkSummary} onRefresh={fetchSummary} />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/monitoring" element={<Monitoring />} />
            <Route path="/map" element={<Dashboard />} />
            <Route path="/routing" element={<RouteOptimizer />} />
            <Route path="/simulator" element={<Simulator />} />
            <Route path="/signals" element={<SignalAdvisory />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}
