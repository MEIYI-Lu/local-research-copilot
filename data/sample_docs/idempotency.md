# Idempotency and Request Retries

An operation is idempotent when repeating the same intended request does not create additional effects beyond the first successful application. This property is important when networks fail after a server has processed a request but before the client receives the response.

For operations such as payment creation, an application can accept an idempotency key. The server stores the outcome associated with that key and returns the same outcome when the client retries, preventing accidental duplicate charges or duplicate resource creation.
