# Migrations

One file per schema change, named `NNN_short_name.sql` (NNN above the current `PRAGMA user_version`).
`python init_db.py --migrate` applies the new files in order, each in one transaction, and sets the version.
schema.sql always shows the latest schema and sets the same version, so a new database needs no migration.
None yet: version 2 is the first schema deployed to the cloud.
