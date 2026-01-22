# Simulácia obchodu s FIFO radom pri pokladni

Tento projekt simuluje správanie zákazníkov v obchode počas otváracích hodín so zameraním na **FIFO (First-In, First-Out) rad pri pokladni**.  
Cieľom simulácie je analyzovať dĺžku radu, dobu čakania zákazníkov a nečinnosť pokladne.

---

## Obsah
- Použité dátové štruktúry
- FIFO – First In, First Out
- Dôvody používania FIFO
- Implementácia FIFO v projekte
- Simulácia zákazníkov
- Ukážky z behu programu
- Zhrnutie – vlastné slová

---

## Použité dátové štruktúry

V projekte sa používajú nasledovné dátové štruktúry:

- **FIFO (queue)** – modelovanie radu pri pokladni  
- **Deque (`collections.deque`)** – efektívna implementácia FIFO  
- **Zoznamy (`list`)** – evidencia zákazníkov  
- **Triedy a dátové triedy (`class`, `@dataclass`)** – objektový návrh riešenia  

---

## FIFO – First In, First Out

FIFO (First-In, First-Out) je dátová štruktúra, v ktorej platí:

- prvok, ktorý vstúpi ako prvý, je spracovaný ako prvý  
- vkladanie prebieha na koniec radu  
- odoberanie prebieha zo začiatku radu

<img width="4202" height="2139" alt="image" src="https://github.com/user-attachments/assets/424ea9fa-226e-427f-82fc-76467a24b0a1" />


FIFO presne zodpovedá správaniu **reálneho radu ľudí pri pokladni**.

---

## Dôvody používania FIFO

Použitie FIFO v simulácii má viacero výhod:

- spravodlivé obsluhovanie zákazníkov  
- jednoduchá a prehľadná implementácia  
- realistický model reálneho sveta  
- konštantná časová zložitosť operácií  
- dobrá čitateľnosť a rozšíriteľnosť kódu  

---

## Implementácia FIFO v projekte

FIFO rad je v projekte implementovaný vlastnou triedou `FIFO`, ktorá interne využíva dátovú štruktúru `deque`.  
Každý prvok v rade je zapuzdrený triedou `Uzol`.

---

### Trieda Uzol

```python
class Uzol:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"Uzol({self.data})"
```
Trieda reprezentuje jeden prvok FIFO radu a uchováva objekt zákazníka.

---

### Inicializácia FIFO radu

```python
class FIFO:
    def __init__(self, velkost: int):
        self.buffer = deque(maxlen=velkost)
        self.hlava = None
        self.chvost = None
        self.max_velkost = velkost
```
FIFO má definovanú maximálnu kapacitu a uchováva si referencie na hlavu a chvost radu.

---

### Vkladanie prvkov do FIFO

```python
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
```
Zákazník je vložený na koniec radu v správnom poradí.

---

### Odoberanie prvkov z FIFO

```python
def vyber(self):
    if len(self.buffer) == 0:
        return None
    uzol = self.buffer.popleft()
    self.hlava = self.buffer[0] if len(self.buffer) > 0 else None
    if len(self.buffer) == 0:
        self.chvost = None
    return uzol.data
```
Zákazník je obslúžený zo začiatku radu.

---

### Pomocné metódy FIFO

```python
def dlzka(self) -> int:
    return len(self.buffer)

def je_prazdny(self) -> bool:
    return len(self.buffer) == 0

def pozri(self):
    if len(self.buffer) == 0:
        return None
    return self.buffer[0].data
```

---

### Použitie FIFO v simulácii

```python
self.rad_pokladna = FIFO(velkost=1000)
self.rad_pokladna.vloz(c)
dalsi = self.rad_pokladna.vyber()
```

FIFO rad reprezentuje rad pri pokladni.

---

## Simulácia zákazníkov

Každý zákazník je reprezentovaný triedou `Zakaznik` a má:

- čas príchodu  
- dobu nakupovania  
- čas vstupu do radu  
- dobu spracovania pri pokladni  
- čas ukončenia obsluhy  

Simulácia prebieha ako diskrétna udalosťová simulácia.

---

## Ukážky z behu programu

- príchod zákazníka
<img width="490" height="54" alt="Screenshot 2026-01-22 at 19 19 13" src="https://github.com/user-attachments/assets/0e75dfe6-4c95-4b5e-acf2-263b9200015c" />

- vstup do radu
<img width="669" height="84" alt="Screenshot 2026-01-22 at 19 19 18" src="https://github.com/user-attachments/assets/989d712c-2785-450f-b3d5-7efc9e2fc026" />

- finálna štatistika
<img width="793" height="202" alt="Screenshot 2026-01-22 at 19 18 53" src="https://github.com/user-attachments/assets/3b0419a5-015b-4d73-a4ab-6c2f04a96ef6" />

- tabuľka priemerov 
<img width="790" height="285" alt="Screenshot 2026-01-22 at 19 17 26" src="https://github.com/user-attachments/assets/69404987-c662-45db-87e8-15878179363b" />

---

## Zhrnutie – vlastné slová


