# Interfejs graficzny panelu admina:

'''

To do:

-podpięcie funkcji (na koniec)

'''


import customtkinter as ctk
import pandas as pd

import DashboardInterface
import LoginInterface

def addBook(author,title,quantity, label):
    '''
        Funkcja do podłączenia modułu dodawania książki
        Args:
            author : autor książki
            title : tytuł książki
            quantity : ilość e-booków
            label: miejsce do wyświetlania wyników
        Returns:
            Brak
    '''
    print(f"Author: {author} \nTitle: {title} \nQuantity: {quantity}")

def deleteBook(bookId, label):
    '''
        Funkcja do podłączenia modułu usuwania książki

        Args:
            bookId : numer książki
            label: miejsce do wyświetlania wyników
        Returns:
            Brak
    '''

    print(f"Book id: {bookId}")

def searchId(bookId, data, labels, entry):
    '''
        Funkcja do szukania książki po id

        Args:
            bookId : numer książki
            data: baza danych
            labels: miejsca do wyświetlania informacji
            entry: input id
        Returns:
            Brak
    '''
    headers = ["Autor: \n","Tytuł: \n","Ilość: \n","Data utworzenia: \n","Data zaktualizowania: \n"]
    entry.delete(0,"end")
    entry.insert(0, str(bookId))
    if bookId == "" or bookId == "Wybierz id":
        for i in range(len(labels)):
            labels[i].configure(text=headers[i])
        return
    try:
        bookIdInt= int(bookId)
        result = data[data['ID'] == bookIdInt]
    except ValueError:
        return

    if not result.empty:
        row = result.iloc[0]
        dataToShow = [
            str(row['AUTHOR']),
            str(row['TITLE']),
            str(row['NO_EBOOK_AVAILABLE']),
            str(row['CREATED']),
            str(row['UPDATED'])
        ]

        for i in range(len(labels)):
            labels[i].configure(text=headers[i] + dataToShow[i])
    else:
        for i in range(len(labels)):
            labels[i].configure(text=headers[i] + "---")


def makeAdminInterface(window):
    '''
        funkcja tworzy interfejs panelu admina, (opcja dodawania i usuwania książęk)
        Args:
            window (TK): główne okno interfejsu
        Returns:
            brak
    '''


    idInputValidate = (window.register(LoginInterface.numbersCheck), '%P')

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
        text_color="#3a86ff",
        hover_color="#E69A9A",
        font=("arial", 20, "bold"),
        command=window.destroy
    )
    closeButton.pack(side="right", padx=10, pady=5)


    # przycisk do panelu urzytkownika

    profilButton = ctk.CTkButton(
        header,
        text="Twój profil",
        command=lambda : DashboardInterface.openUserInterface(window),
        fg_color="transparent",
        width=150,
        height=50,
        text_color="#3a86ff",
        font=("arial", 20, "bold"),
        hover_color="#002B4A")
    profilButton.pack(side="right", padx=10, pady=5)


    # Przycisk powrotu do głównej strony

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


    # Główna sekcja:

    mainBox = ctk.CTkScrollableFrame(window, fg_color="#001524", corner_radius=0)
    mainBox.pack(side="top", fill="both", expand=True)


    #   Sekcja usuwania książek

    deleteBox = ctk.CTkFrame(
        mainBox,
        width=850,
        height=550,
        corner_radius=15,
        border_width=2,
        fg_color="#1E293B",
        border_color="#3B82F6",
    )

    deleteBox.pack_propagate(False)
    deleteBox.pack(side="top", padx=20, pady=(100,0))


    # Nazwa formularza

    formNameLabel = ctk.CTkLabel(
        deleteBox,
        text="------------ Usuń książkę ------------",
        anchor="center",
        font = ("arial", 20, "bold"),
        text_color = "#F8FAFC",
        fg_color = "transparent"
    )
    formNameLabel.pack(side="top", pady=30)

    # napis 'Podaj numer książki:'

    idInputLabel = ctk.CTkLabel(
        deleteBox,
        text="Podaj numer książki: ",
        anchor="center",
        font = ("arial", 20, "bold"),
        text_color = "#F8FAFC",
        fg_color = "transparent"
    )

    idInputLabel.pack(side="top", pady=20)

    idBox = ctk.CTkFrame(deleteBox,fg_color="transparent")
    idBox.pack(side="top")

    #########################
    # sekcja informacji wybranej książki


    infoBox = ctk.CTkFrame(
        deleteBox,
        fg_color="transparent",

    )
    infoBox.pack(side="top", pady=40)


    # lewa strona sekcji

    leftSideBox = ctk.CTkFrame(
        infoBox,
        fg_color="transparent"
    )
    leftSideBox.pack(side="left")

    # autor

    authorLabel = ctk.CTkLabel(
        leftSideBox,
        width=200,
        height=40,
        anchor="center",
        wraplength=180,
        text="Autor: ",
        font=("arial", 16, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent"
    )

    authorLabel.pack(side="top")


    #tytuł

    titleLabel = ctk.CTkLabel(
        leftSideBox,
        width=200,
        height=40,
        anchor="center",
        wraplength=180,
        text="Tytuł: ",
        font=("arial", 16, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent"
    )

    titleLabel.pack(side="top", pady=(10, 0))


    # środkowa strona sekcji

    midleSideBox = ctk.CTkFrame(
        infoBox,
        fg_color="transparent"
    )
    midleSideBox.pack(side="left", padx=10)


    # ilość

    quantityLabel = ctk.CTkLabel(
        midleSideBox,
        width=200,
        height=40,
        anchor="center",
        wraplength=180,
        text="Ilość: ",
        font=("arial", 16, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent"
    )

    quantityLabel.pack(side="top")


    #data utworzenia

    createdLabel = ctk.CTkLabel(
        midleSideBox,
        width=200,
        height=40,
        anchor="center",
        wraplength=180,
        text="Data utworzenia: ",
        font=("arial", 16, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent"
    )

    createdLabel.pack(side="top", pady=(10, 0))


    # prawa strona sekcji

    rightSideBox = ctk.CTkFrame(
        infoBox,
        fg_color="transparent"
    )
    rightSideBox.pack(side="left", padx=10)


    # data aktualizacji

    updatedLabel = ctk.CTkLabel(
        rightSideBox,
        width=200,
        height=40,
        anchor="center",
        wraplength=180,
        text="Data zaktualizowania: ",
        font=("arial", 16, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent"
    )

    updatedLabel.pack(side="top")


    # lista labelów książki

    bookInfoLabels = [authorLabel, titleLabel, quantityLabel, createdLabel, updatedLabel]


    #########################

    # pobieranie danych z pliku

    data = pd.read_excel("DATABASE/book.xlsx")

    #wszystkie id książek
    allId= data['ID'].astype(str).tolist()


    #rozwijana lista z id

    idInputMenu = ctk.CTkOptionMenu(
        idBox,
        values=allId,
        command= lambda id: searchId(id,data,bookInfoLabels, idInputEntry),
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

    idInputMenu.pack(side="left", pady=0, padx=30)
    idInputMenu.set("Wybierz id")


    # przycisk szukaj

    idSearchButton = ctk.CTkButton(
        idBox,
        text="Szukaj",
        width=40,
        height=40,
        command=lambda: searchId(idInputEntry.get(),data,bookInfoLabels, idInputEntry),
        anchor="center",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        fg_color="transparent",
        border_width=2,
        border_color="#3B82F6",
        hover_color="#1E3A8A",
        corner_radius=10
    )

    idSearchButton.pack(side="right", pady=0, padx=0)


    # input id książki

    idInputEntry = ctk.CTkEntry(
        idBox,
        width=250,
        height=40,
        justify="center",
        fg_color="transparent",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        border_width=2,
        border_color="#3B82F6",
        corner_radius=20,
        placeholder_text="Podaj numer id książki",
        placeholder_text_color="#939699",
        validate="key",
        validatecommand=idInputValidate
    )

    idInputEntry.pack(side="right", pady=0, padx=(30,10))


    # miejsce na wypisywanie błędów

    errorDeleteLabel = ctk.CTkLabel(
        deleteBox,
        text="",
        font=("arial", 16, "bold"),
        text_color="#d62828",
        fg_color="transparent"
    )

    errorDeleteLabel.pack(side="top", pady=10)

    # przycisk do usuwania

    deleteButton = ctk.CTkButton(
        deleteBox,
        command=lambda: deleteBook(idInputEntry.get(), errorDeleteLabel),
        text="Usuń",
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

    deleteButton.pack(side="top", pady=(50, 0))


    ##############################################################
    #
    #     Sekcja dodawania książki
    #
    ##############################################################


    addBox = ctk.CTkFrame(
        mainBox,
        width=850,
        height=550,
        corner_radius=15,
        border_width=2,
        fg_color="#1E293B",
        border_color="#3B82F6",
    )

    addBox.pack_propagate(False)
    addBox.pack(side="top", padx=20, pady=(100, 50))


    # Nazwa formularza

    formNameLabel = ctk.CTkLabel(
        addBox,
        text="------------ Dodaj książkę ------------",
        anchor="center",
        font=("arial", 20, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent"
    )
    formNameLabel.pack(side="top", pady=30)


    # sekcja napisów dodawania książki

    addBookLabels = ctk.CTkFrame(
        addBox,
        fg_color="transparent"
    )
    addBookLabels.pack(side="top", pady=(60,0))


    #label autora

    authorAddLabel = ctk.CTkLabel(
        addBookLabels,
        width=200,
        height=40,
        text="Podaj autora:",
        anchor="center",
        font=("arial", 20, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent"
    )

    authorAddLabel.pack(side="left")


    # label tytułu

    titleAddLabel = ctk.CTkLabel(
        addBookLabels,
        width=200,
        height=40,
        text="Podaj tytuł:",
        anchor="center",
        font=("arial", 20, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent"
    )

    titleAddLabel.pack(side="left", pady=10)


    # label ilości

    quantityAddLabel = ctk.CTkLabel(
        addBookLabels,
        width=200,
        height=40,
        text="Podaj ilość:",
        anchor="center",
        font=("arial", 20, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent"
    )

    quantityAddLabel.pack(side="left")


    # sekcja inputów doadawania książki

    addBookEntry = ctk.CTkFrame(
        addBox,
        fg_color="transparent"
    )
    addBookEntry.pack(side="top", pady=(15,0))


    # input autora

    authorAddEntry = ctk.CTkEntry(
        addBookEntry,
        width=200,
        height=40,
        fg_color="transparent",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        border_width=2,
        border_color="#3B82F6",
        corner_radius=20
    )

    authorAddEntry.pack(side="left")


    #input tytułu

    titleAddEntry = ctk.CTkEntry(
        addBookEntry,
        width=200,
        height=40,
        fg_color="transparent",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        border_width=2,
        border_color="#3B82F6",
        corner_radius=20
    )

    titleAddEntry.pack(side="left", padx=10)


    #input ilośći

    quantityAddEntry = ctk.CTkEntry(
        addBookEntry,
        width=200,
        height=40,
        fg_color="transparent",
        text_color="#F8FAFC",
        font=("arial", 16, "bold"),
        border_width=2,
        border_color="#3B82F6",
        corner_radius=20,
        validate = "key",
        validatecommand = idInputValidate
    )

    quantityAddEntry.pack(side="left")


    # przycisk dodawania książki

    addBookButton = ctk.CTkButton(
        addBox,
        command=lambda: addBook(authorAddEntry.get(),titleAddEntry.get(),quantityAddEntry.get(), errorAddLabel),
        text="Dodaj",
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

    addBookButton.pack(side="bottom", pady=(10,50))


    # miejsce na wypisywanie błędów

    errorAddLabel = ctk.CTkLabel(
        addBox,
        text="",
        font=("arial", 16, "bold"),
        text_color="#d62828",
        fg_color="transparent"
    )

    errorAddLabel.pack(side="bottom", pady=(0,40))