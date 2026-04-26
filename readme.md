# UNMAPPED Prototype

## Structure
- `backend.py` FastAPI backend
- `src/` Vite + React frontend
- `country_packs.json` configurable local packs

## Run backend
```bash
pip install fastapi uvicorn pydantic
uvicorn backend:app --reload --port 8000
```

## Run frontend
```bash
npm install
npm run dev
```

## Demo flow
1. Enter Amara’s profile.
2. Show skills translation.
3. Show AI readiness.
4. Show opportunity matches.
5. Switch country pack to show reconfigurability.
