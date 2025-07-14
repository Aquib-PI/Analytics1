## Environment Variables

1. Copy the sample environment file:

   ```bash
   cp .env.sample .env
   ```

2. Edit `.env` and provide values for:

   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_HOST`
   - `DB_PORT`
   - `DB_NAME`

=======
# Analytics Dashboard

This project provides a prototype analytics dashboard with a FastAPI backend and a React (Vite) frontend. The backend exposes several API endpoints for dashboard metrics while the frontend renders charts and tables using those APIs.

## Backend Setup

1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
2. Create a `.env` file in `backend/` containing your database settings:
   ```bash
   DB_USER=<username>
   DB_PASSWORD=<password>
   DB_HOST=<host>
   DB_PORT=<port>
   DB_NAME=<database>
   ```
3. Start the API server:
   ```bash
   uvicorn main:app --reload --port 8001
   ```
   The frontend expects the API at `http://localhost:8001`.

## Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Launch the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173`.
3. Build for production:
   ```bash
   npm run build
   npm run preview # optional preview of the built site
   ```

## Running the Application

Run the backend and frontend commands in separate terminals. Once both are running, open `http://localhost:5173` in your browser to access the dashboard.
