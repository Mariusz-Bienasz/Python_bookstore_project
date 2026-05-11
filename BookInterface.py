# Interfejs graficzny informacji o książce

'''

To do:
-przycisk buy
-funkcja buy
-dokumentacja
-podpięcie funkcji (na koniec)

'''

import customtkinter as ctk
import pandas as pd
import GlobalVariables
import DashboardInterface
import LoginInterface

def addQuantity(quantityOrderEntry, quantity):
    '''
        Funkcja do zwiększania ilości zamówienia

        Args:
            quantityOrderEntry: input do wpisywania ilości zamówienia
        Returns:
            Brak
    '''
    x = int(quantityOrderEntry.get())
    if x < quantity:
        x += 1
        quantityOrderEntry.delete(0, 'end')
        quantityOrderEntry.insert(0, str(x))

def subQuantity(quantityOrderEntry):
    '''
        Funkcja do zmniejszania ilości zamówienia

        Args:
            quantityOrderEntry: input do wpisywania ilości zamówienia
        Returns:
            Brak
        '''
    x = int(quantityOrderEntry.get())
    if x >1:
        x -= 1
        quantityOrderEntry.delete(0, 'end')
        quantityOrderEntry.insert(0, str(x))

def makeBookInterface(window, bookId):
    '''
        funkcja tworzy  interfejs ksiązki, wyświetla informacje książki z bazdy danych i możliwość zakupu

        Args:
            window (TK): główne okno interfejsu
            bookId: id ksiązki
        Returns:
            brak
    '''

    # Pasek nagłówkowy
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

    # Sprawdzanie czy użytkownik jest zalogowany
    if GlobalVariables.isLoggedIn == False:

        # przejście do logowania i rejsetracji
        loginButton = ctk.CTkButton(
            header,
            text="Zaloguj się",
            command=lambda x=window: DashboardInterface.openLoginInterface(x),
            fg_color="transparent",
            text_color="#334155",
            hover_color="#C8C8C8")

        loginButton.pack(side="right", padx=10, pady=5)

    else:
        # przejście do profilu użytkownika , albo cos innego (jeszcze nie wiem)
        profilButton = ctk.CTkButton(
            header,
            text="Twój profil",
            command="",
            fg_color="transparent",
            text_color="#334155",
            hover_color="#C8C8C8")

        profilButton.pack(side="right", padx=10, pady=5)


    # przycisk do powrotu do dashbordu

    backButton = ctk.CTkButton(
        header,
        text="Powrót do sklepu",
        command=lambda: LoginInterface.openDashboardInterface(window),
        fg_color="transparent",
        text_color="#334155",
        hover_color="#C8C8C8")

    backButton.pack(side="right", padx=10, pady=5)

    ##########################

    #wyciąganie danych z pliku
    data = pd.read_excel("DATABASE/bookNew.xlsx")
    # jedna konkretna ksiązka
    book = data[data['ID'] == bookId]

    #pozyskanie poszczególnych danych
    if not book.empty:
        row = book.iloc[0]
        author = row['AUTHOR']
        title = row['TITLE']
        quantity = row['NO_EBOOK_AVAILABLE']
    else:
        author = "Error"
        title = "Error"
        quantity = "Error"


    # główna sekcja

    mainBox = ctk.CTkFrame(window, fg_color="#DCDCDC", corner_radius=0)
    mainBox.pack(side="top", fill="both", expand=True)


    # sekcja informacji o książce

    bookBox = ctk.CTkFrame(mainBox, corner_radius=15, border_width=2, fg_color="#ffffff", width=400, height=700)
    bookBox.pack_propagate(False)
    bookBox.pack(side="top", pady=20)


    # autor książki

    authorLabel = ctk.CTkLabel(
        bookBox,
        text=f"{author}",
        text_color="#000000",
        font=("arial", 16, "bold"))

    authorLabel.pack(side="top", pady=10)


    # tytuł książki

    titleLabel = ctk.CTkLabel(
        bookBox,
        text=f"{title}",
        text_color="#000000",
        font=("arial", 16, "bold"))

    titleLabel.pack(side="top", pady=10)


    # ilość książek

    quantityLabel = ctk.CTkLabel(
        bookBox,
        text=f"Dostępność towaru: \n{quantity}",
        text_color="#000000",
        font=("arial", 16, "bold"))

    quantityLabel.pack(side="top", pady=10)


    #sekcja kupna książki

    buyBox = ctk.CTkFrame(bookBox, fg_color="transparent")
    buyBox.pack(side="top", pady=20)


    # przycisk do zmniejszania ilości zamówienia

    quantitySubButton = ctk.CTkButton(
        buyBox,
        text="-",
        text_color="#000000",
        font=("arial", 16, "bold"),
        width=35,
        height=35,
        fg_color="transparent",
        border_width=2,
        border_color="#000000",
        corner_radius=10,
        command= lambda: subQuantity(quantityOrderEntry))

    quantitySubButton.pack_propagate(False)
    quantitySubButton.pack(side="left", padx=5, pady=5)


    #input do ilości zamówienia

    quantityOrderEntry = ctk.CTkEntry(
        buyBox,
        text_color="#000000",
        justify="center",
        font=("arial", 16, "bold"),
        width=50,
        height=50,
        border_width=2,
        border_color="#000000",
        corner_radius=10,
        fg_color="transparent")

    quantityOrderEntry.insert(0,"1")
    quantityOrderEntry.pack_propagate(False)
    quantityOrderEntry.pack(side="left", padx=5, pady=5)


    # przycisk do zwiększania ilości zamówienia

    quantityAddButton = ctk.CTkButton(
        buyBox,
        text="+",
        text_color="#000000",
        font=("arial", 16, "bold"),
        width=35,
        height=35,
        fg_color="transparent",
        border_width=2,
        border_color="#000000",
        corner_radius=10,
        command= lambda: addQuantity(quantityOrderEntry, quantity))

    quantityAddButton.pack_propagate(False)
    quantityAddButton.pack(side="left", padx=5, pady=5)
