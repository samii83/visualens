# VisuaLens

VisuaLens is a desktop application built with Electron and React for the frontend, and a Python FastAPI server for the backend. It uses the Hugging Face Inference API to perform machine learning tasks like generating captions for images and creating text embeddings.

## Project Structure

- **/electron-app**: Contains the Electron/React frontend application.
- **/backend**: Contains the FastAPI backend server.
- **.env.example**: Root environment file template.
- **README.md**: This file.

## Getting Started

### Prerequisites

- Node.js and npm (or yarn/pnpm)
- Python 3.8+ and pip

### 1. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment and activate it
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create the environment file
cp .env.example .env

# Edit .env and add your Hugging Face API Key
# HUGGING_FACE_API_KEY="your_key_here"

# Run the backend server
uvicorn app.main:app --reload
```
The backend server will be running at `http://127.0.0.1:8000`.

Note: If you do not set `HUGGING_FACE_API_KEY` in `.env` the backend will run in a light-weight "demo mode" and return mock captions and embeddings. This is helpful for UI development without HF credentials.

### 2. Frontend Setup

```bash
# Navigate to the electron-app directory
cd ../electron-app

# Install dependencies
npm install

# Run the development server
npm run dev
```
This will launch the Electron application in development mode with hot-reloading.

### 3. Building for Production

To build the application for production, run the following command in the `electron-app` directory:

```bash
npm run build
```
This will create a distributable application in the `electron-app/dist` folder.

## How It Works

1.  The **React frontend** (running in an Electron `BrowserWindow`) allows the user to upload an image.
2.  The frontend sends the image to the local **FastAPI backend**.
3.  The backend forwards the request to the **Hugging Face Inference API**, using an API key stored securely in its environment variables.
4.  Hugging Face returns the generated caption.
5.  The backend sends the caption back to the React frontend, which displays it to the user.
