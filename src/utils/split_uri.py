def split_uri(uri: str) -> tuple[str, str, int]:
    protocol_end: int = uri.find("://")
    protocol: str = uri[:protocol_end]
    remaining: str = uri[protocol_end + 3 :]
    host_end: int = remaining.find(":")
    host: str = remaining[:host_end]
    port: int = int(remaining[host_end + 1 :])
    return protocol, host, port
