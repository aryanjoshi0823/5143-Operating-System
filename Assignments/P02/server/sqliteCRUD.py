"""
SQLite CRUD Operations
======================
"""

import sqlite3
from prettytable import PrettyTable
from concurrent.futures import ThreadPoolExecutor, as_completed


class SqliteCRUD:
    """
    Comment
    """

    def __init__(self, db_path):
        """
        Initialize database connection and cursor.
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()



#############  running queries ###########

    def __runQuery(self, query, qtype="all", data = None):
        """
        Description:
            Run a query and return the results.
        Args:
            query (str): SQL query to execute.
            qtype (str): Type of query to run (one, many, all). Defaults to 'all'.
            data (list): List of data to pass to the query. Defaults to None.

        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """
        try:
            # data is passed for appending
            if data is not None:
                self.cursor.execute(query,data)
            else:
                self.cursor.execute(query)
            self.conn.commit()

            # for reading from tables.
            # one, many, all or it is None
            rows = []
            if qtype == "one":
                rows = self.cursor.fetchone()
            elif qtype == "many":
                rows = self.cursor.fetchmany()
            elif qtype == "all":
                rows = self.cursor.fetchall()

            # empty data is passed with executed queries.
            return self.__buildResponse(query, True, f"None", rows)
        except sqlite3.Error as e:
            return self.__buildResponse(query, False, f"Error executing query: {e}", [])

    # run_query_in_thread() function, which executes the query in a separate 
    # thread. This is useful for running multiple queries in parallel without 
    # blocking the main FastAPI thread.
    
    def run_query_in_thread(self, queries, qtype="all"):
        results = []
        # Using ThreadPoolExecutor to execute the queries in parallel
        with ThreadPoolExecutor() as executor:
            # Submit each query to be run in a separate thread
            future_to_query = {
                executor.submit(self.__runQuery, query, qtype): query for query in queries
            }

            # As each thread completes, retrieve the result
            for future in as_completed(future_to_query):
                query = future_to_query[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as exc:
                    print(f"Query {query} generated an exception: {exc}")

        return results
  
    def runQuery(self, query):
        """
        Description:
            Test a query.
        Args:
            query (str): SQL query to test.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """
        return self.__runQuery(query)


#############  result formatting ###########

    def __rawResults(self, results):
        """
        Description:
            Convert raw results to a list of table names.
        Args:
            results (list): List of tuples containing query results.
        Returns:
            list: List of table names
        """
        table = []
        for row in results:
            table.append(row[0])
        return table

    def __formattedResults(self, results):
        """
        Description:
            Format results as a PrettyTable.
        Args:
            results (list): List of tuples containing query results.
        Returns:
            PrettyTable: Table object containing the formatted data.
        """
        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(results)
        return table
    
    def __buildResponse(
        self, query: str, success: bool, message: str, data: list
    ) -> dict:
        """
        Description:
            Build a response object.
        Args:
            query (str): SQL query.
            success (bool): Success status.
            message (str): Message to return.
            data (list): Query results.
        Returns:
            dict: Response object containing query, success status, message, and data.
        """
        return {
            "query": query,
            "success": success,
            "message": message,
            "data": data,
        }
    
    def formattedTableName(self, table_name):
        """
        Description:
            Print the table name in a formatted manner.
        Args:
            table_name (str): Name of the table.
        Returns:
            PrettyTable: Table object containing the formatted data.
        """
        self.cursor.execute(f"SELECT * FROM {table_name};")
        table_info = self.cursor.fetchall()

        table_info_list = []

        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(table_info)

        return table
    


#############  tables ###########

    def createTable(self, table_name, columns):
        """
        Description:
            Create a new table with specified columns.
        Args:
            table_name (str): Name of the table.
            columns (list): List of column definitions.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """

        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
        return self.__runQuery(query)

    def showTables(self, raw=True):
        """
        Description:
            Show all tables in the database.

        Args:
            raw (bool): Whether to return raw results or formatted table.
        Returns:
            list: List of table names
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        results = self.cursor.fetchall()

        if not raw:
            return self.__formatted_results(results)
        else:
            return self.__raw_results(results)

    def describeTable(self, table_name, raw=False):
        """
        Description:
            Describe the structure of a table.
        Args:
            table_name (str): Name of the table.
            raw (bool): Whether to return raw data or a PrettyTable.
        Returns:
            list: List of dictionaries containing column information.
        """
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        results = self.cursor.fetchall()
        table = None

        if not raw:
            table = self.__formatted_results(results)

        else:

            table = []

            for column_info in results:
                column_name = column_info[1]
                data_type = column_info[2]
                is_nullable = "NULL" if column_info[3] == 0 else "NOT NULL"
                table.append(
                    {
                        "column_name": column_name,
                        "data_type": data_type,
                        "isnull": is_nullable,
                    }
                )

        return table

    def tableExists(self, table_name):
        """
        Description:
            Check if a table exists.
        Args:
            table_name (str): Name of the table.
        Returns:

        """
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        return self.__runQuery(query, "one")

    def dropTable(self, table_name):
        """
        Description:
            Drop a table by its name.
        Args:
            table_name (str): Name of the table to drop.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """

        # Drop the table if it exists
        query = f"DROP TABLE IF EXISTS {table_name};"
        return self.__runQuery(query)


    


#############  related  to data manipulation ###########
    def insertData(self, table_name, data):
        """
        Description:
            Insert data into a table.
        Args:
            table_name (str): Name of the table.
            data (tuple): Data to insert.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """
        try:
            placeholders = ", ".join(["?"] * len(data))
            query = f"INSERT INTO {table_name} VALUES ({placeholders});"
            return self.__runQuery(query, "None" ,data)
        
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")
            return self.__buildResponse(query, False, f"Error executing query: {e}", [])

    def readTableDataByPid(self, table_name, optional_id = None):
        """Read data from a table, optionally filtered by id.
        
        Args:
            table_name (str): Name of the table.
            optional_id (int, optional): ID to use in the WHERE clause. Default is None.
        """
        try:
            if optional_id is not None:
                query = f"SELECT * FROM {table_name} WHERE pid = ?;"
            else:
                query = f"SELECT * FROM {table_name};"
            return self.__runQuery(query, "all" , (optional_id,))
        
        except sqlite3.Error as e:
            return self.__buildResponse(query, False, f"Error reading data {e}", [])

    def readFileByPid(self, file_name, pid):
        """read file from files table.
        
        Args:
            file_name (str): Name of the file.
            pid (int): ID to use in the WHERE clause.
        """
        try:
            query = "SELECT * FROM files WHERE name = ? AND pid = ?"
            return self.__runQuery(query, "all" , (file_name, pid))
        
        except sqlite3.Error as e:
            return self.__buildResponse(query, False, f"Error reading data {e}", [])

    def readDirectoriesByPid(self, dir_name, pid):
        """read directory data from Directories table.
        
        Args:
            dir_name (str): Name of the file.
            pid (int): ID to use in the WHERE clause.
        """
        try:
            query = "SELECT * FROM directories WHERE name = ? AND pid = ?"
            return self.__runQuery(query, "all" , (dir_name, pid))
        
        except sqlite3.Error as e:
            return self.__buildResponse(query, False, f"Error reading data {e}", [])
        
    def readFileById(self, id):
        """read file from files table.
        Args:
            id (int): ID to use to fetch the record from files tables.
        """
        try:
            query = "SELECT * FROM files WHERE id = ?"
            return self.__runQuery(query, "all" , (id,))
        
        except sqlite3.Error as e:
            return self.__buildResponse(query, False, f"Error reading data {e}", [])
    
    def postHistory(self, id):
        """read file from files History table.
        
        Args:
            id (int): ID to use to fetch the record from files tables.
        """
        try:
            query = "SELECT * FROM files WHERE id = ?"
            return self.__runQuery(query, "all" , (id,))
        
        except sqlite3.Error as e:
            return self.__buildResponse(query, False, f"Error reading data {e}", [])
        
    def getHistory(self):
        try:
            query = "SELECT * FROM History"
            return self.__runQuery(query, "all")
        
        except sqlite3.Error as e:
            return self.__buildResponse(query, False, f"Error reading data {e}", [])

    def readDirectoryById(self, id):
        """read directory record by id 
        
        Args:
            id (int): ID to use to fetch the record from files tables.
        """
        try:
            query = "SELECT * FROM directories WHERE id = ?"
            return self.__runQuery(query, "all" , (id,))
        
        except sqlite3.Error as e:
            return self.__buildResponse(query, False, f"Error reading data {e}", [])
        
    def  getDirectoryId(self, dir_name, pid):
        """get directory id from directories table.
        
        Args:
            dir_name (str): Name of the directory.
            pid (int): ID to use in the WHERE clause.
        """
        try:
            query = f"SELECT id FROM directories WHERE name = '{dir_name[0]}' AND pid = '{pid}'"
            return self.__runQuery(query, "all")
        
        except sqlite3.Error as e:
            return self.__buildResponse(query, False, f"Error reading data {e}", [])
   
    def readDirContentByPid(self, id: int):
        try:
            query = """
                SELECT id, pid, oid, name, size, created_at, modified_at, read_permission, write_permission, execute_permission, 
                        world_read, world_write, world_execute,'file' AS type  
                FROM files WHERE pid = ?

                UNION ALL
        
                SELECT id, pid, oid, name, NULL AS size, created_at, modified_at, read_permission, write_permission, execute_permission, 
                    world_read, world_write, world_execute,'directory' AS type 
                FROM directories WHERE pid = ?
            """
            return self.__runQuery(query, "all" , (id,id))
        
        except sqlite3.Error as e:
            return self.__buildResponse(query, False, f"Error reading data {e}", [])

    def updateData(self, table_name, target, new_value, where_column, where_value):
        """
        Description:
            Update data in a table based on a condition.
        Args:
            table_name (str): Name of the table.
            column (str): Column to update.
            new_value (str): New value to set.
            condition_column (str): Column to use in the WHERE clause.
            condition_value (str): Value to use in the WHERE clause.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """
        query = f'UPDATE "{table_name}" SET {target} = "{new_value}" WHERE "{where_column}" = "{where_value}";'
        return self.__runQuery(query, None)

    def getFilePermission(self, name, id):
        try:
            query = """
                SELECT read_permission, write_permission, execute_permission, 
                    world_read, world_write, world_execute 
                FROM files 
                WHERE name = ? AND id = ?
                """
            return self.__runQuery(query, "all" ,(name, id))
            
        except sqlite3.Error as e:
            return self.__buildResponse(query, False, f"Error reading data {e}", [])
        
    def updateFilePermission(self, name, pid, r, w, e, wr, ww, we):
        try:
            query = """
                UPDATE files 
                SET read_permission = ?, write_permission = ?, execute_permission = ?, 
                    world_read = ?, world_write = ?, world_execute = ?
                WHERE name = ? AND id = ?
                """
            return self.__runQuery(query, "all" , (r, w, e, wr, ww, we, name, pid))
        
        except sqlite3.Error as err:
            return self.__buildResponse(query, False, f"Error reading data {err}", [])

    def getDirPermission(self, name, id):
        try:
            query = """
                SELECT read_permission, write_permission, execute_permission, 
                    world_read, world_write, world_execute 
                FROM directories 
                WHERE name = ? AND id = ?
                """
            return self.__runQuery(query, "all" ,(name, id))
            
        except sqlite3.Error as e:
            return self.__buildResponse(query, False, f"Error reading data {e}", [])
        
    def updateDirPermission(self, name, pid, r, w, e, wr, ww, we):
        try:
            query = """
                UPDATE directories 
                SET read_permission = ?, write_permission = ?, execute_permission = ?, 
                    world_read = ?, world_write = ?, world_execute = ?
                WHERE name = ? AND id = ?
                """
            return self.__runQuery(query, "all" , (r, w, e, wr, ww, we, name, pid))
        
        except sqlite3.Error as err:
            return self.__buildResponse(query, False, f"Error reading data {err}", [])
    
    def deleteData(self, table_name, condition_column, condition_value):
        """
        Description:
            Delete data from a table based on a single condition.
        Args:
            table_name (str): Name of the table.
            condition_column (str): Column to use in the WHERE clause.
            condition_value (str): Value to use in the WHERE clause.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """
        query = f'DELETE FROM "{table_name}" WHERE "{condition_column}" = "{condition_value}";'
        return self.__runQuery(query)

    def closeConnection(self):
        """Close the database connection."""
        self.conn.close()


