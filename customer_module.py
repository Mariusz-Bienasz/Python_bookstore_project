import random
from datetime import datetime, timedelta
import pandas as pd
import os


def register_customer(name: str, surname: str, email: str = "NULL", phone: str = "NULL") -> dict:
    """
    Funkcja rejestrująca nowego klienta księgarni.
    Generuje ID, tworzy plik historii i dopisuje klienta do bazy customer.csv.
    """

    # 1. Zagnieżdżona funkcja losująca ID
    def generate_unique_id() -> str:
        return str(random.randint(1000, 9999))

    customer_id = generate_unique_id()
    full_name = f"{name} {surname}"
    dzisiejsza_data = datetime.now().strftime('%Y-%m-%d')

    # 2. Tworzenie pliku tekstowego z historią (To, co napisaliśmy wcześniej)
    try:
        file_path = f"DATABASE/{customer_id}.txt"
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"Historia zakupów klienta: {full_name} (ID: {customer_id})\n")
            file.write(f"Konto utworzone: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("-" * 50 + "\n")
    except Exception as e:
        print(f"Błąd przy tworzeniu pliku TXT: {e}")
        return None

    # 3. Dodawanie danych do pliku customer.csv za pomocą Pandas
    try:
        # Tworzymy "słownik" z danymi nowego klienta.
        # Nazwy kluczy (po lewej) MUSZĄ zgadzać się z nagłówkami w waszym pliku customer.csv
        new_customer_data = {
            'ID': [customer_id],
            'NAME': [full_name],
            'E-MAIL': [email],
            'PHONE': [phone],
            'CREATED': [dzisiejsza_data],
            'UPDATED': [dzisiejsza_data]
        }

        # Konwertujemy nasz słownik na DataFrame (tabelkę Pandas)
        new_row_df = pd.DataFrame(new_customer_data)

        # Dopisujemy nasz nowy wiersz na sam dół pliku customer.csv
        # mode='a' oznacza "append" (dopisz na końcu, nie kasuj starych danych!)
        # header=False oznacza, żeby nie wpisywał drugi raz nazw kolumn
        # index=False usuwa domyślną numerację wierszy z Pandasa
        new_row_df.to_csv('DATABASE/customer.csv', mode='a', header=False, index=False)

        print(f"Sukces! Dodano klienta {full_name} do bazy customer.csv.")

    except Exception as e:
        print(f"Błąd podczas dopisywania do CSV: {e}")
        return None

    # Opcjonalnie w przyszłości można dopisać podobny blok dla address.csv!

    # Funkcja zwraca dane, na wypadek gdyby jakaś inna część programu ich potrzebowała
    return {"ID": customer_id, "NAME": full_name}

# test
#register_customer("Adam", "Nowak", "adam@test.pl", "123456789")


# Zakup książki i Dekorator (Funkcja wyższego rzędu)

def allow_multiple_books(func):
    """
    Dekorator (funkcja wyższego rzędu).
    Pozwala funkcji realizującej zakup jednej książki przyjmować wiele ID książek naraz.
    """

    # *books oznacza, że możemy podać dowolną liczbę argumentów (ID książek)
    def wrapper(customer_id: str, *books):
        print(f"\n--- Rozpoczynam transakcję dla klienta ID: {customer_id} ---")

        # Pętla przechodzi przez wszystkie podane książki i wywołuje bazową funkcję dla każdej z nich
        for book_id in books:
            func(customer_id, book_id)

        print("--- Transakcja zakończona! ---\n")

    return wrapper


@allow_multiple_books  # Używamy dekoratora na naszej funkcji!
def buy_book(customer_id: str, book_id: str) -> bool:
    """
    Funkcja realizująca zakup pojedynczej książki.
    Dopisuje dane o zakupie i wygaśnięciu dostępu do pliku txt klienta.
    """
    try:
        file_path = f"DATABASE/{customer_id}.txt"

        # Sprawdzamy, czy klient ma swój plik w systemie
        if not os.path.exists(file_path):
            print(f"Błąd: Klient o ID {customer_id} nie istnieje w bazie (brak pliku)!")
            return False

        # Otwieramy plik klienta w trybie 'a' (append - dopisz na końcu)
        with open(file_path, 'a', encoding='utf-8') as file:
            data_zakupu = datetime.now()
            # Zakładamy, że dostęp do e-booka wygasa po 30 dniach
            data_wygasniecia = data_zakupu + timedelta(days=30)

            file.write(f"Zakupiono E-Book ID: {book_id}\n")
            file.write(f"Data zakupu: {data_zakupu.strftime('%Y-%m-%d %H:%M')}\n")
            file.write(f"Dostęp wygasa: {data_wygasniecia.strftime('%Y-%m-%d %H:%M')}\n")
            file.write("-" * 50 + "\n")

        print(f"Pomyślnie dodano książkę [{book_id}] do konta klienta.")
        return True

    except Exception as e:
        print(f"Błąd podczas zakupu książki {book_id}: {e}")
        return False



# TEST ZAKUPU
buy_book("8909", "B001", "B015", "B042")