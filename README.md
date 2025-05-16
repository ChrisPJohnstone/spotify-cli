# Overview

CLI interface for Spotify using only python standard library.

Uses [PKCE Authorization Flow](https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow)

# Usage

- Install package with `pip install .`
- Get further usage information with `spotify -h`

## Examples

- `spotify top-tracks` Will get your 20 top tracks for the last 6 months
- `spotify top-tracks --term short_term -n 10 --offset 10` Will get your 11th-20th top tracks for the last 4 weeks
- `spotify top-artists` Will get your 20 top artists for the last 6 months

# Links

- [Spotify API Documentation](https://developer.spotify.com/documentation/web-api)
