import cv2
import numpy as np
import mss
import pyautogui
import time
import keyboard
import ctypes
import random

low = np.array([95, 50, 50])
high = np.array([130, 255, 255])
kernel = np.ones((5,5), np.uint8)

low_rosu_metin1 = np.array([0, 160, 160])
high_rosu_metin1 = np.array([10, 255, 255])
low_rosu_metin2 = np.array([165, 160, 160])
high_rosu_metin2 = np.array([180, 255, 255])

low_viata1 = np.array([0, 100, 100])
high_viata1 = np.array([15, 255, 255])
low_viata2 = np.array([170, 100, 100])
high_viata2 = np.array([180, 255, 255])

def apasa(tasta):
    keyboard.press(tasta)
    time.sleep(0.04)
    keyboard.release(tasta)
    time.sleep(0.04)

def cauta_metin(sct, mon):
    img = np.array(sct.grab(mon))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, low, high)
    
    h, w = mask.shape
    cv2.rectangle(mask, (0, 0), (450, 150), 0, -1) 
    cv2.rectangle(mask, (0, h - 130), (w, h), 0, -1) 
    cv2.rectangle(mask, (w - 250, 0), (w, 200), 0, -1) 
    
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for c in contours:
            if cv2.contourArea(c) > 200: 
                x_rect, y_rect, w_rect, h_rect = cv2.boundingRect(c)
                if w_rect / float(h_rect) < 1.5:
                    M = cv2.moments(c)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"]) + mon["left"]
                        cy = int(M["m01"] / M["m00"]) + mon["top"]
                        return cx, cy
    return None, None

def asteapta_si_cauta(timp, taste, sct, mon):
    start = time.time()
    while time.time() - start < timp:
        if keyboard.is_pressed('x'):
            return None, None
        cx, cy = cauta_metin(sct, mon)
        if cx is not None:
            for tasta in taste:
                keyboard.release(tasta)
            return cx, cy
        time.sleep(0.05)
    return None, None

def main():
    print("start bot suprem scanare activa")
    time.sleep(5)
    sct = mss.mss()
    mon = sct.monitors[1]
    
    taura = 0
    tlicori = 0
    tzoom = 0
    timp_ultimul_gasit = time.time()
    
    zona_bara = {
        "top": 36,
        "left": 1015,
        "width": 165,
        "height": 30
    }
    
    zona_viata_caracter = {
        "top": 1018,
        "left": 62,
        "width": 10,
        "height": 4
    }
    
    while True:
        if keyboard.is_pressed('x'):
            print("stop")
            break
            
        t = time.time()
        
        if t - timp_ultimul_gasit > 60:
            print("nu am gasit nimic 60 de secunde dau restart oras")
            cx_ecran = mon["left"] + mon["width"] // 2
            cy_ecran = mon["top"] + mon["height"] // 2 + 50
            
            pyautogui.moveTo(cx_ecran, cy_ecran, 0.3)
            time.sleep(0.2)
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
            time.sleep(0.1)
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
            
            print("astept sa ma invie la oras")
            time.sleep(8) 
            
            taura = 0
            tlicori = 0
            timp_ultimul_gasit = time.time()
            continue
        
        if t - tzoom > 180:
            print("zoom out maxim din page down")
            keyboard.press('page down')
            time.sleep(1)
            keyboard.release('page down')
            tzoom = time.time()
        
        img_viata = np.array(sct.grab(zona_viata_caracter))
        hsv_viata = cv2.cvtColor(img_viata, cv2.COLOR_BGR2HSV)
        m1_v = cv2.inRange(hsv_viata, low_viata1, high_viata1)
        m2_v = cv2.inRange(hsv_viata, low_viata2, high_viata2)
        mask_viata = cv2.bitwise_or(m1_v, m2_v)
        
        if cv2.countNonZero(mask_viata) < 3:
            print("am murit astept 10 secunde")
            time.sleep(10)
            
            print("apas pe reseteaza aici")
            cx_inviere = mon["left"] + 160
            cy_inviere = mon["top"] + 102
            
            pyautogui.moveTo(cx_inviere, cy_inviere, 0.2)
            time.sleep(0.2)
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
            time.sleep(0.1)
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
            
            print("astept 2 secunde sa se incarce viata")
            time.sleep(2)
            
            print("bag abilitatile si reiau")
            apasa('2')
            time.sleep(1.5)
            apasa('3')
            time.sleep(1.5)
            
            keyboard.press('alt')
            time.sleep(0.05)
            keyboard.press('f2')
            time.sleep(0.05)
            keyboard.release('f2')
            keyboard.release('alt')
            time.sleep(0.5)
            
            timp_ultimul_gasit = time.time()
            continue
        
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
            
        cx, cy = cauta_metin(sct, mon)
        
        if cx is not None:
            timp_ultimul_gasit = time.time()
            print("atac perfect matematic")
            pyautogui.moveTo(cx, cy, 0.1) 
            time.sleep(0.1) 
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
            time.sleep(0.08)
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
            
            pyautogui.moveTo(10, 10, 0.1)
            
            bara_gasita = False
            timp_cautare_bara = time.time()
            
            print("astept bara max 4 secunde altfel fac unstuck")
            while time.time() - timp_cautare_bara < 4:
                if keyboard.is_pressed('x'):
                    return
                
                img_sus = np.array(sct.grab(zona_bara))
                hsv_sus = cv2.cvtColor(img_sus, cv2.COLOR_BGR2HSV)
                
                m1 = cv2.inRange(hsv_sus, low_rosu_metin1, high_rosu_metin1)
                m2 = cv2.inRange(hsv_sus, low_rosu_metin2, high_rosu_metin2)
                m_bara = cv2.bitwise_or(m1, m2)
                
                if cv2.countNonZero(m_bara) > 5:
                    bara_gasita = True
                    break
                time.sleep(0.1)
            
            if bara_gasita:
                print("sparg piatra")
                timp_start = time.time()
                ultimii_pixeli = -1
                timp_blocaj = time.time()
                
                while time.time() - timp_start < 120:
                    if keyboard.is_pressed('x'):
                        return
                        
                    img_sus = np.array(sct.grab(zona_bara))
                    hsv_sus = cv2.cvtColor(img_sus, cv2.COLOR_BGR2HSV)
                    
                    m1 = cv2.inRange(hsv_sus, low_rosu_metin1, high_rosu_metin1)
                    m2 = cv2.inRange(hsv_sus, low_rosu_metin2, high_rosu_metin2)
                    m_bara = cv2.bitwise_or(m1, m2)
                    pixeli_curenti = cv2.countNonZero(m_bara)
                    
                    if pixeli_curenti < 5:
                        print("fast loot agresiv")
                        for _ in range(6):
                            apasa('z')
                            time.sleep(0.05)
                        break
                        
                    if abs(pixeli_curenti - ultimii_pixeli) < 10:
                        if time.time() - timp_blocaj > 5:
                            print("blocat in mobi la piatra curat si bag s")
                            keyboard.press('space')
                            time.sleep(2)
                            keyboard.release('space')
                            
                            keyboard.press('s')
                            time.sleep(1)
                            keyboard.release('s')
                            
                            pyautogui.moveTo(10, 10)
                            break
                    else:
                        ultimii_pixeli = pixeli_curenti
                        timp_blocaj = time.time()
                        
                    time.sleep(0.3) 
            else:
                print("nu am ajuns la el bag eschiva stanga dreapta")
                tasta_eschiva = random.choice(['a', 'd', 's'])
                keyboard.press(tasta_eschiva)
                time.sleep(1)
                keyboard.release(tasta_eschiva)
                pyautogui.moveTo(10, 10)
                
            continue 
        
        timp_trecut = time.time() - timp_ultimul_gasit
        
        if timp_trecut > 4:
            print("explorare ma plimb putin prin zona")
            keyboard.press('w')
            cx_gasit, cy_gasit = asteapta_si_cauta(2.0, ['w'], sct, mon)
            if cx_gasit is not None:
                continue
            keyboard.release('w')
            
            print("reglez camera la unghiul perfect")
            keyboard.press('t')
            cx_gasit, cy_gasit = asteapta_si_cauta(2.0, ['t'], sct, mon)
            if cx_gasit is not None:
                continue
            keyboard.release('t')
            
            keyboard.press('g')
            cx_gasit, cy_gasit = asteapta_si_cauta(0.2, ['g'], sct, mon)
            if cx_gasit is not None:
                continue
            keyboard.release('g')
            
            timp_ultimul_gasit = time.time()
            
        print("radar rotesc 1.5 secunde si fac pauza")
        tasta_rotire = random.choice(['q', 'e'])
        keyboard.press(tasta_rotire)
        cx_gasit, cy_gasit = asteapta_si_cauta(1.5, [tasta_rotire], sct, mon)
        if cx_gasit is not None:
            continue
        keyboard.release(tasta_rotire)
        
        cx_gasit, cy_gasit = asteapta_si_cauta(0.3, [], sct, mon)
        if cx_gasit is not None:
            continue

if __name__ == "__main__":
    main()
