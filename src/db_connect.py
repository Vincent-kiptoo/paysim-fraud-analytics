from getpass import getpass
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
import pandas as pd
import prettytable
import os

_db_engine = None
_db_connection = None
_connection_string = None

def connect_to_db(user="root", host="127.0.0.1", port=3306, db=None, password=None):
    """Get cached database connection and engine
    
    Will prompt for database name and password if not provided
    """
    global _db_engine, _db_connection, _connection_string
    
    # If no database specified, ask for it
    if db is None:
        db = input("Please enter database name: ").strip()

        print(f"   Using default: {db}")
    
    # If no password specified, ask for it
    if password is None:
        password = getpass(f" Please enter the password for {user}@{host}: ")
    
    if _db_connection is None:
        try:
            encoded_password = quote_plus(password)
            _connection_string = f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{db}"
            _db_engine = create_engine(
                _connection_string,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False
            )
            _db_connection = _db_engine.connect()
            
            # Test connection
            _db_connection.execute(text("SELECT 1"))
            
            print(f"\n The notebook is successfully connected to MYSQL!")
            print(f"  Server: {host}:{port}")
            print(f"  Database in use: {db}")
            print(f"  User: {user}")
            
            # Setup SQL magic
            _setup_sql_magic()
            
        except Exception as e:
            print(f"\n Connection failed: {e}")
            print("\n Troubleshooting tips:")
            print("  1. Check if database name is correct")
            print("  2. Verify MySQL is running")
            print("  3. Confirm username and password")
            _db_connection = None
            _db_engine = None
            raise
    
    return _db_engine, _db_connection

def _setup_sql_magic():
    """Setup SQL magic for Jupyter notebooks"""
    try:
        ip = get_ipython()
        if ip and _connection_string:
            ip.run_line_magic("load_ext", "sql")
            
            # Fix prettytable style issue
            if not hasattr(prettytable, 'DEFAULT'):
                prettytable.DEFAULT = prettytable.PLAIN_COLUMNS
            
            ip.run_line_magic("sql", _connection_string)
            
            try:
                ip.run_line_magic("config", "SqlMagic.style = 'DEFAULT'")
            except:
                pass
            
            print("SQL magic configured - use %%sql in any cell!")
    except Exception as e:
        pass

def query(sql, **kwargs):
    """Run a SQL query and return pandas DataFrame"""
    engine, conn = connect_to_db()
    return pd.read_sql(sql, conn, **kwargs)

def show_databases():
    """List all databases available on the server"""
    engine, conn = connect_to_db()
    result = pd.read_sql("SHOW DATABASES", conn)
    print("\n Available databases:")
    print("-" * 40)
    for i, db in enumerate(result.iloc[:, 0], 1):
        print(f"  {i:2}. {db}")
    return result

def show_tables():
    """List all tables in current database"""
    engine, conn = connect_to_db()
    result = pd.read_sql("SHOW TABLES", conn)
    tables = result.iloc[:, 0].tolist()
    
    print(f"\n Tables in database:")
    print("-" * 40)
    for i, table in enumerate(tables, 1):
        try:
            count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table}", conn).iloc[0, 0]
            print(f"  {i:2}. {table:<30} ({count:>10,} rows)")
        except:
            print(f"  {i:2}. {table:<30}")
    return result

def describe_table(table_name):
    """Show table structure"""
    engine, conn = connect_to_db()
    print(f"\n Table structure: {table_name}")
    print("-" * 50)
    schema = pd.read_sql(f"DESCRIBE {table_name}", conn)
    display(schema)
    return schema

def switch_database(db_name):
    """Switch to a different database"""
    global _db_engine, _db_connection, _connection_string
    
    # Close current connection
    if _db_connection:
        _db_connection.close()
        _db_engine = None
        _db_connection = None
        _connection_string = None
    
    # Connect to new database
    print(f"\n switching to database: {db_name}")
    return connect_to_db(db=db_name)

def disconnect():
    """Close database connection"""
    global _db_engine, _db_connection, _connection_string
    if _db_connection:
        _db_connection.close()
        _db_engine = None
        _db_connection = None
        _connection_string = None
        print("✓ Database connection closed")