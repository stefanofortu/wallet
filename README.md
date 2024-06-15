# Wallet
## Data Import
*IN* : .csv file, periodotemporale
*OUT* : CategoryClass: classe che contiene un array numpy, 
1a colonna categorie, e poi #in#, #out#, #risparmi" ognuna delle quali con il loro importo
*FDT* : CategoryImport
1. carica il file csv
2. contiene al suo interno la lista delle categorie
3. esegue i seguenti check
4. seleziona solo i wallet che contanto
5. verifica che le categorie con importo 0 siano tali
6. dividi tra #in e #out

## Data Hierarchy
*IN* : CategoryClass, che contiene tutti gli importi
*OUT* : CategoryClass: popola anche gli importi totali 
*FDT" : 

# Data
