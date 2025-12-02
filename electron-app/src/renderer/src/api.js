// electron-app/src/renderer/src/api.js
// Purpose: Wrapper for renderer to call backend FastAPI endpoints.
// A small convenience wrapper used by React components. Uses the Electron `preload` bridge to get API base URL.

async function getApiUrl() {
	if (window.electronAPI && window.electronAPI.getApiConfig) {
		const cfg = await window.electronAPI.getApiConfig();
		return cfg.apiUrl;
	}
	// Fallback to typical dev URL
	return 'http://127.0.0.1:8000/api/v1';
}

export async function postCaption(file) {
	const apiUrl = await getApiUrl();
	const formData = new FormData();
	formData.append('file', file);
	const res = await fetch(`${apiUrl}/caption`, { method: 'POST', body: formData });
	if (!res.ok) {
		const err = await res.json();
		throw new Error(err.detail || 'Caption request failed');
	}
	return res.json();
}

export async function postUploadImage(file) {
	const apiUrl = await getApiUrl();
	const formData = new FormData();
	formData.append('file', file);
	const res = await fetch(`${apiUrl}/images/upload`, { method: 'POST', body: formData });
	if (!res.ok) {
		const err = await res.json();
		throw new Error(err.detail || 'Upload failed');
	}
	return res.json();
}

export async function postSearch(text, k = 5) {
	const apiUrl = await getApiUrl();
	const res = await fetch(`${apiUrl}/search`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ text, k }),
	});
	if (!res.ok) {
		const err = await res.json();
		throw new Error(err.detail || 'Search failed');
	}
	return res.json();
}

export async function listImages() {
	const apiUrl = await getApiUrl();
	const res = await fetch(`${apiUrl}/images/list`);
	if (!res.ok) {
		const err = await res.json();
		throw new Error(err.detail || 'List images failed');
	}
	return res.json();
}

// default export: convenience group
export default { postCaption, postSearch, postUploadImage, listImages };
