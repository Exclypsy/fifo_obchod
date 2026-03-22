# Implementácia zoznamu s operáciami (slovenské názvy premenných)

class MojZoznam:
    def __init__(self):
        self._prvky = []  # Interné uloženie prvkov

    def vypis_struktury(self):
        """Vytvorenie a výpis štruktúry zoznamu"""
        print("Štruktúra zoznamu:", self._prvky)
        return self._prvky.copy()

    def poskytni_hodnotu_podla_indexu(self, index):
        """Poskytnutie/Zmena hodnoty podľa indexu"""
        if 0 <= index < len(self._prvky):
            return self._prvky[index]
        return None

    def nastav_hodnotu_podla_indexu(self, index, nová_hodnota):
        """Zmena hodnoty podľa indexu"""
        if 0 <= index < len(self._prvky):
            self._prvky[index] = nová_hodnota
            return True
        return False

    def dlzka_zoznamu(self):
        """Zistenie dĺžky zoznamu"""
        return len(self._prvky)

    def poskytni_ukazovatel_podla_indexu(self, index):
        """Poskytnutie ukazovateľa podľa indexu (index je ukazovateľ)"""
        return index if 0 <= index < len(self._prvky) else None

    def poskytni_index_podla_hodnoty(self, hodnota):
        """Poskytnutie indexu podľa hodnoty (prvý výskyt)"""
        try:
            return self._prvky.index(hodnota)
        except ValueError:
            return None

    def pridaj_na_koniec(self, prvok):
        """Pridanie prvku na koniec"""
        self._prvky.append(prvok)

    def pridaj_na_zaciato(self, prvok):
        """Pridanie prvku na začiatok"""
        self._prvky.insert(0, prvok)

    def pridaj_podla_indexu(self, index, prvok):
        """Pridanie podľa indexu"""
        if 0 <= index <= len(self._prvky):
            self._prvky.insert(index, prvok)
            return True
        return False

    def pridaj_za_ukazovatel(self, index, prvok):
        """Pridanie za prvok podľa indexu/ukazovateľa"""
        return self.pridaj_podla_indexu(index + 1, prvok)

    def pridaj_pred_ukazovatel(self, index, prvok):
        """Pridanie pred prvok podľa indexu/ukazovateľa"""
        return self.pridaj_podla_indexu(index, prvok)

    def poskytni_ukazovatel_podla_hodnoty(self, hodnota):
        """Poskytnutie ukazovateľa podľa hodnoty"""
        return self.poskytni_index_podla_hodnoty(hodnota)

    def odstran_podla_indexu(self, index):
        """Odstránenie podľa indexu/ukazovateľa"""
        if 0 <= index < len(self._prvky):
            return self._prvky.pop(index)
        return None

    def odstran_podla_hodnoty(self, hodnota):
        """Odstránenie podľa hodnoty (prvý výskyt)"""
        index = self.poskytni_index_podla_hodnoty(hodnota)
        if index is not None:
            return self.odstran_podla_indexu(index)
        return None


# Demo použitia
if __name__ == "__main__":
    zoznam = MojZoznam()

    # Pridávanie prvkov
    zoznam.pridaj_na_koniec(10)
    zoznam.pridaj_na_zaciato(5)
    zoznam.pridaj_podla_indexu(1, 7)

    print("1. Výpis štruktúry:", end=" ")
    zoznam.vypis_struktury()

    print("2. Dĺžka zoznamu:", zoznam.dlzka_zoznamu())  # 3

    print("3. Hodnota na indexe 1:", zoznam.poskytni_hodnotu_podla_indexu(1))  # 7

    print("4. Index hodnoty 10:", zoznam.poskytni_index_podla_hodnoty(10))  # 2

    # Zmena hodnoty
    zoznam.nastav_hodnotu_podla_indexu(1, 8)

    print("5. Po zmene (index 1=8):", end=" ")
    zoznam.vypis_struktury()  # [5, 8, 10]

    # Pridanie za/pred
    zoznam.pridaj_za_ukazovatel(1, 9)
    print("6. Pridané za index 1:", end=" ")
    zoznam.vypis_struktury()  # [5, 8, 9, 10]

    # Odstránenie
    odstraneny = zoznam.odstran_podla_hodnoty(8)
    print("7. Odstránené 8:", odstraneny)
    print("8. Po odstránení:", end=" ")
    zoznam.vypis_struktury()  # [5, 9, 10]