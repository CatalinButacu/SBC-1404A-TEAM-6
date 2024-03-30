(deffacts Ex1

;(Teren <ID_Teren> poziția <rând> <coloana> este <stare>)
;(Teren <ID_Teren> poziția <rând> <coloana> este ocupată de nava <ID_Navă> si este <stare_poziție_navă>)
;(Nava <ID_Navă> în terenul <ID_Teren>)
;(Nava orizontala <ID_Navă> rând <ID_rând> pe coloanele <<< indici_coloane>>>)
;(Nava verticala <ID_Navă> coloana <ID_coloana> pe rândurile <<< indici_rânduri>>>)

(Teren T1 pozitia 1 1 este atacat)
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
(Teren T1 pozitia 4 3 este atacat) 
(Teren T1 pozitia 4 4 este liber)



(Nava orizontala N1 rand 2 pe coloanele 1 2 3)
(Nava verticala N2 coloana 1 pe randurile 2 3 4)


(Nava N1 in terenul T1)
(Nava N2 in terenul T1)

;(Sistem ataca pozitia 2 1 din terenul T1 cu B)
;(Sistem ataca pozitia 2 4 din terenul T1 cu B)

; (Sistem ataca pozitia 2 4 din terenul T1 cu AL)
; (Sistem ataca pozitia 2 4 din terenul T1 cu S)

)

(defglobal
?*nr_linii* = 4
?*nr_coloane* = 4
?*coloana_atac_linie* = 1
)

(defrule Actualizare_Teren_atacat_B (declare (salience 1))
(	or
	?atac <-(Sistem ataca pozitia ?rand&:(and (>= ?rand 1) (<= ?rand ?*nr_linii*)) ?coloana&:(and (>= ?coloana 1) (<= ?coloana ?*nr_coloane*)) din terenul ?Teren cu B)
	?atac <-(Jucator ataca pozitia ?rand&:(and (>= ?rand 1) (<= ?rand ?*nr_linii*)) ?coloana&:(and (>= ?coloana 1) (<= ?coloana ?*nr_coloane*)) din terenul ?Teren cu B)
)

?status_teren<-(Teren ?Teren pozitia ?rand ?coloana este liber)

=>

(retract ?atac ?status_teren)
(assert (Teren ?Teren pozitia ?rand ?coloana este atacata))

)

(defrule Actualizare_Nava_atacata_B (declare (salience 1))
(	or
	?atac <-(Sistem ataca pozitia ?rand&:(and (>= ?rand 1) (<= ?rand ?*nr_linii*)) ?coloana&:(and (>= ?coloana 1) (<= ?coloana ?*nr_coloane*)) din terenul ?Teren cu B)
	?atac <-(Jucator ataca pozitia ?rand&:(and (>= ?rand 1) (<= ?rand ?*nr_linii*)) ?coloana&:(and (>= ?coloana 1) (<= ?coloana ?*nr_coloane*)) din terenul ?Teren cu B)
)

?status_nava<-(Teren ?Teren pozitia ?rand ?coloana este ocupata de nava ?nava si este neatacata)
(Nava ?nava in terenul ?Teren)

=>

(retract ?atac ?status_nava)
(assert (Teren ?Teren pozitia ?rand ?coloana este ocupata de nava ?nava si este atacata))

)

(defrule Atac_linie_sistem (declare (salience 10))

?atac <-(Sistem ataca pozitia ?rand&:(and (>= ?rand 1) (<= ?rand ?*nr_linii*)) ?coloana&:(and (>= ?coloana 1) (<= ?coloana ?*nr_coloane*)) din terenul ?Teren cu AL)

=>

(while (neq ?*coloana_atac_linie* ?*nr_coloane*)
	do
		(assert (Sistem ataca pozitia ?rand ?*coloana_atac_linie* din terenul ?Teren cu B ))
		(bind ?*coloana_atac_linie* (+ ?*coloana_atac_linie* 1))
)

(assert (Sistem ataca pozitia ?rand ?*coloana_atac_linie* din terenul ?Teren cu B ))
(bind ?*coloana_atac_linie* 1)
(retract ?atac)

)

(defrule Atac_linie_jucator (declare (salience 10))

?atac <-(Jucator ataca pozitia ?rand&:(and (>= ?rand 1) (<= ?rand ?*nr_linii*)) ?coloana&:(and (>= ?coloana 1) (<= ?coloana ?*nr_coloane*)) din terenul ?Teren cu AL)

=>

(while (neq ?*coloana_atac_linie* ?*nr_coloane*)
	do
		(assert (Jucator ataca pozitia ?rand ?*coloana_atac_linie* din terenul ?Teren cu B ))
		(bind ?*coloana_atac_linie* (+ ?*coloana_atac_linie* 1))
)

(assert (Jucator ataca pozitia ?rand ?*coloana_atac_linie* din terenul ?Teren cu B ))
(bind ?*coloana_atac_linie* 1)
(retract ?atac)

)

(defrule Atac_scanare_sistem (declare (salience 1))

?atac <-(Sistem ataca pozitia ?rand&:(and (>= ?rand 1) (<= ?rand ?*nr_linii*)) ?coloana&:(and (>= ?coloana 1) (<= ?coloana ?*nr_coloane*)) din terenul ?Teren cu S)
(Teren ?Teren pozitia ?rand_de_verificat&:(and (>= ?rand_de_verificat (- ?rand 1)) (<= ?rand_de_verificat (+ ?rand 1))) ?coloana_de_verificat&:(and (>= ?coloana_de_verificat (- ?coloana 1)) (<= ?coloana_de_verificat (+ ?coloana 1))) este ocupata de nava ? si este neatacata)
=>

(printout t "Exista o nava in zona scanata" crlf)
(retract ?atac)
)

(defrule Atac_scanare_jucator (declare (salience 1))

?atac <-(Jucator ataca pozitia ?rand&:(and (>= ?rand 1) (<= ?rand ?*nr_linii*)) ?coloana&:(and (>= ?coloana 1) (<= ?coloana ?*nr_coloane*)) din terenul ?Teren cu S)
(Teren ?Teren pozitia ?rand_de_verificat&:(and (>= ?rand_de_verificat (- ?rand 1)) (<= ?rand_de_verificat (+ ?rand 1))) ?coloana_de_verificat&:(and (>= ?coloana_de_verificat (- ?coloana 1)) (<= ?coloana_de_verificat (+ ?coloana 1))) este ocupata de nava ? si este neatacata)
=>

(printout t "Exista o nava in zona scanata" crlf)
(retract ?atac)
)



(defrule Rule_Opening_File_Read
	(declare (salience 100))
    => 
	(clear)
	(close)
	(open map.txt map "r")
	(printout t "Faptele au fost actualizare dupa harta" crlf)
)

(defrule Rule_Closing_File_Read
	(declare (salience 98))
	=>
	(close map)
	(printout t "Fisierele au fost inchise" crlf)
)

(defrule Rule_Reading_Map
    (declare (salience 99))
    =>
    (bind ?row_number 1)
    (bind ?each_line (readline map))
    (while (neq ?each_line EOF) do
        (bind ?col_number 1)
        (bind ?each_line_explode (str-explode ?each_line))
        (while (neq (length ?each_line_explode) 0) do
            (bind ?position_type (nth$ 1 ?each_line_explode))
            (if (and (neq ?position_type liber) (neq ?position_type atacat))
                then
                (assert (Teren T1 pozitia ?row_number ?col_number este ocupata de nava  ?position_type si este neatacata))
            else
                (assert (Teren T1 pozitia ?row_number ?col_number este ?position_type))
            )
            (bind ?each_line_explode (rest$ ?each_line_explode))
            (bind ?col_number (+ ?col_number 1))
        )
        (bind ?each_line (readline map))
        (bind ?row_number (+ ?row_number 1))
    )
