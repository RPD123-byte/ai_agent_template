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
    # county  varchar(255)- 1


    try:
        # Depending on what it gets, insert or alter data into the correct table

        if instructions["type"] == "alter":
            column_name =   structured_data.get("column_name")
            type = structured_data.get("type")

            cursor.execute(
                f"alter table users add column {column_name} {type};",
                
                #"alter table  users add (column name) state (type);" #a
            )
            print("Altered users table.")

        elif instructions["type"] == "insert":
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s);",
                (structured_data["name"], structured_data["email"]) 
            )
            print("Inserted into users table.")

        # Commits the transaction
        conn.commit()

    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        conn.close()  # closes the connection

    return state
