# Shifts Cucinone

## Summary
Questo Repository contiene il codice utilizzato per poter generare i turni di pulizia del Cucinone.

## Avviare il programma 
Vedi file Guida.pdf

**N.B. Possono essere generati solamente tre tipologie di turni (light (doppio), heavy (triplo) o hood (cappa))**

Il file csv si aggiornerà in automatico, contando il numero di turni fatti per ogni Utente e gli eventuali punitivi scontati. Un file txt contenente i turni verrà generato, copiarne il contenuto, incollarlo su Overleaf e generare il PDF.


### Logica di estrazione
Viene prima di tutto definita una soglia calcolata come il rapporto tra la somma di tutti i turni fatti da ciascuna persona e il totale degli utenti.  
Gli utenti con score inferiore alla soglia, verranno inseriti all'interno di low_score_list.  
Gli utenti con score superiore alla soglia, verranno inseriti all'interno di high_score_list.  
Gli utenti con almeno una ammonizione ancora da scontare (campo remaining_admonitions > 0), verranno inseriti all'interno di admonished_list.  
Le 3 liste vengono mischiate e, in seguito, vengono prelevati i nomi degli utenti che devono svolgere il turno, secondo il seguente algoritmo di estrazione.


## Algoritmo di estrazione utenti (premessa)
L'algoritmo di estrazione degli utenti utilizza un approccio basato su paradigma Greedy, ovvero è in grado di considerare soltanto soluzioni localmente ottime: l'assegnazione dei turni non sarà sempre ottimale, perchè non esplora tutto lo spazio delle possibili soluzioni.

Esempio: John è disponibile il 5/12/ e il 7/12. Paul è l'unica persona disponibile il 7/12 (turno doppio).  
John viene assegnato il 5/12  
Paul viene assegnato il 7/12  
==> le assegnazioni non sono ottime, John poteva essere assegnato il 7/12  

## Algoritmo di estrazione utenti
```
# Mescola gli utenti delle 3 liste
randomize(admonished_list)
randomize(low_score_list)
randomize(high_score_list)

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

Nota: l'algoritmo è analogo per l'estrazione del turno di cappa, con la sola differenza che vengono prima pescati gli ammoniti, poi score basso e infine score alto.  
Nel caso in cui per una certa data non ci siano persone sufficienti, l'algoritmo lascia slot vuoti, passando a considerare la prossima data.  
Tale condizione può verificarsi per 2 motivi:  
1) Troppi utenti assenti per quella data  
2) Tutti gli utenti che sarebbero presenti per quella data sono già stati assegnati per altre date
```

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
