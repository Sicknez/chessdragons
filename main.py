import pyautogui
import time
import keyboard
from datetime import datetime
from datetime import timedelta
from PIL import Image
import threading
import os
import copy

debug = False
resized_postfix = "_RESIZED"

rows, cols = (8, 8)
arr = [["N"]*cols for _ in range(rows)]
costs = [[0]*cols for _ in range(rows)]
path = os.path.dirname(os.path.abspath(__file__))

#image paths
brood = path+'/Sprites/Brood/brood.png'
b1 = path+'/Sprites/Brood/b_1.png'
b2 = path+'/Sprites/Brood/b_2.png'

lina = path+'/Sprites/Lina/lina.png'
L1 = path+'/Sprites/Lina/L_1.png'
L2 = path+'/Sprites/Lina/L_2.png'

wyvern = path+'/Sprites/Wyvern/wyvern.png'
w1 = path+'/Sprites/Wyvern/w_1.png'
w2 = path+'/Sprites/Wyvern/w_2.png'

venge = path+'/Sprites/Venge/venge.png'
v1 = path+'/Sprites/Venge/v_1.png'
v2 = path+'/Sprites/Venge/v_2.png'

cm = path+'/Sprites/Cm/cm.png'
c1 = path+'/Sprites/Cm/c_1.png'
c2 = path+'/Sprites/Cm/c_2.png'

lich = path+'/Sprites/Lich/lich.png'
l1= path+'/Sprites/Lich/l_1.png'
l2 = path+'/Sprites/Lich/l_2.png'

def_height = 1080
screen_width, screen_height = pyautogui.size()
ratio = screen_height/def_height
images = [brood,b1,b2, wyvern,w1,w2, venge,v1,v2, cm,c1,c2, lich,l1,l2, lina,L1,L2]
piece_costs = [2,8,6, 3,5,10, 1,5,12, 3,7,7, 3,7,7, 3,5,5]

images_resized = []

#patch cropping
Right = 30
Left = 20
Top = 20
Bottom = 20


imagesOpened = []
imagesOpened_resized = []
symbols = ["b","b","b", "w","w","w", "v","v","v", "c","c","c", "l","l","l", "L","L","L"]
candy_style_count = 18
candy_type_count = 6
for i in range(candy_style_count):
    imagesOpened.append(Image.open(images[i]))

for i in range(candy_style_count):
    file = os.path.splitext(images[i])
    resized_name = file[0] + resized_postfix + file[1]
    width, height = imagesOpened[i].size
    width = round(width * ratio)
    height = round(height * ratio)
    new_size = (width, height)
    images_resized.append(resized_name)
    resized_image = imagesOpened[i].resize(new_size,Image.Resampling.LANCZOS)
    resized_image.save(resized_name)
     
for i in range(candy_style_count):
    imagesOpened_resized.append(Image.open(images_resized[i]))

#board constants
startY = round(130 * ratio)
startX = round(230 * ratio)
candyH = round(90 * ratio)
candyW = round(90 * ratio)
startCY = startY + round(candyH/2)
startCX = startX + round(candyH/2)
boardH = round(720 * ratio)
boardW = round(710 * ratio)

region_board = (startX, startY, startX+boardW, startY+boardH)
print("Starting")
start_time = datetime.now()
def get_timestamp():
   dt = datetime.now() - start_time
   return dt
def timestamp_to_ms(dt):
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
   return ms
def get_ms():
    return timestamp_to_ms(get_timestamp())
def trace_debug(msg):
    if(debug):
        print(f"#{get_timestamp()}#\t" + msg)
input()

#Function to check if there are any matches adds a dot to the end of the match
def check_matches(board):
    max_result = 0
    for i in range(rows):
        for j in range(cols):
            if board[i][j] != "N":                
                if j+2< cols and board[i][j] == board[i][j+1] == board[i][j+2]:
                    token = board[i][j]
                    len = matchH(i, j,board)

                    trace_debug(f"Horizontal match found at:{i},{j} | Token:{token} | Length:{len}")
                    
                
                if i+2< rows and board[i][j] == board[i+1][j] == board[i+2][j]:
                    token = board[i][j]
                    len = matchV(i, j,board)
                    trace_debug(f"Vertical match found at:{i},{j} | Token:{token} | Length:{len}")
                
                if board[i][j].count('.') > max_result:
                    max_result = board[i][j].count('.')
    return max_result

def matchH(i, j,board):
    tok = board[i][j][0]
    length = 0
    while j<cols and board[i][j][0]==tok:
        board[i][j] += '.'
        j+=1
        length+=1
    return length

def matchV(i, j,board):
    tok = board[i][j][0]
    length = 0
    while i<rows and board[i][j][0]==tok:
        board[i][j] += '.'
        i+=1
        length+=1
    return length
#prints the board
def print_board(board):
    for i in range(rows):
        for j in range(cols):
            print(board[i][j], end = " ")
        print()
#Function to find the candies on the board
def find_candy(candy, tok,price):
    screenshot = pyautogui.screenshot(region=(startX, startY, boardW, boardH))
    
    for i in range(rows):
        for j in range(cols):
            patch = screenshot.crop((j*candyW+Top, i*candyH+Left, (j+1)*candyW-Right, (i+1)*candyH-Bottom))
            try:
                if pyautogui.locate(candy, patch, grayscale=False, confidence=0.7) != None:
                    arr[i][j] = tok
                    costs[i][j] = price
                    if price>1:
                        trace_debug("found RARE " + tok)
            except:
                trace_debug("No candy found")
                pass

moving = False
def swap_logic(i,j,k,l):
    global moving
    if not moving:
        moving = True
        pyautogui.moveTo(startCX+j*candyW,startCY+i*candyH)
        pyautogui.mouseDown()
        pyautogui.moveTo(startCX+l*candyW,startCY+k*candyH,duration=0.151)
        pyautogui.mouseUp()
        moving = False
        
def swap(i,j,k,l):
    swap_threaded = threading.Thread(target=swap_logic, args=(i,j,k,l))
    swap_threaded.start()
    trace_debug(startCX+j*candyW,startCY+i*candyH)
    trace_debug(startCX+l*candyW,startCY+k*candyH)

def solve(arr):
    max_result = 0
    is_solved = False
    x1 = -1
    y1 = -1
    x2 = -1
    y2 = -1
    for i in range(8):
        for j in range(8):
            temp = arr[i][j]
            if j+1 < 8:
                board1 = copy.deepcopy(arr)
                board1[i][j] = board1[i][j+1]
                board1[i][j+1] = temp
                if max_result <check_matches(board1):
                    max_result = check_matches(board1)
                    x1 = i
                    y1 = j
                    x2 = i
                    y2 = j+1
            if i+1 < 8:
                board2 = copy.deepcopy(arr)
                board2[i][j] = board2[i+1][j]
                board2[i+1][j] = temp
                
                if max_result <check_matches(board2):
                    max_result = check_matches(board2)
                    x1 = i
                    y1 = j
                    x2 = i+1
                    y2 = j
    if max_result > 0:
        is_solved = True
        swap(x1,y1,x2,y2)
    return is_solved

def solveb_for_one(second_iter):
        find_candy(images_resized[second_iter],symbols[second_iter],piece_costs[second_iter])
        second_iter+=1
        find_candy(images_resized[second_iter],symbols[second_iter],piece_costs[second_iter])
        second_iter+=1
        find_candy(images_resized[second_iter],symbols[second_iter],piece_costs[second_iter])
        res = solve(arr)
        return res

def solveb():
    for i in range(8):
        for j in range(8):
            arr[i][j] = "N"
            costs[i][j] = 0
    second_iter = 0
    for i in range(candy_type_count):
        second_iter = i*3
        res = solveb_for_one(second_iter)
        if res:
            break

while True:  # making a loop
    start = get_ms()
    solveb()
    print(f"#SOLVEB DONE IN {get_ms() - start} ms")
    
    try:  # used try so that if user pressed other than the given key error will not be shown
        
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            
            break  # finishing the loop
    except:
        break  # if user pressed a key other than the given key the loop will breakq

print_board(arr)
print("\n")
print("\nCosts:\n")
print_board(costs)



