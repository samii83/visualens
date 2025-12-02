import React, { useState, useEffect } from 'react';
import './App.css';
import CaptionView from './components/CaptionView';
import SearchView from './components/SearchView';

function App() {
  const [apiConfig, setApiConfig] = useState(null);
  const [caption, setCaption] = useState('');
  const [loading, setLoading] = useState(false);
  const [active, setActive] = useState('caption');
  const [error, setError] = useState('');

  useEffect(() => {
    // Get the API config from the main process
    window.electronAPI.getApiConfig().then(config => {
      setApiConfig(config);
      // Expose small helper for components to build image URLs
      window.API_BASE = config.apiUrl.replace(/\/api\/v1\/?$/, '');
    });
  }, []);
  async function viewDataset() {
    try {
      const api = await import('./api');
      const res = await api.listImages();
      console.log('images:', res.images);
      // Could implement a dataset viewer; for now, just log
    } catch (err) {
      console.warn(err);
    }
  }

  // Caption generation handled in <CaptionView>, which calls onCaptionGenerated

  return (
    <div className="App">
      <header className="App-header">
        <h1>VisuaLens</h1>
        <p>Upload an image to generate a caption or search the dataset.</p>
        <div className="nav">
          <button onClick={() => setActive('caption')} className={active === 'caption' ? 'active' : ''}>Caption</button>
          <button onClick={() => setActive('search')} className={active === 'search' ? 'active' : ''}>Search</button>
        </div>

        {active === 'caption' && (
          <div className="card">
            <CaptionView onCaptionGenerated={(txt) => setCaption(txt)} />
            {error && <p className="error">Error: {error}</p>}
            {caption && (
              <div className="caption-result">
                <h2>Generated Caption:</h2>
                <p>{caption}</p>
              </div>
            )}
          </div>
        )}

        {active === 'search' && (
          <div className="card">
            <SearchView onResult={(results) => console.log('got results', results)} />
            <div style={{ marginTop: 16 }}>
              <button onClick={() => viewDataset()}>View dataset (console)</button>
            </div>
          </div>
        )}

      </header>
    </div>
  );
}

export default App;
