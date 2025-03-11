def check_log_for_termination(log_file, stop_term="closeCommunicationChannels"):
        with open(log_file, 'r') as f:
            lines = f.readlines()
            last_line = lines[-1]
            # Check if the stop term appears in the last line
            if stop_term in(last_line):
                return True
            return False
        
def check_log_for_errors(log_file, error_terms=["$fluid_solver:: ERROR from", "$electromagnetic_solver:: ERROR from", 
                                           "-Infinity", "Infinity", "NaN"]):
        with open(log_file, 'r') as f:
            lines = f.readlines()
            last_lines = lines[-20:]
            # Check if error terms appear in the last lines
            for line in last_lines:
                 if any(term in line for term in error_terms):
                    return True
            return False
