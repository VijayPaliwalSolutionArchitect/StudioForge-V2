import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import CreativeBriefsPage from './pages/CreativeBriefsPage';
import BrandGuidelinesPage from './pages/BrandGuidelinesPage';
import CampaignStudioPage from './pages/CampaignStudioPage';
import AssetGalleryPage from './pages/AssetGalleryPage';
import ContentCalendarPage from './pages/ContentCalendarPage';
import ApprovalsPage from './pages/ApprovalsPage';

export default function App() {
  const [activeTab, setActiveTab] = useState('briefs');
  const [stats, setStats] = useState(null);

  const fetchStats = async () => {
    try {
      const res = await axios.get('/api/v1/admin/stats');
      setStats(res.data);
    } catch (err) {
      console.error('Failed to fetch admin stats:', err);
    }
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} stats={stats} />

      <main style={{ flex: 1 }}>
        {activeTab === 'briefs' && <CreativeBriefsPage />}
        {activeTab === 'brands' && <BrandGuidelinesPage />}
        {activeTab === 'campaigns' && <CampaignStudioPage />}
        {activeTab === 'assets' && <AssetGalleryPage />}
        {activeTab === 'calendar' && <ContentCalendarPage />}
        {activeTab === 'approvals' && <ApprovalsPage />}
      </main>

      <footer style={{
        padding: '16px 24px',
        borderTop: '1px solid rgba(255,255,255,0.06)',
        display: 'flex',
        justifyContent: 'space-between',
        fontSize: '11px',
        color: '#64748b'
      }}>
        <div>StudioForge V2 • Shivam ITCS Autonomous AI Fleet • Port 8097</div>
        <div>Two-Man Rule: <span style={{ color: '#10b981' }}>ENFORCED</span> • ComfyUI Headless: <span style={{ color: '#c084fc' }}>STANDBY</span></div>
      </footer>
    </div>
  );
}
