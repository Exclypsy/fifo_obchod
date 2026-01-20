# Simulácia obchodu s FIFO radom pri pokladni

Tento projekt simuluje správanie zákazníkov v obchode počas otváracích hodín so zameraním na **FIFO (First-In, First-Out) rad pri pokladni**.  
Cieľom simulácie je analyzovať dĺžku radu, dobu čakania zákazníkov a nečinnosť pokladne.

---

## Obsah
- [Použité dátové štruktúry](#použité-dátové-štruktúry)
- [FIFO – First In, First Out](#fifo--first-in-first-out)
- [Prečo používať FIFO](#prečo-používať-fifo)
- [Simulácia zákazníkov](#simulácia-zákazníkov)
- [Ukážky z behu programu](#ukážky-z-behu-programu)
- [Zhrnutie – vlastné slová](#zhrnutie--vlastné-slová)

---

## Použité dátové štruktúry

V projekte sa používajú nasledovné dátové štruktúry:

- **FIFO rad (queue)** – modelovanie radu pri pokladni
- **Zoznamy (`list`)** – evidencia zákazníkov v obchode
- **Deque (`collections.deque`)** – efektívna implementácia FIFO
- **Triedy a dátové triedy (`class`, `@dataclass`)** – reprezentácia zákazníka a simulácie

---

## FIFO – First In, First Out

FIFO (First-In, First-Out) je dátová štruktúra, kde:

- prvok, ktorý **vstúpi ako prvý**, je **spracovaný ako prvý**
- nové prvky sa **vkladajú na koniec**
- prvky sa **odoberajú zo začiatku**

V reálnom svete FIFO presne zodpovedá správaniu **radu ľudí pri pokladni**.

### Schéma FIFO radu

<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/f37ea3e3-898a-4db6-9cc0-30db5f44da00" />

---

## Implementácia FIFO v projekte

FIFO je implementované pomocou triedy `FIFO`, ktorá interne využíva `deque`.

Základné operácie:

- `vloz(prvok)` – vloženie zákazníka do radu
- `vyber()` – obslúženie zákazníka
- `dlzka()` – aktuálna dĺžka radu
- `je_prazdny()` – kontrola prázdneho radu
- `pozri()` – náhľad na prvý prvok

### Ilustrácia operácií FIFO

![FIFO operácie](images/fifo_operations.png)

---

## Prečo používať FIFO

Použitie FIFO v tejto simulácii má viacero výhod:

- ✅ **Spravodlivosť** – zákazníci sú obsluhovaní v poradí, v akom prišli
- ✅ **Jednoduchosť implementácie**
- ✅ **Realistický model reálneho sveta**
- ✅ **Predvídateľné správanie systému**
- ✅ **Efektívnosť** – `deque` umožňuje rýchle vkladanie a odoberanie prvkov

FIFO je preto ideálnou voľbou pre simuláciu radu pri pokladni.

---

## Simulácia zákazníkov

Každý zákazník je reprezentovaný triedou `Zakaznik`, ktorá obsahuje:

- identifikátor zákazníka
- čas príchodu do obchodu
- dobu nakupovania
- čas vstupu do radu
- dobu spracovania pri pokladni
- čas ukončenia obsluhy

Zákazníci:
1. prídu do obchodu
2. nakupujú určitý čas
3. vstúpia do FIFO radu
4. čakajú na obsluhu
5. zaplatia a odchádzajú

---

## Ukážky z behu programu

Nižšie sú uvedené ukážky výpisov zo simulácie.

### Príchod zákazníka

![Príchod zákazníka](images/prichod.png)

---

### Vstup zákazníka do radu

![Vstup do radu](images/rad.png)

---

### Obsluha pri pokladni

![Obsluha](images/obsluha.png)

---

### Finálna štatistika simulácie

![Štatistika](images/statistika.png)

---

## Zhrnutie – vlastné slová

*(Túto časť vyplní autor projektu vlastnými slovami.)*
