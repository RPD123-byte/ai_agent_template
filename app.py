from insert_to_db_agent import insert_to_db_agent
from graph import get_graph



def run_agent(states): #def run_agent(state)
    """
    Run the agent workflow
    """
    #state = insert_to_db_agent(state)

    for state in states: #edited for loop
        insert_to_db_agent(state)

    print("Data insertion workflow completed.")
    #return state 


# can insert which command you want (alter/insert), input info, and run it
if __name__ == "__main__":
    #Testing the agent (List of dictionaries)
    states = [ #originally state
        {
            "instructions": {
                "type": "insert",
                "target_table":"student"
            },
            "structured_data":{
                "name":"John",
                "id":123
            }
        },
        {
            # Will bascically alter if there is somethign to alter 
            "instructions": {
                "type": "alter", #change command accordingly (alter/insert)
                "target_table" : "student" # change name of the table accordingly
            },
            "structured_data": {
                "column_name" : "rank",
                "type" : "INT"
                #"column_name": "email",
                #"type": "INT",
            },
        },
        
        # {
        #     "instructions": {
        #         "type": "insert",  # Step 2: Insert a new row
        #         "target_table": "student"
        #     },
        #     "structured_data": {
        #         "name": "John",
        #         "id": 123,
        #     }
        # }
        
    ] # Initialize the state
    run_agent(states) #originally run_agent(state)