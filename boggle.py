from string import ascii_uppercase
from random import choice


def make_grid(width, height):
    """
    Make a grid that will hold all of the tiles
    for a boggle game
    """
    return{(row, col): choice(ascii_uppercase)
           for row in range(height)
           for col in range(width)}


def neighbors_of_position(coords):
    """
    Gets us the neighbors of a given position
    """
    row = coords[0]
    col = coords[1]

    # Assign each of the neighbors
    # Top-left to Tip-right
    top_left = (row - 1, col - 1)
    top_center = (row - 1, col)
    top_right = (row - 1, col + 1)

    # Left to right
    left = (row, col - 1)
    # The '(row, col)' coordinates passed to this
    # function are situated here
    right = (row, col + 1)

    # Bottom left to Bottom-right
    bottom_left = (row + 1, col - 1)
    bottom_center = (row + 1, col)
    bottom_right = (row + 1, col + 1)

    return [top_left, top_center, top_right,
            left, right,
            bottom_left, bottom_center, bottom_right]


def all_grid_neighbors(grid):
    """
    gets all the possible neighbors for each position in the grid
    """
    neighbors = {}
    for position in grid:
        position_neighbors = neighbors_of_position(position)
        neighbors[position] = [p for p in position_neighbors if p in grid]
    return neighbors


def path_to_word(grid, path):
    """
    Add all of the letters on a path to a string
    """
    return ''.join([grid[p] for p in path])


def search(grid, dictionary):
    """
    search through the paths to locate words by 
    matching strings to words in a dictionary
    """

    neighbors = all_grid_neighbors(grid)
    paths = []
    full_words, stems = dictionary

    def do_search(path):
        word = path_to_word(grid, path)
        if word in full_words:
            paths.append(path)
        if word not in stems:
            return
        for next_pos in neighbors[path[-1]]:
            if next_pos not in path:
                do_search(path + [next_pos])

    for position in grid:
        do_search([position])

    words = []
    for path in paths:
        words.append(path_to_word(grid, path))
    return set(words)


def get_dictionary(dictionary_file):
    """
    Load Dictionary File
    """
    full_words, stems = set(), set()
    with open(dictionary_file) as f:
        for word in f:
            word = word.strip().upper()
            full_words.add(word)

            for i in range(1, len(word)):
                stems.add(word[:i])

    return full_words, stems


def main():
    """
    This is the function that will run the whole project
    """
    grid = make_grid(4, 4)
    dictionary = get_dictionary('words.txt')
    words = search(grid, dictionary)
    for word in words:
        print(word)
    print("found %s words" % len(words))


if __name__ == "__main__":
    main()
