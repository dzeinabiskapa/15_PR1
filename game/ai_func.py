from collections import Counter
class AiFunc:
    def _evaluate(self, node, isMaximizing): # heiristiskā funkcija
        delta = node.scores[1] - node.scores[0] # punktu starpības komponente (AI - cilvēks)

        # invertēta vērtība priekš cilvēka gājiena (cilvēks - AI)
        if not isMaximizing:
            delta = -delta
    
        # heiristiskie faktori
        # skaitļa 4 esamība (augstākā prioritāte)
        fourExists = 4 in node.sequence # pārbaudam vai virknē eksistē 4
        aN4 = 1 if fourExists else 0 # 1, ja eksistē, 0 savādāk

        # skaitļa 3 esamība (vidēja prioritāte)
        # ņem vērā tikai, ja nav 4 (lai neuzkrātu bonusus par abiem)
        threeExists = 3 in node.sequence and not fourExists
        aN3 = 1 if threeExists else 0

        # skaitļa 2 esamība (zemāka prioritāte)
        # ņem vērā tikai ja nav augstāku skaitļu
        twoExists = 2 in node.sequence and not (threeExists or fourExists)
        aN2 = 1 if twoExists else 0
    
        # pievienojam svarus klāt heiristiskiem faktoriem un iegūstam heiristiskās funkcijas rezultāt vērtību
        fN = delta + 0.5 * aN4 + 0.4 * aN3 + 0.2 * aN2
        return fN

    def _getMoveFromChild(self, parent, child): # gājiena noteikšana salīdzinot vecāku un bērnu
        # skaitļu biežuma analīze
        parentCounts = Counter(parent.sequence) # skaitļu daudzums sākotnējā stāvoklī
        childCounts = Counter(child.sequence) # skaitļu daudzums pēc gājiena
    
        # skaitļa paņemšanas gājiena noteikšana
        # meklējam skaitli, kurš vairs nav virknē
        for num in parentCounts:
            if parentCounts[num] == childCounts[num] + 1: # paņemšanas gadījumā bērna virkne būs par 1 īsāka
                # atrodam precīzu pozīciju, kur skaitlis tika noņemts
                for i in range(len(parent.sequence)):
                    # pārbaudam vai pozīcijā ir izmaiņas
                    # pozīcija ir ārpus bērna virknes robežām, t.i., paņemts pēdējais skaitlis
                    # vai elementi šajā pozīcijā atšķiras, t.i., paņemts virknes vidū skaitlis
                    # pat ja virknē ir trīs vienādi skaitļi viens no šiem diviem kritērijiem izpildīsies ejot cauri virknei
                    # mums nav starpības, kuru no trim vienādajiem skaitļiem kods uzskata par paņemtu
                    if i >= len(child.sequence) or parent.sequence[i] != child.sequence[i]:
                        if parent.sequence[i] == num:
                            return ("take", i) # atgriežam gājiena tipu un precīzu indeksu
    
        # skaitļa dalīšanas gājiena noteikšana
        # 2 sadalīšana
        # ja "1" skaits palielinājās par 2 un "2" skaits samazinājās par 1
        if childCounts[1] == parentCounts[1] + 2 and childCounts[2] == parentCounts[2] - 1:
            # meklējam, kuru divi mēs uzskatīsim par sadalītu
            for i, num in enumerate(parent.sequence):
                if num == 2:
                    return ("split", i)
        # 4 sadalīšana
        # ja "2" skaits palielinājās par 2 un "4" skaits samazinājās par 1
        elif childCounts[2] == parentCounts[2] + 2 and childCounts[4] == parentCounts[4] - 1:
            # meklējam, kuru četri mēs uzskatīsim par sadalītu
            for i, num in enumerate(parent.sequence):
                if num == 4:
                    return ("split", i)
    

        return None  # ja notiek kļūda tad vajag atgriezt None (drošības mehānisms, nevajadzētu nekad notikt)