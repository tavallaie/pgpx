"""
Unit tests for pgpx.connection module.

This module contains tests for database connection management
including context managers and persistent connections.
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from src.pgpx.connection import DatabaseConnection, DatabaseClient
from src.pgpx.exceptions import ConnectionError
import psycopg


def get_test_connection_params():
    """Get test connection parameters from environment variables.

    Returns:
        Dictionary with connection parameters
    """
    return {
        "host": os.getenv("PGPX_TEST_HOST", "localhost"),
        "port": int(os.getenv("PGPX_TEST_PORT", "5432")),
        "user": os.getenv("PGPX_TEST_USER", "postgres"),
        "password": os.getenv("PGPX_TEST_PASSWORD", "postgres"),
        "dbname": os.getenv("PGPX_TEST_DB", "postgres"),
    }


class TestDatabaseConnectionMocked(unittest.TestCase):
    """Test DatabaseConnection class with mocked psycopg."""

    def setUp(self):
        """Set up test fixtures."""
        self.connection_params = get_test_connection_params()

    def test_init(self):
        """Test DatabaseConnection initialization."""
        conn = DatabaseConnection(self.connection_params)

        self.assertEqual(conn.connection_params, self.connection_params)
        self.assertIsNone(conn._connection)

    def test_normalize_params_dict(self):
        """Test parameter normalization with dict."""
        conn = DatabaseConnection(self.connection_params)
        normalized = conn._normalize_params(self.connection_params)

        self.assertEqual(normalized, self.connection_params)

    def test_normalize_params_with_to_dict(self):
        """Test parameter normalization with object having to_dict method."""
        config_mock = MagicMock()
        config_mock.to_dict.return_value = self.connection_params

        conn = DatabaseConnection({})  # Use dummy params for init
        normalized = conn._normalize_params(config_mock)

        self.assertEqual(normalized, self.connection_params)
        config_mock.to_dict.assert_called_once()

    def test_normalize_params_invalid(self):
        """Test parameter normalization with invalid input."""
        conn = DatabaseConnection("invalid")
        normalized = conn._normalize_params("invalid")

        self.assertEqual(normalized, {})

    @patch("src.pgpx.connection.psycopg.connect")
    def test_connect_success(self, mock_connect):
        """Test successful connection establishment."""
        mock_connection = MagicMock()
        mock_connection.closed = False
        mock_connect.return_value = mock_connection

        conn = DatabaseConnection(self.connection_params)
        result = conn.connect()

        self.assertEqual(result, conn)
        self.assertEqual(conn._connection, mock_connection)
        mock_connect.assert_called_once_with(**self.connection_params)

    @patch("src.pgpx.connection.psycopg.connect")
    def test_connect_failure(self, mock_connect):
        """Test connection establishment failure."""
        mock_connect.side_effect = psycopg.Error("Connection failed")

        conn = DatabaseConnection(self.connection_params)

        with self.assertRaises(ConnectionError) as cm:
            conn.connect()

        self.assertIn("Failed to connect to database", str(cm.exception))
        self.assertIsNone(conn._connection)

    @patch("src.pgpx.connection.psycopg.connect")
    def test_disconnect(self, mock_connect):
        """Test connection disconnection."""
        mock_connection = MagicMock()
        mock_connection.closed = False
        mock_connect.return_value = mock_connection

        conn = DatabaseConnection(self.connection_params)
        conn.connect()
        conn.disconnect()

        mock_connection.close.assert_called_once()
        self.assertIsNone(conn._connection)

    def test_disconnect_no_connection(self):
        """Test disconnect when no connection exists."""
        conn = DatabaseConnection(self.connection_params)
        conn.disconnect()  # Should not raise an exception

        self.assertIsNone(conn._connection)

    @patch("src.pgpx.connection.psycopg.connect")
    def test_connection_property(self, mock_connect):
        """Test connection property getter."""
        mock_connection = MagicMock()
        mock_connection.closed = False
        mock_connect.return_value = mock_connection

        conn = DatabaseConnection(self.connection_params)
        conn.connect()

        self.assertEqual(conn.connection, mock_connection)

    def test_connection_property_not_connected(self):
        """Test connection property when not connected."""
        conn = DatabaseConnection(self.connection_params)

        with self.assertRaises(ConnectionError) as cm:
            _ = conn.connection

        self.assertIn("Not connected to database", str(cm.exception))

    @patch("src.pgpx.connection.psycopg.connect")
    def test_is_connected(self, mock_connect):
        """Test is_connected method."""
        mock_connection = MagicMock()
        mock_connection.closed = False
        mock_connect.return_value = mock_connection

        conn = DatabaseConnection(self.connection_params)

        # Not connected
        self.assertFalse(conn.is_connected())

        # Connected
        conn.connect()
        self.assertTrue(conn.is_connected())

        # Connection closed
        mock_connection.closed = True
        self.assertFalse(conn.is_connected())

    @patch("src.pgpx.connection.psycopg.connect")
    def test_context_manager(self, mock_connect):
        """Test context manager functionality."""
        mock_connection = MagicMock()
        mock_connection.closed = False
        mock_connect.return_value = mock_connection

        conn = DatabaseConnection(self.connection_params)

        with conn as context:
            self.assertEqual(context, conn)
            self.assertEqual(conn._connection, mock_connection)

        # Connection should be closed after context
        mock_connection.close.assert_called_once()

    @patch("src.pgpx.connection.psycopg.connect")
    def test_context_manager_with_exception(self, mock_connect):
        """Test context manager with exception."""
        mock_connection = MagicMock()
        mock_connection.closed = False
        mock_connect.return_value = mock_connection

        conn = DatabaseConnection(self.connection_params)

        try:
            with conn:
                raise ValueError("Test exception")
        except ValueError:
            pass  # Expected

        # Connection should still be closed despite exception
        mock_connection.close.assert_called_once()

    def test_repr(self):
        """Test string representation."""
        conn = DatabaseConnection(self.connection_params)

        # Not connected
        self.assertEqual(repr(conn), "<DatabaseConnection status=disconnected>")

        # Mock connection for connected state
        conn._connection = MagicMock()
        conn._connection.closed = False
        self.assertEqual(repr(conn), "<DatabaseConnection status=connected>")


class TestDatabaseClientMocked(unittest.TestCase):
    """Test DatabaseClient class with mocked psycopg."""

    def setUp(self):
        """Set up test fixtures."""
        self.connection_params = get_test_connection_params()

    @patch("src.pgpx.connection.DatabaseConnection.connect")
    def test_init_auto_connect(self, mock_connect):
        """Test DatabaseClient initialization with auto_connect."""
        client = DatabaseClient(self.connection_params, auto_connect=True)

        self.assertIsInstance(client._connection, DatabaseConnection)
        mock_connect.assert_called_once()

    @patch("src.pgpx.connection.DatabaseConnection.connect")
    def test_init_no_auto_connect(self, mock_connect):
        """Test DatabaseClient initialization without auto_connect."""
        client = DatabaseClient(self.connection_params, auto_connect=False)

        self.assertIsInstance(client._connection, DatabaseConnection)
        mock_connect.assert_not_called()

    @patch("src.pgpx.connection.DatabaseConnection.is_connected")
    @patch("src.pgpx.connection.DatabaseConnection.connect")
    def test_connect(self, mock_connect, mock_is_connected):
        """Test connect method."""
        mock_is_connected.return_value = False

        client = DatabaseClient(self.connection_params, auto_connect=False)
        result = client.connect()

        self.assertEqual(result, client)
        mock_connect.assert_called_once()

    @patch("src.pgpx.connection.DatabaseConnection.is_connected")
    @patch("src.pgpx.connection.DatabaseConnection.connect")
    def test_connect_already_connected(self, mock_connect, mock_is_connected):
        """Test connect method when already connected."""
        mock_is_connected.return_value = True

        client = DatabaseClient(self.connection_params, auto_connect=False)
        result = client.connect()

        self.assertEqual(result, client)
        mock_connect.assert_not_called()

    @patch("src.pgpx.connection.DatabaseConnection.disconnect")
    def test_disconnect(self, mock_disconnect):
        """Test disconnect method."""
        client = DatabaseClient(self.connection_params, auto_connect=False)
        client.disconnect()

        mock_disconnect.assert_called_once()

    @patch("src.pgpx.connection.DatabaseConnection.is_connected")
    def test_is_connected(self, mock_is_connected):
        """Test is_connected method."""
        mock_is_connected.return_value = True

        client = DatabaseClient(self.connection_params, auto_connect=False)
        result = client.is_connected()

        self.assertTrue(result)
        mock_is_connected.assert_called_once()

    @patch("src.pgpx.connection.DatabaseConnection.connect")
    def test_context_manager(self, mock_connect):
        """Test context manager functionality."""
        client = DatabaseClient(self.connection_params, auto_connect=False)

        with client as context:
            self.assertEqual(context, client)
            mock_connect.assert_called_once()

    @patch("src.pgpx.connection.DatabaseConnection")
    def test_context_manager_no_disconnect(self, MockDatabaseConnection):
        """Test context manager doesn't disconnect on exit."""
        mock_instance = MockDatabaseConnection.return_value
        mock_instance.is_connected.return_value = False

        client = DatabaseClient(self.connection_params, auto_connect=False)

        with client:
            pass  # Do nothing

        # connect should be called but disconnect should not
        mock_instance.connect.assert_called_once()
        mock_instance.disconnect.assert_not_called()

    def test_repr(self):
        """Test string representation."""
        client = DatabaseClient(self.connection_params, auto_connect=False)

        # Mock the is_connected method
        with patch.object(client._connection, "is_connected", return_value=False):
            self.assertEqual(repr(client), "<DatabaseClient status=disconnected>")

        # Mock the is_connected method for connected state
        with patch.object(client._connection, "is_connected", return_value=True):
            self.assertEqual(repr(client), "<DatabaseClient status=connected>")


class TestDatabaseConnectionReal(unittest.TestCase):
    """Test DatabaseConnection class with real PostgreSQL connection."""

    def setUp(self):
        """Set up test fixtures."""
        self.connection_params = get_test_connection_params()

    def test_real_connection(self):
        """Test real connection to PostgreSQL."""
        conn = DatabaseConnection(self.connection_params)

        # Test connection
        self.assertFalse(conn.is_connected())

        # Connect
        conn.connect()
        self.assertTrue(conn.is_connected())

        # Test connection property
        self.assertIsNotNone(conn.connection)

        # Test simple query
        with conn.connection.cursor() as cursor:
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)

        # Disconnect
        conn.disconnect()
        self.assertFalse(conn.is_connected())

    def test_real_connection_context_manager(self):
        """Test real connection with context manager."""
        conn = DatabaseConnection(self.connection_params)

        with conn as context:
            self.assertEqual(context, conn)
            self.assertTrue(conn.is_connected())

            # Test simple query
            with conn.connection.cursor() as cursor:
                cursor.execute("SELECT version()")
                result = cursor.fetchone()
                self.assertIn("PostgreSQL", result[0])

        # Connection should be closed after context
        self.assertFalse(conn.is_connected())

    def test_real_connection_with_invalid_params(self):
        """Test connection with invalid parameters."""
        invalid_params = {
            "host": "localhost",
            "port": 5432,
            "user": "nonexistent",
            "password": "wrong",
            "dbname": "nonexistent",
        }

        conn = DatabaseConnection(invalid_params)

        with self.assertRaises(ConnectionError):
            conn.connect()

        self.assertFalse(conn.is_connected())

    def test_real_connection_context_manager_with_exception(self):
        """Test context manager with exception."""
        conn = DatabaseConnection(self.connection_params)

        try:
            with conn:
                self.assertTrue(conn.is_connected())
                raise ValueError("Test exception")
        except ValueError:
            pass  # Expected

        # Connection should be closed despite exception
        self.assertFalse(conn.is_connected())


class TestDatabaseClientReal(unittest.TestCase):
    """Test DatabaseClient class with real PostgreSQL connection."""

    def setUp(self):
        """Set up test fixtures."""
        self.connection_params = get_test_connection_params()

    def test_real_client_auto_connect(self):
        """Test real client with auto_connect."""
        client = DatabaseClient(self.connection_params, auto_connect=True)

        # Should be connected
        self.assertTrue(client.is_connected())

        # Test simple query
        with client.connection.cursor() as cursor:
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)

        # Disconnect
        client.disconnect()
        self.assertFalse(client.is_connected())

    def test_real_client_no_auto_connect(self):
        """Test real client without auto_connect."""
        client = DatabaseClient(self.connection_params, auto_connect=False)

        # Should not be connected
        self.assertFalse(client.is_connected())

        # Connect manually
        client.connect()
        self.assertTrue(client.is_connected())

        # Test simple query
        with client.connection.cursor() as cursor:
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)

        # Disconnect
        client.disconnect()
        self.assertFalse(client.is_connected())

    def test_real_client_context_manager(self):
        """Test real client with context manager."""
        client = DatabaseClient(self.connection_params, auto_connect=False)

        with client as context:
            self.assertEqual(context, client)
            self.assertTrue(client.is_connected())

            # Test simple query
            with client.connection.cursor() as cursor:
                cursor.execute("SELECT version()")
                result = cursor.fetchone()
                self.assertIn("PostgreSQL", result[0])

        # Should still be connected after context exit
        self.assertTrue(client.is_connected())

        # Clean up
        client.disconnect()
        self.assertFalse(client.is_connected())

    def test_real_client_persistence(self):
        """Test client maintains connection across operations."""
        client = DatabaseClient(self.connection_params, auto_connect=True)

        # First operation
        with client.connection.cursor() as cursor:
            cursor.execute("SELECT 1 as first")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)

        # Second operation (should use same connection)
        with client.connection.cursor() as cursor:
            cursor.execute("SELECT 2 as second")
            result = cursor.fetchone()
            self.assertEqual(result[0], 2)

        # Should still be connected
        self.assertTrue(client.is_connected())

        # Clean up
        client.disconnect()
        self.assertFalse(client.is_connected())


if __name__ == "__main__":
    unittest.main()
