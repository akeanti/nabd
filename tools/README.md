# Command-line tool

The `nabd` command is installed with the `nabd` distribution from the repository root:

```bash
pip install -e ".[dev]"
nabd --version
```

Planned commands: node provisioning, raw sample capture over serial, calibration, dataset export, and compliance reports.

`tests/` also holds repository data checks, such as the arithmetic of `hardware/BOM.csv`.
