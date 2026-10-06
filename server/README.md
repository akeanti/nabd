# Server

Python packages for the collector and event detection. Both ship in the `nabd` distribution defined in the repository root `pyproject.toml`.

| Package | Role |
| --- | --- |
| `nabd_collector` | asyncio service that accepts IEEE C37.118.2 over TCP and JSON over WebSocket, aligns frames from all nodes by timestamp, writes Parquet partitioned by day and node, and serves a live WebSocket feed. |
| `nabd_events` | Detection of frequency excursions, ROCOF spikes, and inter-node angle oscillations from FFT and matrix pencil analysis of angle differences. |

```bash
pip install -e ".[dev]"
pytest server/tests
```

Status: package skeletons only.
