# Analytics

## Frontend Configuration

The frontend expects an API base URL defined via the `VITE_API_BASE_URL` environment variable. Create a `.env` file inside the `frontend` directory during development:

```bash
VITE_API_BASE_URL=http://localhost:8001
```

For production builds, set the variable when running `npm run build`:

```bash
VITE_API_BASE_URL=https://your-domain.example.com npm run build
```

If no value is specified, the code falls back to `http://localhost:8001`.
