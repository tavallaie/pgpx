"""
Custom exceptions for the pgpx library.

This module defines all custom exception classes used throughout
the pgpx library for better error handling and debugging.
"""


class PgpxError(Exception):
    """Base exception for all pgpx errors."""

    pass


class ConnectionError(PgpxError):
    """Raised when database connection fails."""

    pass


class SchemaError(PgpxError):
    """Raised when schema validation fails."""

    pass


class ValidationError(PgpxError):
    """Raised when data validation fails."""

    pass


class QueryError(PgpxError):
    """Raised when query execution fails."""

    pass


class PrimaryKeyError(SchemaError):
    """Raised when primary key constraints are violated."""

    pass


class TransactionError(PgpxError):
    """Raised when transaction operations fail."""

    pass


class MigrationError(PgpxError):
    """Raised when migration operations fail."""

    pass


class RelationshipError(PgpxError):
    """Raised when relationship operations fail."""

    pass


class PoolError(PgpxError):
    """Raised when connection pool operations fail."""

    pass


class ExtensionError(PgpxError):
    """Raised when extension operations fail."""

    pass


class ORMError(PgpxError):
    """Raised when ORM operations fail."""

    pass


class ConfigurationError(PgpxError):
    """Raised when configuration is invalid."""

    pass
