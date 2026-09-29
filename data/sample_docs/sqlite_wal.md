# SQLite Write-Ahead Logging

SQLite can operate in Write-Ahead Logging (WAL) mode. Instead of writing modified database pages directly into the main database file before commit, changes are appended to a separate WAL file. Readers can continue using a stable snapshot of the database while a writer appends new changes.

WAL can improve read/write concurrency for many local applications. A checkpoint later transfers committed changes from the WAL into the main database. WAL does not remove the need for transactions or backups; it changes the write path and concurrency behaviour.
