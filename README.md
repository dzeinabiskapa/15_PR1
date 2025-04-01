# Ciparu spēle
### 15. grupa, PR1

## Spēles apraksts 
Spēles sākumā ir dota ģenerētā skaitļu virkne. Katram spēlētājam ir 0 punktu. Spēlētāji izpilda gājienus secīgi. Gājiena laikā spēlētājs: 
* var paņemt jebkuru skaitli no virknes un pieskaitīt to savam punktu skaitam;  
* sadalīt «2» divos skaitļos «1» un «1», bet par to neiegūt punktus; 
* sadalīt “4” divos skaitļos “2” un “2” un par to pieskaitīt savam punktu skaitam 1 punktu.

Spēle beidzas, kad virkne paliek tukša. Uzvar spēlētājs, kam ir vairāk punktu. Ja punktu skaits ir vienāds, tad rezultāts ir neizšķirts. 

## Projekta struktūra

```
.idea/
│-- .gitignore
│-- indexLayout.xml
│-- vcs.xml

game/
│-- ai_func.py            # Mākslīgā intelekta funkcijas
│-- alpha_beta_algo.py    # Alpha-Beta atzarošanas algoritms
│-- data_structurs.py     # Datu struktūras spēlei
│-- game_logic.py         # Spēles mehānikas un noteikumu ieviešana
│-- gui.py                # GUI ieviešana, izmantojot Tkinter
│-- main.py               # Programmas palaišanas fails
│-- minimax_algo.py       # Minimax algoritms MI darbībai
│-- LICENSE               # Licences fails
│-- README.md             # Projekta dokumentācija (šis fails)
```

## Lietošana

Lai sāktu spēli, palaidiet komandu:

```sh
python main.py
```

Sekojiet ekrānā redzamajām instrukcijām, lai spēlētu spēli.

## Licence

Šis projekts ir licencēts ar MIT licenci. Jūs varat to brīvi modificēt un izplatīt.

