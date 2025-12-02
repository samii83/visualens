import React, { useState } from 'react';
import api from '../api';

// electron-app/src/renderer/src/components/SearchView.jsx
// Purpose: UI component for search — accepts text or image queries and shows results.
// Basic implementation using the renderer API wrapper.

export default function SearchView({ onResult }) {
	const [queryText, setQueryText] = useState('');
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState('');
	const [results, setResults] = useState([]);

	async function handleSearch() {
		if (!queryText) return;
		setLoading(true);
		setError('');
		try {
			const res = await api.postSearch(queryText, 8);
			setResults(res.results || []);
			if (onResult) onResult(res.results || []);
		} catch (err) {
			setError(err.message);
		} finally {
			setLoading(false);
		}
	}

	return (
		<div className="search-view">
			<div className="search-input">
				<input value={queryText} onChange={(e) => setQueryText(e.target.value)} placeholder="Search by text (e.g., 'city street')" />
				<button onClick={handleSearch} disabled={loading || !queryText}>{loading ? 'Searching...' : 'Search'}</button>
			</div>
			{error && <div className="error">{error}</div>}
			<div className="results">
				{results.length === 0 && <div>No results yet</div>}
				{results.map((r) => (
					<div className="result-item" key={r.id}>
						<img src={`${(window.API_BASE || '')}/images/${r.filename}`} alt={r.caption} width={160} />
						<div className="result-meta">
							<div className="caption">{r.caption}</div>
							<div className="score">score: {r.score?.toFixed(3)}</div>
						</div>
					</div>
				))}
			</div>
		</div>
	);
}
