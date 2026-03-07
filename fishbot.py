import time
import keyboard

def apasa(tasta):
    keyboard.press(tasta)
    time.sleep(0.04)
    keyboard.release(tasta)
    time.sleep(0.04)

def main():
    print("start bot pescuit clasic")
    time.sleep(5)
    
    while True:
        if keyboard.is_pressed('x'):
            print("stop")
            break
            
        print("bag momeala de pe 1")
        apasa('1')
        time.sleep(1.5) 
        
        print("arunc undita")
        apasa('space')
        
        print("astept fix 60 de secunde")
        timp_start = time.time()
        oprire_urgenta = False
        
        while time.time() - timp_start < 60:
            if keyboard.is_pressed('x'):
                oprire_urgenta = True
                break
            time.sleep(0.1)
            
        if oprire_urgenta:
            print("oprit din x")
            break
            
        print("trag pestele")
        apasa('space')
        
        time.sleep(3.5) 

if __name__ == "__main__":
    main()