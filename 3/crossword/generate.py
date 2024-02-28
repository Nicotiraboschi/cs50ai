import sys

# from colorama import Fore, Style, init

from crossword import *

# def printc(comment, color='magenta'):
#     color  = color.upper()
#     color = getattr(Fore, color)
#     print(color + comment + Style.RESET_ALL)


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, domain in list(self.domains.items()):
            for word in domain.copy():
                if len(word) != variable.length:
                    domain.remove(word)
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        value = self.crossword.overlaps[(x,y)]
        if not value:
            return False
        found = False
        revision = False
        for word in self.domains[x].copy():
            found = False
            letter = word[value[0]]
            for wordinsecond in self.domains[y].copy():
                secondletter = wordinsecond[value[1]]
                if secondletter == letter:
                    found = True
            if found == False:
                revision = True
                self.domains[x].remove(word)
        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """ 
        for words in list(self.domains.values()):
            if len(words) == 0:
                return False
            
        if arcs and len(arcs) == 0:
            return True
           
        newarcs = arcs or []
        
        if not arcs:
            for variable1 in list(self.domains.keys()):
                for variable2 in list(self.domains.keys()):
                    if variable1 != variable2:
                        neighbors = list(self.crossword.neighbors(variable1))
                        
                        for neighbor in neighbors:
                            newarcs.append((variable1, neighbor))
                                    
        for arc in newarcs:
            if self.revise(arc[0], arc[1]):
                neighbors = list(self.crossword.neighbors(arc[0]))
                for neighbor in neighbors:
                    if (arc[0], neighbor) not in newarcs:
                        newarcs.append((arc[0], neighbor))
                return self.ac3(newarcs)

        return True 

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.domains):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        
        words = []
        
        for variable, word in assignment.items():
            if variable.length != len(word):
                return False
            if word not in words:
                words.append(word)
            else:
                return False
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                if letters[i][j] != None and letters[i][j] != word[k] :
                    return False
                else:
                    letters[i][j] = word[k]
                    
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        words_to_choose = {}
        for word in self.domains[var]:
            temp_num = 0
            for variable, words in list(self.domains.items()):
                if variable in assignment:
                    continue
                else: 
                    if word in words:
                        temp_num += 1
            words_to_choose[word] = temp_num
        
        sorted_words = sorted(words_to_choose, key=lambda x: words_to_choose[x])

        return sorted_words
        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        max_neighbors_number = 0
        words_number = 0
        max_neighbors_variable = ''
                      
        sorted_data = dict(sorted(self.domains.items(), key=lambda x: len(x[1])))
        
        i = 0
        for variable, words in list(sorted_data.items()):
            if variable in assignment:
                continue
            if i == 0:
                words_number = len(words)
                i+= 1
            if words_number == len(words):
                neighbors_number = len(self.crossword.neighbors(variable))
                if neighbors_number > max_neighbors_number:
                    max_neighbors_variable = variable
                    max_neighbors_number = neighbors_number
                    
        return max_neighbors_variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        # CHOOSE THE NODE TO CHECK AND THE WORDS
        def choose_variable_and_words(assignment_to_work_with):
            new_variable_to_start_with = self.select_unassigned_variable(assignment_to_work_with)
            list_of_words_to_check = self.order_domain_values(new_variable_to_start_with, assignment_to_work_with)
            return new_variable_to_start_with, list_of_words_to_check
                
        def getlistfromassignnment(assignmenttostartwith):
            newlist = self.domains.copy()
            for variable, word in list(assignmenttostartwith.items()):
                newlist[variable] = word
            return newlist    
                
        def remove(variable, word, new_assignment):
            updated_assignment = new_assignment
            updated_assignment[variable] = word
            newlist = getlistfromassignnment(updated_assignment)
            for variable, words in list(newlist.items()):
                if variable not in updated_assignment and word in words:
                    if len(words) == 1:
                        return None
                    else:
                        newlist[variable].remove(word)
            return newlist
        
        def check_solutions(assignmenttostartwith):
            newlist = getlistfromassignnment(assignmenttostartwith)
            updated_assignment = assignmenttostartwith
            comment = "list and assignment at the start of check solutions"
            stop = True 
            newlist_after_remove = {}
            
            if self.assignment_complete(assignmenttostartwith) and self.consistent(assignmenttostartwith):
                return assignmenttostartwith
            for variable, words in list(newlist.items()):
                if variable in assignmenttostartwith or len(words) != 1:
                    continue
                else: 
                    stop = False
                    updated_assignment[variable] = list(words)[0]
                    newlist_after_remove = remove(variable, list(words)[0], assignmenttostartwith)
                    if not newlist_after_remove:
                        continue
            if not stop:
                # if i found a solution, i should try again and search for another solution
                check_solutions(updated_assignment)
            else:
                # if i didn't find any more solution, i should pick another word from the beginning
                backtrack_main(updated_assignment)
                                
        def backtrack_main(assignment_to_work_with):
                
            if self.assignment_complete(assignment_to_work_with):
                if self.consistent(assignment_to_work_with):
                    return assignment_to_work_with
                else:
                    return None
            else:
                new_variable_to_start_with, list_of_words_to_check = choose_variable_and_words(assignment_to_work_with)                
                for i in range(len(list_of_words_to_check)):
                    new_assignment = assignment_to_work_with.copy()
                    newlist = remove(new_variable_to_start_with, list_of_words_to_check[i], new_assignment)
                    
                    if not newlist:
                        continue
                    
                    if self.assignment_complete(new_assignment):
                        if self.consistent(new_assignment):
                            return new_assignment
                        else:
                            return None                            
                        
                    assignment_solution = check_solutions(new_assignment)
                    
                    backtrack_main(new_assignment)
                    
                    if assignment_solution:
                        return assignment_solution
                    else:
                        return backtrack_main(new_assignment)
                    
                    
                return None
                
        return backtrack_main(assignment)
                            

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
