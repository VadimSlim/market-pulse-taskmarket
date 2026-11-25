# Market Pulse

Independent Taskmarket market intelligence. Made for a paid Taskmarket bounty; not an official Taskmarket product.

## Architecture

Dependency-free Python data collector, static HTML, CSS, JavaScript and SVG visualizations. Public API only; no wallet connection, user tracking or API secrets.

## Local use

Requires Python 3.13 and `python -m pip install -r requirements.txt`. Run `python refresh.py` and then `python -m http.server 8000 --bind 127.0.0.1 --directory site`.

## Methodology

Both Tempo (4217) and Base (8453) are queried. Identical endpoint responses are displayed without adding them across networks. Weekly distinct requester addresses are derived from paginated task histories. Addresses do not identify people. Current status shares do not predict eventual success. Rewards posted and paid in the same period can concern different task cohorts.

## Refresh

The public snapshot is replaced atomically after collection and analysis. Failed updates preserve the last bundled snapshot. A production scheduler and HTTPS host must be configured before release.

## Licensing

Original source code: MIT. Third-party fonts retain their respective OFL licenses. Taskmarket logos and brand assets are not relicensed under MIT; used under the bounty brand-kit terms.

## GitHub Pages deployment

For an authorized administrator of the target repository, run `python deploy.py` after pushing the source. The workflow refreshes every 30 minutes on a best-effort schedule; delayed executions are possible.
