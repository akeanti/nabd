# Privacy

A node is usually installed in someone's home, office, or lab, and its GPS receiver reports its exact position. Nabd treats that position as personal data.

## Rule

**Public outputs round node coordinates to city level. Exact coordinates stay private to the node owner and the collector administrator.**

City level means that latitude and longitude are each rounded to the nearest 0.1 degree. A step of 0.1 degree is about 11.1 km of latitude and about 11.1 km multiplied by the cosine of the latitude in longitude, for example 9.6 km at 30 degrees north.

## Where coordinates appear

| Output | Coordinates |
| --- | --- |
| Live map | rounded |
| Public WebSocket feed from the collector | rounded |
| MQTT summary topics published by the node | rounded |
| Published dataset | rounded |
| C37.118.2 stream (CFG-2 configuration frames carry no position) | none |
| Prometheus `/metrics` on the node | none |
| Node REST API `/api/v1` | rounded; exact only for requests authenticated with the node owner's token |
| Node to collector channel (authenticated) | exact |
| Collector administrator database | exact, not exported |

## Registration

The node registration issue template asks only for city and country. Never post an address or exact coordinates in an issue, pull request, discussion, or log. Bug report logs must have coordinates, WiFi credentials, and node tokens removed.

## Other data

- WiFi credentials are stored in the node's non-volatile storage and are never transmitted.
- The collector sees the public IP address of each node and does not publish it.
- A node owner can ask the collector administrator to delete the exact coordinates of their node at any time. Published dataset releases are immutable; a withdrawn node is excluded from later releases.
