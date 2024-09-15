import pyautogui
import time
import keyboard
from datetime import datetime
from datetime import timedelta
from PIL import Image
import threading
import os

debug = False
resized_postfix = "_RESIZED"

rows, cols = (8, 8)
arr = [[0]*cols for _ in range(rows)]
costs = [[0]*cols for _ in range(rows)]
path = os.path.dirname(os.path.abspath(__file__))

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

def_height = 1080;
screen_width, screen_height = pyautogui.size()
ratio = screen_height/def_height;
images = [brood,b1,b2, lina,L1,L2, wyvern,w1,w2, venge,v1,v2, cm,c1,c2, lich,l1,l2]
piece_costs = [1,8,6, 1,5,5, 1,5,10, 1,8,10, 1,7,7, 1,7,7]
images_resized = []

imagesOpened = []
imagesOpened_resized = []
symbols = ["b","b","b", "L","L","L", "w","w","w", "v","v","v", "c","c","c", "l","l","l"]
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
   

startY = round(130 * ratio)
startX = round(230 * ratio)
candyH = round(90 * ratio)
candyW = round(90 * ratio)
startCY = startY + round(candyH/2)
startCX = startX + round(candyH/2)
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
def find_candy(candy,tok,price):
    #screenshot = pyautogui.screenshot(region=(220,110, 730, 750))
    try:
        for element in pyautogui.locateAllOnScreen(candy,confidence=0.85,grayscale=False):
            arr[(element[1]-startY)//candyH][(element[0]-startX)//candyW] = tok
            costs[(element[1]-startY)//candyH][(element[0]-startX)//candyW] = price
            if price>1:
                trace_debug("found RARE " + tok)
            #x = input("Press Enter to continue...")
    except:
        trace_debug("No candy found")
        pass
def find_candy2(candy,tok, screenshot):
    #screenshot = pyautogui.screenshot(region=(220,110, 730, 750))
    try:
        start = get_ms()
        for element in pyautogui.locateAll(candy,screenshot,confidence=0.69,grayscale=False):
            arr[(element[1]-startY)//candyH][(element[0]-startX)//candyW] = tok
            #x = input("Press Enter to continue...")
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
        pyautogui.moveTo(startCX+l*candyW,startCY+k*candyH,duration=0.2)
        pyautogui.mouseUp()
        moving = False
        
def swap(i,j,k,l):
    swap_threaded = threading.Thread(target=swap_logic, args=(i,j,k,l))
    swap_threaded.start()
    #arr[i][j],arr[k][l] = arr[k][l],arr[i][j]
    trace_debug(startCX+j*candyW,startCY+i*candyH)
    trace_debug(startCX+l*candyW,startCY+k*candyH)
    
def swap(i,j,k,l):
    swap_threaded = threading.Thread(target=swap_logic, args=(i,j,k,l))
    swap_threaded.start()
def solve(arr,tok):
    is_solved = False
    itera = 0
    x1 = -1
    y1 = -1
    x2 = -1
    y2 = -1
    total_price = 0
    temp1 = 0
    temp2 = 0
    for i in range(8):
        for j in range(8):
            itera += 1
            if arr[i][j] == tok:
                trace_debug(tok+" found at "+str(i)+","+str(j))
                temp1 = costs[i][j]
                try:
                    #VERTICAL
                    ##SEQUENTIAL
                    if i>1 and arr[i-1][j] == tok:
                        temp2 = temp1 + costs[i-1][j]
                        trace_debug("second "+tok+" found at "+str(i-1)+","+str(j))
                        if j<7 and arr[i-2][j+1] == tok:
                            trace_debug("third "+tok+" found at "+str(i-2)+","+str(j+1)+" DDR")
                            if temp2 + costs[i-2][j+1] > total_price:
                                total_price = temp2 + costs[i-2][j+1]
                                x1 = i-2
                                y1 = j+1
                                x2 = i-2
                                y2 = j
                        if j>0 and arr[i-2][j-1] == tok:
                            trace_debug("third "+tok+" found at "+str(i-2)+","+str(j-1)+" DDR")
                            if temp2 + costs[i-2][j-1] > total_price:
                                total_price = temp2 + costs[i-2][j-1]
                                x1 = i-2
                                y1 = j-1
                                x2 = i-2
                                y2 = j
                        if i>2 and arr[i-3][j] == tok:
                            trace_debug("third "+tok+" found at "+str(i-3)+","+str(j)+" DDR")
                            if temp2 + costs[i-3][j] > total_price:
                                total_price = temp2 + costs[i-3][j]
                                x1 = i-3
                                y1 = j
                                x2 = i-2
                                y2 = j
                        
                    ##INBETWEEN
                    if i>1 and arr[i-2][j] == tok:
                        temp2 = temp1 + costs[i-2][j]
                        trace_debug("second "+tok+" found at "+str(i-2)+","+str(j))
                        if j>0 and arr[i-1][j-1] == tok:
                            trace_debug(" third "+tok+" found at "+str(i-1)+","+str(j-1)+" DLD")
                            if temp2 + costs[i-1][j-1] > total_price:
                                total_price = temp2 + costs[i-1][j-1]
                                x1 = i-1
                                y1 = j-1
                                x2 = i-1
                                y2 = j
                        if j<7 and arr[i-1][j+1] == tok:
                            trace_debug("third "+tok+" found at "+str(i-1)+","+str(j+1)+" DRD")
                            if temp2 + costs[i-1][j+1] > total_price:
                                total_price = temp2 + costs[i-1][j+1]
                                x1 = i-1
                                y1 = j+1
                                x2 = i-1
                                y2 = j
                        if i>2 and arr[i-3][j] == tok:
                            trace_debug("third "+tok+" found at "+str(i-3)+","+str(j)+" DRD")
                            if temp2 + costs[i-3][j] > total_price:
                                total_price = temp2 + costs[i-3][j]
                                x1 = i
                                y1 = j
                                x2 = i-1
                                y2 = j
                    ##DIAGONAL
                    if i>1 and j<7 and arr[i-1][j+1] == tok and arr[i-2][j+1] == tok:
                        trace_debug("second "+tok+" found at "+str(i-1)+","+str(j+1))
                        trace_debug("third "+tok+" found at "+str(i-2)+","+str(j+1)+" DDR")
                        if temp1 + costs[i-1][j+1] + costs[i-2][j+1] > total_price:
                            total_price = temp1 + costs[i-1][j+1] + costs[i-2][j+1]
                            x1 = i
                            y1 = j
                            x2 = i
                            y2 = j+1
                    if i>1 and j>0 and arr[i-1][j-1] == tok and arr[i-2][j-1] == tok:
                        trace_debug("second "+tok+" found at "+str(i-1)+","+str(j-1))
                        trace_debug("third "+tok+" found at "+str(i-2)+","+str(j-1)+" DDR")
                        if temp1 + costs[i-1][j-1] + costs[i-2][j-1] > total_price:
                            total_price = temp1 + costs[i-1][j-1] + costs[i-2][j-1]
                            x1 = i
                            y1 = j
                            x2 = i
                            y2 = j-1
                    #HORIZONTAL
                    ##SEQUENTIAL
                    if j>1 and arr[i][j-1] == tok:
                        temp2 = temp1 + costs[i][j-1]
                        trace_debug("second "+tok+" found at "+str(i)+","+str(j - 1))
                        if i>0 and arr[i-1][j-2] == tok:
                            trace_debug("third "+tok+" found at "+str(i-1)+","+str(j-2)+" DDR")
                            if temp2 + costs[i-1][j-2] > total_price:
                                total_price = temp2 + costs[i-1][j-2]
                                x1 = i-1
                                y1 = j-2
                                x2 = i
                                y2 = j-2
                        if i<7 and arr[i+1][j-2] == tok:
                            trace_debug("third "+tok+" found at "+str(i+1)+","+str(j-2)+" DDR")
                            if temp2 + costs[i+1][j-2] > total_price:
                                total_price = temp2 + costs[i+1][j-2]
                                x1 = i+1
                                y1 = j-2
                                x2 = i
                                y2 = j-2
                        if j>2 and arr[i][j-3] == tok:
                            trace_debug("third "+tok+" found at "+str(i+1)+","+str(j-2)+" DDR")
                            if temp2 + costs[i][j-3] > total_price:
                                total_price = temp2 + costs[i][j-3]
                                x1 = i
                                y1 = j-3
                                x2 = i
                                y2 = j-2
                    ##INBETWEEN
                    if j>1 and arr[i][j-2] == tok:
                        temp2 = temp1 + costs[i][j-2]
                        trace_debug("second "+tok+" found at "+str(i)+","+str(j - 2))
                        if i<7 and arr[i+1][j-1] == tok:
                            trace_debug("third "+tok+" found at "+str(i+1)+","+str(j-1)+" DDR")
                            if temp2 + costs[i+1][j-1] > total_price:
                                total_price = temp2 + costs[i+1][j-1]
                                x1 = i+1
                                y1 = j-1
                                x2 = i
                                y2 = j-1
                        if i>0 and arr[i-1][j-1] == tok:
                            trace_debug("third "+tok+" found at "+str(i-1)+","+str(j-1)+" DDR")
                            if temp2 + costs[i-1][j-1] > total_price:
                                total_price = temp2 + costs[i-1][j-1]
                                x1 = i-1
                                y1 = j-1
                                x2 = i
                                y2 = j-1
                        if j>2 and arr[i][j-3] == tok:
                            trace_debug("third "+tok+" found at "+str(i)+","+str(j-3)+" DRD")
                            if temp2 + costs[i][j-3] > total_price:
                                total_price = temp2 + costs[i][j-3]
                                x1 = i
                                y1 = j
                                x2 = i
                                y2 = j-1
                    ##DIAGONAL
                    if j>1 and i<7 and arr[i+1][j-1] == tok and arr[i+1][j-2] == tok:
                        trace_debug("second "+tok+" found at "+str(i+1)+","+str(j - 1))
                        trace_debug("third "+tok+" found at "+str(i+1)+","+str(j-2)+" DDR")
                        if temp1 + costs[i+1][j-1] + costs[i+1][j-2] > total_price:
                            total_price = temp1 + costs[i+1][j-1] + costs[i+1][j-2]
                            x1 = i
                            y1 = j
                            x2 = i+1
                            y2 = j
                    if j>1 and i>0 and arr[i-1][j-1] == tok and arr[i-1][j-2] == tok:
                        trace_debug("second "+tok+" found at "+str(i-1)+","+str(j - 1))
                        trace_debug("third "+tok+" found at "+str(i-1)+","+str(j-2)+" DDR")
                        if temp1 + costs[i-1][j-1] + costs[i-1][j-2] > total_price:
                            total_price = temp1 + costs[i-1][j-1] + costs[i-1][j-2]
                            x1 = i
                            y1 = j
                            x2 = i-1
                            y2 = j
                    
                except:
                    pass
    trace_debug("took " +str(itera)+" iters")
    if total_price > 0:
        is_solved = True
        trace_debug(f"Swapping ({x1}:{y1}) with ({x2}:{y2}) for the total price of {total_price})")
        swap(x1,y1,x2,y2)
    return is_solved

def grav(arr):
    for i in range(8):
        for j in range(8):
            if arr[i][j] == "a":
                for k in range(i,0,-1):
                    arr[k][j] = arr[k-1][j]
                arr[0][j] = "a"
    return arr

def find():
    find_candy(brood,"b",1)
    find_candy(lina,"L",1)
    find_candy(wyvern,"w",1)
    find_candy(venge,"v",1)
    find_candy(cm,"c",1)
    find_candy(lich,"l",1)
def solveb():
    for i in range(8):
        for j in range(8):
            arr[i][j] = "N"#igger
            costs[i][j] = 0
    second_iter = 0
    for i in range(candy_type_count):
        find_candy(images_resized[second_iter],symbols[second_iter],piece_costs[second_iter])
        second_iter+=1
        find_candy(images_resized[second_iter],symbols[second_iter],piece_costs[second_iter])
        second_iter+=1
        find_candy(images_resized[second_iter],symbols[second_iter],piece_costs[second_iter])
        res = solve(arr, symbols[second_iter])
        second_iter+=1
        if res:
            break;

while True:  # making a loop
    start = get_ms()
    solveb()
    print(f"#SOLVEB DONE IN {get_ms() - start} ms")
    
    try:  # used try so that if user pressed other than the given key error will not be shown
        
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            
            break  # finishing the loop
    except:
        break  # if user pressed a key other than the given key the loop will breakq

for row in arr:
    print(row)
print("\n")
print("\nCosts:\n")
for row in costs:
    print(row)
