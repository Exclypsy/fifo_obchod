
# Simulácia obchodu s **Dynamickým FIFO** radom pri pokladni

Tento projekt simuluje správanie zákazníkov v obchode počas otváracích hodín so zameraním na **dynamický FIFO (First-In, First-Out) rad pri pokladni**.  
Cieľom simulácie je analyzovať dĺžku radu, dobu čakania zákazníkov a nečinnosť pokladne pri **neobmedzenej kapacite radu**.

---

## Obsah
- Použité dátové štruktúry
- **Dynamické FIFO** – First In, First Out
- Dôvody používania dynamického FIFO
- Implementácia **DynamicFIFO** v projekte
- Simulácia zákazníkov
- Ukážky z behu programu
- Zhrnutie – vlastné slová

---

## Použité dátové štruktúry

V projekte sa používajú nasledovné dátové štruktúry:

- **DynamicFIFO** – **dynamický rad pri pokladni** (neobmedzená kapacita)  
- **Deque (`collections.deque`)** – efektívna implementácia s `maxlen=None`  
- **Zoznamy (`list`)** – evidencia zákazníkov  
- **Triedy a dátové triedy (`class`, `@dataclass`)** – objektový návrh  

---

## Dynamické FIFO – First In, First Out

**Dynamické FIFO** je vylepšená verzia klasického FIFO:

```
 PRVÁ ZMENA: Neobmedzená kapacita radu
 DRUHÁ ZMENA: Vždy úspešné vloženie (vracia True)
 TRETIA ZMENA: Automatické rozširovanie podľa potreby
```

<img width="4202" height="2139" alt="Dynamic FIFO" src="https://github.com/user-attachments/assets/424ea9fa-226e-427f-82fc-76467a24b0a1" />

**Dynamické FIFO** presne modeluje **reálny rad bez obmedzenia počtu ľudí**.

---

## Dôvody používania dynamického FIFO

```
 Žiadne odrádzanie zákazníkov
 Realistické správanie obchodu
 Automatické prispôsobenie zaťaženiu
 Konštantná časová zložitosť O(1)
 Jednoduché rozšírenie na ďalšie scenáre
 Lepšie štatistiky maximálnej dĺžky radu
```

---

## Implementácia **DynamicFIFO** v projekte

**DynamicFIFO** je implementovaný vlastnou triedou, ktorá **interné využíva `deque(maxlen=None)`**.

---

### Trieda Uzol (zachovaná pre kompatibilitu)

```python
class Uzol:
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return f"Uzol({self.data})"
```

---

### Inicializácia **dynamického FIFO**

```python
class DynamicFIFO:
    def __init__(self, init_velkost: int = 10):
        self.buffer = deque(maxlen=None)  # ← KLÚČOVÁ ZMENA
        self.hlava = None
        self.chvost = None
        self.init_velkost = init_velkost
        self.aktualna_velkost = 0         # ← SLEDOVANIE VEĽKOSTI
```

**`maxlen=None`** = **neobmedzená kapacita**.

---

### Vkladanie prvkov – **VŽDY ÚSPEŠNÉ**

```python
def vloz(self, prvok):
    # Žiadne obmedzenie kapacity!
    uzol = Uzol(prvok)
    self.buffer.append(uzol)
    self.aktualna_velkost = len(self.buffer)  # Aktualizácia
    # ... udržiavanie hlava/chvost
    return True  # ← VŽDY True
```

**Zákazník sa NIKDY neodradí.**

---

### Odoberanie prvkov z dynamického FIFO

```python
def vyber(self):
    if len(self.buffer) == 0:
        return None
    uzol = self.buffer.popleft()  # O(1) efektivita
    self.aktualna_velkost = len(self.buffer)
    # ... aktualizácia hlava/chvost
    return uzol.data
```

---

### Nové sledovanie dynamického správania

```python
def __repr__(self):
    return f"DynamicFIFO(dlzka={self.dlzka()}, init_velkost={self.init_velkost})"

# Pridané do logov:
if self.rad_pokladna.aktualna_velkost > 1000:
    self.pridaj_log(f"*** DYNAMICKÉ ROZŠÍRENIE RADU nad 1000! ***")
```

---

### Použitie v simulácii

```python
# ZMENENÉ:
self.rad_pokladna = DynamicFIFO(init_velkost=1000)

# VŽDY úspešné vloženie:
uspech = self.rad_pokladna.vloz(c)  # Vždy True
dalsi = self.rad_pokladna.vyber()
```

---

## Simulácia zákazníkov

**Žiadne zmeny** v modelovaní zákazníkov:
- čas príchodu  
- doba nakupovania  
- čas vstupu do radu  
- doba spracovania pri pokladni  

**Jedna veľká zmena**: **Všetci zákazníci sú obslúžení** (žiadne odrádzanie).

---

## Ukážky z behu programu

```
[T=125 s] VSTUP DO RADU zakaznika #15
*** Dĺžka radu: 1005 | Nečinnosť pokladne: 45 s ***
*** DYNAMICKÉ ROZŠÍRENIE RADU nad 1000! Aktuálna veľkosť: 1005 ***

KONIEC SIMULÁCIE - FINÁLNA ŠTATISTIKA (DYNAMICKÁ FIFO)
Maximálna dĺžka radu pri pokladni: 1247 ľudí
Finálna veľkosť dynamickej FIFO: 823
```

**Nový stĺpec v štatistikách**: `Fin.rád` (finálna veľkosť radu).

---

## Porovnanie so statickým FIFO:
```
Statické FIFO: Max. rad 1000 | Odráža zákazníkov
Dynamické FIFO: Max. rad 1247 | Všetci obslúžení
```
```

## Hlavné zmeny oproti pôvodnému README:

✅ **DynamicFIFO** namiesto statického FIFO  
✅ Zvýraznené **3 kľúčové zmeny**  
✅ Nové logy a štatistiky  
✅ Porovnanie so statickým riešením  
✅ **Vždy úspešné vloženie**  
✅ **`maxlen=None`** ako hlavná zmena  
✅ **Finálna veľkosť radu** v tabuľke  

README je **plne prispôsobené dynamickému FIFO** a hotové na použitie!
```
## Zhrnutie – vlastné slová
