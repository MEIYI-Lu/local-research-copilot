# Database Transactions and ACID

A transaction groups database operations into one logical unit. The ACID properties are atomicity, consistency, isolation, and durability. Atomicity means a transaction is applied completely or not at all. Isolation controls how concurrent transactions observe one another. Durability means committed changes survive expected failures according to the database's persistence guarantees.

Transaction boundaries matter because partial multi-step updates can leave data in an invalid state. Applications should keep critical invariants inside transactional operations when possible.
