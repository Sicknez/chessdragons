import pyautogui
import time
import keyboard
from datetime import datetime
from datetime import timedelta
from PIL import Image
import os

debug = True

rows, cols = (8, 8)
arr = [[0]*cols for _ in range(rows)]
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

images = [brood,b1,b2, lina,L1,L2, wyvern,w1,w2, venge,v1,v2, cm,c1,c2, lich,l1,l2]
imagesOpened = []
symbols = ["b","b","b", "L","L","L", "w","w","w", "v","v","v", "c","c","c", "l","l","l"]
candy_style_count = 18
for i in range(candy_style_count):
    imagesOpened.append(Image.open(images[i]))


def_height = 1080;
screen_width, screen_height = pyautogui.size()
ratio = screen_height/def_height;
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
def find_candy(candy,tok):
    #screenshot = pyautogui.screenshot(region=(220,110, 730, 750))
    try:
        for element in pyautogui.locateAllOnScreen(candy,confidence=0.85,grayscale=False):
            arr[(element[1]-startY)//candyH][(element[0]-startX)//candyW] = tok
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
    

def swap(i,j,k,l):
    #arr[i][j],arr[k][l] = arr[k][l],arr[i][j]
    pyautogui.moveTo(startCX+j*candyW,startCY+i*candyH)
    pyautogui.mouseDown()
    pyautogui.moveTo(startCX+l*candyW,startCY+k*candyH,duration=0.2)
    trace_debug(startCX+j*candyW,startCY+i*candyH)
    trace_debug(startCX+l*candyW,startCY+k*candyH)
    pyautogui.mouseUp()

def swap(i,j,k,l):
    #arr[i][j],arr[k][l] = arr[k][l],arr[i][j]
    pyautogui.moveTo(startCX+j*candyW,startCY+i*candyH)
    pyautogui.mouseDown()
    pyautogui.moveTo(startCX+l*candyW,startCY+k*candyH,duration=0.2)
    pyautogui.mouseUp()
def solve(arr,tok):
    is_solved = False
    itera = 0
    for i in range(8):
        for j in range(8):
            if is_solved:
                break;
            itera += 1
            if arr[i][j] == tok:
                trace_debug(tok+" found at "+str(i)+","+str(j))
                try:
                    #VERTICAL
                    ##SEQUENTIAL
                    if i>1 and arr[i-1][j] == tok:
                        trace_debug("second "+tok+" found at "+str(i-1)+","+str(j))
                        if j<7 and arr[i-2][j+1] == tok:
                            trace_debug("third "+tok+" found at "+str(i-2)+","+str(j+1)+" DDR")
                            swap(i-2,j+1,i-2,j)
                            is_solved = True
                            break
                        if j>0 and arr[i-2][j-1] == tok:
                            trace_debug("third "+tok+" found at "+str(i-2)+","+str(j-1)+" DDR")
                            swap(i-2,j-1,i-2,j)
                            is_solved = True
                            break
                        if i>2 and arr[i-3][j] == tok:
                            trace_debug("third "+tok+" found at "+str(i-3)+","+str(j)+" DDR")
                            swap(i-3,j,i-2,j)
                            is_solved = True
                            break
                        
                    ##INBETWEEN
                    if i>1 and arr[i-2][j] == tok:
                        trace_debug("second "+tok+" found at "+str(i-2)+","+str(j))
                        if j>0 and arr[i-1][j-1] == tok:
                            trace_debug(" third "+tok+" found at "+str(i-1)+","+str(j-1)+" DLD")
                            swap(i-1,j-1,i-1,j)
                            is_solved = True
                            break
                        if j<7 and arr[i-1][j+1] == tok:
                            trace_debug("third "+tok+" found at "+str(i-1)+","+str(j+1)+" DRD")
                            swap(i-1,j+1,i-1,j)   
                            is_solved = True  
                            break
                    ##DIAGONAL
                    if i>1 and j<7 and arr[i-1][j+1] == tok and arr[i-2][j+1] == tok:
                        trace_debug("second "+tok+" found at "+str(i-1)+","+str(j+1))
                        trace_debug("third "+tok+" found at "+str(i-2)+","+str(j+1)+" DDR")
                        swap(i,j,i,j+1)
                        is_solved = True
                        break
                    if i>1 and j>0 and arr[i-1][j-1] == tok and arr[i-2][j-1] == tok:
                        trace_debug("second "+tok+" found at "+str(i-1)+","+str(j-1))
                        trace_debug("third "+tok+" found at "+str(i-2)+","+str(j-1)+" DDR")
                        swap(i,j,i,j-1)
                        is_solved = True
                        break
                    #HORIZONTAL
                    ##SEQUENTIAL
                    if j>1 and arr[i][j-1] == tok:
                        trace_debug("second "+tok+" found at "+str(i)+","+str(j - 1))
                        if i>0 and arr[i-1][j-2] == tok:
                            trace_debug("third "+tok+" found at "+str(i-1)+","+str(j-2)+" DDR")
                            swap(i-1,j-2,i,j-2)
                            is_solved = True
                            break
                        if i<7 and arr[i+1][j-2] == tok:
                            trace_debug("third "+tok+" found at "+str(i+1)+","+str(j-2)+" DDR")
                            swap(i+1,j-2,i,j-2)
                            is_solved = True
                            break
                        if j>2 and arr[i][j-3] == tok:
                            trace_debug("third "+tok+" found at "+str(i+1)+","+str(j-2)+" DDR")
                            swap(i,j-3,i,j-2)
                            is_solved = True
                            break
                    ##INBETWEEN
                    if j>1 and arr[i][j-2] == tok:
                        trace_debug("second "+tok+" found at "+str(i)+","+str(j - 2))
                        if i<7 and arr[i+1][j-1] == tok:
                            trace_debug("third "+tok+" found at "+str(i+1)+","+str(j-1)+" DDR")
                            swap(i+1,j-1,i,j-1)
                            is_solved = True
                            break
                        if i>0 and arr[i-1][j-1] == tok:
                            trace_debug("third "+tok+" found at "+str(i-1)+","+str(j-1)+" DDR")
                            swap(i-1,j-1,i,j-1)
                            is_solved = True
                            break
                    ##DIAGONAL
                    if j>1 and i<7 and arr[i+1][j-1] == tok and arr[i+1][j-2] == tok:
                        trace_debug("second "+tok+" found at "+str(i+1)+","+str(j - 1))
                        trace_debug("third "+tok+" found at "+str(i+1)+","+str(j-2)+" DDR")
                        swap(i,j,i+1,j)
                        is_solved = True
                        break
                    if j>1 and i>0 and arr[i-1][j-1] == tok and arr[i-1][j-2] == tok:
                        trace_debug("second "+tok+" found at "+str(i-1)+","+str(j - 1))
                        trace_debug("third "+tok+" found at "+str(i-1)+","+str(j-2)+" DDR")
                        swap(i,j,i-1,j)
                        is_solved = True
                        break
                    
                except:
                    pass
    trace_debug("took " +str(itera)+" iters")
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
    find_candy(brood,"b")
    find_candy(lina,"L")
    find_candy(wyvern,"w")
    find_candy(venge,"v")
    find_candy(cm,"c")
    find_candy(lich,"l")
def solveb():
    for i in range(8):
        for j in range(8):
            arr[i][j] = "N"#igger
    for i in range(candy_style_count):
        find_candy(images[i],symbols[i])
        res = solve(arr, symbols[i])
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
