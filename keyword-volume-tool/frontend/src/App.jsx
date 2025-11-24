import React, { useState } from 'react';
import './App.css';

function App() {
  const [keyword, setKeyword] = useState('');
  const [location, setLocation] = useState('México');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const locations = [
    'México',
    'Culiacán',
    'Sinaloa',
    'Guadalajara',
    'CDMX'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!keyword.trim()) {
      setError('Por favor ingresa un keyword');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/keyword-volume', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          keyword: keyword.trim(),
          location: location
        })
      });

      if (!response.ok) {
        throw new Error('Error al obtener datos');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num) => {
    return new Intl.NumberFormat('es-MX').format(num);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔍 Keyword Volume Tool</h1>
        <p className="subtitle">100% Gratis - Google Trends + ML</p>
      </header>

      <main className="container">
        <form onSubmit={handleSubmit} className="search-form">
          <div className="form-group">
            <label htmlFor="keyword">Keyword:</label>
            <input
              type="text"
              id="keyword"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder="Ej: plomero culiacan"
              className="input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="location">Ubicación:</label>
            <select
              id="location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="select"
            >
              {locations.map((loc) => (
                <option key={loc} value={loc}>
                  {loc}
                </option>
              ))}
            </select>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary"
          >
            {loading ? 'Analizando...' : 'Analizar Keyword'}
          </button>
        </form>

        {error && (
          <div className="alert alert-error">
            <strong>Error:</strong> {error}
          </div>
        )}

        {result && (
          <div className="results">
            <div className="result-card">
              <h2>Resultados para "{result.keyword}"</h2>
              <p className="location-tag">📍 {result.location}</p>

              <div className="volume-display">
                <div className="volume-number">
                  {formatNumber(result.volume_estimate)}
                </div>
                <div className="volume-label">Búsquedas/mes (estimado)</div>
              </div>

              <div className="confidence-badge">
                Confianza: <span className={`badge ${result.confidence.toLowerCase()}`}>
                  {result.confidence}
                </span>
              </div>

              <div className="metrics-grid">
                <div className="metric-card">
                  <div className="metric-label">Google Trends Score</div>
                  <div className="metric-value">
                    {result.trend_data.interest_score}/100
                  </div>
                </div>

                <div className="metric-card">
                  <div className="metric-label">Peak Score</div>
                  <div className="metric-value">
                    {result.trend_data.peak_score}/100
                  </div>
                </div>

                <div className="metric-card">
                  <div className="metric-label">Autocomplete Rank</div>
                  <div className="metric-value">
                    {result.autocomplete_rank ? `#${result.autocomplete_rank}` : 'N/A'}
                  </div>
                </div>

                <div className="metric-card">
                  <div className="metric-label">Tendencia</div>
                  <div className="metric-value">
                    {result.trend_data.trend === 'rising' ? '📈 Subiendo' :
                     result.trend_data.trend === 'stable' ? '➡️ Estable' :
                     '❌ Sin datos'}
                  </div>
                </div>
              </div>

              {result.trend_data.related_queries &&
               result.trend_data.related_queries.length > 0 && (
                <div className="related-queries">
                  <h3>Keywords Relacionadas:</h3>
                  <ul>
                    {result.trend_data.related_queries.map((query, index) => (
                      <li key={index}>{query}</li>
                    ))}
                  </ul>
                </div>
              )}

              {result.cached && (
                <div className="cache-notice">
                  ℹ️ Resultados del cache (últimos 7 días)
                </div>
              )}
            </div>
          </div>
        )}

        <footer className="info-section">
          <h3>💡 ¿Cómo funciona?</h3>
          <div className="info-grid">
            <div className="info-card">
              <h4>1️⃣ Google Trends</h4>
              <p>Obtiene tendencia de búsqueda (score 0-100)</p>
            </div>
            <div className="info-card">
              <h4>2️⃣ Autocomplete</h4>
              <p>Mide popularidad según ranking en sugerencias</p>
            </div>
            <div className="info-card">
              <h4>3️⃣ ML Estimation</h4>
              <p>Algoritmo que estima volumen real</p>
            </div>
          </div>

          <div className="disclaimer">
            <strong>Nota:</strong> Los volúmenes son estimaciones basadas en señales públicas.
            Para datos exactos, usar Google Keyword Planner (requiere cuenta de Google Ads).
          </div>
        </footer>
      </main>
    </div>
  );
}

export default App;
