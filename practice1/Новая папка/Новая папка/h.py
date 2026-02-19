names = ["abay", "aldik"]
ages = [90, 77]

# Используем разные имена для списков (мн. число) и переменных цикла (ед. число)
for n, a in zip(names, ages):
    if a > 50:
        print(f"Damn {n}, you are old")