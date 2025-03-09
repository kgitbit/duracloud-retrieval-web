import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
import glob
from datetime import datetime

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }

    def connect(self):
        try:
            connection = mysql.connector.connect(**self.config)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def migrate_csv_logs(self, logs_directory):
        print(f"Starting migration from directory: {logs_directory}")
        connection = self.connect()
        if not connection:
            print("Failed to connect to database")
            return {"error": "Failed to connect to database"}

        try:
            cursor = connection.cursor()
            csv_files = glob.glob(os.path.join(logs_directory, '*.csv'))
            print(f"Found CSV files: {csv_files}")
            
            if not csv_files:
                print(f"No CSV files found in directory: {logs_directory}")
                return {"error": f"No CSV files found in directory: {logs_directory}"}
            
            total_processed = 0
            for csv_file in csv_files:
                try:
                    print(f"Processing file: {csv_file}")
                    # Read CSV file with more flexible options
                    df = pd.read_csv(
                        csv_file,
                        skipinitialspace=True,
                        lineterminator='\n',
                        encoding='utf-8'
                    )
                    print(f"CSV columns found: {df.columns.tolist()}")
                    
                    # Clean up column names - remove leading/trailing spaces and convert to lowercase
                    df.columns = df.columns.str.strip().str.lower()
                    print(f"Cleaned columns: {df.columns.tolist()}")
                    
                    # Map CSV columns to database columns
                    column_mapping = {
                        'result': 'result',
                        'spaceid': 'space_id',
                        'contentid': 'content_id',
                        'local file': 'local_file',
                        'error': 'error_message',
                        'attempts': 'attempts',
                        'date': 'download_date'
                    }
                    
                    # Check if all required columns exist
                    missing_columns = [col for col in column_mapping.keys() if col not in df.columns]
                    if missing_columns:
                        error_msg = f"Missing columns in CSV: {missing_columns}. Available columns: {df.columns.tolist()}"
                        print(error_msg)
                        return {"error": error_msg}
                    
                    # Rename columns to match database
                    df = df.rename(columns=column_mapping)
                    print("Columns renamed successfully")
                    print(f"Final columns: {df.columns.tolist()}")
                    
                    # Process each row
                    rows_processed = 0
                    for index, row in df.iterrows():
                        print(f"Processing row {index + 1}: {row.to_dict()}")
                        query = """
                        INSERT INTO download_history 
                        (result, space_id, content_id, local_file, error_message, attempts, download_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                        try:
                            values = (
                                str(row['result']).strip(),
                                str(row['space_id']).strip(),
                                str(row['content_id']).strip(),
                                str(row['local_file']).strip(),
                                None if pd.isna(row['error_message']) or str(row['error_message']).lower() == 'none' else str(row['error_message']).strip(),
                                int(row['attempts']),
                                datetime.strptime(str(row['download_date']).strip(), '%Y-%m-%dT%H:%M:%S.%f')
                            )
                            cursor.execute(query, values)
                            connection.commit()
                            rows_processed += 1
                            print(f"Successfully inserted row {index + 1}")
                        except Exception as row_error:
                            error_msg = f"Error processing row {index + 1} in {csv_file}: {str(row_error)}"
                            print(f"Row data: {row.to_dict()}")
                            print(error_msg)
                            return {"error": error_msg}
                    
                    total_processed += rows_processed
                    print(f"Successfully processed {rows_processed} rows from file: {csv_file}")
                    
                except pd.errors.EmptyDataError:
                    error_msg = f"CSV file is empty: {csv_file}"
                    print(error_msg)
                    return {"error": error_msg}
                except KeyError as e:
                    error_msg = f"Missing required column in CSV: {str(e)} in file {csv_file}"
                    print(error_msg)
                    return {"error": error_msg}
                except ValueError as e:
                    error_msg = f"Invalid data format in CSV: {str(e)} in file {csv_file}"
                    print(error_msg)
                    return {"error": error_msg}
                except Error as e:
                    error_msg = f"Database error while processing {csv_file}: {str(e)}"
                    print(error_msg)
                    return {"error": error_msg}
                except Exception as e:
                    error_msg = f"Unexpected error processing {csv_file}: {str(e)}"
                    print(error_msg)
                    return {"error": error_msg}
            
            success_msg = f"Log migration completed successfully. Processed {total_processed} records from {len(csv_files)} files."
            print(success_msg)
            return {"message": success_msg}
            
        except Error as e:
            error_msg = f"Error migrating CSV data: {str(e)}"
            print(error_msg)
            return {"error": error_msg}
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
                print("Database connection closed")

    def get_download_history(self):
        connection = self.connect()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT * FROM download_history 
            ORDER BY download_date DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
            
        except Error as e:
            print(f"Error fetching download history: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def add_download_record(self, username, result, space_id, content_id, local_file, error_message=None, attempts=1):
        connection = self.connect()
        if not connection:
            return False

        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO download_history 
            (username, result, space_id, content_id, local_file, error_message, attempts, download_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            """
            values = (username, result, space_id, content_id, local_file, error_message, attempts)
            cursor.execute(query, values)
            connection.commit()
            return True
            
        except Error as e:
            print(f"Error adding download record: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()