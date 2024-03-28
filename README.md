# Shifts Cucinone

## Summary
Questo Repository contiene il codice utilizzato per poter generare i turni di pulizia del Cucinone.

## Avviare il programma 
Vedi guida.pdf nella release

**N.B. Possono essere generati solamente 3 tipologie di turni (light, heavy e hood). Momentaneamente, non esiste una definizione di turno medio.**

Il file csv si aggiornerà in automatico, contando il numero di turni fatti per ogni Utente e gli eventuali punitivi scontati. Un file txt rappresentante la tabella in LaTex verrà generato, sarà sufficiente copiarne il contenuto su un interprete Latex (Heroku, Overleaf, ecc...).

## Logica di estrazione

### Turno cappa
Generazione e rispettiva estrazione da lista ammoniti, lista persone con punteggio basso e lista persone con punteggio alto. Tutte le liste vengono popolate esclusivamente da persone disponibili per la data del turno.

### Turni normali (doppi e tripli)
Per ogni data prevista (non inclusa nel file "./database/exception_dates_list.txt")
1) Ricalcola la soglia di riferimento punteggi, per discriminare le persone con punteggio basso da quello alto
2) Rigenera le liste delle persone a punteggio-basso e punteggio-alto, tenendo conto delle date di assenza
3) Se non vuota, estrai persone dalla lista degli ammoniti, poi procedi per punteggio-basso, infine per punteggio alto; se non ci sono abbastanza persone disponibili per questa data, inserisci un utente fittizio "--da nominare--", in modo che i responsabili della cucina valutino se trovare sostituti oppure rimuovere eventualmente la data del turno
4) Aggiorna i punteggi (ed eventualmente decrementa ammonizioni) delle persone estratte


## Miglioramenti
Per suggerimenti e miglioramenti nel codice potete aprire un issue o potete diventare dei contributors sottomettendo delle PR.
