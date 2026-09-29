# Backpressure

Backpressure is a flow-control mechanism used when a producer can generate work faster than a downstream consumer can safely process it. Instead of allowing an unbounded queue to grow, the system slows, pauses, blocks, batches, or rejects upstream production until capacity becomes available.

Backpressure is common in streaming systems, message pipelines, and asynchronous services. It protects memory and latency by making overload visible to upstream components rather than hiding it in an ever-growing buffer.
