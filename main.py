import pyautogui
import time
import keyboard

rows, cols = (8, 8)
arr = [[0]*cols for _ in range(rows)]


brood = 'brood.png'
lina = 'lina.png'
wyvern = 'wyvern.png'
venge = 'venge.png'
cm = 'cm.png'
lich = 'lich.png'

def find_candy(candy,tok):
    #screenshot = pyautogui.screenshot(region=(220,110, 730, 750))
    
    try:
        for element in pyautogui.locateAllOnScreen(candy,confidence=0.70,grayscale=False):
            arr[(element[1]-130)//90][(element[0]-230)//90] = tok
            #x = input("Press Enter to continue...")
    except:
        print("No candy found")
        pass
    

def swap(i,j,k,l):
    #arr[i][j],arr[k][l] = arr[k][l],arr[i][j]
    pyautogui.moveTo(270+j*90,180+i*90)
    pyautogui.mouseDown()
    pyautogui.moveTo(270+l*90,180+k*90,duration=0.2)
    print(270+j*90,180+i*90)
    print(270+l*90,180+k*90)
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
                        if arr[i+1][j+2] == tok:
                            print("third "+tok+" found at "+str(i+1)+","+str(j+2)+" RRD")
                            swap(i+1,j+2,i,j+2)
                            break
                        if i>0 and arr[i-1][j+2] == tok:
                            print("third "+tok+" found at "+str(i-1)+","+str(j+2)+" RRU")
                            swap(i-1,j+2,i,j+2) 
                            break
                        if arr[i][j+3] == tok:
                            print("third "+tok+" found at "+str(i)+","+str(j+3)+" RRR")
                            swap(i,j+3,i+2,j)
                            break
                        if i>0 and j>1 and arr[i-1][j-1] == tok:
                            print("third "+tok+" found at "+str(i-1)+","+str(j-1)+" LLU")
                            swap(i-1,j-1,i,j-1)
                            break
                        if j>0 and arr[i+1][j-1] == tok:
                            print("third "+tok+" found at "+str(i+1)+","+str(j-1)+" LLD")
                            swap(i+1,j-1,i,j-1) 
                            break
                        if j>1 and arr[i][j-2] == tok:
                            print("third "+tok+" found at "+str(i)+","+str(j-2)+" LLL")
                            swap(i,j-2,i,j-1)
                            break
                    if arr[i][j+2] == tok:
                        if arr[i+1][j+1] == tok:
                            print(" third "+tok+" found at "+str(i+1)+","+str(j+1)+" DLD")
                            swap(i+1,j+1,i,j+1)
                            break
                        if i>0 and arr[i-1][j+1] == tok:
                            print("third "+tok+" found at "+str(i-1)+","+str(j+1)+" DRD")
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
    grav(arr)
    solve(arr,"L")
    grav(arr)
    solve(arr,"w")
    grav(arr)
    solve(arr,"c")
    grav(arr)
    solve(arr,"l")
    grav(arr)
    solve(arr,"v")
    grav(arr)

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