import customtkinter
import time
import pyautogui
import math

monitor = pyautogui.size()
max_x = monitor[0]
max_y = monitor[1]

x = int(max_x/2-225)
y = int(max_y/2-100)

size_x = 450
size_y = 200

distance_treshold = 400
border_treshold = 5

speed_x = 0
speed_y = 0
max_speed = 20

app = customtkinter.CTk()
app.geometry(f"{size_x}x{size_y}+{x}+{y}")
customtkinter.set_appearance_mode("dark")

text = customtkinter.CTkLabel(app, text="close me", font=("Arial", 32, "bold"))
text.pack(pady=70)


#increases max speed if cursor gets too close
def speed_control(input, treshold):
    global max_speed
    
    if input < treshold:
        max_speed = 60
    else:
        max_speed = 20    
    

def close_event():
    print("u did it")
    app.destroy()

def move():
    while True:
        global speed_x
        global speed_y
        global x
        global y
        
        #window center point
        origin = (x + size_x/2, y + size_y/2)
        
        #reading cursor position
        cursor_position = pyautogui.position()
        
        
        #calculating cursor position relative to center of the window
        leg_y = origin[1] - cursor_position[1]
        leg_x = cursor_position[0] - origin[0]
        prepona = math.hypot(leg_x, leg_y)
        sin = int((leg_y/prepona) * 10)
        cos = int(-(leg_x/prepona) * 10)
        
        
        #window speed manipulation
        if prepona < distance_treshold:
            move = True
            #lateral
            if cos > 0 and speed_x < max_speed and x + size_x < max_x:
                speed_x += 2
            elif cos < 0 and speed_x > -max_speed and x > 0:
                speed_x -= 2
            elif speed_x > 0:
                speed_x -= 1
            elif speed_x < 0:
                speed_x += 1     
              
            #vertical   
            if sin > 0 and speed_y < max_speed and y + size_y < max_y:
                speed_y += 2
            elif sin < 0 and speed_y > -max_speed and y > 0:
                speed_y -= 2
            elif speed_y > 0:
                speed_y -= 1
            elif speed_y < 0:
                speed_y += 1        
                  
        else:
            move = False
            if prepona + 100 > distance_treshold:
                if speed_x > 0:
                    speed_x -= 1
                elif speed_x < 0:
                    speed_x += 1    
                if speed_y > 0:    
                    speed_y -= 1 
                elif speed_y < 0:
                    speed_y +=1
        
        #screen border bounce-off mechanics           
        if x + size_x + speed_x >=  max_x - border_treshold or x + speed_x <= 0 + border_treshold:
            speed_x = -speed_x
        if y + size_y + speed_y >=  max_y - border_treshold or y + speed_y <= 0 + border_treshold:
            speed_y = -speed_y    
            
        speed_control(prepona, 180)               
         
        time.sleep(0.02)      
        x += speed_x
        y += speed_y
        
        #output
        print(f"x:{x}, y:{y}, mouse_x:{cursor_position[0]}, mouse_y:{cursor_position[1]}, origin: {origin}, leg_x: {leg_x}, leg_y: {leg_y}, prepona: {prepona}, sin:{sin}, cos: {cos}, move: {move}, speed_x: {speed_x}, speed_y:{speed_y}, max_speed:{max_speed}")       
        
        #window update
        app.geometry(f"{size_x}x{size_y}+{x}+{y}")
        app.update()

app.after(100, move)
app.mainloop()
app.protocol("WM_DELETE_WINDOW", close_event)
