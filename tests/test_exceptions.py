"""
Unit tests for pgpx.exceptions module.

This module contains tests for all custom exception classes
defined in the exceptions module.
"""

import unittest


class TestPgpxError(unittest.TestCase):
    """Test base PgpxError exception."""

    def test_pgpx_error_inheritance(self):
        """Test PgpxError inherits from Exception."""
        from src.pgpx.exceptions import PgpxError

        self.assertTrue(issubclass(PgpxError, Exception))

    def test_pgpx_error_instantiation(self):
        """Test PgpxError can be instantiated."""
        from src.pgpx.exceptions import PgpxError

        error = PgpxError("Test error")
        self.assertEqual(str(error), "Test error")

        # Test without message
        error_no_msg = PgpxError()
        self.assertEqual(str(error_no_msg), "")

    def test_pgpx_error_with_cause(self):
        """Test PgpxError with cause exception."""
        from src.pgpx.exceptions import PgpxError

        original_error = ValueError("Original error")
        try:
            raise PgpxError("Wrapped error") from original_error
        except PgpxError as pgpx_error:
            self.assertEqual(str(pgpx_error), "Wrapped error")
            self.assertEqual(pgpx_error.__cause__, original_error)


class TestConnectionError(unittest.TestCase):
    """Test ConnectionError exception."""

    def test_connection_error_inheritance(self):
        """Test ConnectionError inherits from PgpxError."""
        from src.pgpx.exceptions import ConnectionError, PgpxError

        self.assertTrue(issubclass(ConnectionError, PgpxError))

    def test_connection_error_instantiation(self):
        """Test ConnectionError can be instantiated."""
        from src.pgpx.exceptions import ConnectionError

        error = ConnectionError("Connection failed")
        self.assertEqual(str(error), "Connection failed")
        self.assertIsInstance(error, Exception)


class TestSchemaError(unittest.TestCase):
    """Test SchemaError exception."""

    def test_schema_error_inheritance(self):
        """Test SchemaError inherits from PgpxError."""
        from src.pgpx.exceptions import SchemaError, PgpxError

        self.assertTrue(issubclass(SchemaError, PgpxError))

    def test_schema_error_instantiation(self):
        """Test SchemaError can be instantiated."""
        from src.pgpx.exceptions import SchemaError

        error = SchemaError("Invalid schema")
        self.assertEqual(str(error), "Invalid schema")


class TestValidationError(unittest.TestCase):
    """Test ValidationError exception."""

    def test_validation_error_inheritance(self):
        """Test ValidationError inherits from PgpxError."""
        from src.pgpx.exceptions import ValidationError, PgpxError

        self.assertTrue(issubclass(ValidationError, PgpxError))

    def test_validation_error_instantiation(self):
        """Test ValidationError can be instantiated."""
        from src.pgpx.exceptions import ValidationError

        error = ValidationError("Validation failed")
        self.assertEqual(str(error), "Validation failed")


class TestQueryError(unittest.TestCase):
    """Test QueryError exception."""

    def test_query_error_inheritance(self):
        """Test QueryError inherits from PgpxError."""
        from src.pgpx.exceptions import QueryError, PgpxError

        self.assertTrue(issubclass(QueryError, PgpxError))

    def test_query_error_instantiation(self):
        """Test QueryError can be instantiated."""
        from src.pgpx.exceptions import QueryError

        error = QueryError("Query failed")
        self.assertEqual(str(error), "Query failed")


class TestPrimaryKeyError(unittest.TestCase):
    """Test PrimaryKeyError exception."""

    def test_primary_key_error_inheritance(self):
        """Test PrimaryKeyError inherits from SchemaError."""
        from src.pgpx.exceptions import PrimaryKeyError, SchemaError

        self.assertTrue(issubclass(PrimaryKeyError, SchemaError))

    def test_primary_key_error_instantiation(self):
        """
        Verify PrimaryKeyError instantiates and preserves the provided message.
        
        Asserts that the exception's string representation equals the message passed at construction.
        """
        from src.pgpx.exceptions import PrimaryKeyError

        error = PrimaryKeyError("Primary key violation")
        self.assertEqual(str(error), "Primary key violation")


class TestTransactionError(unittest.TestCase):
    """Test TransactionError exception."""

    def test_transaction_error_inheritance(self):
        """Test TransactionError inherits from PgpxError."""
        from src.pgpx.exceptions import TransactionError, PgpxError

        self.assertTrue(issubclass(TransactionError, PgpxError))

    def test_transaction_error_instantiation(self):
        """Test TransactionError can be instantiated."""
        from src.pgpx.exceptions import TransactionError

        error = TransactionError("Transaction failed")
        self.assertEqual(str(error), "Transaction failed")


class TestMigrationError(unittest.TestCase):
    """Test MigrationError exception."""

    def test_migration_error_inheritance(self):
        """Test MigrationError inherits from PgpxError."""
        from src.pgpx.exceptions import MigrationError, PgpxError

        self.assertTrue(issubclass(MigrationError, PgpxError))

    def test_migration_error_instantiation(self):
        """Test MigrationError can be instantiated."""
        from src.pgpx.exceptions import MigrationError

        error = MigrationError("Migration failed")
        self.assertEqual(str(error), "Migration failed")


class TestRelationshipError(unittest.TestCase):
    """Test RelationshipError exception."""

    def test_relationship_error_inheritance(self):
        """Test RelationshipError inherits from PgpxError."""
        from src.pgpx.exceptions import RelationshipError, PgpxError

        self.assertTrue(issubclass(RelationshipError, PgpxError))

    def test_relationship_error_instantiation(self):
        """Test RelationshipError can be instantiated."""
        from src.pgpx.exceptions import RelationshipError

        error = RelationshipError("Relationship error")
        self.assertEqual(str(error), "Relationship error")


class TestPoolError(unittest.TestCase):
    """Test PoolError exception."""

    def test_pool_error_inheritance(self):
        """Test PoolError inherits from PgpxError."""
        from src.pgpx.exceptions import PoolError, PgpxError

        self.assertTrue(issubclass(PoolError, PgpxError))

    def test_pool_error_instantiation(self):
        """Test PoolError can be instantiated."""
        from src.pgpx.exceptions import PoolError

        error = PoolError("Pool error")
        self.assertEqual(str(error), "Pool error")


class TestExtensionError(unittest.TestCase):
    """Test ExtensionError exception."""

    def test_extension_error_inheritance(self):
        """Test ExtensionError inherits from PgpxError."""
        from src.pgpx.exceptions import ExtensionError, PgpxError

        self.assertTrue(issubclass(ExtensionError, PgpxError))

    def test_extension_error_instantiation(self):
        """Test ExtensionError can be instantiated."""
        from src.pgpx.exceptions import ExtensionError

        error = ExtensionError("Extension error")
        self.assertEqual(str(error), "Extension error")


class TestORMError(unittest.TestCase):
    """Test ORMError exception."""

    def test_orm_error_inheritance(self):
        """Test ORMError inherits from PgpxError."""
        from src.pgpx.exceptions import ORMError, PgpxError

        self.assertTrue(issubclass(ORMError, PgpxError))

    def test_orm_error_instantiation(self):
        """Test ORMError can be instantiated."""
        from src.pgpx.exceptions import ORMError

        error = ORMError("ORM error")
        self.assertEqual(str(error), "ORM error")


class TestConfigurationError(unittest.TestCase):
    """Test ConfigurationError exception."""

    def test_configuration_error_inheritance(self):
        """Test ConfigurationError inherits from PgpxError."""
        from src.pgpx.exceptions import ConfigurationError, PgpxError

        self.assertTrue(issubclass(ConfigurationError, PgpxError))

    def test_configuration_error_instantiation(self):
        """Test ConfigurationError can be instantiated."""
        from src.pgpx.exceptions import ConfigurationError

        error = ConfigurationError("Configuration error")
        self.assertEqual(str(error), "Configuration error")


class TestExceptionHierarchy(unittest.TestCase):
    """Test the overall exception hierarchy."""

    def test_all_exceptions_inherit_from_pgpx_error(self):
        """Test all custom exceptions inherit from PgpxError."""
        from src.pgpx.exceptions import (
            PgpxError,
            ConnectionError,
            SchemaError,
            ValidationError,
            QueryError,
            PrimaryKeyError,
            TransactionError,
            MigrationError,
            RelationshipError,
            PoolError,
            ExtensionError,
            ORMError,
            ConfigurationError,
        )

        exceptions = [
            ConnectionError,
            SchemaError,
            ValidationError,
            QueryError,
            PrimaryKeyError,
            TransactionError,
            MigrationError,
            RelationshipError,
            PoolError,
            ExtensionError,
            ORMError,
            ConfigurationError,
        ]

        for exc in exceptions:
            self.assertTrue(
                issubclass(exc, PgpxError),
                f"{exc.__name__} should inherit from PgpxError",
            )

    def test_exception_chaining(self):
        """Test exception chaining works properly."""
        from src.pgpx.exceptions import PgpxError, ConnectionError

        try:
            raise ConnectionError("Database connection failed")
        except ConnectionError as e:
            self.assertIsInstance(e, PgpxError)
            self.assertIsInstance(e, ConnectionError)
            self.assertEqual(str(e), "Database connection failed")


if __name__ == "__main__":
    unittest.main()