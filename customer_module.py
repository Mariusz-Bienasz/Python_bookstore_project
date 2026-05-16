import random
from datetime import datetime, timedelta
import pandas as pd
import os
import GlobalVariables


def register_customer(name: str, surname: str, password: str, email: str = "NULL", phone: str = "NULL") -> tuple:
    """
    Funkcja rejestrująca nowego klienta księgarni.
    Generuje unikalne ID, sprawdza czy email nie jest zajęty i dopisuje dane do pliku CSV.

    Args:
        name (str): Imię klienta.
        surname (str): Nazwisko klienta.
        password (str): Hasło klienta do systemu.
        email (str, optional): Adres e-mail. Domyślnie "NULL".
        phone (str, optional): Numer telefonu. Domyślnie "NULL".

    Returns:
        tuple: Krotka (bool, str). Zwraca True i komunikat o sukcesie przy udanej rejestracji,
               lub False i komunikat o błędzie (np. gdy e-mail jest już zajęty).
    """
    try:
        df = pd.read_csv('DATABASE/customer.csv')
        zajete_id = df['ID'].astype(str).tolist()

        # Pobieramy listę e-maili z bazy
        # Wyciągamy kolumnę 'E-MAIL', zamieniamy na tekst i robimy z tego listę Pythona
        zajete_emaile = df['E-MAIL'].astype(str).tolist()
    except FileNotFoundError:
        zajete_id = []
        zajete_emaile = []  # Jeśli nie ma pliku, lista maili jest pusta

    #Sprawdzanie unikalności E-MAILA
    # Jeśli klient podał maila (czyli nie jest to domyślne "NULL") i ten mail
    # znajduje się na naszej liście 'zajete_emaile', to przerywamy rejestrację.
    if email != "NULL" and email in zajete_emaile:
        # Zwracamy False oraz gotowy tekst błędu
        return False, "Błąd: Podany e-mail jest już przypisany do innego konta!"

    # Zagnieżdżona funkcja losująca ID
    def generate_unique_id() -> str:
        while True:
            nowe_id = str(random.randint(1000, 9999))
            if nowe_id not in zajete_id:
                return nowe_id

    customer_id = generate_unique_id()
    full_name = f"{name} {surname}"
    dzisiejsza_data = datetime.now().strftime('%Y-%m-%d')

    # Tworzenie pliku tekstowego z historią
    try:
        file_path = f"DATABASE/{customer_id}.txt"
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"Historia zakupów klienta: {full_name} (ID: {customer_id})\n")
            file.write(f"Konto utworzone: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("-" * 50 + "\n")
    except Exception as e:
        return False, f"Błąd przy tworzeniu pliku z historią: {e}"

    # Dodawanie danych do pliku customer.csv za pomocą Pandas
    try:
        new_customer_data = {
            'ID': [customer_id],
            'NAME': [full_name],
            'PASSWORD': [password],
            'E-MAIL': [email],
            'PHONE': [phone],
            'CREATED': [dzisiejsza_data],
            'UPDATED': [dzisiejsza_data]
        }

        new_row_df = pd.DataFrame(new_customer_data)
        new_row_df.to_csv('DATABASE/customer.csv', mode='a', header=False, index=False)

    except Exception as e:
        return False, f"Błąd podczas zapisu do bazy danych CSV: {e}"

    # Przypisanie id do zmiennej globalnej
    GlobalVariables.userID = customer_id

    # REJESTRACJA UDANA! Zwracamy True oraz ładny komunikat z nowym ID
    return True, f"Rejestracja udana! Twoje nowo wygenerowane ID to: {customer_id}"


# test
#register_customer("Adam", "Nowak", "adam@test.pl", "123456789")

# Usuwanie klienta
def delete_customer(identifier: str, by_id: bool = True) -> tuple:
    """
    Funkcja usuwająca klienta z bazy CSV oraz usuwająca jego plik z historią.

    Args:
        identifier (str): ID klienta lub jego Imię i Nazwisko.
        by_id (bool, optional): Flaga decydująca o sposobie szukania.
                                True szuka po ID, False po Nazwisku. Domyślnie True.

    Returns:
        tuple: Krotka (bool, str). Zwraca True i komunikat o sukcesie przy usunięciu,
               lub False i komunikat o błędzie, gdy klient nie istnieje.
    """
    try:
        df = pd.read_csv('DATABASE/customer.csv')
        initial_count = len(df)

        if by_id:
            df = df[df['ID'].astype(str) != str(identifier)]
        else:
            df = df[df['NAME'] != str(identifier)]

        if len(df) == initial_count:
            # Jeśli ilość wierszy przed i po usunięciu jest taka sama, to nikogo nie znaleźliśmy
            return False, f"Błąd: Nie znaleziono klienta '{identifier}' w bazie!"

        df.to_csv('DATABASE/customer.csv', index=False)

        # Jeśli usuwamy po ID, to fizycznie kasujemy też plik z dysku
        if by_id:
            file_path = f"DATABASE/{identifier}.txt"
            if os.path.exists(file_path):
                os.remove(file_path)

        # Zwracamy sukces dla interfejsu
        return True, f"Sukces: Pomyślnie usunięto klienta '{identifier}' z systemu."

    except FileNotFoundError:
        return False, "Błąd: Nie znaleziono głównego pliku bazy danych (customer.csv)!"
    except Exception as e:
        return False, f"Wystąpił nieoczekiwany błąd podczas usuwania: {e}"

# Zakup książki i Dekorator (Funkcja wyższego rzędu)

def buy_book(customer_id: str, *books) -> tuple:
    """
    Funkcja realizująca zakup książek.
    Przyjmuje dowolną liczbę ID książek i wpisuje je do pliku historii klienta.

    Args:
        customer_id (str): Unikalny identyfikator klienta z bazy CSV.
        *books (str): Dowolna liczba identyfikatorów książek (np. "B001", "B002").

    Returns:
        tuple: Krotka (bool, str). Zwraca True i komunikat o sukcesie transakcji,
               lub False i komunikat o błędzie (np. gdy klienta nie ma w bazie).
    """
    try:
        # Sprawdzenie w głównej bazie czy gość jest zarejestrowany
        df = pd.read_csv('DATABASE/customer.csv')
        if str(customer_id) not in df['ID'].astype(str).values:
            return False, f"Błąd: Klient o ID {customer_id} nie istnieje. Zarejestruj się najpierw!"

        file_path = f"DATABASE/{customer_id}.txt"

        # Tworzenie pliku dla starych klientów, jeśli go nie mają
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f"Historia zakupów klienta (ID: {customer_id})\n")
                file.write(f"Plik wygenerowany przy pierwszym zakupie: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                file.write("-" * 50 + "\n")

        # Księgowanie zakupów (dopisywanie na końcu pliku txt)
        with open(file_path, 'a', encoding='utf-8') as file:
            data_zakupu = datetime.now()
            data_wygasniecia = data_zakupu + timedelta(days=30)

            formatowane_ksiazki = list(map(lambda x: str(x).upper(), books))

            for book_id in formatowane_ksiazki:
                file.write(f"Zakupiono E-Book ID: {book_id}\n")
                file.write(f"Data zakupu: {data_zakupu.strftime('%Y-%m-%d %H:%M')}\n")
                file.write(f"Dostęp wygasa: {data_wygasniecia.strftime('%Y-%m-%d %H:%M')}\n")
                file.write("-" * 50 + "\n")

        return True, "Transakcja zakończona pomyślnie! Książki dopisane do konta."

    except Exception as e:
        return False, f"Wystąpił błąd podczas dokonywania transakcji: {e}"
# TEST ZAKUPU
#buy_book("8909", "B001", "B015", "B042")

# Logowanie użytkownika
def login_customer(identifier: str, password: str, by_id: bool = True) -> tuple:
    """
    Funkcja odpowiedzialna za logowanie klienta do systemu.
    Weryfikuje hasło z bazą i zmienia flagę logowania w zmiennych globalnych.

    Args:
        identifier (str): ID klienta lub jego Imię i Nazwisko.
        password (str): Hasło podane przez klienta.
        by_id (bool, optional): Tryb szukania. True szuka po ID, False po Nazwisku. Domyślnie True.

    Returns:
        tuple: Krotka (bool, str). Zwraca True i komunikat powitalny dla poprawnego hasła,
               lub False i komunikat o błędzie (błędne hasło/brak użytkownika).
    """
    try:
        df = pd.read_csv('DATABASE/customer.csv')

        # Filtrujemy Pandasem w poszukiwaniu wiersza z naszym gościem
        if by_id:
            user_row = df[df['ID'].astype(str) == str(identifier)]
        else:
            user_row = df[df['NAME'] == str(identifier)]

        # Jeśli wynik jest pusty, to znaczy, że takiego człowieka nie ma
        if user_row.empty:
            return False, f"Błąd: Nie znaleziono użytkownika '{identifier}' w naszej bazie!"

        # Wyciągamy hasło z bazy danych
        db_password = str(user_row['PASSWORD'].iloc[0])

        # Porównanie haseł
        if str(password) == db_password:
            user_name = user_row['NAME'].iloc[0]

            # Zmieniamy status w pliku konfiguracyjnym, co pozwoli interfejsowi wejść dalej
            GlobalVariables.isLoggedIn = True

            return True, f"Udało się zalogować! Witaj ponownie, {user_name}."

        else:
            # Hasło wpisane nie równa się temu w bazie
            return False, "Błąd logowania: Podano nieprawidłowe hasło!"

    except FileNotFoundError:
        return False, "Błąd krytyczny: Brak pliku bazy danych!"
    except Exception as e:
        return False, f"Wystąpił nieoczekiwany błąd podczas logowania: {e}"