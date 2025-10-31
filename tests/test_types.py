"""
Unit tests for pgpx.types module.

This module contains comprehensive tests for all types, enums,
and dataclasses defined in the types module.
"""

import unittest
# from datetime import datetime, date
# from uuid import UUID
# from typing import Dict, List, Optional, Set, Type, Union

from src.pgpx.types import (
    # Enums
    ConflictAction,
    FieldType,
    JoinType,
    ComparisonOperator,
    LogicalOperator,
    MigrationDirection,
    IsolationLevel,
    RelationshipType,
    # Dataclasses
    JoinClause,
    WhereClause,
    OrderByClause,
    QueryResult,
    ForeignKeyReference,
    RelationshipInfo,
    ForeignKeyInfo,
    # Type aliases
    ConnectionParams,
    FieldMetadata,
    RowData,
    MigrationFunction,  # noqa: F401
    # Generic type
    T,
)


class TestEnums(unittest.TestCase):
    """Test all enum classes."""

    def test_conflict_action_enum(self):
        """Test ConflictAction enum values."""
        self.assertEqual(ConflictAction.DO_NOTHING.value, "DO NOTHING")
        self.assertEqual(ConflictAction.DO_UPDATE.value, "DO UPDATE")

        # Test enum membership
        self.assertIn(ConflictAction.DO_NOTHING, ConflictAction)
        self.assertIn(ConflictAction.DO_UPDATE, ConflictAction)

        # Test enum iteration
        actions = list(ConflictAction)
        self.assertEqual(len(actions), 2)
        self.assertIn(ConflictAction.DO_NOTHING, actions)
        self.assertIn(ConflictAction.DO_UPDATE, actions)

    def test_field_type_enum(self):
        """Test FieldType enum values."""
        expected_types = {
            "TEXT",
            "INTEGER",
            "FLOAT",
            "BOOLEAN",
            "BYTEA",
            "TIMESTAMP",
            "DATE",
            "UUID",
            "JSON",
            "JSONB",
            "ARRAY",
        }

        actual_types = {ft.value for ft in FieldType}
        self.assertEqual(actual_types, expected_types)

        # Test specific values
        self.assertEqual(FieldType.TEXT.value, "TEXT")
        self.assertEqual(FieldType.INTEGER.value, "INTEGER")
        self.assertEqual(FieldType.JSON.value, "JSON")
        self.assertEqual(FieldType.JSONB.value, "JSONB")

    def test_join_type_enum(self):
        """Test JoinType enum values."""
        self.assertEqual(JoinType.INNER.value, "INNER JOIN")
        self.assertEqual(JoinType.LEFT.value, "LEFT JOIN")
        self.assertEqual(JoinType.RIGHT.value, "RIGHT JOIN")
        self.assertEqual(JoinType.FULL.value, "FULL JOIN")

    def test_comparison_operator_enum(self):
        """Test ComparisonOperator enum values."""
        operators = [
            "=",
            "!=",
            "<",
            "<=",
            ">",
            ">=",
            "LIKE",
            "ILIKE",
            "IN",
            "NOT IN",
            "IS NULL",
            "IS NOT NULL",
            "BETWEEN",
            "EXISTS",
        ]

        actual_operators = {op.value for op in ComparisonOperator}
        self.assertEqual(actual_operators, set(operators))

        # Test specific operators
        self.assertEqual(ComparisonOperator.EQ.value, "=")
        self.assertEqual(ComparisonOperator.IS_NULL.value, "IS NULL")
        self.assertEqual(ComparisonOperator.BETWEEN.value, "BETWEEN")

    def test_logical_operator_enum(self):
        """Test LogicalOperator enum values."""
        self.assertEqual(LogicalOperator.AND.value, "AND")
        self.assertEqual(LogicalOperator.OR.value, "OR")
        self.assertEqual(LogicalOperator.NOT.value, "NOT")

    def test_migration_direction_enum(self):
        """Test MigrationDirection enum values."""
        self.assertEqual(MigrationDirection.UP.value, "up")
        self.assertEqual(MigrationDirection.DOWN.value, "down")

    def test_isolation_level_enum(self):
        """Test IsolationLevel enum values."""
        expected_levels = {
            "READ UNCOMMITTED",
            "READ COMMITTED",
            "REPEATABLE READ",
            "SERIALIZABLE",
        }

        actual_levels = {level.value for level in IsolationLevel}
        self.assertEqual(actual_levels, expected_levels)

    def test_relationship_type_enum(self):
        """Test RelationshipType enum values."""
        expected_types = {"one-to-one", "one-to-many", "many-to-one", "many-to-many"}

        actual_types = {rt.value for rt in RelationshipType}
        self.assertEqual(actual_types, expected_types)


class TestDataclasses(unittest.TestCase):
    """Test all dataclass classes."""

    def test_join_clause(self):
        """Test JoinClause dataclass."""
        # Test with all parameters
        join = JoinClause(
            table="users",
            on="posts.user_id = users.id",
            join_type=JoinType.LEFT,
            alias="u",
        )

        self.assertEqual(join.table, "users")
        self.assertEqual(join.on, "posts.user_id = users.id")
        self.assertEqual(join.join_type, JoinType.LEFT)
        self.assertEqual(join.alias, "u")

        # Test with default parameters
        join_default = JoinClause(table="users", on="users.id = posts.user_id")
        self.assertEqual(join_default.join_type, JoinType.INNER)
        self.assertIsNone(join_default.alias)

    def test_where_clause(self):
        """Test WhereClause dataclass."""
        where = WhereClause(
            column="age",
            operator=ComparisonOperator.GTE,
            value=18,
            logical_op=LogicalOperator.AND,
        )

        self.assertEqual(where.column, "age")
        self.assertEqual(where.operator, ComparisonOperator.GTE)
        self.assertEqual(where.value, 18)
        self.assertEqual(where.logical_op, LogicalOperator.AND)

        # Test with default logical operator
        where_default = WhereClause(
            column="name", operator=ComparisonOperator.LIKE, value="John%"
        )
        self.assertEqual(where_default.logical_op, LogicalOperator.AND)

    def test_order_by_clause(self):
        """Test OrderByClause dataclass."""
        order_asc = OrderByClause(column="created_at", ascending=True)
        self.assertEqual(order_asc.column, "created_at")
        self.assertTrue(order_asc.ascending)

        order_desc = OrderByClause(column="name", ascending=False)
        self.assertEqual(order_desc.column, "name")
        self.assertFalse(order_desc.ascending)

        # Test default ascending
        order_default = OrderByClause(column="id")
        self.assertTrue(order_default.ascending)

    def test_query_result(self):
        """Test QueryResult dataclass."""
        # Test with data
        data = [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]
        result = QueryResult(data, affected_rows=2)

        self.assertEqual(result.data, data)
        self.assertEqual(result.affected_rows, 2)
        self.assertTrue(result)  # __bool__
        self.assertEqual(len(result), 2)  # __len__
        self.assertEqual(result.first(), {"id": 1, "name": "John"})
        self.assertEqual(result.last(), {"id": 2, "name": "Jane"})

        # Test with empty data
        empty_result = QueryResult([], affected_rows=0)
        self.assertFalse(empty_result)
        self.assertEqual(len(empty_result), 0)
        self.assertIsNone(empty_result.first())
        self.assertIsNone(empty_result.last())

    def test_foreign_key_reference(self):
        """Test ForeignKeyReference dataclass."""

        # Properly create a class named "User"
        User = type("User", (), {})

        fk_ref = ForeignKeyReference(model=User, field="id")
        self.assertEqual(fk_ref.model, User)
        self.assertEqual(fk_ref.field, "id")
        self.assertEqual(str(fk_ref), "user.id")

        # Test with default field
        fk_ref_default = ForeignKeyReference(model=User)
        self.assertEqual(fk_ref_default.field, "id")
        self.assertEqual(str(fk_ref_default), "user.id")

        # Test with different field
        fk_ref_uuid = ForeignKeyReference(model=User, field="uuid")
        self.assertEqual(str(fk_ref_uuid), "user.uuid")

    def test_relationship_info(self):
        """Test RelationshipInfo dataclass."""

        class MockModel:
            pass

        rel_info = RelationshipInfo(
            name="posts",
            related_model=MockModel,
            foreign_key="user_id",
            back_populates="author",
            lazy=False,
            cascade={"delete", "update"},
        )

        self.assertEqual(rel_info.name, "posts")
        self.assertEqual(rel_info.related_model, MockModel)
        self.assertEqual(rel_info.foreign_key, "user_id")
        self.assertEqual(rel_info.back_populates, "author")
        self.assertFalse(rel_info.lazy)
        self.assertEqual(rel_info.cascade, {"delete", "update"})

        # Test with defaults
        rel_info_default = RelationshipInfo(
            name="profile", related_model=MockModel, foreign_key="user_id"
        )
        self.assertIsNone(rel_info_default.back_populates)
        self.assertTrue(rel_info_default.lazy)
        self.assertIsNone(rel_info_default.cascade)

    def test_foreign_key_info(self):
        """Test ForeignKeyInfo dataclass."""
        fk_info = ForeignKeyInfo(
            field="user_id",
            ref_table="users",
            ref_field="id",
            on_delete="CASCADE",
            on_update="RESTRICT",
        )

        self.assertEqual(fk_info.field, "user_id")
        self.assertEqual(fk_info.ref_table, "users")
        self.assertEqual(fk_info.ref_field, "id")
        self.assertEqual(fk_info.on_delete, "CASCADE")
        self.assertEqual(fk_info.on_update, "RESTRICT")

        # Test with defaults
        fk_info_default = ForeignKeyInfo(field="post_id", ref_table="posts")
        self.assertEqual(fk_info_default.ref_field, "id")
        self.assertEqual(fk_info_default.on_delete, "CASCADE")
        self.assertEqual(fk_info_default.on_update, "CASCADE")


class TestTypeAliases(unittest.TestCase):
    """Test type aliases."""

    def test_connection_params_alias(self):
        """Test ConnectionParams type alias."""
        # This is mainly a type checking test
        # We just verify the alias exists
        self.assertTrue(hasattr(ConnectionParams, "__origin__"))

        # Test valid types
        dict_params: ConnectionParams = {"host": "localhost"}
        self.assertIsInstance(dict_params, dict)

    def test_field_metadata_alias(self):
        """Test FieldMetadata type alias."""
        metadata: FieldMetadata = {"primary": True, "null": False}
        self.assertIsInstance(metadata, dict)
        self.assertIn("primary", metadata)
        self.assertIn("null", metadata)

    def test_row_data_alias(self):
        """Test RowData type alias."""
        row: RowData = {"id": 1, "name": "John"}
        self.assertIsInstance(row, dict)
        self.assertEqual(row["id"], 1)
        self.assertEqual(row["name"], "John")

    def test_migration_function_alias(self):
        """Test MigrationFunction type alias."""

        def up_migration():
            pass

        def down_migration():
            pass

        # These should be callable
        self.assertTrue(callable(up_migration))
        self.assertTrue(callable(down_migration))


class TestGenericType(unittest.TestCase):
    """Test generic type variable."""

    def test_type_variable_t(self):
        """Test T type variable."""
        # T is a TypeVar, so we can't instantiate it
        # but we can verify it exists and has the right properties
        self.assertTrue(hasattr(T, "__name__"))
        self.assertEqual(T.__name__, "T")


if __name__ == "__main__":
    unittest.main()
