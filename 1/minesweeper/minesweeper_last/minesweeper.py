import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __hash__(self):
        # Convert the set of cells to a frozenset for immutability
        return hash((frozenset(self.cells), self.count))


    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        set_mines = set()
        if len(self.cells) == self.count and self.count != 0:
            for cell in self.cells:
                set_mines.add(cell)
        return set_mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        set_safes = set()
        if self.count == 0:
            for cell in self.cells:
                self.mark_safe(cell)
                set_safes.add(cell)
        return set_safes
           
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            print("sentence before marking mine 🦍", self)
            self.count -= 1
            self.cells.discard(cell)
            print("sentence after marking mine 🦍", self)
            if len(self.cells) == 0:
                del self
                
        else: 
            return
        


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.cells.discard(cell)

        if len(self.cells) == 0:
            del self

    def delete_self(self):
        del self

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge.copy():
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge.copy():
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.knowledge = list(set(self.knowledge))
        
        self.moves_made.add(cell)
        
        self.mark_safe(cell)
        
        def find_cells_around(cell):
            cell_height = cell[0]
            cell_width = cell[1]
            
            temp_cells = []
            cells = []
            
            mines_count = 0
            
            cell_up = cell_height -1
            cell_down = cell_height +1
            cell_left = cell_width -1
            cell_right = cell_width +1
            
            def check_range(cell):
                if cell[0] >= 0 and cell[0] <8 and cell[1] >= 0 and cell[1] <8:
                    return True
                else:
                    return False
            
            for i in range(-1, 2):
                new_cell = (cell_up, cell_width + i)
                temp_cells.append(new_cell)
                new_cell = (cell_down, cell_width + i)
                temp_cells.append(new_cell)
                
            temp_cells.append((cell_height, cell_left))
            temp_cells.append((cell_height, cell_right))
                
            print(temp_cells, "📣")
                    
            for temp_cell in temp_cells:
                if check_range(temp_cell):
                    if temp_cell in self.mines:
                        print(temp_cell, "temp_cell as bomb 📣")
                        mines_count += 1
                        continue
                    if temp_cell in self.safes:
                        continue
                    cells.append(temp_cell)
            
            return cells, mines_count
                

        cells, mines_count = find_cells_around(cell)
        new_sentence = Sentence(cells, count-mines_count)
        if len(new_sentence.cells) > 0:
            self.knowledge.append(new_sentence)
            print(new_sentence, "new_sentence based on move and count 🎃")
                
            
        for sentence in self.knowledge.copy():
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)
        
        print("all_sentences i have before marking mines or safes: 🎆")
        for sentence in self.knowledge:
            print(sentence, "one of the knowledge sentences")


            if sentence.count == len(sentence.cells) and sentence.count > 0:
                print(sentence, "count: shouldn't be 0")
                for cell_for in sentence.cells.copy():
                    self.mark_mine(cell_for)

        for sentence in self.knowledge.copy():
            if sentence.count == 0:
                for cell_for in sentence.cells.copy():
                    if cell_for not in self.mines and cell_for not in self.moves_made:
                        print(sentence, "before marking cell as safe 🦁")
                        self.mark_safe(cell_for)
                        print(sentence, "after marking cell as safe 🦁")
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)
        
        print("all_sentences i have before checking subsets: 🎆")
        for sentence in self.knowledge:
            print(sentence, "one of the knowledge sentences")

        
        new_sentences = []
        

        for sentence in self.knowledge.copy():
            for sen2 in self.knowledge.copy():
                if sentence.cells < sen2.cells:
                    if len(sentence.cells) == 0:
                        # print("fuck 🎄", sentence) TO-DO
                        continue
                    print(sentence, sen2, "small and big sets, 🍓")
                    new_sentence = Sentence((sen2.cells - sentence.cells), (sen2.count - sentence.count))
                    print(new_sentence, "new_sentence after subset🍓")
                    new_sentences.append(new_sentence)

        # Append the new sentences after the iteration is complete
        self.knowledge.extend(new_sentences)        


        
        print(cell, "move made 🎄")
        
        self.knowledge = list(set(self.knowledge))
                    
        print("all_sentences i have at the end: 🎆")
        for sentence in self.knowledge:
            print(sentence, "one of the knowledge sentences")
        print(self.safes, "safe squares")
        print(self.mines, "mines 🥎")
        print(self.moves_made, "moves_made")
        
        
        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) > len(self.moves_made):
            move = random.choice(list(self.safes - self.moves_made))
            print(move, "move i'll make")
            return move
        return 

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        minesweeper_set = set((row, col) for row in range(self.height) for col in range(self.width))
        
        
        minesweeper_set_to_choose_from = list((minesweeper_set-self.mines-self.safes))

        if len(minesweeper_set_to_choose_from):
            return random.choice(minesweeper_set_to_choose_from)
                   
        return