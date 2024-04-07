(deffacts Ex1

;(Teren <ID_Teren> poziția <rând> <coloana> este <stare>)
;(Teren <ID_Teren> poziția <rând> <coloana> este ocupată de nava <ID_Navă> si este <stare_poziție_navă>)
;(Nava <ID_Navă> în terenul <ID_Teren>)
;(Nava orizontala <ID_Navă> rând <ID_rând> pe coloanele <<< indici_coloane>>>)
;(Nava verticala <ID_Navă> coloana <ID_coloana> pe rândurile <<< indici_rânduri>>>)

(Nava orizontala N1 rand 2 pe coloanele 1 2 3)
(Nava verticala N2 coloana 1 pe randurile 3 4)


(Nava N1 in terenul T1)
(Nava N2 in terenul T1)

(Sistem ataca pozitia 2 1 din terenul T1 cu B)
(Sistem ataca pozitia 2 4 din terenul T1 cu B)
(Sistem ataca pozitia 2 4 din terenul T1 cu AL)


(global_var 1 1) ; folosit pt actualizare live a variabilelor de scriere in map.txt
(update_map Yes) ; foosit pt actualizarea hartii
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

(defrule DeclareShipDistroyed "Invalidate a ship -> declare as a distroyed"
    (declare (salience 50))
    ?idx <- (Nava ?id nu este distrusa)
    (not (Teren T1 pozitia ? ? este ocupata de nava ?id si este neatacata))
    =>
    (retract ?idx)
    (assert (Nava ?id este distrusa))
    (printout t "Nava " ?id " a fost declarata distrusa!" crlf)
)


(defrule Rule_Opening_File_Read
	(declare (salience 100))
    => 
	(close)
	(open map_start.txt map_start "r")
	(printout t "Faptele au fost actualizare dupa harta" crlf)
)


(defrule Rule_Closing_File_Read
	(declare (salience 98))
	=>
	(close map_start)
	(printout t "Fisierele au fost inchise" crlf)
)


(defrule Rule_Reading_Map
    (declare (salience 99))
    =>
    (bind ?row_number 1)
    (bind ?each_line (readline map_start))
    (while (neq ?each_line EOF) do
        (bind ?col_number 1)
        (bind ?each_line_explode (str-explode ?each_line))
        (while (neq (length ?each_line_explode) 0) do
            (bind ?position_type (nth$ 1 ?each_line_explode))
            (if (and (neq ?position_type liber) (neq ?position_type atacata))
                then
                (assert (Teren T1 pozitia ?row_number ?col_number este ocupata de nava  ?position_type si este neatacata))
            else
                (assert (Teren T1 pozitia ?row_number ?col_number este ?position_type))
            )
            (bind ?each_line_explode (rest$ ?each_line_explode))
            (bind ?col_number (+ ?col_number 1))
        )
        (bind ?each_line (readline map_start))
        (bind ?row_number (+ ?row_number 1))
    )
)


(defrule Rule_Opening_File_Write
	(declare (salience 97))
    =>
	(open map_parcurs.txt map_parcurs "w")
	(printout t "Putem scrie in map.txt" crlf)
)

(defrule Rule_Closing_File_Write
	(declare (salience 95))
	=>
	(close map_parcurs)
	(printout t "Fisierele au fost inchise" crlf)
)



(defrule Rule_Writing_In_Map
    (declare (salience 96))
	?Delete1 <-(update_map Yes)
	?Delete2 <-(global_var ?row ?col)
	(or (Teren T1 pozitia ?row ?col este ocupata de nava ?check si este ?atacat_sau_nu)
		(Teren T1 pozitia ?row ?col este ?check)
	)
    =>
	(if (<= ?row ?*nr_linii*)
		then 
			(printout map_parcurs ?check " " )
			(printout t  ?row ?col ?check crlf)
			
			(if (< ?col ?*nr_coloane*)
				then
					(assert (global_var ?row (+ ?col 1)))
				;	(retract ?Delete1)
					(retract ?Delete2)
	;				(assert (rule_writing_in_map 2))
				else
					(printout t  "else" crlf)
					(retract ?Delete2)
					(if (< ?row ?*nr_linii*)
						then
							(assert (global_var (+ ?row 1) 1))
						else
							(assert (global_var 1 1))
							(assert (update_map No))
							(retract ?Delete1)
							(retract ?Delete2)
					)
						
					(printout map_parcurs crlf)
			)

	)
		
	(printout t " am actualizat o pozitie" crlf)
)



(defrule Update_Map_Command   ; daca dai (assert (update_map_now)) se va face automat o rescrie completa a hartei cu variabilele actuale
	(declare (salience 96))
	?Delete1 <-(update_map_now)
	?Delete2 <-(update_map No)
	=>
	(assert (update_map Yes))
	(retract ?Delete1)
	(retract ?Delete2)
)
