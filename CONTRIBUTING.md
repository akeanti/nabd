# Contributing to Nabd

Thank you for helping build an open grid measurement network. This guide covers the development setup, the checks that CI runs, and the rules for code, text, and commits.

## Ground rules

- **Safety.** Nodes never connect directly to mains. Voltage sensing goes only through an isolated AC-AC adapter, a resistor divider, and a midscale bias network, as described in [docs/hardware.md](docs/hardware.md). Changes that add any other path to mains are not accepted.
- **Privacy.** Never commit or post exact node coordinates, WiFi credentials, or node tokens, including in test data, logs, and screenshots. Public outputs use city-level coordinates; see [docs/privacy.md](docs/privacy.md).
- **Conduct.** Participation is governed by the [code of conduct](CODE_OF_CONDUCT.md).

## Development setup

Requirements: Git, Python 3.11 or newer, Node.js 22.12 or newer, and a C++17 compiler for host builds. PlatformIO and clang-format are installed through pip.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]" -r firmware/requirements.txt -r docs/requirements.txt
cd web && npm ci
```

## Checks

CI runs each of these on every pull request.

| Area | Command, from the repository root |
| --- | --- |
| C and C++ formatting | `git ls-files -z -- '*.c' '*.cpp' '*.h' '*.hpp' \| xargs -0 clang-format --dry-run --Werror` |
| Firmware host tests | `cd firmware && pio test -e native` |
| Firmware builds | `cd firmware && pio run -e tier_a && pio run -e tier_b` |
| Python lint | `ruff check .` |
| Python formatting | `black --check .` |
| Python types | `mypy` |
| Python tests | `pytest` |
| Web | `cd web && npm run typecheck && npm run build` |
| Compliance | `cmake -S compliance -B compliance/build && cmake --build compliance/build && compliance/build/nabd_compliance --report compliance/build/report.md` |
| Documentation | `mkdocs build --strict` |
| Text style | `python .github/scripts/check_text_style.py` |

## Code

- **Firmware:** C++17, formatted with the committed `.clang-format` (Google base style, 100 columns). `nabd_dsp`, `nabd_time`, and `nabd_c37118` must not include Arduino or ESP-IDF headers so that they build and test on the host.
- **Python:** 3.11 or newer, linted with ruff, formatted with black, type-checked with mypy in strict mode.
- **Web:** TypeScript in strict mode with Vite and MapLibre GL, without a UI framework.
- **Names and structure** carry the meaning. Write comments only for physical units, safety limits, references to standards (IEEE C37.118.1-2011, C37.118.1a-2014, C37.118.2-2011), and non-obvious math.

## Writing

Plain, precise technical English in code, documentation, commit messages, and user interfaces. No emojis, no em dashes, and no marketing language. The text style check lists the words it rejects.

## Commits and pull requests

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) with a short imperative subject, for example `feat(dsp): add frequency-tracking DFT`.

| Types | `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `chore` |
| --- | --- |
| Scopes | `firmware`, `dsp`, `time`, `hal`, `c37118`, `collector`, `events`, `web`, `tools`, `compliance`, `dataset`, `hardware`, `docs` |

Release notes are generated from these messages, so describe the change, not the process. Keep each pull request to one topic and fill in the template. Hardware pull requests include the ERC and DRC results from the `kicad` workflow.

## Licensing of contributions

Contributions are licensed under the license of the part they change: MIT for code and documentation, CERN-OHL-P-2.0 for `hardware/`, and CC BY 4.0 for `dataset/`.

## Releases

Maintainers release by:

1. Setting the new version in `pyproject.toml`, `CITATION.cff`, and `web/package.json`.
2. Regenerating the changelog with `git cliff --tag vX.Y.Z --output CHANGELOG.md`.
3. Committing, then pushing the tag `vX.Y.Z`.

The `release` workflow checks that the tag matches the declared versions, builds both firmware tiers, attaches merged and OTA images to a GitHub release with notes from the commit history, and rebuilds the documentation site so that the browser flasher serves the new firmware.

One-time repository settings: set GitHub Pages to deploy from GitHub Actions, and enable private vulnerability reporting.
