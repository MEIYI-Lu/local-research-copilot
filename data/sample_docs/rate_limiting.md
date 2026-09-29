# Rate Limiting

Rate limiting bounds how much work a client or tenant may request over a period of time. Common designs include token buckets, leaky buckets, and fixed or sliding windows. A limiter can protect shared capacity, reduce accidental overload, and enforce fair-use policies.

A useful response communicates that the limit was reached and, when appropriate, when a retry may succeed. Rate limiting is different from backpressure: rate limits enforce an admission policy, whereas backpressure coordinates flow between components that are already exchanging work.
