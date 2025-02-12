class StateManager:
    def __init__(self):
        self.state = {}

    def update_state(self, file_name, processed_data):
        """Save processed data for a file"""
        self.state[file_name] = processed_data

    def get_state(self, file_name):
        """Retrieve processed data for a file"""
        return self.state.get(file_name, None)
