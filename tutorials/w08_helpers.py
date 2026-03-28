"""CSC271 Week 8 Tutorial: SQL DDL"""

import sqlite3
import pandas as pd

### Provided Helper Functions

def create_database(db_name: str) -> None:
    """Create a new SQLite database file named db_name."""
    conn = sqlite3.connect(db_name)
    conn.close()


def add_table(conn: sqlite3.Connection, sql_create: str) -> None:
    """Create a new table in the database connected via conn using
    the SQL statement sql_create."""
    conn.execute(sql_create)
    conn.commit()


def connect(db_name: str) -> sqlite3.Connection:
    """Return a connection to the SQLite database db_name with foreign
    keys enabled.
    """

    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def run_sql(conn: sqlite3.Connection, sql: str) -> pd.DataFrame | None:
    """Run the SQL statement sql using connection conn. Return a DataFrame
    containing the query results if sql is a SELECT statement, or None otherwise.
    """

    if sql.strip().upper().startswith("SELECT"):
        return pd.read_sql_query(sql, conn)
    else:
        conn.execute(sql)
        conn.commit()
        return None


def describe_database(conn: sqlite3.Connection) -> list[tuple[str, pd.DataFrame]]:
    """Return schema information for all tables in the database connected
    to by conn.

    The result is a list of (table_name, schema_df) pairs, where schema_df
    is the DataFrame returned by PRAGMA table_info for that table.
    """

    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    ).fetchall()

    result: list[tuple[str, pd.DataFrame]] = []

    for table, in tables:
        schema = pd.read_sql_query(f"PRAGMA table_info({table});", conn)
        result.append((table, schema))

    return result


def print_database_description(desc: list[tuple[str, pd.DataFrame]]) -> None:
    """Print database schema information for the tables in desc."""

    for table, schema in desc:
        print(f"\nTable: {table}")
        print(schema)

def print_foreign_key(conn: sqlite3.Connection, table: str) -> None:
    """Print the foreign key for a table in schema-notation style."""

    rows = conn.execute(f"PRAGMA foreign_key_list({table});").fetchall()
    if not rows:
        print('No foreign key defined for table {table}')
        return

    fk = rows[0]
    print(f'Table {table}: FOREIGN KEY ({fk[3]}) references {fk[2]}({fk[4]})')