# Overview

CLI interface for Spotify using only python standard library.

Uses [PKCE Authorization Flow](https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow)

# Usage

- You can install package with `pip install .` which will create `spotify` command in your shell
- Get further usage information with `spotify -h`
- Player commands can only control existing sessions (e.g. listening on mobile)

## Examples

- `spotify top-tracks` Will get your 20 top tracks for the last 6 months
- `spotify top-tracks --term short_term -n 10 --offset 10` Will get your 11th-20th top tracks for the last 4 weeks
- `spotify saved-tracks` Will get your 20 most recently saved tracks
- `spotify next` Will skip the current song

# Links

- [Spotify API Documentation](https://developer.spotify.com/documentation/web-api)
