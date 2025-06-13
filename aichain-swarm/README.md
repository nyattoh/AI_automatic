# AI Chain Swarm

This repository provides a small orchestration demo composed of FastAPI agents
and a React dashboard. The services can be launched together with Docker
Compose. The orchestrator spawns `PM` agents and `Dev` agents that communicate
via asyncio queues. Metrics are exported for Prometheus and visualised via
Grafana.

## Quick start

```bash
# lint and tests
ruff check .
pytest -q

# start full stack
docker compose up -d --build
curl -sf http://localhost:8000/health
```

Use `scripts/launch_swarm.sh --pm 3 --dev 4` to spawn a local tmux based swarm
for development.
