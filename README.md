# metin2 auto farmer

acest proiect este un bot complet autonom pentru jocul metin2 creat pentru a demonstra concepte avansate de computer vision automatizare si pixel reading in timp real
dincolo de utilitatea lui in joc codul reprezinta o arhitectura solida pentru orice agent vizual care trebuie sa ia decizii decizii de navigare si timing pe baza elementelor de pe ecran fara sa citeasca memoria ram a aplicatiei

## ce face botul efectiv in joc

* scaneaza harta si identifica pietrele metin pe baza semnaturii lor vizuale
* navigheaza cursorul si ataca piatra folosind clickuri hardware la nivel de kernel
* monitorizeaza in timp real bara de viata a pietrei si apasa tasta de loot instant cand viata ajunge la zero
* gestioneaza buffurile caracterului coboara de pe cal activeaza aura si iures si urca inapoi pe baza de timere asincrone
* aplica licori si roua dintr un inventar secundar folosind combinatii rapide de taste ascunse
* roteste camera automat cand nu mai gaseste nicio tinta valida pe ecran pentru a explora zona

## tehnologii si concepte software folosite

* python pentru logica principala state machines si gestionarea buclei infinite de actiuni
* opencv libraria principala pentru procesarea imaginilor convertirea spatiului de culori in hsv si detectia de contururi
* mss pentru captura de ecran frame by frame la viteze extrem de mari cu impact minim asupra procesorului
* numpy pentru calcule matematice matriciale si gasirea centrului de masa al formelor geometrice detectate
* ctypes si win32api pentru simularea inputului de mouse direct din kernelul de windows facand clickurile invizibile pentru sistemele de securitate simple care blocheaza clickurile virtuale

## cum functioneaza sub capota

botul ruleaza o bucla continua care captureaza ecranul si aplica o masca de culoare hsv pentru a izola pietrele metin
dupa ce izoleaza culorile opencv gaseste contururile si numpy calculeaza centrul celui mai mare obiect detectat
odata inceput atacul intra intr un sub loop de inalta frecventa care decupeaza doar zona in care apare bara de viata si numara pixelii rosii de mai multe ori pe secunda
cand pixelii rosii dispar botul stie cert ca obiectivul a fost distrus si declanseaza functia de colectare fara delay

## instalare si rulare

ai nevoie de python instalat pe sistem
deschide un cmd sau terminal si instaleaza dependintele ruland comanda de mai jos

pip install opencv-python numpy mss pyautogui keyboard

pentru a rula scriptul scrie in terminal

python nume_script.py

ai mereu la dispozitie tasta x pentru oprire de urgenta in caz ca trebuie sa intrerupi procesul instantaneu

## ghid tehnic calibrarea culorilor hsv

daca vrei sa farmezi alte pietre sau obiecte trebuie sa schimbi valorile low si high din cod
hsv inseamna hue saturation value si e un model mult mai bun decat rgb pentru detectia obiectelor in medii 3d unde lumina si umbrele se schimba constant
in script ai array urile astea doua

low = np.array([138, 60, 60])
high = np.array([165, 255, 255])

primul numar din paranteza este hue adica nuanta culorii de baza pe roata culorilor
al doilea este saturation adica cat de stearsa sau pura e culoarea
al treilea este value adica cat de intunecata sau luminoasa e culoarea
poti folosi utilitare online de color picker hsv ca sa gasesti codurile pentru orice alta piatra mob sau element vizual din joc si sa le inlocuiesti in script pentru a i schimba tinta complet

