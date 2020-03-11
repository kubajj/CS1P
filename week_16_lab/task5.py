import tkinter


functions = {}

def draw(shape, start=0, end=0):
    global functions
    if shape == "line":
        canvas.create_line(start[0],start[1],end[0],end[1])
    elif shape == "circle":
        radius = end
        canvas.create_oval(start[0]-radius,start[1]-radius,start[0]+radius,start[1]+radius)
    elif shape in functions:
        apply_function(shape)

def apply_function(f_name, current_position):
    global functions
    for line in functions[f_name]:
        current_instruction = line.strip().split()
        if current_instruction[0] == "line" and len(current_instruction) == 3:
            new_pos = [current_position[0],current_position[1]]
            new_pos[0] = new_pos[0] + int(current_instruction[1])
            new_pos[1] = new_pos[1] + int(current_instruction[2])
            draw("line",current_position,new_pos)                
            current_position = new_pos
        elif current_instruction[0] == "circle" and len(current_instruction) == 2:
            radius = int(current_instruction[1])
            draw("circle", current_position, radius)
        elif current_instruction[0] in functions:
            current_position = apply_function(current_instruction[0])
        elif current_instruction[0] == "move": 
            current_position[0] += int(current_instruction[1])
            current_position[1] += int(current_instruction[2])
            
        print("I want to do this", line)
    return current_position
        
def read_file(filename):
    global functions
    current_loop_body = []
    current_loop_n_iterations = 0
    with open(filename) as f:
        reading_a_function = False
        current_f_name = ""
        loop_body = False
        current_position = [0,0]
        for line in f:
            current_instruction = line.strip().split() 
            
            if len(current_instruction) == 0:
                continue
            #print(current_instruction)
            #print(current_instruction[0])
            if current_instruction[0] == "end":
                if reading_a_function and not loop_body:
                    reading_a_function = False
                    current_f_name = ""
                if loop_body:
                    loop_body = False
                    for i in range(current_loop_n_iterations):
                        current_position = apply_function("loop", current_position)
            elif reading_a_function:
                functions[current_f_name].append(line.strip())
            elif current_instruction[0] == "position" and len(current_instruction) == 3:
                current_position[0] = int(current_instruction[1])
                current_position[1] = int(current_instruction[2])
            elif current_instruction[0] == "move" and len(current_instruction) == 3:
                current_position[0] += int(current_instruction[1])
                current_position[1] += int(current_instruction[2])
            elif current_instruction[0] == "line" and len(current_instruction) == 3:
                new_pos = [current_position[0],current_position[1]]
                new_pos[0] = new_pos[0] + int(current_instruction[1])
                new_pos[1] = new_pos[1] + int(current_instruction[2])
                draw("line",current_position,new_pos)                
                current_position = new_pos
            elif current_instruction[0] == "circle" and len(current_instruction) == 2:
                radius = int(current_instruction[1])
                draw("circle", current_position, radius)
            elif current_instruction[0] == "define" and len(current_instruction) == 2:
                f_name = current_instruction[1]
                current_f_name = f_name
                reading_a_function = True
                functions[f_name] = []
            elif current_instruction[0] == "loop" and len(current_instruction) == 2:
                loop_body = True
                current_f_name = "loop"
                reading_a_function = True
                functions["loop"] = []
                current_loop_n_iterations = int(current_instruction[1])
                loop_body = True
            elif current_instruction[0] in functions:
                current_position = apply_function(current_instruction[0], current_position)
            #print("I am at:",current_position[0], current_position[1])

# MAIN WINDOW
def on_enter(event):
	read_file(textVar.get().strip())

def call_read_file():
	filename = textVar.get().strip()
	try:
		read_file(filename)
	except:
		print("Error while reading", filename)

top = tkinter.Tk()
top.grid_rowconfigure(1, weight=1)
top.grid_columnconfigure(0, weight=1)

canvas = tkinter.Canvas(top, width=500,bg="white")
canvas.grid(row=0,column=0,rowspan=2,sticky="nsew")

#maybe replace with text widget
textVar = tkinter.StringVar("")
textEntry = tkinter.Entry(top,textvariable=textVar)
textEntry.grid(row=0,column=1,sticky="nsew")
textEntry.bind('<Return>',on_enter)


loadButton = tkinter.Button(top,text="Load",command=call_read_file,width=6)
loadButton.grid(row=0,column=2)

tkinter.mainloop()
