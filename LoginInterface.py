# Interfejs grficzyny do modułu Logowania i Rejestracji

'''

To do:

-podpiąć funkcje logowania

'''

from datetime import datetime
import customtkinter as ctk
import DashboardInterface
import hashlib
import re

import GlobalVariables
import customer_module


def numbersCheck(txt):
    '''
        Funkcja do sprawdzania czy podane przez użytkownika znaki to cyfry
        (do sprawdzania numeru telefonu)

        Args:
            txt : znak podany w entry przez użytkownika
        Returns:
            true lub false w zależności od wyniku sprawdzenia
    '''

    return txt == "" or txt.isdigit() or txt == "Podaj numer id książki"


def register(name, surname, email, phone, password, passwordAgain, errorLabel):
    '''
            Funkcja do podłączenia rejestracji i walidacja inputów

            Args:
                login, email, phone, password, passwordAgain: wartości jakie podał użytkownik
                errorLabel: Label do wypisywania błędów
            Returns:
                Brak
        '''

    error = False
    errorTxt = ''
    name = name.strip()
    surname = surname.strip()
    email = email.strip()
    phone = phone.strip()

    emailPattern = r'^[\w.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


    # szyfrowanie hasła

    password = password.strip()
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    passwordAgain = passwordAgain.strip()
    passwordAgain = hashlib.sha256(passwordAgain.encode('utf-8')).hexdigest()


    # Walidacja danych:

    if name == "":
        error = True
        errorTxt += 'Pole imie nie może być puste \n'

    if surname == "":
        error = True
        errorTxt += 'Pole nazwisko nie może być puste \n'

    if email == "":
        error = True
        errorTxt += 'Pole email nie może być puste \n'

    if not re.match(emailPattern, email):
        error = True
        errorTxt += 'W polu email jest błąd \n'

    if phone == "":
        phone="NULL"

    if phone != "" and len(phone) != 9:
        error = True
        errorTxt += 'Numer telefonu musi mieć 9 cyfr \n'

    if password == "" or passwordAgain == "":
        error = True
        errorTxt += 'Pole hasło nie może być puste \n'

    if password != passwordAgain:
        error = True
        errorTxt += 'Hasła nie są takie same\n'

    errorLabel.configure(text=errorTxt)


    if error == False:
        result, message = customer_module.register_customer(name,surname, password, email, phone)
        if result == True:
            GlobalVariables.isLoggedIn = True
            errorLabel.configure(text=message, text_color="#00FF00")
        else:
            errorLabel.configure(text=message)


    #print(f"Name: {name} \nSurname: {surname} \nEmail: {email} \nPhone: {phone} \nPassword: {password} \nPassword Again: {passwordAgain} \n")

def login(email, password, errorLabel):
    '''
        Funkcja do podłączenia logowania

        Args:
            login, password: wartości jakie podał użytkownik
            errorLabel: Label do wypisywania błędów
        Returns:
            Brak
    '''

    # usuwam spacje na poczatku i końcu zmiennych
    email = email.strip()
    password = password.strip()
    # zabezpieczam hasło szyfrowaniem typu hash
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    error = False
    errorTxt = ''
    emailPattern = r'^[\w.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


    if  email == "":
        error = True
        errorTxt += "Pole e-mail nie może być puste \n"
    if not re.match(emailPattern, email):
        error = True
        errorTxt +=  "W polu e-mail jest błąd \n"
    if password == "":
        error = True
        errorTxt += "Pole hasło nie może być puste"

    errorLabel.configure(text=errorTxt)

    if error == False:
        # if customer_module.login_customer() == True:
        #     print(f"Login: {login} \nPassword: {password}")
        #     errorLabel.configure(text="Udało ci się zalogować", text_color="#00FF00")
        # else:
        #     errorLabel.configure(text="Coś poszło nie tak/Błędny e-mail lub hasło")
        return



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

def loginForm(wrapper, loginFormButton, registerFormButton):
    for widget in wrapper.winfo_children():
        widget.destroy()
    ## LOGOWANIE:

    loginFormButton.configure(fg_color="#1E3A8A")
    registerFormButton.configure(fg_color="transparent")

    # Sekcja logowania

    loginBox = ctk.CTkFrame(
        wrapper,
        width=350,
        height=750,
        border_width=2,
        corner_radius=15,
        border_color="#3B82F6",
        fg_color="#1E293B")

    loginBox.pack_propagate(False)
    loginBox.pack(side="left", padx=20, pady=10)

    # tekst nazwy formularza (sekcji)

    formNameLabel = ctk.CTkLabel(
        loginBox,
        text="Logowanie",
        font=("arial", 25, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent")
    formNameLabel.pack(side="top", pady=(30, 90))
    # napis Podaj login

    emailLoginLabel = ctk.CTkLabel(
        loginBox,
        text="Podaj e-mail: ",
        font=("arial", 16, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent")
    emailLoginLabel.pack(side="top", pady=20)
    # input dla loginu

    emailLoginEntry = ctk.CTkEntry(
        loginBox,
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        border_width=2,
        border_color="#3B82F6",
        corner_radius=20)
    emailLoginEntry.pack(side="top")
    # napis Podaj hasło

    passwordLabel = ctk.CTkLabel(
        loginBox,
        text="Podaj Hasło: ",
        font=("arial", 16, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent")
    passwordLabel.pack(side="top", pady=20)
    # input dla hasła

    passwordEntry = ctk.CTkEntry(
        loginBox,
        show="*",
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        border_width=2,
        border_color="#3B82F6",
        corner_radius=20)
    passwordEntry.pack(side="top")

    # przycisk logowania
    loginButton = ctk.CTkButton(
        loginBox,
        text="Zaloguj!",
        border_width=2,
        corner_radius=10,
        border_color="#3B82F6",
        width=200,
        height=50,
        hover_color="#1E3A8A",
        text_color="#F8FAFC",
        fg_color="transparent",
        font=("arial", 20, "bold"),
        command=lambda: login(emailLoginEntry.get(), passwordEntry.get(), errorLabel))
    loginButton.pack(side="top", pady=70)

    # Label do wyświetlania błędów

    errorLabel = ctk.CTkLabel(
        loginBox,
        text="",
        font=("arial", 16, "bold"),
        text_color="#d62828",
        fg_color="transparent"
    )

    errorLabel.pack(side="bottom", pady=30)

    #############################################

def registerForm(wrapper, loginFormButton, registerFormButton):
    for widget in wrapper.winfo_children():
        widget.destroy()

    ## REJESTRACJA:

    loginFormButton.configure(fg_color="transparent")
    registerFormButton.configure(fg_color="#1E3A8A")

    # Tworzenie walidacji dla numeru telefonu
    phoneValidate = (wrapper.register(numbersCheck), '%P')

    # Sekcja rejsetracji:

    registerBox = ctk.CTkScrollableFrame(
        wrapper,
        width=350,
        height=750,
        border_width=2,
        corner_radius=15,
        border_color="#3B82F6",
        fg_color="#1E293B")

    registerBox.pack(side="left", padx=20, pady=10)
    registerBox._scrollbar.grid_configure(padx=(0, 10))

    # Tekst 'Rejestracja'

    formNameLabel = ctk.CTkLabel(
        registerBox,
        text="Rejestracja",
        font=("arial", 25, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent")

    formNameLabel.pack(side="top", pady=30)


    # Napis 'Podaj nazwę konta:'

    nameRegisterLabel = ctk.CTkLabel(
        registerBox,
        text="Podaj imię: ",
        font=("arial", 16, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent"
    )

    nameRegisterLabel.pack(side="top", pady=10)

    # input loginu

    nameRegisterEntry = ctk.CTkEntry(
        registerBox,
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        border_width=2,
        border_color="#3B82F6",
        corner_radius=20)

    nameRegisterEntry.pack(side="top")

    # Napis 'Podaj nazwisko:'

    surnameRegisterLabel = ctk.CTkLabel(
        registerBox,
        text="Podaj nazwisko: ",
        font=("arial", 16, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent"
    )

    surnameRegisterLabel.pack(side="top", pady=10)

    # input loginu

    surnameRegisterEntry = ctk.CTkEntry(
        registerBox,
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        border_width=2,
        border_color="#3B82F6",
        corner_radius=20)

    surnameRegisterEntry.pack(side="top")

    # napis 'Podaj e-mail:'

    emailRegisterLabel = ctk.CTkLabel(
        registerBox,
        text="Podaj e-mail: ",
        font=("arial", 16, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent")

    emailRegisterLabel.pack(side="top", pady=10)

    # input email

    emailRegisterEntry = ctk.CTkEntry(
        registerBox,
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        border_width=2,
        border_color="#3B82F6",
        corner_radius=20)

    emailRegisterEntry.pack(side="top")

    # napis 'Podaj numer telefonu:'

    phoneRegisterLabel = ctk.CTkLabel(
        registerBox,
        text="Podaj numer telefonu: ",
        font=("arial", 16, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent")

    phoneRegisterLabel.pack(side="top", pady=10)

    # input numeru telefonu

    phoneRegisterEntry = ctk.CTkEntry(
        registerBox,
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        border_width=2,
        border_color="#3B82F6",
        corner_radius=20,
        validate="key",
        validatecommand=phoneValidate)

    phoneRegisterEntry.pack(side="top")

    # napis 'podaj hasło:'

    passwordRegisterLabel = ctk.CTkLabel(
        registerBox,
        text="Podaj hasło: ",
        font=("arial", 16, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent")

    passwordRegisterLabel.pack(side="top", pady=10)

    # input hasła

    passwordRegisterEntry = ctk.CTkEntry(
        registerBox,
        show="*",
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        border_width=2,
        border_color="#3B82F6",
        corner_radius=20)

    passwordRegisterEntry.pack(side="top")


    # napis 'powtórz hasło:'

    passwordRegisterLabel = ctk.CTkLabel(
        registerBox,
        text="powtórz hasło: ",
        font=("arial", 16, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent")

    passwordRegisterLabel.pack(side="top", pady=10)


    # input ponownego hasła

    passwordAgainRegisterEntry = ctk.CTkEntry(
        registerBox,
        show="*",
        width=250,
        height=40,
        fg_color="transparent",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        border_width=2,
        border_color="#3B82F6",
        corner_radius=20)

    passwordAgainRegisterEntry.pack(side="top")

    # Label do wyświetlania błędów

    errorLabel = ctk.CTkLabel(
        registerBox,
        text="",
        font=("arial", 16, "bold"),
        text_color="#d62828",
        fg_color="transparent"
    )

    errorLabel.pack(side="bottom", pady=30)

    # przycisk rejestracji

    registerButton = ctk.CTkButton(
        registerBox,
        text="Zarejestruj!",
        border_width=2,
        width=200,
        height=50,
        corner_radius=10,
        border_color="#3B82F6",
        hover_color="#1E3A8A",
        text_color="#F8FAFC",
        fg_color="transparent",
        font=("arial", 20, "bold"),
        command = lambda: register(
            nameRegisterEntry.get(),
            surnameRegisterEntry.get(),
            emailRegisterEntry.get(),
            phoneRegisterEntry.get(),
            passwordRegisterEntry.get(),
            passwordAgainRegisterEntry.get(),
            errorLabel)
    )

    registerButton.pack(side="bottom", pady=(30,15))



def makeLoginInterface(window):
    '''
        Funkcja tworząca interfejs logoawnia i rejestracji

        Args:
            window (TK): główne okno interfejsu
        Returns:
            brak
    '''

    # Nagłówek
    header = ctk.CTkFrame(window, fg_color="#001524", corner_radius=0, height=80)
    header.pack_propagate(False)  # blokowanie zmiany rozmiaru
    header.pack(side="top", fill="x")

    # Napis w nagłówku
    appNameLabel = ctk.CTkLabel(
        header,
        text="Internetowa Księgarnia",
        font=("arial", 20, "bold"),
        text_color="#3a86ff",
        fg_color="transparent")

    appNameLabel.pack(side="left", padx=30, pady=10)


    # przycisk do zamykania aplikacji

    closeButton = ctk.CTkButton(
        header,
        corner_radius=15,
        text="X",
        width=50,
        height=50,
        fg_color="transparent",
        text_color="#3a86ff",
        hover_color="#E69A9A",
        font=("arial", 20, "bold"),
        command=window.destroy
    )
    closeButton.pack(side="right", padx=10, pady=5)


    # Przycisk powrotu do głównej strony

    backButton = ctk.CTkButton(
        header,
        text="Powrót do sklepu",
        command = lambda: openDashboardInterface(window),
        fg_color="transparent",
        width=150,
        height=50,
        text_color="#3a86ff",
        font=("arial", 20, "bold"),
        hover_color="#002B4A")

    backButton.pack(side="right", padx=10, pady=5)

    buttonsWrapper = ctk.CTkFrame(window, fg_color="#001524", corner_radius=0)
    buttonsWrapper.pack(side="top", fill="x", )

    buttonBox = ctk.CTkFrame(
        buttonsWrapper,
        fg_color="#001524",
        height=100,
        width=700,
    )

    buttonBox.pack(side="top", pady=0)

    mainBox = ctk.CTkScrollableFrame(window, fg_color="#001524", corner_radius=0)
    mainBox.pack(side="top", fill="both", expand=True)

    loginFormButton = ctk.CTkButton(
        buttonBox,
        text="LOGOWANIE",
        command=lambda: loginForm(wrapper, loginFormButton, registerFormButton),
        width=200,
        height=40,
        border_width=2,
        corner_radius=10,
        border_color="#3B82F6",
        hover_color="#1E3A8A",
        text_color="#F8FAFC",
        fg_color="transparent",
        font=("arial", 20, "bold"),
    )

    loginFormButton.pack(side="left", padx=(0, 50))

    registerFormButton = ctk.CTkButton(
        buttonBox,
        text="REJESTRACJA",
        command=lambda: registerForm(wrapper, loginFormButton, registerFormButton),
        width=200,
        height=40,
        border_width=2,
        corner_radius=10,
        border_color="#3B82F6",
        hover_color="#1E3A8A",
        text_color="#F8FAFC",
        fg_color="transparent",
        font=("arial", 20, "bold"),
    )


    registerFormButton.pack(side="left", padx=(0,0))

    # wrapper

    wrapper = ctk.CTkFrame(mainBox, fg_color="transparent")
    wrapper.pack(expand=True , pady=(60,30))

    loginForm(wrapper, loginFormButton, registerFormButton)

