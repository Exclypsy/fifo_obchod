import time
import random

# --- Globálne počítadlá ---
comparison_count = 0
assignment_count = 0


# --- Binárny vyhľadávací strom ---
class Node:
    __slots__ = ('key', 'left', 'right')

    def __init__(self, key):
        global assignment_count
        self.key = key
        assignment_count += 1
        self.left = None
        assignment_count += 1
        self.right = None
        assignment_count += 1


def insert_iterative(root, key):
    global comparison_count, assignment_count

    if root is None:
        assignment_count += 1
        return Node(key)

    curr = root
    while True:
        comparison_count += 1
        if key < curr.key:
            if curr.left is None:
                curr.left = Node(key)
                assignment_count += 2
                break
            curr = curr.left
            assignment_count += 1
        else:
            if curr.right is None:
                curr.right = Node(key)
                assignment_count += 2
                break
            curr = curr.right
            assignment_count += 1

    return root


# --- Iteratívny inorder (vzostupne) ---
def inorder_iterative(root, acc):
    global assignment_count
    if root is None:
        return

    stack = []
    curr = root

    while stack or curr:
        # Ľavé kľuče do zásobníka
        while curr:
            stack.append(curr)
            assignment_count += 1
            curr = curr.left
            assignment_count += 1

        # Vrát sa z vrcholu stacku
        curr = stack.pop()
        assignment_count += 1
        acc.append(curr.key)
        assignment_count += 1

        # Skoč na pravé podstrom
        curr = curr.right
        assignment_count += 1


# --- Iteratívny reverse_inorder (zostupne) ---
def reverse_inorder_iterative(root, acc):
    global assignment_count
    if root is None:
        return

    stack = []
    curr = root

    while stack or curr:
        # Najprv pravé
        while curr:
            stack.append(curr)
            assignment_count += 1
            curr = curr.right
            assignment_count += 1

        curr = stack.pop()
        assignment_count += 1
        acc.append(curr.key)
        assignment_count += 1

        curr = curr.left
        assignment_count += 1


def tree_sort(arr, descending=False):
    global comparison_count, assignment_count

    comparison_count = 0
    assignment_count = 0

    root = None

    start = time.perf_counter()
    for x in arr:
        root = insert_iterative(root, x)
        assignment_count += 1

    sorted_arr = []
    if descending:
        reverse_inorder_iterative(root, sorted_arr)
    else:
        inorder_iterative(root, sorted_arr)

    end = time.perf_counter()
    elapsed_ms = (end - start) * 1000

    return sorted_arr, elapsed_ms, comparison_count, assignment_count


# --- Generovanie rôznych typov dát ---
def generate_array(n, data_type):
    if data_type == "rovnomerne":
        return [random.randint(0, n * 2) for _ in range(n)]

    elif data_type == "kolisave_rastuce":
        arr = list(range(n))
        for i in range(0, n, 2):
            if i + 1 < n and random.random() < 0.3:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
        return arr

    elif data_type == "kolisave_klesajuce":
        arr = list(range(n, 0, -1))
        for i in range(0, n, 2):
            if i + 1 < n and random.random() < 0.3:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
        return arr

    else:
        return [random.randint(0, n * 2) for _ in range(n)]


# --- Main ---
def main():
    n = int(input("Zadaj veľkosť poľa: "))

    print("Vyber typ dát:")
    print("1 - rovnomerne náhodné")
    print("2 - kolísavo rastúce")
    print("3 - kolísavo klesajúce")

    choice = input("Zvoľ (1/2/3): ").strip()

    if choice == "1":
        data_type = "rovnomerne"
    elif choice == "2":
        data_type = "kolisave_rastuce"
    elif choice == "3":
        data_type = "kolisave_klesajuce"
    else:
        print("Neplatná voľba, použijem rovnomerne náhodné.")
        data_type = "rovnomerne"

    arr = generate_array(n, data_type)
    print("Vygenerované pole (prvých 20 prvkov):", arr[:20])

    direction = input("Triediť vzostupne (v) alebo zostupne (z)? [v/z]: ").strip().lower()
    descending = (direction == 'z')

    sorted_arr, elapsed_ms, comps, assigns = tree_sort(arr, descending=descending)

    print("\nVýsledok triedenia (prvých 20 prvkov):", sorted_arr[:20])
    print(f"Čas triedenia: {elapsed_ms:.3f} ms")
    print(f"Počet porovnaní: {comps}")
    print(f"Počet priradení: {assigns}")


if __name__ == "__main__":
    main()
