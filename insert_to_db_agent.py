import psycopg2
from db_helper import get_db_connection

def insert_to_db_agent(state):
    """
    Takes structured data and instructions to insert data into the correct database tables.
    """
    conn = get_db_connection()  # Get the DB connection
    cursor = conn.cursor()

    instructions = state.get("instructions")  # Instructions specify which table to target
    

    structured_data = state.get("structured_data")  # This is the JSON data to be inserted
   


    try:
        # Depending on what it gets, insert or alter data into the correct table
        target_table = instructions.get("target_table")

        if instructions["type"] == "alter":
            column_name =   structured_data.get("column_name")
            type = structured_data.get("type")

            cursor.execute(
                f"alter table {target_table} ADD COLUMN IF NOT EXISTS {column_name} {type};" 
                
            )
            print("Altered student table.")

        #new code (gets column names dynamically)
        elif instructions["type"] == "insert":
            columns = ", ".join(structured_data.keys())  # extracts the column names
            values_placeholder = ", ".join(["%s"] * len(structured_data))  # Create placeholders
            sql_query = f"INSERT INTO {target_table} ({columns}) VALUES ({values_placeholder});" #dynamically creates the command

            
            cursor.execute(sql_query, tuple(structured_data.values())) #executes the command

        conn.commit()

    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        conn.close()  # closes the connection

    return state
