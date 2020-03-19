import tkinter
import math
import copy
from functools import partial


def simply_print_cities(filename):
	cities = []
	with open(filename) as f:
		for city in f:
			city = city.split()
			formated_city = [city[2],(int(city[0]),int(city[1]))]
			cities.append(formated_city)


	top = tkinter.Tk()
	top.grid_rowconfigure(1, weight=1)
	top.grid_columnconfigure(0, weight=1)

	canvas = tkinter.Canvas(top, width=500,bg="white")
	canvas.grid(row=0,column=0,rowspan=2,sticky="nsew")

	first = ()
	previous = ()
	for city in cities:
		# draw a point
		coordinates = city[1]
		r = 1
		canvas.create_oval(coordinates[0]-r,coordinates[1]-r,coordinates[0]+r,coordinates[1]+r)
		# add label with the name of the city to the point
		name = city[0]
		canvas.create_text(coordinates[0]+10,coordinates[1]+7,text=name)	
		# draw a line	
		if not previous == ():
			canvas.create_line(previous[0],previous[1],coordinates[0],coordinates[1])
		else:
			first = coordinates
		previous = coordinates
	canvas.create_line(coordinates[0],coordinates[1],first[0],first[1])

	tkinter.mainloop()

def display(cities_on_tour,cities,canvas,window):
	tour = []
	for i,city in enumerate(cities_on_tour):
		if city.get() == 1:
			tour.append(cities[i])

	if not len(tour) < 2:
		minimum,min_order = nna(tour)
		draw_tour(min_order,minimum,canvas,window,len(cities))
	else:
		canvas.delete("all")
		message_label = tkinter.Label(window,text="Please choose at least 2 cities that you want to visit.")
		message_label.grid(row=(len(cities))-1,column=0,sticky="nsew")

def distance(c,t):
	return math.sqrt((c[0]-t[0])**2+(c[1]-t[1])**2)

def is_further(c,t1,t2): # true if t1 is further than t2 from c
	return distance(c,t1) > distance(c,t2)

def nna(list_of_cities):
	total_distance = 0
	first = list_of_cities[0][1]
	bo = list_of_cities[0][0] == "Warsaw"
	previous = ()
	if len(list_of_cities) == 2:
		total_distance = distance(first,list_of_cities[1][1])
	else:
		for i in range(len(list_of_cities)-1):
			if not i == 0:
				nearest = i
				near_coordinates = list_of_cities[i][1]
				not_visited = list_of_cities[i:]
				for j in range(len(not_visited)):
					if is_further(previous,near_coordinates,not_visited[j][1]):
						nearest = i + j
						near_coordinates = not_visited[j][1]
				if not i == nearest:
					list_of_cities[i],list_of_cities[nearest] = list_of_cities[nearest],list_of_cities[i]
				total_distance += distance(previous,near_coordinates)
				previous = near_coordinates
			else:
				previous = list_of_cities[0][1]
		total_distance += distance(previous,first)
		print(distance(previous,first),list_of_cities[0])
	list_of_cities.append(list_of_cities[0])
	print(total_distance,list_of_cities[0])
	print(sum([distance(list_of_cities[i][1],list_of_cities[i+1][1]) for i in range(len(list_of_cities)-1)]))
	return total_distance,list_of_cities

def draw_tour(tour,minimum,canvas,window,max_n_cities):
	canvas.delete("all")	
	first = ()
	previous = ()
	n = 1
	for city in tour:
		# draw a point
		coordinates = city[1]
		r = 1
		canvas.create_oval(coordinates[0]-r,coordinates[1]-r,coordinates[0]+r,coordinates[1]+r)
		# add label with the name of the city to the point
		name = city[0]
		canvas.create_text(coordinates[0]+13,coordinates[1]+7,text=str(n) + name)
		n += 1	
		# draw a line	
		if not previous == ():
			canvas.create_line(previous[0],previous[1],coordinates[0],coordinates[1], arrow=tkinter.LAST,dash=(5,3))
		else:
			first = coordinates
		previous = coordinates
	canvas.create_line(coordinates[0],coordinates[1],first[0],first[1], arrow=tkinter.LAST,dash=(5,3))
	length_label = tkinter.Label(window,text="Tour length is {:.2f} km".format(minimum))
	length_label.grid(row=max_n_cities-1,column=0,sticky="nsew")


def nearest_neighbour_algorithm_approach(filename):
	cities = []
	with open(filename) as f:
		for city in f:
			city = city.split()
			formated_city = [city[2],(int(city[0]),int(city[1]))]
			cities.append(formated_city)

	window = tkinter.Tk()
	window.grid_rowconfigure(1, weight=1)
	window.grid_columnconfigure(0, weight=1)

	canvas = tkinter.Canvas(window, width=500,bg="white")
	canvas.grid(row=0,column=0,rowspan=len(cities)-1,sticky="nsew")

	c_cities = cities.copy()
	minimum = float('inf')
	min_order = c_cities
	for c in range(len(c_cities)):
		current = nna(c_cities.copy())
		if minimum > current[0]:
			minimum = current[0]
			min_order = current[1]
		c_cities.append(c_cities[0])
		c_cities = c_cities[1:]

	draw_tour(min_order, minimum, canvas, window,len(cities))

	cityButton = list()
	cities_on_tour = []
	for i,city in enumerate(cities):	
		cities_on_tour.append(tkinter.IntVar(0))	
		cityButton.append(tkinter.Checkbutton(window,text=city[0],variable=cities_on_tour[i],onvalue=1,offvalue=0,command=partial(display,cities_on_tour,cities,canvas,window)))
		cityButton[i].grid(row=i,column = 1)
	
	tkinter.mainloop()

filename = "./Lab material/Cities.txt"
#simply_print_cities(filename)
nearest_neighbour_algorithm_approach(filename)
