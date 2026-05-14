# Interfejs graficzny informacji o książce

'''

To do:

-podpięcie funkcji (na koniec)

'''

import customtkinter as ctk
import pandas as pd
from PIL import Image
import GlobalVariables
import DashboardInterface
import LoginInterface
import customer_module


def setRating(rate, bookId, userId):
    print(f"Rate: {rate} \nBook id: {bookId} \nUser id: {userId}")

def buyBook(bookId, quantity, errorLabel):
    print(GlobalVariables.userID)
    if GlobalVariables.isLoggedIn == False:
        errorLabel.configure(text="Nie jesteś zalogowany!")
        return

    userID = str(GlobalVariables.userID)
    print(userID)
    quantity = int(quantity)
    bookList = [str(bookId)] * quantity

    if customer_module.buy_book(userID,*bookList) == True:
        errorLabel.configure(text="Udało się")
    else:
        errorLabel.configure(text="Nie udało się")
    print(f"Book id: {bookId} \nquantity: {quantity}")

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
        text_color="#334155",
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
            command=lambda x=window: DashboardInterface.openLoginInterface(x),
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
            command="",
            fg_color="transparent",
            width=150,
            height=50,
            text_color="#3a86ff",
            font=("arial", 20, "bold"),
            hover_color="#002B4A")

        profilButton.pack(side="right", padx=10, pady=5)


    # przycisk do powrotu do dashbordu

    backButton = ctk.CTkButton(
        header,
        text="Powrót do sklepu",
        command=lambda: LoginInterface.openDashboardInterface(window),
        fg_color="transparent",
        width=150,
        height=50,
        text_color="#3a86ff",
        font=("arial", 20, "bold"),
        hover_color="#002B4A")

    backButton.pack(side="right", padx=10, pady=5)



    ##################################################################################################################################

    #wyciąganie danych z pliku
    data = pd.read_excel("DATABASE/book.xlsx")
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



    ########################################################################################################

    # główna sekcja

    mainBox = ctk.CTkFrame(window, fg_color="#001524", corner_radius=0)
    mainBox.pack(side="top", fill="both", expand=True)


    # sekcja informacji o książce

    bookBox = ctk.CTkFrame(
        mainBox,
        corner_radius=15,
        border_width=2,
        fg_color="#1E293B",
        border_color="#3B82F6",
        width=900,
        height=500)

    bookBox.pack_propagate(False)
    bookBox.pack(side="top", pady=100)


    # sekcja na obrazek:

    imageBox = ctk.CTkFrame(
        bookBox,
        fg_color="#1E293B",
        border_width=3,
        border_color="#001524",
        corner_radius=10,
        width=250,
        height=300,)

    imageBox.pack_propagate(False)
    imageBox.pack(side="left", padx=50, pady=15)

    bookCover = ctk.CTkImage(light_image=Image.open("DATABASE/BookCover.jpg"), size=(237, 287))

    imageLabel = ctk.CTkLabel(
        imageBox,
        image=bookCover,
        text="")

    imageLabel.pack(expand=True)


    # sekcja informacji o książce

    bookInfoBox = ctk.CTkFrame(bookBox, fg_color="transparent")
    bookInfoBox.pack(side="right", padx=50, pady=15)


    # tytuł książki

    titleLabel = ctk.CTkLabel(
        bookInfoBox,
        text=f"{title}",
        text_color="#F8FAFC",
        wraplength=200,
        font=("arial", 20, "bold"))

    titleLabel.pack(side="top", pady=10)


    # autor książki

    authorLabel = ctk.CTkLabel(
        bookInfoBox,
        text=f"{author}",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"))

    authorLabel.pack(side="top", pady=20)

    # skala occen
    ratingOptions = ["1","2","3","4","5"]

    #napis oceń książkę
    ratingLabel = ctk.CTkLabel(
        bookInfoBox,
        text="Oceń książkę: ",
        text_color = "#F8FAFC",
        font = ("arial", 16, "bold"),
    )

    ratingLabel.pack(side="top", pady=15)

    #rozwijane menu
    ratingMenu = ctk.CTkOptionMenu(
        bookInfoBox,
        values=ratingOptions,
        command=lambda rate: setRating(rate,bookId,GlobalVariables.userID),
        font=("arial", 16, "bold"),
        anchor="center",
        fg_color="#1E293B",
        button_color="#3B82F6",
        button_hover_color="#2563EB",
        text_color="#F8FAFC",
        dropdown_fg_color="#0F172A",
        dropdown_hover_color="#1E3A8A",
        dropdown_text_color="#F8FAFC",
        corner_radius=10
    )

    ratingMenu.pack(side="top", pady=0)
    ratingMenu.set("Wybierz ocenę")

    #sekcja kupna książki

    buyBox = ctk.CTkFrame(bookInfoBox, fg_color="transparent")
    buyBox.pack(side="top", pady=20)


    # przycisk do zmniejszania ilości zamówienia

    quantitySubButton = ctk.CTkButton(
        buyBox,
        anchor="center",
        text="-",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        width=35,
        height=35,
        fg_color="transparent",
        border_width=2,
        border_color="#3B82F6",
        hover_color="#1E3A8A",
        corner_radius=10,
        command= lambda: subQuantity(quantityOrderEntry))

    quantitySubButton.pack_propagate(False)
    quantitySubButton.pack(side="left", padx=5, pady=5)


    #input do ilości zamówienia

    quantityOrderEntry = ctk.CTkEntry(
        buyBox,
        text_color="#F8FAFC",
        justify="center",
        font=("arial", 16, "bold"),
        width=50,
        height=50,
        border_width=2,
        border_color="#3B82F6",
        corner_radius=10,
        fg_color="transparent")

    quantityOrderEntry.insert(0,"1")
    quantityOrderEntry.pack_propagate(False)
    quantityOrderEntry.pack(side="left", padx=5, pady=5)


    # przycisk do zwiększania ilości zamówienia

    quantityAddButton = ctk.CTkButton(
        buyBox,
        text="+",
        anchor="center",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        width=35,
        height=35,
        fg_color="transparent",
        border_width=2,
        border_color="#3B82F6",
        hover_color="#1E3A8A",
        corner_radius=10,
        command= lambda: addQuantity(quantityOrderEntry, quantity))

    quantityAddButton.pack_propagate(False)
    quantityAddButton.pack(side="left", padx=5, pady=5)

    errorLabel = ctk.CTkLabel(
        mainBox,
        text="",
        anchor="center",
        font=("arial", 16, "bold"),
        text_color="#d62828",
        fg_color="transparent"
    )

    errorLabel.pack(side="bottom", pady=100)


    buyButton = ctk.CTkButton(
        buyBox,
        text="Kup e-booka!",
        text_color="#F8FAFC",
        width=150,
        height=50,
        fg_color="transparent",
        font=("arial", 16, "bold"),
        border_width=2,
        corner_radius=15,
        border_color="#3B82F6",
        command=lambda: buyBook(bookId,quantityOrderEntry.get(), errorLabel),
        hover_color="#1E3A8A")

    buyButton.pack(side="right", padx=10, pady=10)


    # ilość książek

    quantityLabel = ctk.CTkLabel(
        bookInfoBox,
        text=f"Dostępność towaru: \n\n{quantity}",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"))

    quantityLabel.pack(side="top", pady=20)

