# Interfejs grficzyny do modułu Logowania i Rejestracji

'''

To do:
-kolory
-odstępy
-register form
-dokumentacja (poprawki)

'''

import customtkinter as ctk
import DashboardInterface

'''
    Funkcja do podłączenia logowania
    
    Args:
        login, password: wartości jakie podał użytkownik
    Returns:
        Brak
'''
def login(login, password):
    # usuwam spacje na poczatku i końcu zmiennych
    login = login.strip()
    password = password.strip()
    # zabezpieczam hasło szyfrowaniem typu hash
    password = hash(password)
    print(f"Login: {login} \nPassword: {password}")


'''
    Funkcja do przełączania interfejsu

    Args:
        window (tk): główne okno interfejsu
    Returns:
        Brak
'''
def openDashboardInterface(window):
    # czyszczenie otwartego interfejsu
    for widget in window.winfo_children():
        widget.destroy()
    # otwieranie głównego interfejsu
    DashboardInterface.makeDashboard(window)

def makeLoginInterface(window):
    # Nagłówek
    header = ctk.CTkFrame(window, fg_color="#DCDCDC")
    header.pack(side="top", fill="x")

    # Napis w nagłówku
    appNameLabel = ctk.CTkLabel(header, text="Internetowa Księgarnia", font=("arial", 16, "bold"), text_color="#3498db", fg_color="#DCDCDC")
    appNameLabel.pack(side="left", padx=10, pady=5)

    # Przycisk powrotu do głównej strony
    backButton = ctk.CTkButton(header,text="Powrót do sklepu", command = lambda x=window:openDashboardInterface(x), fg_color="transparent", text_color="#334155", hover_color="#C8C8C8")
    backButton.pack(side="right", padx=10, pady=5)

    # główna sekcja
    mainBox = ctk.CTkFrame(window,fg_color="#DCDCDC")
    mainBox.pack(side="top", fill="both", expand=True)

    # Sekcja logowania
    loginBox = ctk.CTkFrame(mainBox, width=350, height=450, border_width=2, corner_radius=15, fg_color="#FFFFFF")
    loginBox.pack_propagate(False)
    loginBox.pack(side="left", padx=10, pady=10)

    # tekst nazwy formularza (sekcji)
    formNameLabel = ctk.CTkLabel(loginBox, text="Logowanie", font=("arial", 16, "bold"), text_color="#3498db", fg_color="transparent")
    formNameLabel.pack(side="top", pady=10)

    # napis Podaj login
    loginLabel = ctk.CTkLabel(loginBox, text="Podaj Login: ", font=("arial", 16, "bold"), text_color="#000000", fg_color="transparent")
    loginLabel.pack(side="top", pady=20)

    # input dla loginu
    loginEntry = ctk.CTkEntry(loginBox, width=250, height=40, fg_color="transparent", text_color="#000000", border_width=2, corner_radius=20)
    loginEntry.pack(side="top")

    # napis Podaj hasło
    passwordLabel = ctk.CTkLabel(loginBox, text="Podaj Hasło: ", font=("arial", 16, "bold"), text_color="#000000", fg_color="transparent")
    passwordLabel.pack(side="top", pady=20)

    # input dla hasła
    passwordEntry = ctk.CTkEntry(loginBox, show="*", width=250, height=40, fg_color="transparent", text_color="#000000", border_width=2, corner_radius=20)
    passwordEntry.pack(side="top")

    # przycisk logowania
    loginButton = ctk.CTkButton(loginBox, text="Zaloguj!", border_width=2, corner_radius=10, border_color="#000000", hover_color="#C8C8C8", text_color="#000000", fg_color="transparent", command = lambda: login(loginEntry.get(), passwordEntry.get()))
    loginButton.pack(side="top", pady=20)

