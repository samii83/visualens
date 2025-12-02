import React, { useState } from 'react';
import api from '../api';

// electron-app/src/renderer/src/components/CaptionView.jsx
// Purpose: UI component for uploading/selecting an image and displaying generated caption(s).

export default function CaptionView({ onCaptionGenerated }) {
	const [file, setFile] = useState(null);
	const [loading, setLoading] = useState(false);
	const [caption, setCaption] = useState('');
	const [error, setError] = useState('');

	const handleFileChange = (e) => {
		setFile(e.target.files[0]);
		setCaption('');
		setError('');
	};

	async function handleGenerate() {
		if (!file) return;
		setLoading(true);
		setError('');
		try {
			const res = await api.postCaption(file);
			let text = '';
			if (Array.isArray(res)) {
				text = res[0]?.generated_text || res[0]?.caption || '';
			} else {
				text = res.generated_text || res.caption || '';
			}

			async function handleSaveToDataset() {
				if (!file) return;
				setLoading(true);
				setError('');
				try {
					const res = await api.postUploadImage(file);
					// The backend will return id and caption if available
					if (res?.caption) {
						setCaption(res.caption);
						if (onCaptionGenerated) onCaptionGenerated(res.caption);
					}
				} catch (err) {
					setError(err.message);
				} finally {
					setLoading(false);
				}
			}
			setCaption(text);
			if (onCaptionGenerated) onCaptionGenerated(text);
		} catch (err) {
			setError(err.message);
		} finally {
			setLoading(false);
		}
	}

	return (
		<div className="caption-view">
			<input type="file" accept="image/*" onChange={handleFileChange} />
			<button onClick={handleGenerate} disabled={!file || loading}>{loading ? 'Generating...' : 'Generate Caption'}</button>
			<button onClick={handleSaveToDataset} disabled={!file || loading} style={{ marginLeft: 8 }}>{loading ? 'Saving...' : 'Save to dataset'}</button>
			{error && <div className="error">{error}</div>}
			{caption && (
				<div className="caption">Generated Caption: <strong>{caption}</strong></div>
			)}
		</div>
	);
}
