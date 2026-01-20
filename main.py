from collections import deque
from dataclasses import dataclass
from typing import List
import random
import time as time_module


class Uzol:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"Uzol({self.data})"


class FIFO:
    def __init__(self, velkost: int):
        self.buffer = deque(maxlen=velkost)
        self.hlava = None
        self.chvost = None
        self.max_velkost = velkost

    def vloz(self, prvok):
        if len(self.buffer) >= self.max_velkost:
            return False
        uzol = Uzol(prvok)
        self.buffer.append(uzol)
        if self.chvost is None:
            self.hlava = uzol
            self.chvost = uzol
        else:
            self.chvost = uzol
        return True

    def vyber(self):
        if len(self.buffer) == 0:
            return None
        uzol = self.buffer.popleft()
        self.hlava = self.buffer[0] if len(self.buffer) > 0 else None
        if len(self.buffer) == 0:
            self.chvost = None
        return uzol.data

    def dlzka(self) -> int:
        return len(self.buffer)

    def je_prazdny(self) -> bool:
        return len(self.buffer) == 0

    def pozri(self):
        if len(self.buffer) == 0:
            return None
        return self.buffer[0].data

    def __repr__(self):
        return f"FIFO(dlzka={self.dlzka()}, max_velkost={self.max_velkost})"


@dataclass
class Zakaznik:
    id: int
    cas_prichodu: float
    trvanie_nakupovania: float
    trvanie_spracovania: float
    koniec_nakupovania: float
    cas_zaciatku_radu: float = None
    koniec_spracovania: float = None

    def __repr__(self):
        return f"Zakaznik(id={self.id}, prichod={self.cas_prichodu:.1f}s)"


class SimulaciaObchodu:
    def __init__(self, cislo_studenta: int = 15, otvaracie_hodiny: float = 8.0):
        self.cislo_studenta = cislo_studenta
        self.otvaracie_hodiny = otvaracie_hodiny
        self.celkovy_cas = otvaracie_hodiny * 3600
        self.sucasny_cas = 0.0
        self.mierka = 100

        self.rad_pokladna = FIFO(velkost=1000)
        self.zakaznici: List[Zakaznik] = []
        self.zakaznici_v_obchode: List[Zakaznik] = []

        self.celkova_neinnost = 0.0
        self.pokladna_zaneprazdna_do = 0.0
        self.max_cakanie = 0.0
        self.max_dlzka_radu = 0
        self.zakaznici_obsluzeni = 0

        self.logy = []

    def pridaj_log(self, sprava: str):
        self.logy.append(sprava)
        print(sprava)

    def vygeneruj_zakaznikov(self):
        self.zakaznici = []
        id_zakaznika = 1
        posledny_prichod = 0.0

        while True:
            interval_prichodu = 5 + random.randint(0, 25 + self.cislo_studenta)
            cas_prichodu = posledny_prichod + interval_prichodu

            if cas_prichodu > self.celkovy_cas:
                break

            trvanie_nakupovania = 1 + random.randint(0, 10 + self.cislo_studenta)
            trvanie_spracovania = 0.3 + trvanie_nakupovania / 20
            koniec_nakupovania = cas_prichodu + trvanie_nakupovania * 60

            zakaznik = Zakaznik(
                id=id_zakaznika,
                cas_prichodu=cas_prichodu,
                trvanie_nakupovania=trvanie_nakupovania,
                trvanie_spracovania=trvanie_spracovania,
                koniec_nakupovania=koniec_nakupovania
            )

            self.zakaznici.append(zakaznik)
            posledny_prichod = cas_prichodu
            id_zakaznika += 1

    def zoznam_zakaznikov_na_rad(self, cas: float) -> List[Zakaznik]:
        zoznam = []
        for zakaznik in self.zakaznici_v_obchode:
            if (zakaznik.koniec_nakupovania <= cas and
                    zakaznik.cas_zaciatku_radu is None and
                    zakaznik.koniec_spracovania is None):
                zoznam.append(zakaznik)
        return zoznam

    def je_pokladna_volna(self, cas: float) -> bool:
        return self.pokladna_zaneprazdna_do <= cas

    def vypis_stav(self, typ_udalosti: str = ""):
        dlzka_radu = self.rad_pokladna.dlzka()
        cas = self.sucasny_cas / self.mierka

        sprava = f"\n[T={cas:7.2f}s | {typ_udalosti:15} | Rad: {dlzka_radu:3d} | Nečinnosť: {self.celkova_neinnost:8.2f}s]"
        self.pridaj_log(sprava)

    def spusti(self) -> dict:
        self.logy = []
        self.pridaj_log("=" * 100)
        self.pridaj_log("SIMULÁCIA NÁKUPU V OBCHODE")
        self.pridaj_log(f"Poradové číslo študenta: {self.cislo_studenta}")
        self.pridaj_log(f"Doba prevádzky: {self.otvaracie_hodiny} hodín ({self.celkovy_cas}s)")
        self.pridaj_log(f"Zrýchlenie: {self.mierka}x")
        self.pridaj_log("=" * 100)

        self.vygeneruj_zakaznikov()
        self.pridaj_log(f"\nGenerovaných zakaznikov: {len(self.zakaznici)}")

        udalosti = []
        for zakaznik in self.zakaznici:
            udalosti.append((zakaznik.cas_prichodu, "prichod", zakaznik))
            udalosti.append((zakaznik.koniec_nakupovania, "koniec_nakupovania", zakaznik))

        udalosti.sort(key=lambda x: x[0])

        self.sucasny_cas = 0.0
        index_udalosti = 0
        pocet_riadkov = 0
        max_riadkov = 50

        self.pridaj_log(f"\n{'=' * 100}")
        self.pridaj_log("ZAČIATOK SIMULÁCIE")
        self.pridaj_log(f"{'=' * 100}\n")

        while index_udalosti < len(udalosti) and self.sucasny_cas <= self.celkovy_cas:
            cas_udalosti, typ_udalosti, zakaznik = udalosti[index_udalosti]

            if cas_udalosti > self.celkovy_cas:
                break

            self.sucasny_cas = cas_udalosti

            if typ_udalosti == "prichod":
                self.zakaznici_v_obchode.append(zakaznik)
                cas = self.sucasny_cas / self.mierka
                self.pridaj_log(f"\n[T={cas:7.2f}s] PRÍCHOD zakaznika #{zakaznik.id}")
                self.pridaj_log(
                    f"  Čas príchodu: {cas:.2f}s | Nakupovanie: {zakaznik.trvanie_nakupovania}min | Pokladňa: {zakaznik.trvanie_spracovania:.2f}min")
                pocet_riadkov += 3

            elif typ_udalosti == "koniec_nakupovania":
                zoznam = [c for c in self.zakaznici_v_obchode
                          if c.koniec_nakupovania <= self.sucasny_cas
                          and c.cas_zaciatku_radu is None
                          and c.koniec_spracovania is None]

                for c in zoznam:
                    c.cas_zaciatku_radu = self.sucasny_cas
                    self.rad_pokladna.vloz(c)

                    cas = self.sucasny_cas / self.mierka
                    self.pridaj_log(f"\n[T={cas:7.2f}s] VSTUP DO RADU zakaznika #{c.id}")
                    self.pridaj_log(
                        f"  Čas príchodu do obchodu: {c.cas_prichodu / self.mierka:.2f}s | Čas nakupovania: {c.trvanie_nakupovania}min | Čas spracovania: {c.trvanie_spracovania:.2f}min")
                    self.pridaj_log(
                        f"  *** Dĺžka radu: {self.rad_pokladna.dlzka()} | Nečinnosť pokladne: {self.celkova_neinnost:.2f}s ***")
                    pocet_riadkov += 4

                    if self.rad_pokladna.dlzka() > self.max_dlzka_radu:
                        self.max_dlzka_radu = self.rad_pokladna.dlzka()
                        self.pridaj_log(f"  !!! NOVÁ MAXIMÁLNA DĹŽKA RADU: {self.max_dlzka_radu}")
                        pocet_riadkov += 1

            index_udalosti += 1

            if self.je_pokladna_volna(self.sucasny_cas) and not self.rad_pokladna.je_prazdny():
                dalsi = self.rad_pokladna.vyber()
                cakanie = self.sucasny_cas - dalsi.cas_zaciatku_radu
                koniec_spracovania = self.sucasny_cas + dalsi.trvanie_spracovania * 60
                dalsi.koniec_spracovania = koniec_spracovania
                self.pokladna_zaneprazdna_do = koniec_spracovania
                self.zakaznici_obsluzeni += 1

                cas = self.sucasny_cas / self.mierka
                cakanie = cakanie / self.mierka
                spracovanie = dalsi.trvanie_spracovania

                self.pridaj_log(f"\n[T={cas:7.2f}s] ZAPLATENIE zakaznika #{dalsi.id}")
                self.pridaj_log(
                    f"  Čakanie v rade: {cakanie:.2f}s | Doba spracovania: {spracovanie:.2f}min")
                self.pridaj_log(
                    f"  *** Dĺžka radu: {self.rad_pokladna.dlzka()} | Nečinnosť pokladne: {self.celkova_neinnost:.2f}s ***")
                pocet_riadkov += 4

                if cakanie > self.max_cakanie:
                    self.max_cakanie = cakanie
                    self.pridaj_log(
                        f"  !!! NOVÁ MAXIMÁLNA DOBA ČAKANIA V RADE: {self.max_cakanie:.2f}s")
                    pocet_riadkov += 1

            if self.je_pokladna_volna(self.sucasny_cas) and self.rad_pokladna.je_prazdny():
                zaciatok_neinnosti = self.sucasny_cas
                nasledujuci_cas = float('inf')
                for t, _, _ in udalosti[index_udalosti:]:
                    if t > self.sucasny_cas:
                        nasledujuci_cas = t
                        break
                if nasledujuci_cas < float('inf'):
                    trvanie_neinnosti = nasledujuci_cas - self.sucasny_cas
                    self.celkova_neinnost += trvanie_neinnosti

            if pocet_riadkov > max_riadkov:
                self.pridaj_log(f"\n{'=' * 100}")
                self.pridaj_log("SCREENSHOT 1 - PRVÉ VYPLNENIE OBRAZOVKY")
                self.pridaj_log(f"{'=' * 100}\n")
                pocet_riadkov = 0

        self.pridaj_log(f"\n{'=' * 100}")
        self.pridaj_log("KONIEC SIMULÁCIE - FINÁLNA ŠTATISTIKA")
        self.pridaj_log(f"{'=' * 100}")
        self.pridaj_log(f"Celkový počet ľudí v obchode: {len(self.zakaznici)}")
        self.pridaj_log(f"Obslúžení zakazníci: {self.zakaznici_obsluzeni}")
        self.pridaj_log(f"Maximálna dĺžka radu pri pokladni: {self.max_dlzka_radu} ľudí")
        self.pridaj_log(f"Maximálna doba čakania v rade: {self.max_cakanie:.2f} sekúnd")
        self.pridaj_log(f"Celková nečinnosť pokladne: {self.celkova_neinnost:.2f} sekúnd")
        self.pridaj_log(f"{'=' * 100}\n")

        return {
            "celkovy_pocet": len(self.zakaznici),
            "max_cakanie": self.max_cakanie,
            "max_dlzka_radu": self.max_dlzka_radu,
            "celkova_neinnost": self.celkova_neinnost,
            "zakaznici_obsluzeni": self.zakaznici_obsluzeni
        }


def main():
    CISLO_STUDENTA = 2

    print("\n" + "=" * 100)
    print("SIMULÁCIA OBCHODU S FIFO RADOM PRI POKLADNI")
    print("=" * 100)
    print(f"Poradové číslo študenta: {CISLO_STUDENTA}")
    print(f"Doba simulácie: 8 hodín (zrýchľovaná 100x)")
    print(f"Počet spustení: 5")
    print("=" * 100 + "\n")

    vysledky = []

    for cislo in range(1, 6):
        print(f"\n{'*' * 100}")
        print(f"SPUSTENIE #{cislo}")
        print(f"{'*' * 100}\n")

        simulacia = SimulaciaObchodu(cislo_studenta=CISLO_STUDENTA, otvaracie_hodiny=8.0)
        vysledok = simulacia.spusti()
        vysledky.append(vysledok)

        log_subor = f"simulation_run_{cislo}.log"
        with open(log_subor, 'w', encoding='utf-8') as f:
            f.write('\n'.join(simulacia.logy))

        print(f"\nLogy uložené do: {log_subor}")

        time_module.sleep(1)

    print("\n" + "=" * 100)
    print("VÝSLEDKY VŠETKÝCH 5 SPUSTENÍ")
    print("=" * 100)
    print(f"{'Spustenie':<12} {'Počet ľudí':<15} {'Max čakanie(s)':<18} {'Max dĺžka radu':<18} {'Nečinnosť(s)':<15}")
    print("-" * 100)

    for i, vysledok in enumerate(vysledky, 1):
        print(
            f"Spustenie {i:<4} {vysledok['celkovy_pocet']:<15} {vysledok['max_cakanie']:<18.2f} {vysledok['max_dlzka_radu']:<18} {vysledok['celkova_neinnost']:<15.2f}")

    priemer_ludi = sum(r['celkovy_pocet'] for r in vysledky) / len(vysledky)
    priemer_cakanie = sum(r['max_cakanie'] for r in vysledky) / len(vysledky)
    priemer_rad = sum(r['max_dlzka_radu'] for r in vysledky) / len(vysledky)
    priemer_neinnost = sum(r['celkova_neinnost'] for r in vysledky) / len(vysledky)

    print("-" * 100)
    print(f"{'PRIEMER':<12} {priemer_ludi:<15.2f} {priemer_cakanie:<18.2f} {priemer_rad:<18.2f} {priemer_neinnost:<15.2f}")
    print("=" * 100 + "\n")


if __name__ == "__main__":
    main()
