import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [apiConfig, setApiConfig] = useState(null);
  const [file, setFile] = useState(null);
  const [caption, setCaption] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Get the API config from the main process
    window.electronAPI.getApiConfig().then(config => {
      setApiConfig(config);
    });
  }, []);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setCaption('');
    setError('');
  };

  const handleCaptionRequest = async () => {
    if (!file || !apiConfig) return;

    setLoading(true);
    setError('');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${apiConfig.apiUrl}/caption`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to generate caption');
      }

      const result = await response.json();
      setCaption(result[0]?.generated_text || 'No caption generated.');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>VisuaLens</h1>
        <p>Upload an image to generate a caption.</p>
        <div className="card">
          <input type="file" accept="image/*" onChange={handleFileChange} />
          <button onClick={handleCaptionRequest} disabled={!file || loading}>
            {loading ? 'Generating...' : 'Get Caption'}
          </button>
        </div>
        {error && <p className="error">Error: {error}</p>}
        {caption && (
          <div className="caption-result">
            <h2>Generated Caption:</h2>
            <p>{caption}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
