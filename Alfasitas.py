#A fő ablakhoz használt könyvtárak
from tkinter import *
import tkinter as tk
from tkinter import filedialog

#Képfeldolgozás könyvtárai
import cv2 as cv
import numpy as np

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #képernyő információk lekérése
        sw = self.winfo_screenwidth()     #szélesség
        sh = self.winfo_screenheight()    #magasság
        #tkinter
        self.geometry("+{}+{}".format(int(sw/8),int(sh/8))) #kezdő ablak pozíciója
        self.title("Balázs Márk Beadandó")
        fr = Frame(self)
        fr.pack(side=LEFT)
        self.uj = tk.Button(fr,text="Új kép", command=(lambda:self.Megy()), width=22, height=3)
        self.uj.pack()
        self.kilep = tk.Button(fr,text="Kilépés", command=(lambda:self.destroy()), width=22, height=3)
        self.kilep.pack()
        #valtozok és konstansok
        self.tegla = False
        self.rajz = False
        self.xx = 0
        self.yy = 0
        self.mod = 0
        self.maszkos = False
        self.ok = False

    def FajlValaszt(self):
        self.fpath = filedialog.askopenfilename(initialdir =  "./", title = "Válassz ki egy fájlt!", filetype = (("jpg fájlok","*.jpg"),("jpeg fájlok","*.jpeg"),("bitmap fájlok","*.bmp"),("TIFF fájlok","*.tiff"),("TIF fájlok","*.tif"),("Portable fájlok","*.png")) )
        self.fn = self.fpath.split('/')
        self.fn = self.fn[len(self.fn)-1]
        self.alap_kep = cv.imread(self.fn)
        self.kep = np.zeros(self.alap_kep.shape,np.uint8)
        self.bkup = self.alap_kep.copy()
        self.mask = np.zeros(self.alap_kep.shape[:2], np.uint8)
        self.mod = 0

    def Eger(self,event,x,y,flags,param):
        if self.mod == 0:
            if event == cv.EVENT_LBUTTONDOWN:
                self.tegla = True
                self.xx, self.yy = x,y
            elif event == cv.EVENT_MOUSEMOVE:
                if self.tegla == True:
                    self.alap_kep = self.bkup.copy()
                    cv.rectangle(self.alap_kep, (self.xx, self.yy), (x, y), (30,200,100),2)
                    self.rect = (min(self.xx, x), min(self.yy, y), max(self.xx, x), max(self.yy, y))
            elif event == cv.EVENT_LBUTTONUP:
                self.tegla = False
                cv.rectangle(self.alap_kep, (self.xx, self.yy), (x, y), (300,200,100),2)
                self.rect = (min(self.xx, x), min(self.yy, y), max(self.xx, x), max(self.yy, y))

        if self.mod == 1:
            if event == cv.EVENT_LBUTTONDOWN:
                self.rajz = True
            elif event == cv.EVENT_MOUSEMOVE:
                if self.rajz == True:
                    cv.circle(self.alap_kep,(x,y),6,(200,200,200),-1)
                    cv.circle(self.mask,(x,y),6,0,-1)
            elif event == cv.EVENT_LBUTTONUP:
                self.rajz = False
                self.maszkos = True

        if self.mod == 2:
            if event == cv.EVENT_LBUTTONDOWN:
                self.rajz = True
            elif event == cv.EVENT_MOUSEMOVE:
                if self.rajz == True:
                    cv.circle(self.alap_kep,(x,y),2,(100,100,100),-1)
                    cv.circle(self.mask,(x,y),6,1,-1)
            elif event == cv.EVENT_LBUTTONUP:
                self.rajz = False
                self.maszkos = True

    def Megy(self):
        print("===========================")
        print("q - Alfásítás")
        print("w - Négyzet kijelölése")
        print("e - Háttér korrigálás")
        print("r - Előtér korrigálás")
        print("t - Korrigálás végrehajtása")
        print("z - Mentés")
        print("Esc - Kilépés")
        print("===========================")
        try:
            self.FajlValaszt()
            self.ok = True
        except Exception as e:
            print("Nincs kiválasztott kép.")
            self.ok = False
        if self.ok:
            #ablakok létrehozása
            cv.namedWindow('bevisz')
            cv.namedWindow('mutat')
            cv.setMouseCallback('bevisz', self.Eger)
            cv.moveWindow('bevisz', 60, 60)
            cv.moveWindow('mutat', self.alap_kep.shape[1]+60, 60)
            while(1):
                cv.imshow('bevisz', self.alap_kep )
                cv.imshow('mutat', self.kep)
                gomb = cv.waitKey(1)
                if gomb == 27:
                    cv.destroyAllWindows()
                    break
                elif gomb == ord('q'):
                    bgModel = np.zeros((1,65), np.float64)
                    fgModel = np.zeros((1,65), np.float64)
                    cv.grabCut(self.bkup, self.mask, self.rect,bgModel,fgModel,1,cv.GC_INIT_WITH_RECT)
                    mask2 = np.where((self.mask == 1) + (self.mask == 3), 255, 0).astype('uint8')
                    self.kep = cv.bitwise_and(self.bkup, self.bkup, mask=mask2)
                elif gomb == ord('w'):
                    #négyzet
                    self.mod = 0
                    self.maszkos = False
                elif gomb == ord('e'):
                    #bg
                    self.mod = 1
                elif gomb == ord('r'):
                    #fg
                    self.mod = 2
                elif gomb == ord('t'):
                    if self.maszkos == True:
                        bgdModel = np.zeros((1,65), np.float64)
                        fgdModel = np.zeros((1,65), np.float64)
                        self.mask, bgdModel, fgdModel = cv.grabCut(self.kep, self.mask,None,bgdModel,fgdModel,5,cv.GC_INIT_WITH_MASK)
                        self.mask = np.where((self.mask==2)|(self.mask==0),0,1).astype('uint8')
                        self.kep = self.kep*self.mask[:,:,np.newaxis]

                elif gomb == ord('z'):
                    cv.imwrite("alfa_"+self.fn, self.kep)

if __name__=="__main__":
    app=App()
    app.mainloop()
