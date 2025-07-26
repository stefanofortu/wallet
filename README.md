# REGOLE
1.	Tutte le spese in ingresso: devono avere etichetta #in. 
2. 	Tutte le spese in uscita: devono avere etichetta #out. 
3.  I transfer non devono avere label, eccetto per contabile.
   - Forse da togliere in futuro?
3. Tutte le spese che vanno in risparmi, devono avere etichetta risparmi.
	- Risulteranno in una colonna
4. Spese Contabili.
   OPZIONE 1
   - Quando c'è la necessità di spostare una spesa/ingresso in un altro anno contabile, bisogna fare come in questo esempio. 
	 - Stipendio di Dicembre 2024 ricevuto a Gennaio 2025
	 - Lo stipendio effettivo [Gennaio 2025] deve diventare un trasferimento in ingresso (dal di-fuori del wallet, con etichetta #contabile
	 - Lo stipendio contabile [Dicembre 2024] deve avere una voce in ingresso (#in) e un trasferimento in uscita (al difuori del wallet, con etichetta #contabile)
   OPZIONE 2
   - Usare categoria "Contabile" senza tag! (obbiettivo: diminuire il num di trasferimenti) 

5. Prestiti e Crediti.
   - Non devono avere l'etichetta #in e #out


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
2. A seconda della selezione, setta solo gli account di interesse:
   1. Se interesse "Cash", "Carta", "Banca", "Poste", "Barclays", "BPM"
4. Crea il dataframe dei transfer e quello delle spese correnti
5. Per il dataframe normale: 
	- Seleziona i dati solo nel periodo di interesse
	- controlla che le label siano solo in/out/risparmi 
6. Per il dataframe dei transfer:
   1. Controlla che le label siano solo "contabile". I transfer non devono avere label, eccetto per contabile.
   
**OUT** : walletData: dati importati e filtrati

## 2. Category_Label_Checker
**IN** : walletData

**FDT** : Category_Label_Checker
Process:
1. check_categories_name(): controlla che i nomi delle categorie siano corrette
2. Verifica che le categorie con importo 0 siano tali

**OUT** : bool

## 3. Category Classification
**IN** : class WalletData

**FDT** : 
1. Splitta tra #in #out e #risparmi
2. calcola le somme per ogni categoria base
Ke colonne di Results dovranno essere ['category', '#in', '#out', '#risparmi', '#no_tags']
3. Fa alcune verifiche sulle categorie basiche ???

**OUT** : class Results

## 4. Category Structurer
**IN** : class Results

**FDT** : 
1. Splitta tra #in #out e #risparmi
2. calcola le somme per ogni gruppi di categorie (main_categories)
3. Fa alcune verifiche sulle categorie basiche ???

**OUT** : class Results

## 5. Group Creator
**IN** : wallet_category_results
**FDT** : 
1. Calcola i gruppi di spesa
2. Verifica che i segni dei gruppi di spesa siano corretti
**OUT** : group_results (instance of Results)

## 6. File Export
**IN** : group_results , Piano_Spesa_Template_v02
**FDT** : scrive su file excel il df del categoryResult
**OUT** : File excel


# Regole di utilizzo categorie
** Bolletta telefono
Quota inquilino: come prestito
Quota mia: energia ed utenze la mia. 
Quando rimborsato, aggiungere un "Refunds" equivalente