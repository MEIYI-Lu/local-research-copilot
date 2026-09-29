# JSON Web Tokens

A JSON Web Token (JWT) is a compact format for carrying signed claims. A typical signed JWT has a header, payload, and signature. The signature lets a verifier detect tampering and confirm that the token was produced by an entity holding the expected signing key.

The payload is encoded rather than encrypted by default, so sensitive information should not be placed in a JWT merely because it is signed. Verifiers should also check claims such as expiration, issuer, and audience rather than validating only the signature.
