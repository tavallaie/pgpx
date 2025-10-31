"""
Database connection management for pgpx.

This module provides classes for managing PostgreSQL database connections
with support for context managers and persistent connections.
"""

import psycopg
from typing import Any, Dict

from .exceptions import ConnectionError
from .types import ConnectionParams


class DatabaseConnection:
    """Manages database connections with automatic cleanup and context manager support."""

    def __init__(self, connection_params: ConnectionParams):
        """Initialize connection parameters.

        Args:
            connection_params: Database connection configuration
        """
        self.connection_params = self._normalize_params(connection_params)
        self._connection = None
        self._transaction_manager = None

    def _normalize_params(self, params: ConnectionParams) -> Dict[str, Any]:
        """Normalize connection parameters to dictionary format.

        Args:
            params: Connection parameters in various formats

        Returns:
            Normalized connection parameters as dictionary
        """
        if hasattr(params, "to_dict"):
            return params.to_dict()
        return params if isinstance(params, dict) else {}

    def connect(self) -> "DatabaseConnection":
        """Establish database connection.

        Returns:
            Self for method chaining

        Raises:
            ConnectionError: If connection fails
        """
        try:
            self._connection = psycopg.connect(**self.connection_params)
            return self
        except psycopg.Error as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

    def disconnect(self) -> None:
        """Close database connection if it exists."""
        if self._connection:
            try:
                self._connection.close()
            except Exception:
                pass  # Ignore errors during cleanup
            finally:
                self._connection = None

    @property
    def connection(self):
        """Get the underlying psycopg connection.

        Returns:
            The psycopg connection object

        Raises:
            ConnectionError: If not connected
        """
        if not self._connection:
            raise ConnectionError("Not connected to database")
        return self._connection

    def is_connected(self) -> bool:
        """Check if connection is active.

        Returns:
            True if connection is active, False otherwise
        """
        return self._connection is not None and not self._connection.closed

    def __enter__(self) -> "DatabaseConnection":
        """Context manager entry.

        Returns:
            Self for method chaining
        """
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit with cleanup.

        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        self.disconnect()

    def __repr__(self) -> str:
        """String representation showing connection status.

        Returns:
            String representation of the connection
        """
        status = "connected" if self.is_connected() else "disconnected"
        return f"<DatabaseConnection status={status}>"


class DatabaseClient:
    """Database client that maintains a persistent connection."""

    def __init__(self, connection_params: ConnectionParams, auto_connect: bool = True):
        """Initialize database client.

        Args:
            connection_params: Database connection configuration
            auto_connect: Whether to connect immediately
        """
        self.connection_params = connection_params
        self._connection = DatabaseConnection(connection_params)

        if auto_connect:
            self._connection.connect()

    @property
    def connection(self) -> DatabaseConnection:
        """Get the underlying connection.

        Returns:
            The DatabaseConnection instance
        """
        return self._connection

    def connect(self) -> "DatabaseClient":
        """Connect to the database.

        Returns:
            Self for method chaining
        """
        if not self._connection.is_connected():
            self._connection.connect()
        return self

    def disconnect(self) -> None:
        """Disconnect from the database."""
        self._connection.disconnect()

    def is_connected(self) -> bool:
        """Check if connected to the database.

        Returns:
            True if connected, False otherwise
        """
        return self._connection.is_connected()

    def __enter__(self) -> "DatabaseClient":
        """Context manager entry.

        Returns:
            Self for method chaining
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit with cleanup.

        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        # Don't disconnect by default to allow reuse
        pass

    def __repr__(self) -> str:
        """String representation showing connection status.

        Returns:
            String representation of the client
        """
        status = "connected" if self.is_connected() else "disconnected"
        return f"<DatabaseClient status={status}>"
