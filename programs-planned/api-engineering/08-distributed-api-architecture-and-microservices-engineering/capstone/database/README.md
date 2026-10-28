# Database ownership and migrations

`legacy/` preserves the Course 7 migration history through revision 015. The other directories begin service-owned migration histories after extraction.

The course models logical ownership, not a requirement that every service run on a separate database server. Application credentials and migrations must prevent cross-owner writes and private-schema reads.
