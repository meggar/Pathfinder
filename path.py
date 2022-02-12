from curses import wrapper, init_pair, color_pair
from time import sleep

my_map = [
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0,-1,-1, 0, 0, 0,-1,-1,-1,-1, 0, 0, 0, 0, 0],
  [0, 0,-1, 0, 0, 0, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0,-1, 0,-1,-1,-1, 0, 0, 0,-1,-1,-1, 0, 0, 0],
  [0, 0,-1, 0,-1, 0, 0, 0, 0,-1, 0, 0, 0,-1,-1,-1],
  [0, 0,-1,-1, 0, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   ]


def show_path_animation(stdscr, stack, this_map, rows, cols, start_pos, end_pos):
	"""
	do an animation of a "*" making its way from the start to the end
	along the shortest path.

	@param stack: a stack of (x,y,i) for each node along the path
	@param this_map: the 2d map after pathfinding is done, -1 for obastacle
	@param start_pos: (x,y) of start node
	@param end_pos: (x,y) of end node
	"""

	stdscr.clear()

        # A 2d array of the stuff that's actually printed on screen.
        # replace obstacles with "&", everything else with ".", etc..
	printable_map = [["."]*cols for r in range(rows)]
	for r in range(rows):
		for c in range(cols):
			if this_map[r][c] == -1:
				printable_map[r][c] = "&" # obstacle
			if (r,c) == start_pos:
				printable_map[r][c] = "S" # start
			if (r,c) == end_pos:
				printable_map[r][c] = "X" # end

	# Color pairs to color text, (id, foreground, background)
	init_pair(1, 69, 0) # cornflower blue, black
	init_pair(2, 45, 0) # turquoise, black
	init_pair(3, 11, 0) # yellow, black
	init_pair(4, 9, 0)  # red, black

	# each type of item in the map gets its own color
	color_map = {
		".": color_pair(1),
		"&": color_pair(2),
		"*": color_pair(3),
		"S": color_pair(4),
		"X": color_pair(4),
	}

	# step through the path on the stack, update teh screen each time.
	while stack:

		stdscr.clear()
		stdscr.addstr("\n\n")

		x,y,i = stack.pop()

		printable_map[x][y] = "*"

		for row in printable_map:

			stdscr.addstr("\t")
			for item in row:
				stdscr.addstr(" " + item,  color_map[item])
			stdscr.addstr("\n")

		sleep(0.5)
		stdscr.refresh()
		
	stdscr.addstr("\n\n\t\tpress any key to exit! :D", color_pair(1))
	stdscr.getkey()


def print_results(this_map, rows, cols, start_pos, end_pos):
	"""
	create a stack of nodes along the shortest path, by starting
	at the end node in the map, and picking a neighbor node whose
	value is current_node's value - 1. repeat until the value is 1,
	which is the starting node. pass the stack to a function
	that can display stuff.

	@param this_map: the 2d map, after pathfining
	@param start_pos: the starting node
	@param end_pos: the end node
	"""

	stack = [(end_pos[0], end_pos[1], this_map[end_pos[0]][end_pos[1]])]

	isValidRowAndCol = lambda r,c: r in range(rows) and c in range(cols)

	x,y,i = stack[-1]

	while (x,y) != start_pos:

		for (r,c) in ((x,-~y), (x,~-y), (~-x,y), (-~x,y)):
			if isValidRowAndCol(r, c):
				if this_map[r][c] == i - 1:
					stack.append( (r,c,i-1) )
					x = r
					y = c
					i -= 1
					break

	wrapper(show_path_animation, stack, this_map, rows, cols, start_pos, end_pos)


def shortest_path(this_map, start_pos, end_pos):
	"""
	find a shortest path in this_map from start_pos to end_pos

	@param this_map: 2d map before pathfinding
	@param start_pos: (x,y) of starting node
	@param end_pos: (x,y) of end node
	"""

	rows = len(this_map)
	cols = len(this_map[0])

	q = [(start_pos[0], start_pos[1], 1)]

	path_completed = False

	isValidRowAndCol = lambda r,c: r in range(rows) and c in range(cols)

	while q:
		x,y,i = q.pop(0)
		this_map[x][y] = i
		if (x,y) == end_pos:
			print_results(this_map, rows, cols, start_pos, end_pos)
			path_completed = True
			break

		for (r,c) in ((x,-~y), (x,~-y), (~-x,y), (-~x,y)):
			if isValidRowAndCol( r,c ):
				if this_map[r][c] == 0:
				    q.append( (r,c, i+1) )

	if not path_completed:
		print("Could not complete a path.")


shortest_path(my_map, (0,0), (6,11))
