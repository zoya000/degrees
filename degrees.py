import csv
from hashlib import new
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

    with open("movie.txt", "w") as f:
        for i in movies.keys():
            f.write(i)
            f.write(str( movies[i]))
            f.write("\n")
    with open("people.txt", "w") as f:
        for i in people.keys():
            f.write(i)
            f.write(str(people[i]))
            f.write("\n")
    # source = person_id_for_name(input("Name: "))
    source = person_id_for_name("Emma Watson")
    if source is None:
        sys.exit("Person not found.")
    # target = person_id_for_name(input("Name: "))
    target = person_id_for_name("Jennifer Lawrence")
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)
    print(path)
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    print("hi")
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # print("hiii")
    # ideas: use BFS
    # node gets t he source and turns it into id
    nodes = [Node(source, None, None)] # has to get all the movies the person in
    bfs = QueueFrontier()
    bfs.add(nodes[0])
    # print(bfs.frontier)
    explored = []
    explored.append(nodes[0].state)
    # print("movies: ", movies)
    while True:
        print("hi")
        if bfs.empty():
            return None
        currentNode = bfs.remove() # check if return object
        # print("currentNOdeState", currentNode.state)
        if currentNode.state == target:
            # print("hi")
            pairs = []
            while currentNode.parent != None:
                pairs.append((currentNode.action, currentNode.state))
                currentNode = currentNode.parent
            # print(pairs)
            pairs.reverse()
            return pairs
        
        # print("explored: ", explored)
        # print("Currmovie: ", people[str(currentNode.state)]["movies"])
        CurrMovies = people[str(currentNode.state)]["movies"]
        newPeopleToAdd = []
        for i in CurrMovies:
            
            var1 = list(movies[i]["stars"])
            var2 = i
            # print("VAr1", var1, type(var1))
            # print("VAr2", var2, type(var2))
            for j in var1:
                newPeopleToAdd.append((var2, j))
        
        # print("moviescurr:", CurrMovies)
        # print("newpeople: ", newPeopleToAdd)

        for i in newPeopleToAdd:
            if i[0] not in explored:
                explored.append(i[0])
            if i[1] not in explored:
                explored.append(i[1])
                # action: movie
                # print("newPeopleNotExplored:", i[1])
                bfs.add(Node(i[1], currentNode, i[0]))
        # explored.append(newPeopleToAdd)
        




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
