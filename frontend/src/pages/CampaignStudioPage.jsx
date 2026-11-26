import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function CampaignStudioPage() {
  const [campaigns, setCampaigns] = useState([]);
  const [brands, setBrands] = useState([]);
  const [name, setName] = useState('');
  const [brandId, setBrandId] = useState('');
  const [objective, setObjective] = useState('LEAD_GEN');
  const [budget, setBudget] = useState(15000);
  const [isPaid, setIsPaid] = useState(true);

  const fetchData = async () => {
    try {
      const [campRes, brandRes] = await Promise.all([
        axios.get('/api/v1/campaigns'),
        axios.get('/api/v1/brands'),
      ]);
      setCampaigns(campRes.data);
      setBrands(brandRes.data);
      if (brandRes.data.length > 0) setBrandId(brandRes.data[0].id);
    } catch (err) {
      console.error('Failed to fetch campaigns:', err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/v1/campaigns', {
        brand_id: brandId,
        name,
        objective,
        budget_usd: parseFloat(budget),
        is_paid: isPaid,
      });
      setName('');
      fetchData();
    } catch (err) {
      alert('Failed to create campaign: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div style={{ padding: '0 24px 32px 24px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#fff' }}>🚀 Marketing Campaigns & Budget Governance</h2>
        <p style={{ fontSize: '13px', color: '#94a3b8' }}>
          Multi-channel campaign orchestration with automated Two-Man approval gating on paid advertising budgets
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Create Campaign Form */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#fff', marginBottom: '12px' }}>
            + Launch New Campaign
          </h3>
          <form onSubmit={handleCreate} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div>
              <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Campaign Name</label>
              <input
                className="glass-input"
                style={{ width: '100%', fontSize: '12px' }}
                placeholder="e.g. Q1 Defense Autonomous AI Launch"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <div>
                <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Brand</label>
                <select
                  className="glass-input"
                  style={{ width: '100%', fontSize: '12px' }}
                  value={brandId}
                  onChange={(e) => setBrandId(e.target.value)}
                >
                  {brands.map((b) => (
                    <option key={b.id} value={b.id}>{b.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Objective</label>
                <select
                  className="glass-input"
                  style={{ width: '100%', fontSize: '12px' }}
                  value={objective}
                  onChange={(e) => setObjective(e.target.value)}
                >
                  <option value="AWARENESS">Brand Awareness</option>
                  <option value="LEAD_GEN">Enterprise Lead Gen</option>
                  <option value="PRODUCT_LAUNCH">Product Launch</option>
                  <option value="CONVERSION">Paid Conversion</option>
                </select>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <div>
                <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Budget (USD)</label>
                <input
                  type="number"
                  className="glass-input"
                  style={{ width: '100%', fontSize: '12px' }}
                  value={budget}
                  onChange={(e) => setBudget(e.target.value)}
                />
              </div>

              <div>
                <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Campaign Type</label>
                <select
                  className="glass-input"
                  style={{ width: '100%', fontSize: '12px' }}
                  value={isPaid ? 'PAID' : 'ORGANIC'}
                  onChange={(e) => setIsPaid(e.target.value === 'PAID')}
                >
                  <option value="PAID">Paid Ads (Requires Two-Man Rule)</option>
                  <option value="ORGANIC">Organic Social (Direct Publish)</option>
                </select>
              </div>
            </div>

            <button type="submit" className="btn-primary" style={{ marginTop: '8px' }}>
              Create Campaign
            </button>
          </form>
        </div>

        {/* Campaigns List */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#fff', marginBottom: '12px' }}>
            Active Campaigns ({campaigns.length})
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '460px', overflowY: 'auto' }}>
            {campaigns.map((c) => (
              <div key={c.id} className="glass-card" style={{ padding: '14px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                  <h4 style={{ fontSize: '14px', fontWeight: 700, color: '#fff' }}>{c.name}</h4>
                  <span className={`badge ${c.is_paid_campaign ? 'badge-topsecret' : 'badge-airgap'}`}>
                    {c.is_paid_campaign ? 'PAID MEDIA' : 'ORGANIC'}
                  </span>
                </div>
                <div style={{ display: 'flex', gap: '16px', fontSize: '11px', color: '#94a3b8', marginTop: '6px' }}>
                  <span>Objective: <strong style={{ color: '#cbd5e1' }}>{c.objective}</strong></span>
                  <span>Budget: <strong style={{ color: '#10b981' }}>${c.budget_usd.toLocaleString()}</strong></span>
                  <span>Status: <strong style={{ color: '#38bdf8' }}>{c.status}</strong></span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
