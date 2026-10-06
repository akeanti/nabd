# Security policy

## Supported versions

Until version 1.0, only the latest release receives security fixes.

## Reporting a vulnerability

Report vulnerabilities privately through [GitHub private vulnerability reporting](https://github.com/OWNER/nabd/security/advisories/new). Do not open a public issue. Include the affected component and version, the steps to reproduce, and the impact you expect. Maintainers acknowledge reports within 7 days and agree on a disclosure date with the reporter.

## Scope

- Node firmware network services: C37.118.2 over TCP, JSON over WebSocket, MQTT, Prometheus `/metrics`, REST `/api/v1`, OTA updates, and captive portal provisioning.
- The collector, event detection, and live map.
- The `nabd` command-line tool.
- The release pipeline and published firmware images.
- Exposure of exact node coordinates, WiFi credentials, or node tokens.
- Hardware design errors that could weaken the isolation between mains and the node. Report these privately as well; they are handled first.

## Deployment guidance

- Nodes are designed for private networks. Do not forward node ports to the internet.
- Treat node tokens as secrets. Ask the collector administrator to rotate a token that may have been exposed.
- Exact node coordinates are personal data; see [docs/privacy.md](docs/privacy.md).
