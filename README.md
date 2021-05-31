# Shifts Cucinone

## Summary
Questo Repository contiene il codice utilizzato per poter generare i turni di pulizia del Cucinone.

## Avviare il programma 
Per avviare il programma bisogna seguire i seguenti step:
- Inserire un file .csv con i Nomi ed i parametri appropriati (tale CSV non è caricato nel repository poiché in costante aggiornamento)
- Eseguire lo script main.py da linea di comando fornendo i seguenti parametri
  - Anno attuale (in formato YYYY, e.g 2021)
  - Mese di cui generare i turni (in formato M, e.g. 6 indica Giugno)
  - Il pattern dei turni (in formato DayName-NumberOfPerson;DayName-NumberOfPerson, e.g. Wed-2;Sun-3 crea per ogni settimana un turno doppio il mercoledì ed un triplo la domenica)

**N.B. Possono essere generati solamente due tipologie di turni (light and heavy). Momentaneamente, non esiste una definizione di turno medio**

Il file csv si aggiornerà in automatico, contando il numero di turni fatti per ogni Utente e gli eventuali punitivi scontati. Un file txt rappresentante la tabella in LaTex verrà generata, così da consentire la realizzazione istantanea di una tabella utilizzando OverLeaf

## Logica
I nomi degli Utenti vengono inseriti in una lista. Ogni utente viene ripetuto una sola volta.
In presenza di un utente con un numero di ammonizioni superiore ad 1, l'utente verrà aggiunto n volte. Il valore n viene estratto da una serie convergente. Nello specifico, per ogni ammonizione bisogna scontare un turno punitivo. Ogni volta che il numero delle ammonizioni supera un multiplo di tre, ad ogni ammonizione il numero dei turni da scontare aumenta di 1 rispetto a quelli precendenti. La logica finale, dunque, viene qui rappresentata:

```
multiplier = int(punitive / 3) + 1
position = punitive % 3 + 1
amount_of_shifts = 1

while multiplier != 0:
  amount_of_shifts = amount_of_shifts + (multiplier * position)
  multiplier -= 1
  position = 3
```

Gli utenti vengono dunque estratti dalla lista ottenuta. Chi ha un numero di ammonizioni maggiore compare molteplici volte nella lista, aumentando in tal modo le probabilità di essere estratto. Prima di effettuare l'estrazione, la lista viene mischiata.

## Miglioramenti
Per suggerimenti e miglioramenti nel codice potete aprire un issue o potete diventare dei contributors sottomettendo delle PR
