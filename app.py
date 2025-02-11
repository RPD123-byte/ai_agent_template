from insert_to_db_agent import insert_to_db_agent
from graph import get_graph



def run_agent(state):
    """
    Run the agent workflow
    """
    state = insert_to_db_agent(state)
    
    print("Data insertion workflow completed.")
    return state 

if __name__ == "__main__":
    #Testing the agent
    state = {
         "instructions": {
            "type": "alter",
            "target_table" : "users"
        },
        "structured_data": {
            "column_name": "age",
            "type": "INT",
            "name": "Sue",
            "email": "sue@gmail.com",
            "street": "123 Main St"
            #"column name": "new column name type columm", #if DDL
            #"type":"data type",

            #if DML give all corresponding values
            #"column names" : ["name", "email", "street", "city", "state"] ,
            #"column values" :["Sue","sue@gmail.com", "123 main st", "charlotte", "NC"]
        }
    }  # Initialize the state
    run_agent(state)