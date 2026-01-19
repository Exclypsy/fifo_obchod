"""
FIFO Queue Simulator - Nákupná simulácia v obchode
Autor: Simulátor obchodu
Dátum: 2026
"""

import random
import math
from collections import deque
from dataclasses import dataclass
from typing import List
import time as time_module


# ============================================================================
# FIFO TRIEDA
# ============================================================================

class FIFONode:
    """Uzol v FIFO rade"""

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"Node({self.data})"


class FIFO:
    """FIFO rad s head, tail, buffer"""

    def __init__(self, size: int):
        """
        Inicializácia FIFO radu

        Args:
            size: Maximálna veľkosť buffra
        """
        self.buffer = deque(maxlen=size)
        self.head = None
        self.tail = None
        self.max_size = size

    def put(self, item):
        """
        Pridaj prvok do radu

        Args:
            item: Prvok na pridanie

        Returns:
            bool: True ak bolo pridané, False ak je rad plný
        """
        if len(self.buffer) >= self.max_size:
            return False

        node = FIFONode(item)
        self.buffer.append(node)

        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.tail = node

        return True

    def get(self):
        """
        Vyberi prvok z radu

        Returns:
            any: Prvok z radu alebo None ak je prázdny
        """
        if len(self.buffer) == 0:
            return None

        node = self.buffer.popleft()
        self.head = self.buffer[0] if len(self.buffer) > 0 else None

        if len(self.buffer) == 0:
            self.tail = None

        return node.data

    def length(self) -> int:
        """Vráti dĺžku radu"""
        return len(self.buffer)

    def is_empty(self) -> bool:
        """Vráti True ak je rad prázdny"""
        return len(self.buffer) == 0

    def peek(self):
        """Pozri sa na prvý prvok bez jeho vybrania"""
        if len(self.buffer) == 0:
            return None
        return self.buffer[0].data

    def __repr__(self):
        return f"FIFO(length={self.length()}, max_size={self.max_size})"


# ============================================================================
# KUPUJÚCI TRIEDA
# ============================================================================

@dataclass
class Customer:
    """Údaje o kupujúcom"""
    id: int  # Poradové číslo
    arrival_time: float  # Čas príchodu do obchodu (sekundy)
    shopping_duration: float  # Trvanie nákupovania (minúty)
    checkout_duration: float  # Trvanie spracovania pri pokladni (minúty)
    finish_shopping_time: float  # Čas na konci nákupovania
    queue_start_time: float = None  # Čas vstupu do radu
    checkout_finish_time: float = None  # Čas konca spracovania pri pokladni

    def __repr__(self):
        return f"Customer(id={self.id}, arrival={self.arrival_time:.1f}s)"


# ============================================================================
# SIMULÁTOR
# ============================================================================

class ShopSimulator:
    """Simulátor pohybu ľudí v obchode"""

    def __init__(self, student_number: int = 15, operating_hours: float = 8.0):
        """
        Inicializácia simulátora

        Args:
            student_number: Poradové číslo v triednej knihe
            operating_hours: Počet hodín prevádzky (3600 * hours sekúnd)
        """
        self.student_number = student_number
        self.operating_hours = operating_hours
        self.total_simulation_time = operating_hours * 3600  # v sekundách
        self.current_time = 0.0
        self.time_scale = 100  # Simulácia je zrýchľovaná 100x

        # FIFO rad pri pokladni
        self.checkout_queue = FIFO(size=1000)

        # Evidencia všetkých kupujúcich
        self.all_customers: List[Customer] = []
        self.customers_in_shop: List[Customer] = []

        # Štatistiky
        self.total_idle_time = 0.0  # Súhrnná doba nečinnosti pokladne
        self.checkout_busy_until = 0.0  # Čas, kedy je pokladňa obsadená
        self.max_queue_wait = 0.0  # Maximálna doba čakania v rade
        self.max_queue_length = 0  # Maximálna dĺžka radu
        self.customers_served = 0  # Počet obsúžených kupujúcich

        # Logovanie
        self.log_lines = []

    def add_log(self, message: str):
        """Pridaj log správu"""
        self.log_lines.append(message)
        print(message)

    def generate_customers(self):
        """Generuj zoznam kupujúcich na základe zadaných pravidiel"""
        self.all_customers = []
        customer_id = 1
        prev_arrival = 0.0

        while True:
            # Ti = Ti-1 + 5 + random(25 + P.Č.) sekúnd
            arrival_interval = 5 + random.randint(0, 25 + self.student_number)
            arrival_time = prev_arrival + arrival_interval

            # Skontroluj, či je čas príchodu v rámci otváracej doby
            if arrival_time > self.total_simulation_time:
                break

            # Tn = 1 + random(10 + P.Č.) minút
            shopping_duration = 1 + random.randint(0, 10 + self.student_number)

            # Tp = 0.3 + Tn/20 minút
            checkout_duration = 0.3 + shopping_duration / 20

            # Čas na konci nákupovania
            finish_shopping_time = arrival_time + shopping_duration * 60  # Konverzia minút na sekundy

            customer = Customer(
                id=customer_id,
                arrival_time=arrival_time,
                shopping_duration=shopping_duration,
                checkout_duration=checkout_duration,
                finish_shopping_time=finish_shopping_time
            )

            self.all_customers.append(customer)
            prev_arrival = arrival_time
            customer_id += 1

    def get_customers_needing_checkout(self, current_time: float) -> List[Customer]:
        """Nájdi kupujúcich, ktorí majú prejsť do radu pri pokladni"""
        customers = []
        for customer in self.customers_in_shop:
            if (customer.finish_shopping_time <= current_time and
                    customer.queue_start_time is None and
                    customer.checkout_finish_time is None):
                customers.append(customer)
        return customers

    def is_checkout_free(self, current_time: float) -> bool:
        """Skontroluj, či je pokladňa voľná"""
        return self.checkout_busy_until <= current_time

    def print_state(self, event_type: str = ""):
        """Vytlač stav simulácie"""
        queue_length = self.checkout_queue.length()
        display_time = self.current_time / self.time_scale

        msg = f"\n[T={display_time:7.2f}s | {event_type:15} | Rad: {queue_length:3d} | Nečinnosť: {self.total_idle_time:8.2f}s]"
        self.add_log(msg)

    def run(self) -> dict:
        """Spusti simuláciu"""
        self.log_lines = []
        self.add_log("=" * 100)
        self.add_log(f"SIMULÁCIA NÁKUPU V OBCHODE")
        self.add_log(f"Poradové číslo študenta: {self.student_number}")
        self.add_log(f"Doba prevádzky: {self.operating_hours} hodín ({self.total_simulation_time}s)")
        self.add_log(f"Zrýchlenie: {self.time_scale}x")
        self.add_log("=" * 100)

        # Vygeneruj kupujúcich
        self.generate_customers()
        self.add_log(f"\nGenerovaných kupujúcich: {len(self.all_customers)}")

        # Generuj všetky časové udalosti
        events = []  # (time, event_type, customer)

        for customer in self.all_customers:
            events.append((customer.arrival_time, "arrival", customer))
            events.append((customer.finish_shopping_time, "finish_shopping", customer))

        events.sort(key=lambda x: x[0])

        self.current_time = 0.0
        event_index = 0
        screen_line_count = 0
        max_lines_before_screenshot = 50

        self.add_log(f"\n{'=' * 100}")
        self.add_log("ZAČIATOK SIMULÁCIE")
        self.add_log(f"{'=' * 100}\n")

        while event_index < len(events) and self.current_time <= self.total_simulation_time:
            current_event_time, event_type, customer = events[event_index]

            if current_event_time > self.total_simulation_time:
                break

            self.current_time = current_event_time

            # ==== PRÍCHOD KUPUJÚCEHO DO OBCHODU ====
            if event_type == "arrival":
                self.customers_in_shop.append(customer)
                display_time = self.current_time / self.time_scale
                self.add_log(f"\n[T={display_time:7.2f}s] PRÍCHOD kupujúceho #{customer.id}")
                self.add_log(
                    f"  Čas príchodu: {display_time:.2f}s | Nákupovanie: {customer.shopping_duration}min | Pokladňa: {customer.checkout_duration:.2f}min")
                screen_line_count += 3

            # ==== KONIEC NÁKUPOVANIA - VSTUP DO RADU ====
            elif event_type == "finish_shopping":
                # Kupujúci skončil s nakupovaním
                customers_to_queue = [c for c in self.customers_in_shop
                                      if c.finish_shopping_time <= self.current_time
                                      and c.queue_start_time is None
                                      and c.checkout_finish_time is None]

                for cust in customers_to_queue:
                    cust.queue_start_time = self.current_time
                    self.checkout_queue.put(cust)

                    display_time = self.current_time / self.time_scale
                    self.add_log(f"\n[T={display_time:7.2f}s] VSTUP DO RADU kupujúceho #{cust.id}")
                    self.add_log(
                        f"  Čas príchodu do obchodu: {cust.arrival_time / self.time_scale:.2f}s | Čas nákupovania: {cust.shopping_duration}min | Čas spracovania: {cust.checkout_duration:.2f}min")
                    self.add_log(
                        f"  *** Dĺžka radu: {self.checkout_queue.length()} | Nečinnosť pokladne: {self.total_idle_time:.2f}s ***")
                    screen_line_count += 4

                    # Aktualizuj štatistiky
                    if self.checkout_queue.length() > self.max_queue_length:
                        self.max_queue_length = self.checkout_queue.length()
                        self.add_log(f"  !!! NOVÁ MAXIMÁLNA DĹŽKA RADU: {self.max_queue_length}")
                        screen_line_count += 1

            event_index += 1

            # ==== SPRACOVANIE POKLADNE ====
            # Skontroluj, či pokladňa môže spracovať ďalšieho kupujúceho
            if self.is_checkout_free(self.current_time) and not self.checkout_queue.is_empty():
                next_customer = self.checkout_queue.get()

                # Výpočet čakania v rade
                wait_time = self.current_time - next_customer.queue_start_time

                # Čas konca spracovania pri pokladni (v sekundách)
                checkout_end_time = self.current_time + next_customer.checkout_duration * 60
                next_customer.checkout_finish_time = checkout_end_time
                self.checkout_busy_until = checkout_end_time
                self.customers_served += 1

                display_time = self.current_time / self.time_scale
                display_wait = wait_time / self.time_scale
                display_checkout_duration = next_customer.checkout_duration

                self.add_log(f"\n[T={display_time:7.2f}s] ZAPLATENIE kupujúceho #{next_customer.id}")
                self.add_log(
                    f"  Čakanie v rade: {display_wait:.2f}s | Doba spracovania: {display_checkout_duration:.2f}min")
                self.add_log(
                    f"  *** Dĺžka radu: {self.checkout_queue.length()} | Nečinnosť pokladne: {self.total_idle_time:.2f}s ***")
                screen_line_count += 4

                # Aktualizuj maximálne čakanie
                if wait_time > self.max_queue_wait:
                    self.max_queue_wait = wait_time
                    self.add_log(
                        f"  !!! NOVÁ MAXIMÁLNA DOBA ČAKANIA V RADE: {self.max_queue_wait / self.time_scale:.2f}s")
                    screen_line_count += 1

            # Skontroluj nečinnosť pokladne
            if self.is_checkout_free(self.current_time) and self.checkout_queue.is_empty():
                idle_start = self.current_time
                # Hľadaj ďalšiu udalosť
                next_event_time = float('inf')
                for time, _, _ in events[event_index:]:
                    if time > self.current_time:
                        next_event_time = time
                        break

                if next_event_time < float('inf'):
                    idle_duration = next_event_time - self.current_time
                    self.total_idle_time += idle_duration

            # Screenshot po vyplnení obrazovky
            if screen_line_count > max_lines_before_screenshot:
                self.add_log(f"\n{'=' * 100}")
                self.add_log("SCREENSHOT 1 - PRVÉ VYPLNENIE OBRAZOVKY")
                self.add_log(f"{'=' * 100}\n")
                screen_line_count = 0

        # ==== FINÁLNA ŠTATISTIKA ====
        self.add_log(f"\n{'=' * 100}")
        self.add_log("KONIEC SIMULÁCIE - FINÁLNA ŠTATISTIKA")
        self.add_log(f"{'=' * 100}")
        self.add_log(f"Celkový počet ľudí v obchode: {len(self.all_customers)}")
        self.add_log(f"Obsúžení kupujúci: {self.customers_served}")
        self.add_log(f"Maximálna dĺžka radu pri pokladni: {self.max_queue_length} ľudí")
        self.add_log(f"Maximálna doba čakania v rade: {self.max_queue_wait / self.time_scale:.2f} sekúnd")
        self.add_log(f"Celková nečinnosť pokladne: {self.total_idle_time / self.time_scale:.2f} sekúnd")
        self.add_log(f"{'=' * 100}\n")

        return {
            "total_customers": len(self.all_customers),
            "max_queue_wait": self.max_queue_wait / self.time_scale,
            "max_queue_length": self.max_queue_length,
            "total_idle_time": self.total_idle_time / self.time_scale,
            "customers_served": self.customers_served
        }


# ============================================================================
# HLAVNÝ PROGRAM
# ============================================================================

def main():
    """Hlavný program"""

    STUDENT_NUMBER = 2

    print("\n" + "=" * 100)
    print("SIMULÁCIA OBCHODU S FIFO RADOM PRI POKLADNI")
    print("=" * 100)
    print(f"Poradové číslo študenta: {STUDENT_NUMBER}")
    print(f"Doba simulácie: 8 hodín (zrýchľovaná 100x)")
    print(f"Počet spustení: 5")
    print("=" * 100 + "\n")

    results = []

    # Spusti simuláciu 5x
    for run_number in range(1, 6):
        print(f"\n{'*' * 100}")
        print(f"SPUSTENIE #{run_number}")
        print(f"{'*' * 100}\n")

        simulator = ShopSimulator(student_number=STUDENT_NUMBER, operating_hours=8.0)

        result = simulator.run()
        results.append(result)

        log_filename = f"simulation_run_{run_number}.log"
        with open(log_filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(simulator.log_lines))

        print(f"\nLogy uložené do: {log_filename}")

        time_module.sleep(1)

    print("\n" + "=" * 100)
    print("VÝSLEDKY VŠETKÝCH 5 SPUSTENÍ")
    print("=" * 100)
    print(f"{'Spustenie':<12} {'Počet ľudí':<15} {'Max čakanie(s)':<18} {'Max dĺžka radu':<18} {'Nečinnosť(s)':<15}")
    print("-" * 100)

    for i, result in enumerate(results, 1):
        print(
            f"Spustenie {i:<4} {result['total_customers']:<15} {result['max_queue_wait']:<18.2f} {result['max_queue_length']:<18} {result['total_idle_time']:<15.2f}")

    avg_customers = sum(r['total_customers'] for r in results) / len(results)
    avg_wait = sum(r['max_queue_wait'] for r in results) / len(results)
    avg_queue = sum(r['max_queue_length'] for r in results) / len(results)
    avg_idle = sum(r['total_idle_time'] for r in results) / len(results)

    print("-" * 100)
    print(f"{'PRIEMER':<12} {avg_customers:<15.2f} {avg_wait:<18.2f} {avg_queue:<18.2f} {avg_idle:<15.2f}")
    print("=" * 100 + "\n")


if __name__ == "__main__":
    main()
