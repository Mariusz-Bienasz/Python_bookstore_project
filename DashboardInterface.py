# Interfejs graficzny głównej strony
'''

To do:
-rozmiary
-odstępy
-podpięcie funkcji (na koniec)

'''


import customtkinter as ctk
import pandas as pd

import AdminInterface
import BookInterface
import GlobalVariables
import LoginInterface
import RatingSystem
import UserInterface

def openUserInterface(window):
    '''
        Funkcja do przełączania interfejsu

        Args:
            window (tk): główne okno interfejsu
        Returns:
            Brak
    '''

    for widget in window.winfo_children():
        widget.destroy()

    UserInterface.makeUserInterface(window)

def openAdminInterface(window):
    '''
        Funkcja do przełączania interfejsu

        Args:
            window (tk): główne okno interfejsu
        Returns:
            Brak
    '''

    for widget in window.winfo_children():
        widget.destroy()

    AdminInterface.makeAdminInterface(window)

def openLoginInterface(window):
    '''
        Funkcja do przełączania interfejsu

        Args:
            window (tk): główne okno interfejsu
        Returns:
            Brak
    '''

    for widget in window.winfo_children():
        widget.destroy()

    LoginInterface.makeLoginInterface(window)


def openBookInterface(window, bookId):
    '''
        funkcja do przekierowywania do strony książki

        Args:
            window (tk): główne okno interfejsu
            bookID : id książki
        Returns:
            brak
    '''

    for widget in window.winfo_children():
        widget.destroy()

    BookInterface.makeBookInterface(window,bookId)



def makeDashboard(window):
    '''
        funkcja tworzy główny interfejs programu, wyświetla książki z bazdy danych

        Args:
            window (TK): główne okno interfejsu
        Returns:
            brak
    '''

    # Pasek nagłówkowy
    header = ctk.CTkFrame(window, fg_color="#001524", corner_radius=0, height=80)
    header.pack_propagate(False) # blokowanie zmiany rozmiaru
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

    # Sprawdzanie czy użytkownik jest zalogowany
    if GlobalVariables.isLoggedIn == False:

        # przejście do logowania i rejsetracji
        loginButton = ctk.CTkButton(
            header,
            text="Zaloguj się",
            command= lambda x=window:openLoginInterface(x),
            fg_color="transparent",
            width=150,
            height=50,
            text_color="#3a86ff",
            font=("arial", 20, "bold"),
            hover_color="#002B4A")

        loginButton.pack(side="right", padx=10, pady=5)

    else:
        # przejście do profilu użytkownika , albo cos innego (jeszcze nie wiem)
        profilButton = ctk.CTkButton(
            header,
            text="Twój profil",
            command=lambda : openUserInterface(window),
            fg_color="transparent",
            width=150,
            height=50,
            text_color="#3a86ff",
            font=("arial", 20, "bold"),
            hover_color="#002B4A")

        profilButton.pack(side="right", padx=10, pady=5)

    # sprawdzanie czy to admin
    if GlobalVariables.isAdmin == True:
        #przycisk do panelu admina
        adminButton = ctk.CTkButton(
            header,
            text="Panel admina",
            command=lambda: openAdminInterface(window),
            fg_color="transparent",
            width=150,
            height=50,
            text_color="#3a86ff",
            font=("arial", 20, "bold"),
            hover_color="#002B4A"
        )
        adminButton.pack(side="right", padx=10, pady=5)

    # główna sekcja dashbordu
    mainBox =  ctk.CTkScrollableFrame(window, fg_color="#001524", corner_radius=0)
    mainBox.pack(side="top", fill="both", expand=True)

    # dane pobrane z pliku
    data = pd.read_excel("DATABASE/book.xlsx")

    # maksymalna ilośc kolumn
    maxColumns = 4

    # pętla dla kazdego wiersza w pliku
    for index, row in data.iterrows():
        #przypisanie wartości do zmiennnych
        id = row['ID']
        author = row['AUTHOR']
        title = row['TITLE']
        quantity = row['NO_EBOOK_AVAILABLE']

        # jakieś obliczenia pozycji xd
        columnGrid = index % maxColumns
        rowGrid = index // maxColumns

        # sekcja książki
        bookFrame = ctk.CTkFrame(
            mainBox,
            width=200,
            height=300,
            fg_color="#1E293B",
            border_color="#3B82F6",
            border_width=2,
            corner_radius=15,)

        bookFrame.pack_propagate(False)
        bookFrame.grid(row=rowGrid, column=columnGrid, padx=25, pady=15, sticky="nsew")

        #tytuł
        titleLabel = ctk.CTkLabel(
            bookFrame,
            anchor="center",
            text=f'Tytuł: \n{title}',
            font=("arial",14,"bold"),
            fg_color="transparent",
            wraplength=180,
            text_color="#F8FAFC")

        titleLabel.pack(side="top", pady=(20, 0))

        # autor
        authorLabel = ctk.CTkLabel(
            bookFrame,
            anchor="center",
            text=f'Autor: \n{author}',
            font=("arial",14,"bold"),
            fg_color="transparent",
            text_color="#F8FAFC")

        authorLabel.pack(side="top", pady=(20,0))

        # ilość
        quantityLabel = ctk.CTkLabel(
            bookFrame,
            anchor="center",
            text=f'Ilość: \n{quantity}',
            font=("arial", 14, "bold"),
            fg_color="transparent",
            text_color="#F8FAFC")

        quantityLabel.pack(side="top", pady=(20,0))

        rateLabel = ctk.CTkLabel(
            bookFrame,
            anchor="center",
            text=f'Ocena: \n{RatingSystem.getMeanRate(id)}',
            font=("arial", 14, "bold"),
            fg_color="transparent",
            text_color="#F8FAFC")

        rateLabel.pack(side="top", pady=(20,0))

        # przycisk kup
        buyButton = ctk.CTkButton(
            bookFrame,
            anchor="center",
            text="Zobacz więcej",
            command=lambda  bookId=id:openBookInterface(window, bookId),
            fg_color="transparent",
            width=150,
            height=40,
            text_color="#F8FAFC",
            hover_color="#1E3A8A",
            font=("arial",16,"bold"),
            border_width=2,
            border_color="#3B82F6")

        buyButton.pack(side="bottom", padx=5, pady=20)


    # coś tam z pozycją, sam dokładnie nie wiem co to robi
    for i in range(maxColumns):
        mainBox.grid_columnconfigure(i, weight=1)
