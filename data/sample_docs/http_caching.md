# HTTP Caching and ETags

HTTP caching can avoid transferring or recomputing a representation that a client already holds. An `ETag` is an opaque validator associated with a particular representation. A client can later send `If-None-Match` with that ETag. If the representation has not changed, the server may respond with `304 Not Modified` instead of sending the full body again.

Cache-Control directives define freshness and caching policy, while validators such as ETags support conditional requests after freshness has expired.
