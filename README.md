# Shifts Cucinone

## Summary
Questo Repository contiene il codice utilizzato per poter generare i turni di pulizia del Cucinone.

## Avviare il programma 
Vedi file Guida.pdf

**N.B. Possono essere generati solamente tre tipologie di turni (light (doppio), heavy (triplo) or hood (cappa))**

Il file csv si aggiornerà in automatico, contando il numero di turni fatti per ogni Utente e gli eventuali punitivi scontati (solo nel caso si adotti il calcolo dei turni con ammonizione). Un file txt contenente i turni verrà generato, copiarne il contenuto, incollarlo su Overleaf e generare il PDF.

## Algoritmo di estrazione utenti (premessa)
L'algoritmo di estrazione degli utenti utilizza un approccio basato su paradigma Greedy, ovvero è in grado di considerare soltanto soluzioni localmente ottime: l'assegnazione dei turni non sarà sempre ottimale, perchè non esplora tutto lo spazio delle possibili soluzioni.

Esempio: John è disponibile il 5/12/ e il 7/12. Paul è l'unica persona disponibile il 7/12 (turno doppio).
John viene assegnato il 5/12
Paul viene assegnato il 7/12
==> le assegnazioni non sono ottime, John poteva essere assegnato il 7/12

## Algoritmo di estrazione utenti
```
Per ogni data di turno prevista:
    Seleziona tutte le persone disponibili per tale data
    Identifica utenti a score basso, score alto e ammoniti e inseriscili in 3 liste separate
    
    Fintanto che servono persone per quel turno:
        Se ci sono ancora persone con score basso:
            Estrai una persona con score basso
        Altrimenti se ci sono ancora persone con ammonizioni da scontare:
            Estrai una persona ammonita
        Altrimenti se ci sono ancora persone con score alto:
            Estrai una persona con score alto
        Altrimenti:
            Non ci sono abbastanza persone disponibili per quella data, passa alla data successiva

```

### ------------- Da rivedere --------------

### Logica con ammonizioni
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

### Logica con threshold
Viene definita una soglia calcolata come il rapporto tra la somma di tutti i turni fatti da ciascuna persona e il totale degli utenti.
Nella generazione dei turni, gli utenti che si trovano al di sotto della soglia verranno inseriti all'interno di una lista.
La lista viene mischiata e, in seguito, vengono prelevati i nomi degli utenti che devono svolgere il turno.
Se tale lista si esaurisce prima di aver completato l'elenco dei turni del mese vengono presi gli utenti al di sopra della soglia e vengono inseriti in una lista. In seguito, gli utenti verranno estratti per completare i turni di pulizia rimanenti.

## What's new
* Added user's availability field management
* Added hood shift management (introduced by Cucinone meeting in October 2022)
* Added punitive shifts fields
* Added remaining_admonition field
* Changes to admonitions management
* Added swap users shifts feature (swap 2 users in the current month or take a replacement from the whole users list)
* Heavy changes to users extraction algorithm
* Added console user menu (made as much user friendly as I could :D)
* Added add/remove user features
* Added clear all user data feature (must only be called at the end of the academic year)
* Fixed and improved latex file export, added exception_dates_list.txt management
* Added automatic backup of users.csv before shifts generation
* Changes to shifts weights (light=2, heavy=3, hood=6, punitive=0)
