# Multi-Version Concurrency Control

Multi-Version Concurrency Control (MVCC) keeps multiple logical versions of data so readers can observe a consistent snapshot while other transactions update newer versions. This reduces direct read-write blocking in many database engines.

A snapshot does not mean every isolation anomaly disappears. The exact guarantees depend on the database and isolation level. MVCC is a concurrency mechanism that helps readers and writers coexist, while transaction rules still determine which versions a transaction is allowed to see.
