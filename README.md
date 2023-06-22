# 2022. tavaszi félév - Haladó Programozás Beadandó Feladat – Alfásítás (háttér kivágása)
A program célja, hogy egy kapott kép tárgyát (előtér) körül vágja, hátterét kivágja. A feladat elvégzéséhez Python (3.9.9) szkriptet készítettem.
## Használat:
Indítás után az ’Új Kép’ gombot megnyomva kiválaszthatjuk a feldolgozni kívánt képet. 
 
A kiválasztott kép lehet .jpg, .jpeg, .bmp, .png, .tiff vagy .tif kiterjesztésű.  
 
Megnyitás után a program betölt két ablakot egymás mellett. A bal oldali az eredeti képet mutatja, ez a beviteli ablak. A jobb oldali az algoritmussal módosított képet jeleníti meg, miután végeztünk el bármilyen műveletet.
 
Az elvégezhető műveletek és a gyorsgombok fel vannak tűntetve a parancssorban, ha semmit sem választunk ki, akkor a ’Négyzet kijelölése’ az alapművelet.
 
Az algoritmus precizitását növelhetjük, ha kijelöljük a kép tárgyát (amit körbe szeretnénk vágni). Ezt egy téglalap rajzolásával végezhetjük el. Az egérmutató bal gombját lenyomva, és lenyomva tartva kijelölhetünk egy téglalapot a ’bevisz’ ablakban. Lényegében a téglalap átlóját kell lerajzolnunk, de a könnyebb átláthatóság érdekében folyamatosan frissül a visszajelzés (zöld színű téglalap). 
  
A bal gombot felengedve véglegesíthető a téglalap, ezt indikálja, ha a téglalap színe türkiz kékre vált át. Ha új téglalapot szeretnénk rajzolni, akkor a fenti műveletet meg kell ismételnünk, ezzel felülírjuk a képre rajzolt téglalapot. 
 
Amennyiben megfelelő a kiemelésre szánt terület a Q billentyű lenyomásával elvégezhető az alfásítás. Ez a mutat ablakban jelenik meg:
 
Látható, hogy nem tökéletes a kivágás. Ezt először is az újra futtatással orvosolhatjuk ( q gomb ). De ha nem hoz jelentős javulást, akkor új eszközök alkalmazásával javíthatjuk.
A bevisz ablakban kijelöljük a hibás területeket (a megjelölés hasonló a Paint programból ismert ecset eszköz használatához.) Miután kiválasztottuk az eszközt ( e / r gomb ), a bal egérgomb lenyomásával jelölhetünk ki javítandó területeket. Először az előtérnek titulált háttér részeket jelöljük ki ( e gomb ) – e világos szürke színnel van feltüntetve. Amennyiben a kép tárgya csonkítás áldozatává vált, a hibásan háttérnek ítélt előtéri részeket jelöljük meg ( r gomb ) – sötét szürke színnel. Nem szükséges kisatíroznunk az egész hibás részt, elég ha részben megjelöljük, az algoritmus kisebb-nagyobb pontossággal felfedezi. A korrigálást a ( t  gomb ) lenyomásával végezhetjük el.
 
Ha az eredményünk megfelelő, elmenthetjük a kapott képet ( z gomb). Mentéskor a ’.jpg’ kiterjesztést alkalmazva, az eredeti fájl nevét az ’alfa_’ előtaggal kiegészíti a program, majd elhelyezi a gyökérkönyvtárunkban (a példában szereplő eset: 7.jpg -> alfa_7.jpg).
Ezután az ESC gomb lenyomásával kiléphetünk a fentebb ismertetett főmenübe. Itt ismét elvégezhető a műveletsor, vagy bezárhatjuk a programot.

## Felhasznált könyvtárak:
-	Tkinter: A központi felhasználói felületet biztosítja, ebből adódóan a programkód osztály szerkezete is köré épül. Egyik alkönyvtára (filedialog) teszi lehetővé a feldolgozásra kerülő fájl kiválasztását.
-	OpenCV: A képfeldolgozáshoz, megjelenítéshez és interakciókhoz szükséges. 
-	Numpy: Mátrix műveletek elvégzésére, az OpenCV dependenciája.

## A metódusok és a program menetének ismertetése:

### A kezdő ablak
A program indítása után létrejön egy 2 gombot tartalmazó ablak („főmenü”). A főmenüben 2 gomb található:
-	Új kép: Beléptet a központi metódusba („Megy()”).
-	Kilépés: Bezárja a programot. A Tkinter könyvtár ’destroy()’ metódusával.

### A fő metódus ( Megy() )
Két fő feladata van: meghívni a többi metódust és kezelni a felhasználói interakciókat. Elsőként kiírja a konzolba a használati utasítást, majd megpróbálja meghívni a FajlValaszt() metódust. Ha hiba lépett fel (nem választottunk ki képet), akkor ezt a konzolban kiírja, majd visszalép a főmenübe. Ha nem merül fel hiba, akkor megnyitja a ’bevisz’ és ’mutat’ ablakokat, egymás mellé helyezi őket, és nyit egy while ciklust. A while cikluson belül tölti be a beviteli és kimeneti képeket, és várja a felhasználói interakciókat. 
 

### Fájl kiválasztása ( FajlValaszt() )
Egy böngésző ablakot nyit meg, amiben kiválasztható egy kép (a fent említett kiterjesztésűek közül), majd menti az elérési útvonalát. Itt létrejön több változó is, a legfontosabbak:
-	alap_kep: Az eredeti példány, a felhasználó erre fog jelölni.
-	bkup: Mentés az eredeti képről, ha a felhasználó a jelölését változtatja, ez állítja helyre az alap_kep változót.
-	mask: Téglalap nélkül szegmentál.
-	kep: A kimenetet tartalmazza.

### Felhasználói bevitel kezelése ( Eger() )
#### Miután kiválasztottuk a szerkesztésre szánt képet és megnyílt a két ablak, az alábbi gombokkal választhatunk a műveletek közül (self.mod):
-	[ q ] Alfásítás: A gomb megnyomásakor fut le a GrabCut algoritmus. Ha rajzoltunk fel téglalapot, akkor az alapján, ellenkező esetben 
-	[ w ] Téglalap rajzolása kivágáshoz: A háttér kivágásának egyik módszere, hogy egy téglalapot rajzolunk az eredeti képre. Ez a kezdő állapot is. Egyszerre csak egy téglalapot lehet rajzolni, minden új felülírja a régit.
-	[ t ] Mentés: Lementi a képet. A fájl eredeti neve ’alfa_’ előtaggal lesz kiegészítve, a kiterjesztése ugyan az, mint a bevitelinek. A szkript aktuális könyvtárába ment.
-	[ Esc ] Kilépés

#### Az egérmutató bal gombja a legfontosabb eszköz a programban. Az előfeltétel (self.mod) megvizsgálása után, a bal egérgomb lenyomásával végezhetünk különböző műveleteket:
-	w gomb: {self.mod = 0} Téglalap rajzolását teszi lehetővé a beviteli ablakban. Az egérrel a téglalap átlóját kell megrajzolnunk. A bal egérgomb lenyomásakor kijelölünk egy pontot a képen az x és y tengelyen, felengedéskor ezzel a sarokkal átlósan egy másik pontot. Ezt a két pontot a cv.rectangle() metódusba táplálva kapjuk meg a jelölő téglalapot. Ez a téglalap a szegmentációhoz szükséges. A kívül eső pixelek PR_BGD flag-et, azaz „valószínűleg háttér” jelzést kapnak a GrabCut() algoritmustól, a bentiek PR_FGD flag-et, azaz „valószínűleg előtér” jelzést. Ahhoz, hogy a szegmentációban érvényesüljön a téglalap szerepe, a GrabCut()-ot GC_INIT_WITH_RECT állapotban kell futtatni.
-	e gomb: {self.mod = 1} Ha az algoritmus futása után maradt a képen olyan részlet, ami a háttérhez tartozik, akkor az ecset eszköz használatával írhatjuk át a mask értékeit. Az eszköz egyrészt a képen világos szürke színnel jelöli, másrészt a maszkon 0 értéket helyez el, ez a flag a GC_BGD.
-	r gomb: {self.mod = 2} Az előző eset ellenkezője. Ha olyan részt vágott ki az algoritmus, aminek szerepelnie kéne a képen, megjelölhetjük a maszkon a „biztosan előtér” (GC_FGD) flag-gel, azaz 1-es értékkel. 

## Felhasznált források:
-	OpenCV: 
  https://learnopencv.com/getting-started-with-opencv/
-	OpenCV dokumentáció:
  https://docs.opencv.org/4.x/df/d65/tutorial_table_of_content_introduction.html
-	GrabCut algoritmus:
  https://docs.opencv.org/3.4/d8/d83/tutorial_py_grabcut.html
-	egér kezelése:
  https://docs.opencv.org/4.x/db/d5b/tutorial_py_mouse_handling.html
-	Numpy:
  https://numpy.org/doc/stable/numpy-user.pdf
