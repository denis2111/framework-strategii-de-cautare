# Framework pentru strategii de căutare

* Dispune de implementări configurabile cel puțin pentru toate strategiile (informate și neinformate) menţionate la curs;
* Permite folosirea unei funcții de scor implementată de utilizator cu o strategie disponibilă fără ca utilizatorul să editeze codul sursă al framework-ului;
* Permite selectarea unei probleme predefinite și a unei strategii disponibile (eventual configurarea ei), procesul de căutare va putea fi vizualizat de utilizator în interfața framework-ului;
* Procesul de căutare poate fi generat și sub forma unui document extern framework-ului (secvența de stări încercate, deciziile luate de strategie, eventuale scoruri date de euristici, stări memorate la fiecare pas)


# Scenariu de utilizare
  Aplicatia rezolva probleme de cautare folosind doua tipuri de algoritmi(informati si neinformati), dintre cei informati utilizatorul poate alege dintre: Hill Climbing,
  Greedy, Simulated Annealing, A*, iar dintre cei neinformati: BKT, DFS, BFS, Bidirectional, Random. 
  Totodata oferim utilizatorului posibilitatea de a-si configura propria functie de scor pentru algoritmii informati si sa faca export la datele solutiei.
  
  In aplicatia noastra poti testa algoritmii pe doua problema de cautare diferite(Maze si Hanoi)
  
  - Maze
    
    Aici se pot configura dimensiunea labirintului cu obstacole, punctul de start, punctul de final, poti alege un algoritm si in functie de acesta apar alte optiuni. 
    
  - Hanoi
    
    Pentru Hanoi se pot configura numarul de piese, numarul de turnuri si pozitia de start. De asemenea poti alege un tip de algoritm.   
    
# Dependente
  Trebuie instalata libraria mpmath (comanda: "pip install mpmath")


# Distributia echipei:
  La inceput am avut o intalnire in care toti am discutat despre arhitectura aplicatie, la urmatoarea intalnire, am inceput sa o dezvoltam.
  Banu Denis s-a ocupat de partea de algoritmi
  Filimon Raluca si Simion Andra s-au ocupat de reprezeentarea problemei Maze si baza interfetei grafice
  Popa Andrei si Avram Andrei s-au ocupat de reprezentarea problemei Hanoi

# Echipa
* Avram Andrei-George
* Banu Denis-Andrei
* Filimon Raluca-Elena
* Popa Andrei
* Simion Andra
