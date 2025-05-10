# REGOLE
1.	Tutte le spese in ingresso: devono avere etichetta #in. 
2. 	Tutte le spese in uscita: devono avere etichetta #out. 
3.  I transfer non devono avere label, eccetto per contabile.
   - Forse da togliere in futuro?
3. Tutte le spese che vanno in risparmi, devono avere etichetta risparmi.
	- Risulteranno in una colonna
4. Spese Contabili.
   - Quando c'è la necessità di spostare una spesa/ingresso in un altro anno contabile, bisogna fare come in questo esempio. 
	 - Stipendio di Dicembre 2024 ricevuto a Gennaio 2025
	 - Lo stipendio effettivo [Gennaio 2025] deve diventare un trasferimento in ingresso (dal di-fuori del wallet, con etichetta #contabile
	 - Lo stipendio contabile [Dicembre 2024] deve avere una voce in ingresso (#in) e un trasferimento in uscita (al difuori del wallet, con etichetta #contabile)

# DataTypes:
## walletData
Dataframe panda, con i dati importati. 
Le colonne sono: ['account', 'category', 'amount', 'type', 'note', 'date', 'labels']
Ce ne sono due:
	1. Per le spese - solo per anno corrente
	2. L'altro per i trasferimenti - di tutti gli anni!

## categoryResult
Dataframe panda, con categorie e loro importi 
Le colonne sono: ['category', 'amount', '#in', '#out', '#risparmi']
 **riverificare questo**

# Process
## 1. DataImporter
**IN** : .csv file, time_period

Process:
1. carica il file csv, 
	1. Ccontrolla che la currency sia euro su tutti e poi cancella la colonna 
	2. Cancella le colonne di non interesse
	3. Seleziona solo gli account di interesse
2. Seleziona solo gli account di interesse: "Cash", "Carta", "Banca", "Poste", "Barclays", "BPM"
4. Crea il dataframe dei transfer e quello delle spese correnti
5. Per il dataframe normale: 
	- Seleziona i dati solo nel periodo di interesse
	- controlla che le label siano solo in/out/risparmi 
6. Per il dataframe dei transfer:
   1. Controlla che le label siano solo "contabile". I transfer non devono avere label, eccetto per contabile.
   
**OUT** : walletData: dati importati e filtrati

## 2. CategoryImport
**IN** : walletData

**FDT** : CategoryImport 
Process:
1. riempie la lista delle categorie 
2. TO DO : splitta tra #in #out e #risparmi
   3. le colonne di categoryResult dovranno essere ['category', '#in', '#out', '#risparmi']
2. TO DO verifica che le categorie con importo 0 siano tali
3. TO 

**OUT** : categoryResult: dati importati e filtrati

## 3. Category Hierarchy
**IN** : categoryResult

**FDT** : CategoryImport
Process
1. calcola le categorie di primo livello

**OUT** : categoryResult

## 4. File Export
**IN** : categoryResult, outfile

**FDT** : scrive su file excel il df
Process
1. calcola le categorie di primo livello

**OUT** : categoryResult


# Regole di utilizzo categorie
** Bolletta telefono
Quota inquilino: come prestito
Quota mia: energia ed utenze la mia. 
Quando rimborsato, aggiungere un "Refunds" equivalente