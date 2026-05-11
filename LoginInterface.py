# Interfejs grficzyny do modułu Logowania i Rejestracji

'''

To do:
-kolory
-odstępy
-podpięcie funkcji (na koniec)

'''

from datetime import datetime
import customtkinter as ctk
import DashboardInterface
import hashlib


def numbersCheck(txt):
    '''
        Funkcja do sprawdzania czy podane przez użytkownika znaki to cyfry
        (do sprawdzania numeru telefonu)

        Args:
            txt : znak podany w entry przez użytkownika
        Returns:
            true lub false w zależności od wyniku sprawdzenia
    '''

    return txt == "" or txt.isdigit()


def register(login, email, phone, password, passwordAgain, errorLabel):
    '''
            Funkcja do podłączenia rejestracji

            Args:
                login, email, phone, password, passwordAgain: wartości jakie podał użytkownik
                errorLabel: Label do wypisywania błędów
            Returns:
                Brak
        '''

    login = login.strip()
    email = email.strip()
    phone = phone.strip()

    password = password.strip()
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    passwordAgain = passwordAgain.strip()
    passwordAgain = hashlib.sha256(passwordAgain.encode('utf-8')).hexdigest()

    date = datetime.now().strftime("%d.%m.%Y")

    errorLabel.configure(text=f"Login: {login} \nEmail: {email} \nPhone: {phone} \nPassword: {password} \nPassword Again: {passwordAgain} \nDate: {date}")
    print(f"Login: {login} \nEmail: {email} \nPhone: {phone} \nPassword: {password} \nPassword Again: {passwordAgain} \nDate: {date}")

def login(login, password, errorLabel):
    '''
        Funkcja do podłączenia logowania

        Args:
            login, password: wartości jakie podał użytkownik
            errorLabel: Label do wypisywania błędów
        Returns:
            Brak
    '''

    # usuwam spacje na poczatku i końcu zmiennych
    login = login.strip()
    password = password.strip()
    # zabezpieczam hasło szyfrowaniem typu hash
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    errorLabel.configure(text=f"Login: {login} \nPassword: {password}")
    print(f"Login: {login} \nPassword: {password}")



def openDashboardInterface(window):
    '''
        Funkcja do przełączania interfejsu

        Args:
            window (tk): główne okno interfejsu
        Returns:
            Brak
    '''

    # czyszczenie otwartego interfejsu
    for widget in window.winfo_children():
        widget.destroy()
    # otwieranie głównego interfejsu
    DashboardInterface.makeDashboard(window)

def makeLoginInterface(window):
    '''
        Funkcja tworząca interfejs logoawnia i rejestracji

        Args:
            window (TK): główne okno interfejsu
        Returns:
            brak
    '''

    # Tworzenie walidacji dla numeru telefonu
    phoneValidate = (window.register(numbersCheck), '%P')

    # Nagłówek
    header = ctk.CTkFrame(window, fg_color="#DCDCDC", corner_radius=0, height=80)
    header.pack_propagate(False)  # blokowanie zmiany rozmiaru
    header.pack(side="top", fill="x")

    # Napis w nagłówku
    appNameLabel = ctk.CTkLabel(
        header,
        text="Internetowa Księgarnia",
        font=("arial", 16, "bold"),
        text_color="#3498db",
        fg_color="#DCDCDC")

    appNameLabel.pack(side="left", padx=10, pady=5)


    # przycisk do zamykania aplikacji

    closeButton = ctk.CTkButton(
        header,
        corner_radius=15,
        text="X",
        width=50,
        height=50,
        fg_color="transparent",
        text_color="#334155",
        hover_color="#E69A9A",
        font=("arial", 16, "bold"),
        command=window.destroy
    )
    closeButton.pack(side="right", padx=10, pady=5)


    # Przycisk powrotu do głównej strony

    backButton = ctk.CTkButton(
        header,
        text="Powrót do sklepu",
        command = lambda: openDashboardInterface(window),
        fg_color="transparent",
        text_color="#334155",
        hover_color="#C8C8C8")

    backButton.pack(side="right", padx=10, pady=5)

    # główna sekcja
    mainBox = ctk.CTkFrame(window, fg_color="#DCDCDC", corner_radius=0)
    mainBox.pack(side="top", fill="both", expand=True)

    # wrapper

    wrapper = ctk.CTkFrame(mainBox, fg_color="transparent")
    wrapper.pack(expand=True)

    ## LOGOWANIE:

    # Sekcja logowania

    loginBox = ctk.CTkFrame(
        wrapper,
        width=350,
        height=650,
        border_width=2,
        corner_radius=15,
        fg_color="#FFFFFF")

    loginBox.pack_propagate(False)
    loginBox.pack(side="left", padx=20, pady=10)

    # tekst nazwy formularza (sekcji)
    formNameLabel = ctk.CTkLabel(
        loginBox,
        text="Logowanie",
        font=("arial", 16, "bold"),
        text_color="#3498db",
        fg_color="transparent")

    formNameLabel.pack(side="top", pady=10)

    # napis Podaj login
    loginLabel = ctk.CTkLabel(
        loginBox,
        text="Podaj nazwę konta: ",
        font=("arial", 16, "bold"),
        text_color="#000000",
        fg_color="transparent")

    loginLabel.pack(side="top", pady=20)

    # input dla loginu
    loginEntry = ctk.CTkEntry(
        loginBox,
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#000000",
        border_width=2,
        corner_radius=20)

    loginEntry.pack(side="top")

    # napis Podaj hasło

    passwordLabel = ctk.CTkLabel(
        loginBox,
        text="Podaj Hasło: ",
        font=("arial", 16, "bold"),
        text_color="#000000",
        fg_color="transparent")

    passwordLabel.pack(side="top", pady=20)

    # input dla hasła

    passwordEntry = ctk.CTkEntry(
        loginBox,
        show="*",
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#000000",
        border_width=2,
        corner_radius=20)

    passwordEntry.pack(side="top")

    # przycisk logowania

    loginButton = ctk.CTkButton(
        loginBox,
        text="Zaloguj!",
        border_width=2,
        corner_radius=10,
        border_color="#000000",
        hover_color="#C8C8C8",
        text_color="#000000",
        fg_color="transparent",
        command = lambda: login(loginEntry.get(), passwordEntry.get(), errorLabel))

    loginButton.pack(side="top", pady=20)


    ## REJESTRACJA:

    # Sekcja rejsetracji:

    registerBox = ctk.CTkFrame(
        wrapper,
        width=350,
        height=650,
        border_width=2,
        corner_radius=15,
        fg_color="#FFFFFF")

    registerBox.pack_propagate(False)
    registerBox.pack(side="left", padx=20, pady=10)

    # Tekst 'Rejestracja'

    formNameLabel = ctk.CTkLabel(
        registerBox,
        text="Rejestracja",
        font=("arial", 16, "bold"),
        text_color="#3498db",
        fg_color="transparent")

    formNameLabel.pack(side="top", pady=10)

    # Napis 'Podaj nazwę konta:'

    loginRegisterLabel = ctk.CTkLabel(
        registerBox,
        text="Podaj nazwę konta: ",
        font=("arial", 16, "bold"),
        text_color="#000000",
        fg_color="transparent")

    loginRegisterLabel.pack(side="top", pady=10)

    # input loginu

    loginRegisterEntry = ctk.CTkEntry(
        registerBox,
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#000000",
        border_width=2,
        corner_radius=20)

    loginRegisterEntry.pack(side="top")

    # napis 'Podaj e-mail:'

    emailRegisterLabel = ctk.CTkLabel(
        registerBox,
        text="Podaj e-mail: ",
        font=("arial", 16, "bold"),
        text_color="#000000",
        fg_color="transparent")

    emailRegisterLabel.pack(side="top", pady=10)

    # input email

    emailRegisterEntry = ctk.CTkEntry(
        registerBox,
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#000000",
        border_width=2,
        corner_radius=20)

    emailRegisterEntry.pack(side="top")

    # napis 'Podaj numer telefonu:'

    phoneRegisterLabel = ctk.CTkLabel(
        registerBox,
        text="Podaj numer telefonu: ",
        font=("arial", 16, "bold"),
        text_color="#000000",
        fg_color="transparent")

    phoneRegisterLabel.pack(side="top", pady=10)

    # input numeru telefonu

    phoneRegisterEntry = ctk.CTkEntry(
        registerBox,
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#000000",
        border_width=2,
        corner_radius=20,
        validate="key",
        validatecommand=phoneValidate)

    phoneRegisterEntry.pack(side="top")

    # napis 'podaj hasło:'

    passwordRegisterLabel = ctk.CTkLabel(
        registerBox,
        text="Podaj hasło: ",
        font=("arial", 16, "bold"),
        text_color="#000000",
        fg_color="transparent")

    passwordRegisterLabel.pack(side="top", pady=10)

    # input hasła

    passwordRegisterEntry = ctk.CTkEntry(
        registerBox,
        show="*",
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#000000",
        border_width=2,
        corner_radius=20)

    passwordRegisterEntry.pack(side="top")


    # napis 'powtórz hasło:'

    passwordRegisterLabel = ctk.CTkLabel(
        registerBox,
        text="powtórz hasło: ",
        font=("arial", 16, "bold"),
        text_color="#000000",
        fg_color="transparent")

    passwordRegisterLabel.pack(side="top", pady=10)


    # input ponownego hasła

    passwordAgainRegisterEntry = ctk.CTkEntry(
        registerBox,
        show="*",
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#000000",
        border_width=2,
        corner_radius=20)

    passwordAgainRegisterEntry.pack(side="top")

    # przycisk rejestracji

    registerButton = ctk.CTkButton(
        registerBox,
        text="Zarejestruj!",
        border_width=2,
        corner_radius=10,
        border_color="#000000",
        hover_color="#C8C8C8",
        text_color="#000000",
        fg_color="transparent",
        command = lambda: register(
            loginRegisterEntry.get(),
            emailRegisterEntry.get(),
            phoneRegisterEntry.get(),
            passwordRegisterEntry.get(),
            passwordAgainRegisterEntry.get(),
            errorLabel)
    )

    registerButton.pack(side="top", pady=20)


    # Label do wyświetlania błędów

    errorLabel = ctk.CTkLabel(
        mainBox,
        text="",
        font=("arial", 16, "bold"),
        text_color="red",
        fg_color="transparent")

    errorLabel.pack(side="bottom", pady=30)


