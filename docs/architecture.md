# Architecture
Flask blueprints separate authentication, pages, records, emergency UI, and API input. SQLAlchemy persists users/readings in SQLite. `services/simulation.py` produces device-shaped payloads; `services/health_analysis.py` explains deterministic scoring; `services/ai_service.py` is the safe provider boundary. Environment configuration belongs in `.env`, never browser JavaScript.
