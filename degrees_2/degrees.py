import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    # source = person_id_for_name('Ian McKellen')
    # 1 DEGREE:
    # source = "129" 
    # 2 DEGREE:
    source = "398"
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    # target = person_id_for_name('Kevin Bacon')
    # 1 DEGREE:
    # target = "193"
    # 2 DEGREE:
    # target= "102"
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(path, "path")
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            print(person1)
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

# MAIN


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # TODO

    if source == target:
        return []
    
    def create_path(node):
        path = []
        nod = node
        while nod:
            path = [(nod.action, nod.state)] + path
            nod = nod.parent
        return path

    neighbors = neighbors_for_person(source)
    # stack = StackFrontier()
    stack = QueueFrontier()
    for n in neighbors:
        
        new_node = Node(n[1], None, n[0])
        state = new_node.state
        if state == target:
            return create_path(new_node)
        if not stack.contains_state(state):  
            stack.add(new_node)
    
    def create_stack():
        nonlocal stack
        print(len(stack.frontier), "💫💫length stack before")
        n = stack.remove()
        print(len(stack.frontier), "💫💫length stack after")

        actor_state = n.state
        if actor_state == target:
            return create_path(n)
        neighbors = neighbors_for_person(actor_state)
        for nei in neighbors:
            new_node = Node(nei[1], n, nei[0])
            state = new_node.state                
            if state == target:
                return create_path(new_node)
            if stack.contains_state(state) or stack.contains_state(actor_state): 
                continue
            else:
                person = False
                nod = new_node
                while nod.parent:
                    nod = nod.parent
                    if nod.state == state:  
                        person = True 
                        break  
                if not person:
                    stack.add(new_node)
                else:
                    continue
                    
    solutions = None               
    while len(stack.frontier) != 0 and solutions == None:        
        solutions = create_stack()

    return solutions
        
        
def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            print("error")
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
