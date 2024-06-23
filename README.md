# DataTypes:
## walletData
Dataframe panda, con i dati importati. 
Le colonne sono: ['account', 'category', 'amount', 'type', 'note', 'date', 'labels']

## categoryResult
Dataframe panda, con categorie e loro importi 
Le colonne sono: ['category', 'amount']
, '#in', '#out', '#risparmi']


# Process
## 1. Data Import
**IN** : .csv file, data inizio, data fine

**FDT** : CategoryImport 
Data:


Process:
1. carica il file csv
3. esegue i seguenti check 
   . DONE: seleziona solo i wallet che contano
   . TO DO: controlla che la currency sia euro su tutti e poi cancella la colonna 
   
**OUT** : walletData: dati importati e filtrati

## 2. CategoryImport
**IN** : walletData

**FDT** : CategoryImport 
Data:
contiene al suo interno la lista delle categorie solo != da zero

Process:
1. riempie la lista delle categorie 
2. TO DO : splitta tra #in #out e #risparmi
   3. le colonne di categoryResult dovranno essere ['category', '#in', '#out', '#risparmi']
2. TO DO verifica che le categorie con importo 0 siano tali
3. TO 

**OUT** : categoryResult: dati importati e filtrati

## 3. Category Hierarchy
** IN ** : categoryResult

** FDT ** : CategoryImport
Data:
contiene al suo interno la lista delle categorie di secondo livello

Process
1. calcola le categorie di primo livello

** OUT ** : categoryResult