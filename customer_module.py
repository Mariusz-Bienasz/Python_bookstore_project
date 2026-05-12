import random
from datetime import datetime, timedelta
import pandas as pd
import os
import GlobalVariables


def register_customer(name: str, surname: str, password: str, email: str = "NULL", phone: str = "NULL") -> dict:
    """
    Funkcja rejestrująca nowego klienta księgarni.
    Generuje ID, tworzy plik historii i dopisuje klienta do bazy customer.csv z hasłem.
    """

    # 1. Zagnieżdżona funkcja losująca ID
    def generate_unique_id() -> str:
        try:
            # Wczytujemy bazę, żeby zobaczyć zajęte ID
            df = pd.read_csv('DATABASE/customer.csv')
            zajete_id = df['ID'].astype(str).tolist()
        except FileNotFoundError:
            zajete_id = []

        while True:
            # Losujemy tak długo, aż trafimy na numer, którego nie ma na liście "zajete_id"
            nowe_id = str(random.randint(1000, 9999))
            if nowe_id not in zajete_id:
                return nowe_id


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
            'PASSWORD': [password],
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
        print(f"\n Rozpoczynam transakcję dla klienta ID: {customer_id} ")

        # Pętla przechodzi przez wszystkie podane książki i wywołuje bazową funkcję dla każdej z nich
        for book_id in books:
            func(customer_id, book_id)

        print("Transakcja zakończona!\n")

    return wrapper


@allow_multiple_books  # Używamy dekoratora na naszej funkcji!
def buy_book(customer_id: str, book_id: str) -> bool:
    """
    Funkcja realizująca zakup pojedynczej książki.
    Dopisuje dane o zakupie i wygaśnięciu dostępu do pliku txt klienta.
    """
    try:
        # Sprawdzanie czy klient isnieje
        df = pd.read_csv('DATABASE/customer.csv')
        # Zmieniamy wszystko na tekst (astype(str)), żeby uniknąć błędów przy porównywaniu.
        if str(customer_id) not in df['ID'].astype(str).values:
            print(f"Błąd: Klient o ID {customer_id} NIE ISTNIEJE w bazie CSV. Rejestracja wymagana.")
            return False

        file_path = f"DATABASE/{customer_id}.txt"

        # Jeśli klient jest w CSV, ale nie ma swojego pliku (np. stary klient z bazy), to mu go tworzymy
        if not os.path.exists(file_path):
            # Używamy 'w' aby stworzyć nową teczke dla naszego klienta
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f"Historia zakupów klienta (ID: {customer_id})\n")
                file.write(f"Plik wygenerowany przy pierwszym zakupie: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                file.write("-" * 50 + "\n")

        # Właściwy zakup (dopisywanie książki do pliku)
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
#buy_book("8909", "B001", "B015", "B042")

# Logowanie użytkownika
def login_customer(identifier: str, password: str, by_id: bool = True) -> bool:
    """
    Funkcja odpowiedzialna za logowanie klienta.
    Sprawdza, czy podane ID (lub Nazwisko) i hasło zgadzają się z bazą.
    """
    try:
        # Wczytujemy naszą baze danych
        df = pd.read_csv('DATABASE/customer.csv')
        # Szukamy klienta w tabeli
        if by_id:
            # Szukamy wiersza, gdzie w kolumnie ID jest wpisany nasz numerek
            user_row = df[df['ID'].astype(str) == str(identifier)]
        else:
            # Szukamy wiersza, gdzie w kolumnie NAME jest wpisane podane nazwisko
            user_row = df[df['NAME'] == str(identifier)]

        # Sprawdzamy, czy ktoś taki istnieje
        if user_row.empty:
            print(f"Błąd logowania: Nie znaleziono użytkownika '{identifier}'.")
            return False

        # Wyciągamy hasło z bazy dla tego znalezionego gościa
        # .iloc[0] oznacza, że bierzemy wartość z pierwszego wiersza
        db_password = str(user_row['PASSWORD'].iloc[0])

        # KROK 4: Porównujemy hasło podane przez klienta z tym z bazy
        if str(password) == db_password:
            user_name = user_row['NAME'].iloc[0]
            print(f"Sukces! Zalogowano pomyślnie jako: {user_name}")

            GlobalVariables.isLoggedIn = True
            return True

        else:
            print("Błąd logowania: Nieprawidłowe hasło!")
            return False

    except FileNotFoundError:
        print("Błąd: Brak pliku bazy (customer.csv).")
        return False

    except Exception as e:
        print(f"Wystąpił błąd podczas logowania: {e}")
        return False