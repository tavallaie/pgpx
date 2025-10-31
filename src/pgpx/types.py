"""
Core type definitions and enums for the pgpx library.

This module contains all the fundamental types, enums, and dataclasses
used throughout the pgpx library for type safety and clarity.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Type, TypeVar, Callable, Set
from dataclasses import dataclass

# Generic type variable for model classes
T = TypeVar("T")


class ConflictAction(Enum):
    """Enum for conflict resolution strategies in idempotent operations."""

    DO_NOTHING = "DO NOTHING"
    DO_UPDATE = "DO UPDATE"


class FieldType(Enum):
    """Supported field types for schema mapping."""

    TEXT = "TEXT"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    BYTEA = "BYTEA"
    TIMESTAMP = "TIMESTAMP"
    DATE = "DATE"
    UUID = "UUID"
    JSON = "JSON"
    JSONB = "JSONB"
    ARRAY = "ARRAY"


class JoinType(Enum):
    """Types of joins for query building."""

    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL JOIN"


class ComparisonOperator(Enum):
    """Comparison operators for query building."""

    EQ = "="
    NE = "!="
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="
    LIKE = "LIKE"
    ILIKE = "ILIKE"
    IN = "IN"
    NOT_IN = "NOT IN"
    IS_NULL = "IS NULL"
    IS_NOT_NULL = "IS NOT NULL"
    BETWEEN = "BETWEEN"
    EXISTS = "EXISTS"


class LogicalOperator(Enum):
    """Logical operators for query building."""

    AND = "AND"
    OR = "OR"
    NOT = "NOT"


class MigrationDirection(Enum):
    """Migration direction."""

    UP = "up"
    DOWN = "down"


class IsolationLevel(Enum):
    """Transaction isolation levels."""

    READ_UNCOMMITTED = "READ UNCOMMITTED"
    READ_COMMITTED = "READ COMMITTED"
    REPEATABLE_READ = "REPEATABLE READ"
    SERIALIZABLE = "SERIALIZABLE"


class RelationshipType(Enum):
    """Types of relationships between models."""

    ONE_TO_ONE = "one-to-one"
    ONE_TO_MANY = "one-to-many"
    MANY_TO_ONE = "many-to-one"
    MANY_TO_MANY = "many-to-many"


@dataclass
class JoinClause:
    """Represents a join clause in a query."""

    table: str
    on: str
    join_type: JoinType = JoinType.INNER
    alias: Optional[str] = None


@dataclass
class WhereClause:
    """Represents a where clause in a query."""

    column: str
    operator: ComparisonOperator
    value: Any
    logical_op: LogicalOperator = LogicalOperator.AND


@dataclass
class OrderByClause:
    """Represents an order by clause in a query."""

    column: str
    ascending: bool = True


@dataclass
class QueryResult:
    """Container for query results with metadata."""

    def __init__(self, data: List[Dict], affected_rows: int = 0):
        self.data = data
        self.affected_rows = affected_rows

    def __bool__(self) -> bool:
        """Return True if there is data."""
        return bool(self.data)

    def __len__(self) -> int:
        """Return the number of rows."""
        return len(self.data)

    def first(self) -> Optional[Dict]:
        """Return the first row or None."""
        return self.data[0] if self.data else None

    def last(self) -> Optional[Dict]:
        """Return the last row or None."""
        return self.data[-1] if self.data else None


@dataclass
class ForeignKeyReference:
    """Information about a foreign key reference using dot notation."""

    model: Type
    field: str = "id"

    def __str__(self) -> str:
        """String representation of the reference."""
        return f"{self.model.__name__.lower()}.{self.field}"


@dataclass
class RelationshipInfo:
    """Information about a model relationship."""

    name: str
    related_model: Type
    foreign_key: str
    back_populates: Optional[str] = None
    lazy: bool = True
    cascade: Optional[Set[str]] = None


@dataclass
class ForeignKeyInfo:
    """Information about a foreign key relationship."""

    field: str
    ref_table: str
    ref_field: str = "id"
    on_delete: str = "CASCADE"
    on_update: str = "CASCADE"


# Type aliases for better readability
ConnectionParams = Dict[str, Any]
FieldMetadata = Dict[str, Any]
RowData = Dict[str, Any]
MigrationFunction = Callable[[], None]
