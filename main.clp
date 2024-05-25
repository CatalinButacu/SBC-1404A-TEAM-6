(deffacts BattleshipGame

    ;(Teren <ID_Teren> poziția <rând> <coloana> este <stare>)
    ;(Teren <ID_Teren> poziția <rând> <coloana> este ocupată de nava <ID_Navă> si este <stare_poziție_navă>)
    ;(Nava <ID_Navă> în terenul <ID_Teren>)
    ;(Nava orizontala <ID_Navă> rând <ID_rând> pe coloanele <<< indici_coloane>>>)
    ;(Nava verticala <ID_Navă> coloana <ID_coloana> pe rândurile <<< indici_rânduri>>>)
    ;(Sistem ataca pozitia <ID_rând> <ID_coloana> din terenul <ID_Teren> cu <ABILITY>)

    ; Notite structura aplicatie
    ; T1 - client
    ; T2 - sistem expert

    ; Contor de stare pt Sistem: ia decizii sau asteapta input client 
    ; (Sistem asteapta)
    (Sistem decide)

    ; (Teren T1 pozitia 2 3 este atacata)
    (Nava N2 nu este distrusa)
    (Nava N3 nu este distrusa)

    (Nava N2 in terenul T1)
    (Nava N3 in terenul T1)   

    (Nava orizontala N2 rand 2 pe coloanele 1 2 3 4)
    (Nava verticala N3 coloana 1 pe randurile 3 4) 

    (global_var 1 1) ; folosit pt actualizare live a variabilelor de scriere in map.txt
    (update_map Yes) ; folosit pt actualizarea hartii
	(dificultate 3)  ;folosit pentru calculul frontierei
	
)


(defglobal
    ?*nr_linii* = 4
    ?*nr_coloane* = 4
    ?*coloana_atac_linie* = 1
	?*x0* = 0
	?*x1* = 0
	?*y0* = 0
	?*y1* = 0
	?*hit* = 0 ;folosit pentru a opri atacurile random de pe frontiera atunci cand a fost lovita o nava
    ?*isDebugging* = 0 ; just change to 1 to activate prints / to 0 to deactivate prints from operations
)


;;; UPDATE RULES
(defrule Actualizare_Teren_atacat_B_jucator (declare (salience 1))
    ?atac <-(Jucator ataca pozitia ?rand&:(and (>= ?rand 1) (<= ?rand ?*nr_linii*)) ?coloana&:(and (>= ?coloana 1) (<= ?coloana ?*nr_coloane*)) din terenul ?Teren cu B)
    ?status_teren<-(Teren ?Teren pozitia ?rand ?coloana este liber)
    =>
    (retract ?atac ?status_teren)
    (assert (Teren ?Teren pozitia ?rand ?coloana este atacata))
)

(defrule Actualizare_Teren_atacat_B_Sistem (declare (salience 2))
    ?atac <-(Sistem ataca pozitia ?rand&:(and (>= ?rand 1) (<= ?rand ?*nr_linii*)) ?coloana&:(and (>= ?coloana 1) (<= ?coloana ?*nr_coloane*)) din terenul ?Teren cu B)
    ?status_teren<-(Teren ?Teren pozitia ?rand ?coloana este liber)
    =>
    (retract ?atac ?status_teren)
    (assert (Teren ?Teren pozitia ?rand ?coloana este atacata))
)

(defrule Actualizare_Nava_atacata_B_jucator (declare (salience 1))
    ?atac <- (Jucator ataca pozitia ?rand&:(and (>= ?rand 1) (<= ?rand ?*nr_linii*)) ?coloana&:(and (>= ?coloana 1) (<= ?coloana ?*nr_coloane*)) din terenul ?Teren cu B)
    ?status_nava <- (Teren ?Teren pozitia ?rand ?coloana este ocupata de nava ?nava si este neatacata)
    (Nava ?nava in terenul ?Teren)
    =>
    (retract ?atac ?status_nava)
    (assert (Teren ?Teren pozitia ?rand ?coloana este ocupata de nava ?nava si este atacata))
)

(defrule Actualizare_Nava_atacata_B_Sistem (declare (salience 2))
    ?atac <- (Sistem ataca pozitia ?rand&:(and (>= ?rand 1) (<= ?rand ?*nr_linii*)) ?coloana&:(and (>= ?coloana 1) (<= ?coloana ?*nr_coloane*)) din terenul ?Teren cu B)
    ?status_nava <- (Teren ?Teren pozitia ?rand ?coloana este ocupata de nava ?nava si este neatacata)
    (Nava ?nava in terenul ?Teren)
    =>
    (retract ?atac ?status_nava)
    (assert (Teren ?Teren pozitia ?rand ?coloana este ocupata de nava ?nava si este atacata))
	(bind ?*hit* 1)
)

;;; DIRECT ATTACK RULES
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
    (Teren ?Teren pozitia ?rand_de_verificat&:(and (>= ?rand_de_verificat (- ?rand 1)) (<= ?rand_de_verificat (+ ?rand 1))) ?coloana_de_verificat&:(and (>= ?coloana_de_verificat (- ?coloana 1)) (<= ?coloana_de_verificat (+ ?coloana 1))) este ocupata de nava ?nava si este neatacata)
    =>
    (if (eq ?*isDebugging* 1) then (printout t "Exista o nava in zona scanata" crlf))
    (retract ?atac)
	(assert (calcul_frontiera ?rand_de_verificat ?coloana_de_verificat))
)

(defrule Atac_scanare_jucator (declare (salience 1))
    ?atac <-(Jucator ataca pozitia ?rand&:(and (>= ?rand 1) (<= ?rand ?*nr_linii*)) ?coloana&:(and (>= ?coloana 1) (<= ?coloana ?*nr_coloane*)) din terenul ?Teren cu S)
    (Teren ?Teren pozitia ?rand_de_verificat&:(and (>= ?rand_de_verificat (- ?rand 1)) (<= ?rand_de_verificat (+ ?rand 1))) ?coloana_de_verificat&:(and (>= ?coloana_de_verificat (- ?coloana 1)) (<= ?coloana_de_verificat (+ ?coloana 1))) este ocupata de nava ? si este neatacata)
    =>
    (if (eq ?*isDebugging* 1) then (printout t "Exista o nava in zona scanata" crlf))
    (retract ?atac)
)

;;; FRONTIER CALCULATION 

(defrule Calcul_frontiera (declare (salience 3))
	?calcul <- (calcul_frontiera ?rand ?coloana)
	(dificultate ?dificultate)
	=>	
	(if (< (- ?rand (- 4 ?dificultate)) 1) then
	(bind ?*x0* 1)
	else
	(bind ?*x0* (- ?rand (- 4 ?dificultate)))
	)
	
	(if (> (+ ?rand (- 4 ?dificultate)) ?*nr_linii*) then
	(bind ?*x1* ?*nr_linii*)
	else
	(bind ?*x1* (+ ?rand (- 4 ?dificultate)))
	)
	
	(if (< (- ?coloana (- 4 ?dificultate)) 1) then
	(bind ?*y0* 1)
	else
	(bind ?*y0* (- ?coloana (- 4 ?dificultate)))
	)
	
	(if (> (+ ?coloana (- 4 ?dificultate)) ?*nr_coloane*) then
	(bind ?*y1* ?*nr_coloane*)
	else
	(bind ?*y1* (+ ?coloana (- 4 ?dificultate)))
	)
	
	(assert (frontiera ?*x0* ?*y0* ?*x1* ?*y1*))
	(retract ?calcul)
	(bind ?*x0* 0)
	(bind ?*x1* 0)
	(bind ?*y0* 0)
	(bind ?*y1* 0)
	(bind ?*hit* 0)
)

;;; SYSTEM RANDOM ATTACK USING FRONTIER - WORK IN PROGRESS

(defrule Sistem_ataca_frontiera (declare (salience 1))
	(frontiera ?x0 ?y0 ?x1 ?y1)
	(or
	(Teren T1 pozitia ?rand&:(and (>= ?rand ?x0) (<= ?rand ?x1)) ?coloana&:(and (>= ?coloana ?y0) (<= ?coloana ?y1)) este liber)
	(Teren T1 pozitia ?rand&:(and (>= ?rand ?x0) (<= ?rand ?x1)) ?coloana&:(and (>= ?coloana ?y0) (<= ?coloana ?y1)) este ocupata $?)
	)
	=>
	(if (eq ?*hit* 0) then
		(assert (Sistem ataca pozitia ?rand ?coloana din terenul T1 cu B))
	)
)

(defrule Reset_hit (declare (salience -1))
	=>
	(if (eq ?*hit* 1) then
		(bind ?*hit* 0)
	)

)
;;; SEARCH ALGO RULES
(defrule CruceSearch "Sistem has info for only ONE HIT and NOTHING MORE"
    (declare (salience 20))
    (Sistem decide)
    (Teren T1 pozitia ?rowAttacked ?colAttacked este ocupata de nava ?id_nava si este ?stare&:(eq ?stare atacata))
    (Nava ?id_nava nu este distrusa)  
    (not (Sistem ataca pozitia ? ? din terenul ? cu ?))  ; check for no more planning actions

    ; investigam teritoriul alaturat
    (and ; in the MIDDLE - it fails for edges because some facts doesn't exist at moment in database
        ; check UP state
        (Teren T1 pozitia ?UP_rowAttack&:(eq ?UP_rowAttack (- ?rowAttacked 1)) ?UP_colAttack&:(eq ?UP_colAttack ?colAttacked) este $? ?stareUP)
        ; check DOWN state
        (Teren T1 pozitia ?DOWN_rowAttack&:(eq ?DOWN_rowAttack (+ ?rowAttacked 1)) ?DOWN_colAttack&:(eq ?DOWN_colAttack ?colAttacked) este $? ?stareDOWN)
        ; check LEFT state
        (Teren T1 pozitia ?LEFT_rowAttack&:(eq ?LEFT_rowAttack ?rowAttacked) ?LEFT_colAttack&:(eq ?LEFT_colAttack (- ?colAttacked 1)) este $? ?stareLEFT)
        ; check RIGHT state
        (Teren T1 pozitia ?RIGHT_rowAttack&:(eq ?RIGHT_rowAttack ?rowAttacked) ?RIGHT_colAttack&:(eq ?RIGHT_colAttack (+ ?colAttacked 1)) este $? ?stareRIGHT)
    )

    ; exclude this rule if a navy has 2 hits and let LineSearch to do his work
    (Teren T1 pozitia ?row ?col este ocupata de nava ?id_nava si este ?stare&:(eq ?stare atacata))
    (not (test (or (neq ?row ?rowAttacked) (neq  ?col ?colAttacked))))
    

    ; TODO: add a way to check for edges
    ; 
    ; A solution would be to add dummy facts, like this example for UP:
    ;   + (Teren T1 pozitia 0 <current_col> este $? ?) 
    ; Explanations: in action zone algo check if an edge is Approacheble, so Sistem will never attack a dummy fact
    ; Problem now is that this rule is filtering too much, edges fail at the (and ..) above

    =>    
    ; check for frontier edges - WARNING: it is not feasible with a 1x1 or 2x2 terrain
    (bind ?is_UP_Approachable    (and (neq ?rowAttacked 1) (neq ?stareUP atacata)))
    (bind ?is_DOWN_Approachable  (and (neq ?rowAttacked ?*nr_linii*) (neq ?stareDOWN atacata)))
    (bind ?is_LEFT_Approachable  (and (neq ?colAttacked 1) (neq ?stareLEFT atacata)))
    (bind ?is_RIGHT_Approachable (and (neq ?colAttacked ?*nr_coloane*) (neq ?stareRIGHT atacata)))

    (bind ?rowToAttack -1)
    (bind ?colToAttack -1)

    (bind ?rand (random 1 4))
    (printout t ?rand crlf)
    (while (neq ?rand 0) do
        ; update attack zone if UP is unattacked
        (if (and ?is_UP_Approachable (neq ?rand 0)) then 
            (bind ?rand (- ?rand 1)) 
            (bind ?rowToAttack ?UP_rowAttack) 
            (bind ?colToAttack ?UP_colAttack)
            (if (eq ?*isDebugging* 1) then (printout t "UP:"?stareUP crlf))
        )

        ; update attack zone if DOWN is unattacked
        (if (and ?is_DOWN_Approachable (neq ?rand 0)) then 
            (bind ?rand (- ?rand 1)) 
            (bind ?rowToAttack ?DOWN_rowAttack) 
            (bind ?colToAttack ?DOWN_colAttack)
            (if (eq ?*isDebugging* 1) then (printout t "DOWN:"?stareDOWN crlf))
        )

        ; update attack zone if LEFT is unattacked
        (if (and ?is_LEFT_Approachable (neq ?rand 0)) then 
            (bind ?rand (- ?rand 1)) 
            (bind ?rowToAttack ?LEFT_rowAttack) 
            (bind ?colToAttack ?LEFT_colAttack)
            (if (eq ?*isDebugging* 1) then (printout t "LEFT:"?stareLEFT crlf))
        )

        ; update attack zone if RIGHT is unattacked
        (if (and ?is_RIGHT_Approachable (neq ?rand 0)) then 
            (bind ?rand (- ?rand 1)) 
            (bind ?rowToAttack ?RIGHT_rowAttack) 
            (bind ?colToAttack ?RIGHT_colAttack)
            (if (eq ?*isDebugging* 1) then (printout t "RIGHT:"?stareRIGHT crlf))
        )
    )

    (if (and (neq ?rowToAttack -1) (neq ?colToAttack -1)) then
        (assert (Sistem ataca pozitia ?rowToAttack ?colToAttack din terenul T1 cu B))
        (if (eq ?*isDebugging* 1) then  (printout t "[PLANNING] S-a planificat un atac in T1 pe pozX:" ?rowToAttack ", pozY:" ?colToAttack crlf))
    else
        (if (eq ?*isDebugging* 1) then (printout t "[WARNING] Pozitii invalide gasite de met. CruceSearch" crlf))
        (if (eq ?*isDebugging* 1) then (printout t "[WARNING] Nava " ?id_nava " ar putea fi deja distrusa!!" crlf))
    )
)

(defrule LineSearch "Sistem has info for at least TWO HIT POINTS"
    (declare (salience 20))
    (Sistem decide)
    (Teren T1 pozitia ?rowHit1 ?colHit1 este ocupata de nava ?id_nava si este ?stare&:(eq ?stare atacata))
    (Teren T1 pozitia ?rowHit2 ?colHit2 este ocupata de nava ?id_nava si este ?stare&:(eq ?stare atacata))
    (Teren T1 pozitia ?rowHitIntern ?colHitIntern este ocupata de nava ?id_nava si este ?stare&:(eq ?stare atacata))
    (Nava ?id_nava nu este distrusa)
    (not (Sistem ataca pozitia ? ? din terenul ? cu ?))  ; check for no more planning actions
   
    ; check if last hits are on different rows or columns
    (test
        (if (or (and (eq ?rowHitIntern ?rowHit1) (eq ?colHitIntern ?colHit1)) (and (eq ?rowHitIntern ?rowHit2) (eq ?colHitIntern ?colHit2))) then
            (or 
                ; TODO: find a way to better check for 2 hits ships, without duplicating the rule activation or redirect ships w/ 2hits to +3 ships method
                (and (eq ?rowHit1 ?rowHit2) (> ?colHit1 ?colHit2) (eq ?rowHitIntern ?rowHit1) (neq ?rowHitIntern ?rowHit2) (if (eq ?*isDebugging* 1) then  (printout t "Same row = 2 hits" crlf) )) ; same row
                (and (eq ?colHit1 ?colHit2) (> ?rowHit1 ?rowHit2) (eq ?colHitIntern ?colHit1) (neq ?colHitIntern ?colHit2) (if (eq ?*isDebugging* 1) then (printout t "Same col = 2 hits" crlf) )) ; same col
            )               
        else
            (or
                ; TODO: fix that many fule activations on +3 hits
                (and FALSE (eq ?rowHit1 ?rowHit2 ?rowHitIntern) (not (and (> ?colHitIntern ?colHit1) (> ?colHitIntern ?colHit2))))
                (and FALSE (eq ?colHit1 ?colHit2 ?colHitIntern) (not (and (> ?rowHitIntern ?rowHit1) (> ?rowHitIntern ?rowHit2))))
            )    
        )
    )    
    
    ; TODO: find an algo to take in count attacked zones
    ;
    ; investigam teritoriul alaturat
    ;(and 
        ; check UP terrain state
        ;(Teren T1 pozitia ?UP_rowAttack&:(eq ?UP_rowAttack (- ?rowHit2 1)) ?UP_colAttack&:(eq ?UP_colAttack ?colHit2) este $? ?stareUP&:(neq ?stareUP atacata))
        ; check DOWN terrain state
        ;(Teren T1 pozitia ?DOWN_rowAttack&:(eq ?DOWN_rowAttack (+ ?rowHit1 1)) ?UP_colAttack&:(eq ?UP_colAttack ?colHit2) este $? ?stareDOWN&:(neq ?stareDOWN atacata))
        ; check LEFT terrain state
        ;(Teren T1 pozitia ?LEFT_rowAttack&:(eq ?LEFT_rowAttack (- ?colHit2 1)) ?UP_colAttack&:(eq ?UP_colAttack ?rowHit1) este $? ?stareLEFT&:(neq ?stareLEFT atacata))
        ; check RIGHT terrain state
        ;(Teren T1 pozitia ?RIGHT_rowAttack&:(eq ?RIGHT_rowAttack (+ ?colHit1 1)) ?UP_colAttack&:(eq ?UP_colAttack ?rowHit1) este $? ?stareRIGHT&:(neq ?stareRIGHT atacata))
    ;)
                        
    =>
    ; init    
    (bind ?rowToAttack -1)
    (bind ?colToAttack -1)

    ; look after direction
    (if (eq ?rowHit1 ?rowHit2) then (bind ?rowToAttack ?rowHit1))
    (if (eq ?colHit1 ?colHit2) then (bind ?colToAttack ?colHit1))

    (bind ?rand (random 1 2)) ; left or right / up or down

    (if (eq ?colToAttack -1) then
        ; Sistem attack on horizontal line 
        (bind ?is_LEFT_Approachable (neq (min ?colHit1 ?colHit2) 1))
        (bind ?is_RIGHT_Approachable (neq (max ?colHit1 ?colHit2) ?*nr_coloane*))

        (if (and (eq ?rand 1) ?is_LEFT_Approachable) then 
            (bind ?colToAttack (- (min ?colHit1 ?colHit2) 1))
            (if (eq ?*isDebugging* 1) then (printout t "LEFT" crlf))
        )

        (if (and (neq ?rand 1) ?is_RIGHT_Approachable) then 
            (bind ?colToAttack (+ (max ?colHit1 ?colHit2) 1))
            (if (eq ?*isDebugging* 1) then (printout t "RIGHT" crlf))
        )
    ) 

    (if (eq ?rowToAttack -1) then 
        ; Sistem attack on vertical line       
        (bind ?is_UP_Approachable (neq (min ?rowHit1 ?rowHit2) 1))
        (bind ?is_DOWN_Approachable (neq (max ?rowHit1 ?rowHit2) ?*nr_linii*))

        (if (and (eq ?rand 1) ?is_UP_Approachable) then
            (bind ?rowToAttack (- (min ?rowHit1 ?rowHit2) 1))
            (if (eq ?*isDebugging* 1) then (printout t "UP" crlf))
        )

        (if (and (neq ?rand 1) ?is_DOWN_Approachable) then
            (bind ?rowToAttack (+ (max ?rowHit1 ?rowHit2) 1))
            (if (eq ?*isDebugging* 1) then (printout t "DOWN" crlf))
        )
    )

    (if (and (neq ?rowToAttack -1) (neq ?colToAttack -1)) then
        (assert (Sistem ataca pozitia ?rowToAttack ?colToAttack din terenul T1 cu B))
        (if (eq ?*isDebugging* 1) then (printout t "[PLANNING] S-a planificat un atac in T1 pe pozX:" ?rowToAttack ", pozY:" ?colToAttack crlf))
    else
        (if (eq ?*isDebugging* 1) then (printout t "[WARNING] Pozitii invalide gasite de met. LineSearch" crlf))
        (if (eq ?*isDebugging* 1) then (printout t "[WARNING] Nava " ?id_nava " ar putea fi deja distrusa!!" crlf))
    )
)

;;; AUTOMATIONS
(defrule DeclareShipDistroyed "Invalidate a ship -> declare as a distroyed"
    (declare (salience 50))
    ?idx <- (Nava ?id nu este distrusa)
    (not (Teren T1 pozitia ? ? este ocupata de nava ?id si este neatacata))
    =>
    (retract ?idx)
    (assert (Nava ?id este distrusa))
    (if (eq ?*isDebugging* 1) then (printout t "Nava " ?id " a fost declarata distrusa!" crlf))
)

(defrule FreezeStateSistem "Prepare terrain for the new state comutation that will be inserted"
    (declare (salience 500))
    ?idx_freeze <- (freeze_state_sistem)
    ?idx_state <- (Sistem ?)
    =>
    (retract ?idx_freeze ?idx_state)
)

(defrule Update_Map_Command "daca dai (assert (update_map_now)) se va face automat o rescrie completa a hartei cu variabilele actuale"
	(declare (salience 96))
	?Delete1 <-(update_map_now)
	?Delete2 <-(update_map No)
	=>
	(assert (update_map Yes))
	(retract ?Delete1)
	(retract ?Delete2)
)
;;; FILES OPERATIONS
(defrule Rule_Opening_File_Read
	(declare (salience 100))
    => 
	(close)
	(open map_start.txt map_start "r")
	(if (eq ?*isDebugging* 1) then (printout t "Faptele au fost actualizare dupa harta" crlf))
)


(defrule Rule_Closing_File_Read
	(declare (salience 98))
	=>
	(close map_start)
	(if (eq ?*isDebugging* 1) then (printout t "Fisierele au fost inchise" crlf))
)


(defrule Rule_Reading_Map
    (declare (salience 99))
    =>
    (bind ?row_number 1)
    (bind ?each_line (readline map_start))
    (while (neq ?each_line EOF) do
        (bind ?col_number 1)
        (bind ?each_line_explode (explode$ ?each_line))
        (while (neq (length$ ?each_line_explode) 0) do
            (bind ?position_type (nth$ 1 ?each_line_explode))
            (if (and (neq ?position_type liber) (neq ?position_type atacata))
                then
                (assert (Teren T1 pozitia ?row_number ?col_number este ocupata de nava ?position_type si este neatacata))
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
	(if (eq ?*isDebugging* 1) then (printout t "Putem scrie in map.txt" crlf))
)

(defrule Rule_Closing_File_Write
	(declare (salience 95))
	=>
	(close map_parcurs)
	(if (eq ?*isDebugging* 1) then (printout t "Fisierele au fost inchise" crlf))
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
			(if (eq ?*isDebugging* 1) then (printout t  ?row ?col ?check crlf))
			
			(if (< ?col ?*nr_coloane*)
				then
					(assert (global_var ?row (+ ?col 1)))
				;	(retract ?Delete1)
					(retract ?Delete2)
	;				(assert (rule_writing_in_map 2))
				else
					(if (eq ?*isDebugging* 1) then (printout t  "else" crlf))
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
		
	(if (eq ?*isDebugging* 1) then (printout t " am actualizat o pozitie" crlf))
)



