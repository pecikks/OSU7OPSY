def safety_check(available, allocated, need):
    """
    Realizuje bezpečnostní kontrolu.
    Zjišťuje, zda existuje bezpečné pořadí dokončení klientů.
    """
    n = len(allocated)
    work = available
    finish = [False] * n
    safe_sequence = []

    while len(safe_sequence) < n:
        found = False
        for i in range(n):
            # Pokud klient ještě neskončil a jeho potřeby jsou menší než volné zdroje
            if not finish[i] and need[i] <= work:
                # Simulujeme uvolnění prostředků po dokončení klienta
                work += allocated[i]
                finish[i] = True
                safe_sequence.append(f"K{i}")
                found = True

        # Pokud jsme v jednom průchodu nenašli nikoho, koho lze dokončit, systém je v nebezpečí
        if not found:
            return False, []

    return True, safe_sequence


def print_state(available, allocated, max_req, need):
    # Vytiskne aktuální tabulku stavu systému.
    print("\n" + "=" * 50)
    print(f"{'Klient':<10} | {'Max':<10} | {'Alloc':<10} | {'Need':<10}")
    print("-" * 50)
    for i in range(len(allocated)):
        print(f"K{i:<9} | {max_req[i]:<10} | {allocated[i]:<10} | {need[i]:<10}")
    print("-" * 50)
    print(f"Aktuálně volné prostředky (Available): {available}")
    print("=" * 50 + "\n")


def main():
    print("--- Simulace Bankerova algoritmu ---")

    # Načtení celkových prostředků
    try:
        total_banker = int(input("Zadejte celkové prostředky bankéře: "))
        if total_banker < 0: raise ValueError
    except ValueError:
        print("Chyba: Celkové prostředky musí být nezáporné celé číslo.")
        return

    max_req = []
    allocated = []

    # Načtení dat pro 4 klienty
    for i in range(4):
        print(f"\nNastavení pro klienta K{i}:")
        m = int(input(f"  Maximální požadavek (max[{i}]): "))
        a = int(input(f"  Aktuálně přiděleno (allocated[{i}]): "))

        if m > total_banker:
            print(f"Chyba: Maximální požadavek klienta K{i} ({m}) převyšuje kapitál banky ({total_banker}).")
            return

        # Kontrola 0 <= allocated[i] <= max[i]
        if not (0 <= a <= m):
            print(f"Chyba: Neplatné hodnoty pro klienta K{i}. (0 <= allocated <= max)")
            return

        max_req.append(m)
        allocated.append(a)

    # Výpočet need[i] a available
    need = [max_req[i] - allocated[i] for i in range(4)]
    current_available = total_banker - sum(allocated)

    # Kontrola sum(max) > totalBanker
    if sum(max_req) <= total_banker:
        print("\nChyba: Součet maximálních požadavků musí být větší než celkové prostředky.")
        print("V takovém případě není Bankerův algoritmus potřeba, banka má dost pro všechny.")
        return

    if current_available < 0:
        print("\nChyba: Součet přidělených prostředků převyšuje kapitál banky!")
        return

    # Kontrola bezpečnosti počátečního stavu
    is_safe, sequence = safety_check(current_available, allocated, need)
    if not is_safe:
        print("\nChyba: Počáteční stav není bezpečný! Hrozí deadlock.")
        return
    else:
        print(f"\nPočáteční stav je bezpečný. Posloupnost: {' -> '.join(sequence)}")

    # Hlavní smyčka pro žádosti
    while True:
        print_state(current_available, allocated, max_req, need)

        cmd = input("Chcete zadat novou žádost? (ano/ne): ").lower()
        if cmd != 'ano':
            break

        try:
            idx = int(input("Index klienta (0-3): "))
            request = int(input("Výše žádosti (request): "))

            if not (0 <= idx <= 3):
                print("Chyba: Index musí být 0 až 3.")
                continue

            if request <= 0:
                print("Chyba: Výše žádosti musí být kladné číslo.")
                continue

            # Step 1: Kontrola request <= need
            if request > need[idx]:
                print(f"ZAMÍTNUTO: Žádost {request} je vyšší než zbývající potřeba (need={need[idx]}).")
                continue

            # Step 2: Kontrola request <= available
            if request > current_available:
                print(f"ČEKEJTE: Žádost nelze nyní uspokojit (nedostatek volných prostředků).")
                continue

            # Step 3: Dočasné přidělení (Trial Allocation)
            current_available -= request
            allocated[idx] += request
            need[idx] -= request

            # Step 4: Safety Check
            is_safe, sequence = safety_check(current_available, allocated, need)

            if is_safe:
                print(f"\n>>> POTVRZENO: Žádost byla schválena.")
                print(f">>> SYSTÉM JE V BEZPEČNÉM STAVU.")
                print(f">>> Bezpečná posloupnost: {' -> '.join(sequence)}")

                # Pokud klient dosáhl své potřeby, uvolní zdroje
                if need[idx] == 0:
                    print(f"\n[!] Klient K{idx} získal všechny potřebné zdroje, dokončil práci a vrací {allocated[idx]} prostředků bance.")
                    current_available += allocated[idx]
                    allocated[idx] = 0
            else:
                # Rollback - vrácení změn (vypsání znova tabulky)
                current_available += request
                allocated[idx] -= request
                need[idx] += request
                print(f"\n>>> ZAMÍTNUTO: Žádost by vedla k nebezpečnému stavu (možný deadlock).")

        except ValueError:
            print("Chyba: Zadejte platná čísla.")

    print("Program ukončen.")


if __name__ == "__main__":
    main()