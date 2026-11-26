import React from 'react';

export default function Navbar({ activeTab, setActiveTab, stats }) {
  const tabs = [
    { id: 'briefs', label: '✨ Creative Briefs & Prompts' },
    { id: 'brands', label: '🎨 Brand Guidelines' },
    { id: 'campaigns', label: '🚀 Campaigns' },
    { id: 'assets', label: '🖼️ Asset Gallery' },
    { id: 'calendar', label: '📅 Content Calendar' },
    { id: 'approvals', label: '🔒 Two-Man Approvals', badge: stats?.pending_two_man_approvals },
  ];

  return (
    <header className="glass-panel" style={{ margin: '16px 24px', padding: '14px 24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, #a855f7, #06b6d4)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 800,
            fontSize: '22px',
            color: '#fff',
            boxShadow: '0 0 20px rgba(168,85,247,0.45)'
          }}>
            SF
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h1 style={{ fontSize: '18px', fontWeight: 700, letterSpacing: '-0.02em', color: '#fff' }}>StudioForge V2</h1>
              <span className="badge" style={{ background: 'rgba(168,85,247,0.2)', color: '#c084fc', border: '1px solid rgba(168,85,247,0.4)' }}>
                PROD :8097
              </span>
              <span style={{ fontSize: '11px', color: '#64748b', fontWeight: 500 }}>ComfyUI + Flux Engine</span>
            </div>
            <p style={{ fontSize: '12px', color: '#94a3b8' }}>Autonomous AI Brand & Media Factory</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
          {tabs.map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '7px 12px',
                  borderRadius: '8px',
                  fontSize: '12px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  border: isActive ? '1px solid rgba(168, 85, 247, 0.5)' : '1px solid transparent',
                  background: isActive ? 'rgba(168, 85, 247, 0.16)' : 'transparent',
                  color: isActive ? '#c084fc' : '#94a3b8',
                  transition: 'all 0.15s ease'
                }}
              >
                <span>{tab.label}</span>
                {tab.badge > 0 && (
                  <span style={{
                    fontSize: '10px',
                    padding: '1px 6px',
                    borderRadius: '10px',
                    background: '#f43f5e',
                    color: '#fff',
                    fontWeight: 700
                  }}>
                    {tab.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Telemetry pill */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', fontSize: '12px' }}>
          <div style={{ textAlign: 'right' }}>
            <div style={{ color: '#64748b' }}>AI Spend</div>
            <div style={{ fontWeight: 700, color: '#10b981' }}>${stats?.ai_spend?.total_spend_usd?.toFixed(4) || '0.0000'}</div>
          </div>
          <div style={{ height: '24px', width: '1px', background: 'rgba(255,255,255,0.1)' }}></div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ color: '#64748b' }}>ComfyUI Headless</div>
            <div style={{ fontWeight: 700, color: '#38bdf8' }}>:8188 Standby</div>
          </div>
        </div>
      </div>
    </header>
  );
}
