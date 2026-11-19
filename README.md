# BRAF Binder Pipeline

Transformer-based protein sequence generation (ProtGPT2) and binding affinity
prediction against BRAF V600E. Final-year project, TJIT Bengaluru.

- `src/braf_pipeline/`: shared, testable pipeline library
- `notebooks/`: thin Colab notebooks that call `src/`
- `backend/`: FastAPI service
- `db/`: PostgreSQL schema and migrations
- `frontend/`: React + TypeScript dashboard
- `configs/`: thresholds, paths and seeds

Data and model files are stored on Google Drive, not in this repository.
