import pyautogui
import time
import keyboard

rows, cols = (8, 8)
arr = [[0]*cols for _ in range(rows)]
default_height = 1080
screen_width, screen_height = pyautogui.size()
ratio = screen_height/default_height

brood = 'brood.png'
lina = 'lina.png'
wyvern = 'wyvern.png'
venge = 'venge.png'
cm = 'cm.png'
lich = 'lich.png'

def_height = 1080;
screen_width, screen_height = pyautogui.size()
ratio = screen_height/def_height;
startY = round(130 * ratio)
startX = round(230 * ratio)
candyH = round(90 * ratio)
candyW = round(90 * ratio)
startCY = startY + round(candyH/2)
startCX = startX + round(candyH/2)
def find_candy(candy,tok):
    #screenshot = pyautogui.screenshot(region=(220,110, 730, 750))
    try:
        for element in pyautogui.locateAllOnScreen(candy,confidence=0.85,grayscale=False):
            arr[(element[1]-startY)//candyH][(element[0]-startX)//candyW] = tok
            #x = input("Press Enter to continue...")
    except:
        print("No candy found")
        pass
    

def swap(i,j,k,l):
    #arr[i][j],arr[k][l] = arr[k][l],arr[i][j]
    pyautogui.moveTo(startCX+j*candyW,startCY+i*candyH)
    pyautogui.mouseDown()
    pyautogui.moveTo(startCX+l*candyW,startCY+k*candyH,duration=0.2)
    print(startCX+j*candyW,startCY+i*candyH)
    print(startCX+l*candyW,startCY+k*candyH)
    pyautogui.mouseUp()

def swap(i,j,k,l):
    #arr[i][j],arr[k][l] = arr[k][l],arr[i][j]
    pyautogui.moveTo(270+j*90,180+i*90)
    pyautogui.mouseDown()
    pyautogui.moveTo(270+l*90,180+k*90,duration=0.2)
    pyautogui.mouseUp()

def solve(arr,tok):
    for i in range(8):
        for j in range(8):
            if arr[i][j] == tok:
                print(tok+" found at "+str(i)+","+str(j))
                try:
                    if arr[i+1][j] == tok:
                        print("second "+tok+" found at "+str(i+1)+","+str(j))
                        
                        if arr[i+2][j+1] == tok:
                            print("third "+tok+" found at "+str(i+2)+","+str(j+1)+" DDR")
                            arr[i+2][j+1]=arr[i+2][j]
                            arr[i+2][j],arr[i+1][j],arr[i][j] = "a","a","a"
                            swap(i+2,j+1,i+2,j)
                            break
                        if j>0 and arr[i+2][j-1] == tok:
                            print(" third "+tok+" found at "+str(i+2)+","+str(j-1)+" DDL")
                            arr[i+2][j-1]=arr[i+2][j]
                            arr[i+2][j],arr[i+1][j],arr[i][j] = "a","a","a"
                            swap(i+2,j-1,i+2,j)
                            break
                        if arr[i+3][j] == tok:
                            print("third "+tok+" found at "+str(i+3)+","+str(j)+" DDD")
                            arr[i+3][j]=arr[i+2][j]
                            arr[i+2][j],arr[i+1][j],arr[i][j] = "a","a","a"
                            swap(i+3,j,i+2,j)   
                            break
                        if i>0 and arr[i-1][j+1] == tok:
                            print("third "+tok+" found at "+str(i-1)+","+str(j+1)+" UUR")
                            arr[i-1][j+1]=arr[i-1][j]
                            arr[i-1][j],arr[i+1][j],arr[i][j] = "a","a","a"
                            swap(i-1,j+1,i-1,j)
                            break
                        if i>0 and j>0 and arr[i-1][j-1] == tok:
                            print(" third "+tok+" found at "+str(i-1)+","+str(j-1)+" UUL")
                            arr[i-1][j-1]=arr[i-1][j]
                            arr[i-1][j],arr[i+1][j],arr[i][j] = "a","a","a"
                            swap(i-1,j-1,i-1,j)
                            break
                        if i>1 and arr[i-2][j] == tok:
                            print("third "+tok+" found at "+str(i-2)+","+str(j)+" UUU")
                            arr[i-2][j]=arr[i-1][j]
                            arr[i-1][j],arr[i+1][j],arr[i][j] = "a","a","a"
                            swap(i-2,j,i-1,j)      
                            break 
                    if arr[i+2][j] == tok:
                        if j>0 and arr[i+1][j-1] == tok:
                            print(" third "+tok+" found at "+str(i-1)+","+str(j-1)+" DLD")
                            arr[i+1][j-1]=arr[i+1][j]
                            arr[i+1][j],arr[i+2][j],arr[i][j] = "a","a","a"
                            swap(i+1,j-1,i+1,j)
                            break
                        if arr[i+1][j+1] == tok:
                            print("third "+tok+" found at "+str(i-2)+","+str(j)+" DRD")
                            arr[i+1][j+1]=arr[i+1][j]
                            arr[i+1][j],arr[i+2][j],arr[i][j] = "a","a","a"
                            swap(i+1,j+1,i+1,j)     
                            break 
                except:
                    pass
            if arr[i][j] == tok:   
                print(tok+" found at "+str(i)+","+str(j))         
                try:
                    if arr[i][j+1] == tok:
                        print("second "+tok+" found at "+str(i)+","+str(j+1))
                        print("i,j",i,j)
                        if arr[i+1][j+2] == tok:
                            print("third "+tok+" found at "+str(i+1)+","+str(j+2)+" RRD")
                            arr[i+1][j+2]=arr[i][j+2]
                            arr[i][j+2],arr[i][j+1],arr[i][j] = "a","a","a"
                            swap(i+1,j+2,i,j+2)
                            break
                        if i>0 and arr[i-1][j+2] == tok:
                            print("third "+tok+" found at "+str(i-1)+","+str(j+2)+" RRU")
                            arr[i-1][j+2]=arr[i][j+2]
                            arr[i][j+2],arr[i][j+1],arr[i][j] = "a","a","a"
                            swap(i-1,j+2,i,j+2) 
                            break
                        if arr[i][j+3] == tok:
                            print("third "+tok+" found at "+str(i)+","+str(j+3)+" RRR")
                            arr[i][j+3]=arr[i][j+2]
                            arr[i][j+2],arr[i][j+1],arr[i][j] = "a","a","a"
                            swap(i,j+3,i,j+2)
                            break
                        if i>0 and j>1 and arr[i-1][j-1] == tok:
                            print("third "+tok+" found at "+str(i-1)+","+str(j-1)+" LLU")
                            arr[i-1][j-1]=arr[i][j-1]
                            arr[i][j-1],arr[i][j+1],arr[i][j] = "a","a","a"
                            swap(i-1,j-1,i,j-1)
                            break
                        if j>0 and arr[i+1][j-1] == tok:
                            print("third "+tok+" found at "+str(i+1)+","+str(j-1)+" LLD")
                            arr[i+1][j-1]=arr[i][j-1]
                            arr[i][j-1],arr[i][j+1],arr[i][j] = "a","a","a"
                            swap(i+1,j-1,i,j-1) 
                            break
                        if  arr[i][j-2] == tok:
                            print("third "+tok+" found at "+str(i)+","+str(j-2)+" LLL")
                            arr[i][j-2]=arr[i][j-1]
                            arr[i][j-1],arr[i][j+1],arr[i][j] = "a","a","a"
                            swap(i,j-2,i,j-1)
                            break
                    if arr[i][j+2] == tok:
                        if arr[i+1][j+1] == tok:
                            print(" third "+tok+" found at "+str(i+1)+","+str(j+1)+" DLD")
                            arr[i+1][j+1]=arr[i+1][j]
                            arr[i+1][j],arr[i][j+1],arr[i][j] = "a","a","a"
                            swap(i+1,j+1,i,j+1)
                            break
                        if i>0 and arr[i-1][j+1] == tok:
                            print("third "+tok+" found at "+str(i-1)+","+str(j+1)+" DRD")
                            arr[i-1][j+1]=arr[i-1][j]
                            arr[i-1][j],arr[i][j+1],arr[i][j] = "a","a","a"
                            swap(i-1,j+1,i,j+1)     
                            break 
                except:
                    pass

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
    solve(arr,"b")
    find()
    solve(arr,"L")
    solve(arr,"w")
    find()
    solve(arr,"c")
    solve(arr,"l")
    find()
    solve(arr,"v")

while True:  # making a loop
    find()
    solveb()
    
    try:  # used try so that if user pressed other than the given key error will not be shown
        
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            
            break  # finishing the loop
    except:
        break  # if user pressed a key other than the given key the loop will breakq

for row in arr:
    print(row)
