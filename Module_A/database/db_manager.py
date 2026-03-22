from .table import Table

class DatabaseManager:
    """Manages multiple Table structures within the lightweight DBMS."""
    
    def __init__(self):
        # Dictionary to store multiple tables by their string name
        self.tables = {}

    def create_table(self, table_name, order=4):
        """Create a new table if it doesn't already exist."""
        if table_name in self.tables:
            print(f"Error: Table '{table_name}' already exists.")
            return False
            
        self.tables[table_name] = Table(table_name, order=order)
        print(f"Success: Table '{table_name}' created.")
        return True

    def get_table(self, table_name):
        """Retrieve a table object by its name."""
        if table_name not in self.tables:
            print(f"Error: Table '{table_name}' does not exist.")
            return None
            
        return self.tables[table_name]

    def drop_table(self, table_name):
        """Delete an existing table from the database."""
        if table_name in self.tables:
            del self.tables[table_name]
            print(f"Success: Table '{table_name}' dropped.")
            return True
            
        print(f"Error: Table '{table_name}' does not exist.")
        return False
        
    def list_tables(self):
        """Return a list of all table names in the database."""
        return list(self.tables.keys())