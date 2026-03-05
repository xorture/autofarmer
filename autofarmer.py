import cv2
import numpy as np
import mss
import pyautogui
import time
import keyboard
import ctypes

low = np.array([138, 60, 60])
high = np.array([165, 255, 255])
kernel = np.ones((5,5), np.uint8)

low_rosu1 = np.array([0, 150, 100])
high_rosu1 = np.array([15, 255, 255])
low_rosu2 = np.array([170, 150, 100])
high_rosu2 = np.array([180, 255, 255])

def apasa(tasta):
    keyboard.press(tasta)
    time.sleep(0.04)
    keyboard.release(tasta)
    time.sleep(0.04)

def main():
    print("start")
    time.sleep(5)
    sct = mss.mss()
    mon = sct.monitors[1]
    
    taura = 0
    tlicori = 0
    
    zona_bara = {
        "top": 36,
        "left": 1015,
        "width": 165,
        "height": 30
    }
    
    while True:
        if keyboard.is_pressed('x'):
            print("stop")
            break
            
        t = time.time()
        
        if t - taura > 1800:
            print("aura si iures")
            keyboard.press('ctrl')
            keyboard.press('g')
            time.sleep(0.05)
            keyboard.release('g')
            keyboard.release('ctrl')
            time.sleep(1)
            
            apasa('2')
            time.sleep(2) 
            apasa('3')
            time.sleep(1.5) 
            
            keyboard.press('ctrl')
            keyboard.press('g')
            time.sleep(0.05)
            keyboard.release('g')
            keyboard.release('ctrl')
            time.sleep(0.5)
            taura = time.time()
            
        if t - tlicori > 600:
            print("licori")
            for tasta in ['1', '2', '3', '4', 'f1', 'f2']:
                keyboard.press('alt')
                time.sleep(0.05)
                keyboard.press(tasta)
                time.sleep(0.05)
                keyboard.release(tasta)
                keyboard.release('alt')
                time.sleep(0.1)
            tlicori = time.time()
            
        img = np.array(sct.grab(mon))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, low, high)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        gasit = False
        
        if contours:
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            c = contours[0]
            
            if cv2.contourArea(c) > 60: 
                gasit = True
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"]) + mon["left"]
                    cy = int(M["m01"] / M["m00"]) + mon["top"]
                    
                    print("atac")
                    pyautogui.moveTo(cx, cy)
                    time.sleep(0.3) 
                    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
                    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
                    
                    bara_gasita = False
                    timp_cautare_bara = time.time()
                    
                    print("astept sa apara bara")
                    while time.time() - timp_cautare_bara < 10:
                        if keyboard.is_pressed('x'):
                            return
                        
                        img_sus = np.array(sct.grab(zona_bara))
                        hsv_sus = cv2.cvtColor(img_sus, cv2.COLOR_BGR2HSV)
                        
                        m1 = cv2.inRange(hsv_sus, low_rosu1, high_rosu1)
                        m2 = cv2.inRange(hsv_sus, low_rosu2, high_rosu2)
                        m_bara = cv2.bitwise_or(m1, m2)
                        
                        if cv2.countNonZero(m_bara) > 5:
                            bara_gasita = True
                            break
                        time.sleep(0.1)
                    
                    if bara_gasita:
                        print("verific bara")
                        timp_start = time.time()
                        while time.time() - timp_start < 120:
                            if keyboard.is_pressed('x'):
                                return
                                
                            img_sus = np.array(sct.grab(zona_bara))
                            hsv_sus = cv2.cvtColor(img_sus, cv2.COLOR_BGR2HSV)
                            
                            m1 = cv2.inRange(hsv_sus, low_rosu1, high_rosu1)
                            m2 = cv2.inRange(hsv_sus, low_rosu2, high_rosu2)
                            m_bara = cv2.bitwise_or(m1, m2)
                            
                            if cv2.countNonZero(m_bara) < 5:
                                break
                            time.sleep(0.5) 
                    else:
                        print("nu a dat de el caut altu")
                    
                    print("loot")
                    apasa('z')
                        
                    continue
        
        if not gasit:
            print("caut")
            keyboard.press('e')
            time.sleep(0.8)
            keyboard.release('e')
            time.sleep(0.2)

if __name__ == "__main__":
    main()