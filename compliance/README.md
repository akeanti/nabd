# Compliance harness

Generates the synthetic test signals of IEEE C37.118.1-2011 and its amendment C37.118.1a-2014, runs them through `firmware/lib/nabd_dsp` on the host, and prints a Markdown report with the maximum total vector error (TVE), frequency error (FE), and ROCOF error (RFE) per test condition, with pass or fail against the P-class limits. The executable exits with a non-zero status when any condition fails.

```bash
cmake -S compliance -B compliance/build -DCMAKE_BUILD_TYPE=Release
cmake --build compliance/build
compliance/build/nabd_compliance > compliance/build/report.md
```

The `compliance` GitHub workflow runs the same commands, uploads the report as an artifact, and adds it to the job summary.

Status: the harness builds and prints a report, but no test conditions are registered yet.
