from .bplustree import BPlusTree

class Table:
    """A Table abstraction that uses a B+ Tree as its underlying index."""
    
    def __init__(self, name, order=4):
        self.name = name
        self.index = BPlusTree(order=order)

    def insert_record(self, primary_key, record_data):
        """Insert a row/record into the table."""
        self.index.insert(primary_key, record_data)

    def get_record(self, primary_key):
        """Fetch a record by its primary key."""
        return self.index.search(primary_key)

    def update_record(self, primary_key, new_record_data):
        """Update an existing record."""
        return self.index.update(primary_key, new_record_data)

    def delete_record(self, primary_key):
        """Remove a record from the table."""
        return self.index.delete(primary_key)

    def range_query(self, start_key, end_key):
        """Fetch records within a specific primary key range."""
        return self.index.range_query(start_key, end_key)
        
    def get_all_records(self):
        """Fetch all records in the table."""
        return self.index.get_all()