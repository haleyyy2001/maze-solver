"""
Each futoshiki board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8

Empty values in the board are represented by 0

An * after the letter indicates the inequality between the row represented
by the letter and the next row.
e.g. my_board['A*1'] = '<' 
means the value at A1 must be less than the value
at B1

Similarly, an * after the number indicates the inequality between the
column represented by the number and the next column.
e.g. my_board['A1*'] = '>' 
means the value at A1 is greater than the value
at A2

Empty inequalities in the board are represented as '-'
Huilin Tai
id: ht2666
"""
import sys

#======================================================================#
#*#*#*# Optional: Import any allowed libraries you may need here #*#*#*#
#======================================================================#
import time
from copy import deepcopy
import numpy as np
#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

ROW = "ABCDEFGHI"
COL = "123456789"

class Board:
    '''
    Class to represent a board, including its configuration, dimensions, and domains
    '''
    
    def get_board_dim(self, str_len):
        '''
        Returns the side length of the board given a particular input string length
        '''
        d = 4 + 12 * str_len
        n = (2+np.sqrt(4+12*str_len))/6
        if(int(n) != n):
            raise Exception("Invalid configuration string length")
        
        return int(n)
        
    def get_config_str(self):
        '''
        Returns the configuration string
        '''
        return self.config_str
        
    def get_config(self):
        '''
        Returns the configuration dictionary
        '''
        return self.config
        
    def get_variables(self):
        '''
        Returns a list containing the names of all variables in the futoshiki board
        '''
        variables = []
        for i in range(0, self.n):
            for j in range(0, self.n):
                variables.append(ROW[i] + COL[j])
        return variables
    
    def convert_string_to_dict(self, config_string):
        '''
        Parses an input configuration string, retuns a dictionary to represent the board configuration
        as described above
        '''
        config_dict = {}
        
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_string[0]
                config_string = config_string[1:]
                
                config_dict[ROW[i] + COL[j]] = int(cur)
                
                if(j != self.n - 1):
                    cur = config_string[0]
                    config_string = config_string[1:]
                    config_dict[ROW[i] + COL[j] + '*'] = cur
                    
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_string[0]
                    config_string = config_string[1:]
                    config_dict[ROW[i] + '*' + COL[j]] = cur
                    
        return config_dict
        
    def print_board(self):
        '''
        Prints the current board to stdout
        '''
        config_dict = self.config
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_dict[ROW[i] + COL[j]]
                if(cur == 0):
                    print('_', end=' ')
                else:
                    print(str(cur), end=' ')
                
                if(j != self.n - 1):
                    cur = config_dict[ROW[i] + COL[j] + '*']
                    if(cur == '-'):
                        print(' ', end=' ')
                    else:
                        print(cur, end=' ')
            print('')
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_dict[ROW[i] + '*' + COL[j]]
                    if(cur == '-'):
                        print(' ', end='   ')
                    else:
                        print(cur, end='   ')
            print('')
    
    def __init__(self, config_string):
        '''
        Initialising the board
        '''
        self.config_str = config_string
        self.n = self.get_board_dim(len(config_string))
        if(self.n > 9):
            raise Exception("Board too big")
            
        self.config = self.convert_string_to_dict(config_string)
        self.domains = self.reset_domains()
        
        self.forward_checking(self.get_variables())
        
        
    def __str__(self):
        '''
        Returns a string displaying the board in a visual format. Same format as print_board()
        '''
        output = ''
        config_dict = self.config
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_dict[ROW[i] + COL[j]]
                if(cur == 0):
                    output += '_ '
                else:
                    output += str(cur)+ ' '
                
                if(j != self.n - 1):
                    cur = config_dict[ROW[i] + COL[j] + '*']
                    if(cur == '-'):
                        output += '  '
                    else:
                        output += cur + ' '
            output += '\n'
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_dict[ROW[i] + '*' + COL[j]]
                    if(cur == '-'):
                        output += '    '
                    else:
                        output += cur + '   '
            output += '\n'
        return output
        
    def reset_domains(self):
        '''
        Resets the domains of the board assuming no enforcement of constraints
        '''
        domains = {}
        variables = self.get_variables()
        for var in variables:
            if(self.config[var] == 0):
                domains[var] = [i for i in range(1,self.n+1)]
            else:
                domains[var] = [self.config[var]]
                
        self.domains = domains
                
        return domains

    def forward_checking(self, reassigned_variables):
        '''
        Runs the forward checking algorithm to restrict the domains of all variables based on the values
        of reassigned variables
        '''
        # ======================================================================#
        # *#*#*# TODO: Write your implementation of forward checking here #*#*#*#
        # ======================================================================#
        for var in reassigned_variables:
            assigned_value = self.config[var]
            if assigned_value == 0:
                continue

            row = var[0]
            col = var[1]
            row_index = ROW.index(row) + 1 - 1
            col_index = COL.index(col)
            n = self.n

            for c in COL[0:n]:
                neighbor = row + c
                if neighbor != var:
                    if self.config[neighbor] == 0:

                        if assigned_value in self.domains[neighbor]:
                            self.domains[neighbor].remove(assigned_value)
            for r in ROW[0:n]:
                neighbor = r + col

                if neighbor != var:
                    if self.config[neighbor] == 0:
                        if assigned_value in self.domains[neighbor]:
                            self.domains[neighbor].remove(assigned_value)
            ##### for row check
            if col_index < n - 1:
                key = var + '*'
                if key in self.config:
                    inequality = self.config[key]
                    if inequality != '-':
                        neighbor = var[0] + COL[col_index + 1]
                        if self.config[neighbor] == 0:
                            if inequality == '<':
                                new_domain = []
                                for v in self.domains[neighbor]:
                                    if v > assigned_value:
                                        new_domain.append(v)
                                self.domains[neighbor] = new_domain
                            elif inequality == '>':
                                new_domain = []
                                for v in self.domains[neighbor]:
                                    if v < assigned_value:
                                        new_domain.append(v)
                                self.domains[neighbor] = new_domain
            if col_index > 0:
                key = row + COL[col_index - 1] + '*'
                if key in self.config:
                    inequality = self.config[key]
                    if inequality != '-':
                        neighbor = row + COL[col_index - 1]
                        if self.config[neighbor] == 0:
                            if inequality == '<':
                                new_domain = []
                                for v in self.domains[neighbor]:
                                    if v < assigned_value:
                                        new_domain.append(v)
                                self.domains[neighbor] = new_domain
                            elif inequality == '>':
                                new_domain = []
                                for v in self.domains[neighbor]:
                                    if v > assigned_value:
                                        new_domain.append(v)
                                self.domains[neighbor] = new_domain

            ##### for column check
            if row_index < n - 1:
                key = row + '*' + col
                if key in self.config:
                    inequality = self.config[key]
                    if inequality != '-':
                        neighbor = ROW[row_index + 1] + col
                        if self.config[neighbor] == 0:
                            if inequality == '<':
                                new_domain = []
                                for v in self.domains[neighbor]:
                                    if v > assigned_value:
                                        new_domain.append(v)
                                self.domains[neighbor] = new_domain
                            elif inequality == '>':
                                new_domain = []
                                for v in self.domains[neighbor]:
                                    if v < assigned_value:
                                        new_domain.append(v)
                                self.domains[neighbor] = new_domain


            if row_index > 0:
                key = ROW[row_index - 1] + '*' + col
                if key in self.config:
                    inequality = self.config[key]
                    if inequality != '-':
                        neighbor = ROW[row_index - 1] + col
                        if self.config[neighbor] == 0:
                            if inequality == '<':
                                new_domain = []
                                for v in self.domains[neighbor]:
                                    if v < assigned_value:
                                        new_domain.append(v)
                                self.domains[neighbor] = new_domain
                            elif inequality == '>':
                                new_domain = []
                                for v in self.domains[neighbor]:
                                    if v > assigned_value:
                                        new_domain.append(v)
                                self.domains[neighbor] = new_domain
        # =================================#
        # *#*#*# Your code ends here #*#*#*#
        # =================================#

        #=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#
    def update_config_str(self):

        config_string = ''
        n = self.n
        for i in range(n):
            for j in range(n):
                var = ROW[i] + COL[j]
                value = self.config[var]

                config_string +=str(value)
                if j != n - 1:
                    key = ROW[i] + COL[j] + '*'
                    config_string += self.config[key]

            if i != n - 1:
                for j in range(n):
                       key = ROW[i] + '*' +COL[j]
                       config_string +=self.config[key]
        self.config_str = config_string
    #=================================================================================#
	#*#*#*# Optional: Write any other functions you may need in the Board Class #*#*#*#
	#=================================================================================#
        
    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

#================================================================================#
#*#*#*# Optional: You may write helper functions in this space if required #*#*#*#
#================================================================================#        
def select_unassigned_variable(board):
    empty_cells = [cell for cell in board.get_variables() if board.config[cell] == 0]
    def count_possible_values(cell):
        return len(board.domains[cell])
    cell_with_fewest_options =  min(empty_cells,  key=count_possible_values)

    # Return the chosen cell
    return cell_with_fewest_options
def is_consistent(board, var, value):
    n=board.n
    row = var[0] ; col = var[1];row_index = ROW.index(row) ;col_index = COL.index(col)
    for c in COL[0:n]:
        neighbor = row +c
        if neighbor != var:
            if board.config[neighbor] == value:
                return False
    for r in ROW[:n]:
        neighbor =  r + col
        if neighbor  != var and board.config[neighbor]== value:
            return False


    if col_index < n - 1:
        inequality_key = var + '*'
        if inequality_key in board.config:
            inequality_sign = board.config[inequality_key]
            if inequality_sign != '-':
                right_neighbor =row + COL[col_index +1]
                neighbor_value = board.config[ right_neighbor]

                if neighbor_value != 0:
                    if inequality_sign == '<':
                        if not (value <neighbor_value):
                            return False

                    elif inequality_sign == '>':
                        if not (value > neighbor_value):
                            return False
    # Check horizontal
    if col_index > 0:
        left_neighbor_key = row + COL[col_index - 1] + '*'
        if left_neighbor_key in board.config:
            inequality_sign = board.config[left_neighbor_key]

            if inequality_sign != '-':
                left_neighbor = row + COL[col_index - 1]
                neighbor_value = board.config[left_neighbor]

                if neighbor_value != 0:
                    if inequality_sign == '<':
                        if not (neighbor_value < value):
                            return False
                    elif inequality_sign == '>':
                        if not (neighbor_value > value):
                            return False
    if row_index < n - 1:
        key = row + '*' + col
        if key in board.config:
            inequality = board.config[key]
            if inequality != '-':
                neighbor = ROW[row_index + 1] + col
                neighbor_value = board.config[neighbor]
                if neighbor_value != 0:
                    if inequality == '<' and not (value < neighbor_value):
                        return False
                    elif inequality == '>' and not (value > neighbor_value):
                        return False

    if row_index > 0:
        key = ROW[row_index - 1] + '*' + col
        if key in board.config:
            inequality = board.config[key]
            if inequality != '-':
                neighbor = ROW[row_index - 1] + col
                neighbor_value = board.config[neighbor]
                if neighbor_value != 0:
                    if inequality == '<' and not (neighbor_value < value):
                        return False
                    elif inequality == '>' and not (neighbor_value > value):
                        return False

    return True


def get_solution_string(board):
    '''
     returns theconfiguration string from bord.config
    '''
    config_string = ''
    n = board.n
    for i in range(n):
        for j in range(n):
            var = ROW[i] +COL[j]
            value = board.config[var]
            config_string  += str(value)
            if j != n - 1:
                key = ROW[i] + COL[j] + '*'
                config_string += board.config[key]

        if i != n - 1:
            for j in range(n):
                key = ROW[i] + '*' + COL[j]
                config_string += board.config[key]
    return config_string



#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#


def backtracking(board):
    all_filled = True
    for var in board.get_variables():
        if board.config[var] ==0:

            all_filled = False
            break
    if all_filled:
        board.update_config_str()
        return board

    var = select_unassigned_variable(board)
    for value in board.domains[var]:
        if is_consistent(board, var, value):
            new_board = deepcopy(board)


            new_board.config[var]=value
            new_board.forward_checking([var])

            # domain_empty = False
            # for v in new_board.get_variables():
            #         if len(new_board.domains[v]) == 0:
            #             domain_empty = True
            #             break
            domain_empty = False
            for v in new_board.get_variables():
                if new_board.config[v] ==0 :
                    if len(new_board.domains[v]) == 0:
                        domain_empty = True
                        break

            if domain_empty:
                continue

            result = backtracking(new_board)
            if result is not None:
                return result

    return None

    #==========================================================#
	#*#*#*# TODO: Write your backtracking algorithm here #*#*#*#
	#==========================================================#


    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#
    
def solve_board(board):
    '''
    Runs the backtrack helper and times its performance.
    Returns the solved board and the runtime
    '''
    #================================================================#
	#*#*#*# TODO: Call your backtracking algorithm and time it #*#*#*#
	#================================================================#
    start_time = time.time()
    solved_board =backtracking(board)
    end_time =time.time()
    runtime =end_time-start_time
    return solved_board, runtime

    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

def print_stats(runtimes):
    '''
    Prints a statistical summary of the runtimes of all the boards
    '''
    min = 100000000000
    max = 0
    sum = 0
    n = len(runtimes)

    for runtime in runtimes:
        sum += runtime
        if(runtime < min):
            min = runtime
        if(runtime > max):
            max = runtime

    mean = sum/n

    sum_diff_squared = 0

    for runtime in runtimes:
        sum_diff_squared += (runtime-mean)*(runtime-mean)

    std_dev = np.sqrt(sum_diff_squared/n)

    print("\nRuntime Statistics:")
    print("Number of Boards = {:d}".format(n))
    print("Min Runtime = {:.8f}".format(min))
    print("Max Runtime = {:.8f}".format(max))
    print("Mean Runtime = {:.8f}".format(mean))
    print("Standard Deviation of Runtime = {:.8f}".format(std_dev))
    print("Total Runtime = {:.8f}".format(sum))


if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running futoshiki solver with one board $python3 futoshiki.py <input_string>.
        print("\nInput String:")
        print(sys.argv[1])
        
        print("\nFormatted Input Board:")
        board = Board(sys.argv[1])
        board.print_board()

        solved_board, runtime = solve_board(board)
        
        print("\nSolved String:")
        print(solved_board.get_config_str())
        
        print("\nFormatted Solved Board:")
        solved_board.print_board()
        
        print_stats([runtime])

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(solved_board.get_config_str())
        outfile.write('\n')
        outfile.close()

    else:
        # Running futoshiki solver for boards in futoshiki_start.txt $python3 futoshiki.py

        #  Read boards from source.
        src_filename = 'futoshiki_start.txt'
        try:
            srcfile = open(src_filename, "r")
            futoshiki_list = srcfile.read()
            srcfile.close()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        
        runtimes = []

        # Solve each board using backtracking
        for line in futoshiki_list.split("\n"):
            
            print("\nInput String:")
            print(line)
            
            print("\nFormatted Input Board:")
            board = Board(line)
            board.print_board()
            
            solved_board, runtime = solve_board(board)
            runtimes.append(runtime)
            
            print("\nSolved String:")
            print(solved_board.get_config_str())
            
            print("\nFormatted Solved Board:")
            solved_board.print_board()

            # Write board to file
            outfile.write(solved_board.get_config_str())
            outfile.write('\n')

        # Timing Runs
        print_stats(runtimes)
        
        outfile.close()
        print("\nFinished all boards in file.\n")
