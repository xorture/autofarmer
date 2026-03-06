# metin2 autonomous farm bot v2.0 - intelligent computer vision agent

acest proiect este un agent autonom avansat creat pentru jocul metin2 care demonstreaza integrarea conceptelor de computer vision cu logica de state machine si sisteme automate de crash recovery si anti stuck
spre deosebire de versiunile anterioare botul foloseste acum algoritmi de detectie a blocajelor vizuale si manevre de navigare hardware pentru a asigura continuitatea farmului pe teren accidentat

## noutati in versiunea 2.0 (intelligent update)

* **sistem anti stuck**: botul detecteaza automat daca s a blocat in pereti munti sau mobi prin monitorizarea pixelilor de viata in timp real
* **evadare din munti**: daca botul nu gaseste nicio tinta timp de 12 secunde executa o manevra de repozitionare da cu spatele si reseteaza camera la orizontala
* **explorare dinamica**: daca zona curenta e goala botul apasa w pentru a se deplasa intr o zona noua evitand astfel ramanerea pe loc in puncte fara metine
* **refresh vizual inteligent**: dupa fiecare atac mouseul este mutat automat in coltul ecranului pentru a forța clientul de joc sa faca refresh la bara de viata evitand erorile de tip freeze frame

## ce face botul efectiv in joc

* **identificare vizuala**: scaneaza ecranul si izoleaza pietrele metin folosind masti hsv si detectie de contururi
* **atac hardware**: navigheaza cursorul si trimite comenzi de click direct prin win32api simuland un input fizic
* **monitorizare health**: urmareste bara de viata a obiectivului si reactioneaza instantaneu la disparitia pixelilor rosii
* **buff management**: gestioneaza automat aura si iuresul (descaleaca da buff urca inapoi) pe baza unor timere interne asincrone
* **auto loot**: colecteaza dropul imediat dupa distrugerea obiectivului prin apasarea tastei z

## tehnologii si concepte software folosite

* **python**: arhitectura principala a agentului
* **opencv**: procesarea imaginilor frame by frame convertirea spatiului de culori si filtrare morfologica
* **mss**: captura de ecran ultra rapida
* **numpy**: calcul matricial pentru determinarea centrelor de masa ale obiectelor
* **ctypes & win32api**: simulare input mouse la nivel de kernel pentru bypass protectii software simple

## cum functioneaza sub capota

botul ruleaza un loop principal care cauta obiecte mov pe harta odata gasita o tinta intra intr un sub loop de monitorizare a zonei superioare a ecranului unde apare bara de viata
daca variatia pixelilor rosii ramane sub un anumit prag timp de 7 secunde botul deduce ca este blocat si activeaza secventa de unstuck s (back) + t (camera pitch) + e (rotation)

## instalare si rulare

ai nevoie de python instalat pe sistem
deschide un terminal si instaleaza dependintele

```bash
pip install opencv-python numpy mss pyautogui keyboard
