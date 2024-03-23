(deffacts Ex1

;(Teren <ID_Teren> poziția <rând> <coloana> este <stare>)
;(Teren <ID_Teren> poziția <rând> <coloana> este ocupată de nava <ID_Navă> si este <stare_poziție_navă>)
;(Nava <ID_Navă> în terenul <ID_Teren>)
;(Nava orizontala <ID_Navă> rând <ID_rând> pe coloanele <<< indici_coloane>>>)
;(Nava verticala <ID_Navă> coloana <ID_coloana> pe rândurile <<< indici_rânduri>>>)

(Teren T1 pozitia 1 1 este liber)
(Teren T1 pozitia 1 2 este liber)
(Teren T1 pozitia 1 3 este liber) 
(Teren T1 pozitia 1 4 este liber)

(Teren T1 pozitia 2 1 este ocupata de nava N1 si este neatacata)
(Teren T1 pozitia 2 2 este ocupata de nava N1 si este neatacata)
(Teren T1 pozitia 2 3 este ocupata de nava N1 si este neatacata)
(Teren T1 pozitia 2 4 este liber)

(Teren T1 pozitia 3 1 este ocupata de nava N2 si este neatacata)
(Teren T1 pozitia 3 2 este liber)
(Teren T1 pozitia 3 3 este liber) 
(Teren T1 pozitia 3 4 este liber)

(Teren T1 pozitia 4 1 este ocupata de nava N2 si este neatacata)
(Teren T1 pozitia 4 2 este liber)
(Teren T1 pozitia 4 3 este liber) 
(Teren T1 pozitia 4 4 este liber)


(Nava orizontala N1 rand 2 pe coloanele 1 2 3)
(Nava verticala N2 coloana 1 pe randurile 2 3 4)


(Nava N1 in terenul T1)
(Nava N2 in terenul T1)





)

