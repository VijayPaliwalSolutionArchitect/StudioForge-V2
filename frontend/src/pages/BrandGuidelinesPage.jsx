import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function BrandGuidelinesPage() {
  const [brands, setBrands] = useState([]);
  const [name, setName] = useState('');
  const [industry, setIndustry] = useState('');
  const [tone, setTone] = useState('Authoritative, Visionary, Sovereign');
  const [tagline, setTagline] = useState('');
  const [primaryColor, setPrimaryColor] = useState('#06b6d4');
  const [secondaryColor, setSecondaryColor] = useState('#3b82f6');
  const [forbidden, setForbidden] = useState('cheap, hacky, quick fix, crypto pump');
  const [personas, setPersonas] = useState('Chief Technology Officers, General Counsel');

  const fetchBrands = async () => {
    try {
      const res = await axios.get('/api/v1/brands');
      setBrands(res.data);
    } catch (err) {
      console.error('Failed to fetch brands:', err);
    }
  };

  useEffect(() => {
    fetchBrands();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/v1/brands', {
        name,
        industry,
        tone_of_voice: tone,
        tagline,
        primary_color_hex: primaryColor,
        secondary_color_hex: secondaryColor,
        forbidden_words: forbidden.split(',').map((s) => s.trim()).filter(Boolean),
        target_personas: personas.split(',').map((s) => s.trim()).filter(Boolean),
      });
      setName('');
      setIndustry('');
      setTagline('');
      fetchBrands();
    } catch (err) {
      alert('Failed to create brand: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div style={{ padding: '0 24px 32px 24px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#fff' }}>🎨 Brand Identity Guidelines & Voice Matrix</h2>
        <p style={{ fontSize: '13px', color: '#94a3b8' }}>
          Define core brand pillars, mandatory hex color schemes, forbidden terminology, and ICP personas
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Brand Creation Form */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#fff', marginBottom: '12px' }}>
            + Register Brand Identity
          </h3>
          <form onSubmit={handleCreate} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <div>
                <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Brand Name</label>
                <input
                  className="glass-input"
                  style={{ width: '100%', fontSize: '12px' }}
                  placeholder="e.g. Apex Sovereign AI"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
              <div>
                <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Industry</label>
                <input
                  className="glass-input"
                  style={{ width: '100%', fontSize: '12px' }}
                  placeholder="e.g. Defense Intelligence"
                  value={industry}
                  onChange={(e) => setIndustry(e.target.value)}
                  required
                />
              </div>
            </div>

            <div>
              <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Tone of Voice Pillars</label>
              <input
                className="glass-input"
                style={{ width: '100%', fontSize: '12px' }}
                value={tone}
                onChange={(e) => setTone(e.target.value)}
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <div>
                <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Primary Hex Accent</label>
                <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                  <input
                    type="color"
                    value={primaryColor}
                    onChange={(e) => setPrimaryColor(e.target.value)}
                    style={{ width: '36px', height: '36px', border: 'none', background: 'transparent', cursor: 'pointer' }}
                  />
                  <input
                    className="glass-input"
                    style={{ flex: 1, fontSize: '12px' }}
                    value={primaryColor}
                    onChange={(e) => setPrimaryColor(e.target.value)}
                  />
                </div>
              </div>

              <div>
                <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Secondary Hex Accent</label>
                <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                  <input
                    type="color"
                    value={secondaryColor}
                    onChange={(e) => setSecondaryColor(e.target.value)}
                    style={{ width: '36px', height: '36px', border: 'none', background: 'transparent', cursor: 'pointer' }}
                  />
                  <input
                    className="glass-input"
                    style={{ flex: 1, fontSize: '12px' }}
                    value={secondaryColor}
                    onChange={(e) => setSecondaryColor(e.target.value)}
                  />
                </div>
              </div>
            </div>

            <div>
              <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Forbidden Words (Comma separated)</label>
              <input
                className="glass-input"
                style={{ width: '100%', fontSize: '12px' }}
                value={forbidden}
                onChange={(e) => setForbidden(e.target.value)}
              />
            </div>

            <button type="submit" className="btn-primary" style={{ marginTop: '8px' }}>
              Save Brand Guidelines
            </button>
          </form>
        </div>

        {/* Brand Catalog List */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#fff', marginBottom: '12px' }}>
            Active Brand Guidelines ({brands.length})
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxHeight: '460px', overflowY: 'auto' }}>
            {brands.map((b) => (
              <div key={b.id} className="glass-card" style={{ padding: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <h4 style={{ fontSize: '15px', fontWeight: 700, color: '#fff' }}>{b.name}</h4>
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <div style={{ width: '16px', height: '16px', borderRadius: '4px', background: b.primary_color_hex }}></div>
                    <div style={{ width: '16px', height: '16px', borderRadius: '4px', background: b.secondary_color_hex }}></div>
                  </div>
                </div>
                <div style={{ fontSize: '12px', color: '#c084fc', marginBottom: '6px' }}>
                  Tone: {b.tone_of_voice}
                </div>
                <div style={{ fontSize: '11px', color: '#94a3b8', marginBottom: '6px' }}>
                  Industry: <strong style={{ color: '#cbd5e1' }}>{b.industry}</strong>
                </div>
                <div style={{ fontSize: '10px', color: '#f43f5e' }}>
                  Forbidden Words ({b.forbidden_words?.length || 0}): {b.forbidden_words?.slice(0, 4).join(', ')}...
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
