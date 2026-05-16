# Interfejs grficzyny do panelu urzytkownika:
import os.path
from tkinter import Entry

import customtkinter as ctk
import pandas as pd

import DashboardInterface
import GlobalVariables
import LoginInterface
import customer_module


def deleteAccount(window):
    result, message = customer_module.delete_customer(str(GlobalVariables.userID),True)
    if result == True:
        GlobalVariables.isLoggedIn = False
        GlobalVariables.userID = 0
        DashboardInterface.makeDashboard(window)

def getAddress():
    data = pd.read_csv("DATABASE/address.csv")
    addressRow = data[data['ID'].astype(str) == str(GlobalVariables.userID)]
    address = {}
    if not addressRow.empty:
        address['STREET'] = addressRow.iloc[0]['STREET']
        address['CITY'] = addressRow.iloc[0]['CITY']
        address['COUNTRY'] = addressRow.iloc[0]['COUNTRY']
    return address

def getBookName(bookId):
    try:
        data = pd.read_excel("DATABASE/book.xlsx")
        book = data[data['ID'].astype(str) == str(bookId)]
        if not book.empty:
            return str(book.iloc[0]['TITLE'])
        else:
            return "Błąd odczytu tytułu książki"
    except Exception as e:
        print(e)
        return "Coś poszło nie tak!"


def readBuyHistory():
    filePath = f"DATABASE/{str(GlobalVariables.userID)}.txt"
    purchases = []

    if not os.path.exists(filePath):
        return purchases

    with open(filePath, 'r', encoding="utf-8") as file:
        currentBook = {}

        for line in file:
            line = line.strip()

            if line.startswith("Zakupiono E-Book ID:"):
                currentBook['ID'] = line.replace("Zakupiono E-Book ID:", "").strip()

            elif line.startswith("Data zakupu:"):
                currentBook['startDate'] = line.replace("Data zakupu:", "").strip()

            elif line.startswith("Dostęp wygasa:"):
                currentBook['endDate'] = line.replace("Dostęp wygasa:", "").strip()

            elif line.startswith("-" * 50):
                if currentBook:
                    purchases.append(currentBook)
                    currentBook = {}

    return purchases


#######################################

def buyHistory(mainBox):

    for widget in mainBox.winfo_children():
        widget.destroy()


    historyBox = ctk.CTkScrollableFrame(
        mainBox,
        width=850,
        height=550,
        corner_radius=15,
        border_width=2,
        fg_color="#1E293B",
        border_color="#3B82F6"
    )

    # historyBox.pack_propagate(False)
    historyBox.pack(side="top", padx=20, pady=(100, 0))
    historyBox._scrollbar.grid_configure(padx=(0, 10))

    historyLabel = ctk.CTkLabel(
        historyBox,
        text="HISTORIA ZAKUPÓW",
        anchor="center",
        font=("arial", 20, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent"
    )

    historyLabel.pack(side="top", pady=(35, 20))

    purchases = readBuyHistory()

    if purchases:
        for index, book in enumerate(purchases, start=1):
            purchaseBox = ctk.CTkFrame(
                historyBox,
                width=400,
                height=150,
                fg_color="transparent"
            )
            purchaseBox.pack(side="top", pady=(20, 15), padx=10, fill="x")

            bookNameLabel = ctk.CTkLabel(
                purchaseBox,
                text=f"{index}.  {getBookName(book['ID'])}",
                anchor="center",
                font=("arial", 16, "bold"),
                text_color="#F8FAFC",
                fg_color="transparent"
            )

            bookNameLabel.pack(side="left", padx=(10, 0))

            endDateLabel = ctk.CTkLabel(
                purchaseBox,
                text=f"Data wygaśnięcia: \n{book['endDate']}",
                anchor="center",
                font=("arial", 16, "bold"),
                text_color="#F8FAFC",
                fg_color="transparent"
            )

            endDateLabel.pack(side="right", padx=(10, 10))

            startDateLabel = ctk.CTkLabel(
                purchaseBox,
                text=f"Data zakupu: \n{book['startDate']}",
                anchor="center",
                font=("arial", 16, "bold"),
                text_color="#F8FAFC",
                fg_color="transparent"
            )

            startDateLabel.pack(side="right", padx=(0, 10))
    else:
        purchaseBox = ctk.CTkFrame(
            historyBox,
            width=400,
            height=150,
            fg_color="transparent"
        )
        purchaseBox.pack(side="top", pady=(5, 15))

        errorLabel = ctk.CTkLabel(
            purchaseBox,
            text="Nie kupiłeś jescze ani jednego e-booka",
            anchor="center",
            font=("arial", 16, "bold"),
            text_color="#F8FAFC",
            fg_color="transparent"
        )
        errorLabel.pack(side='top', pady=(15, 0))

#########################################


########################################

def address(mainBox):

    for widget in mainBox.winfo_children():
        widget.destroy()


    addressBox = ctk.CTkFrame(
        mainBox,
        width=850,
        height=550,
        corner_radius=15,
        border_width=2,
        fg_color="#1E293B",
        border_color="#3B82F6"
    )

    addressBox.pack_propagate(False)
    addressBox.pack(side="top", padx=20, pady=(100, 0))

    address = getAddress()

    addressLabel = ctk.CTkLabel(
        addressBox,
        text="ADRES",
        anchor="center",
        font=("arial", 20, "bold"),
        text_color="#F8FAFC",
        fg_color="transparent"
    )

    addressLabel.pack(side="top", pady=(35, 20))

    if address:
        streetLabel = ctk.CTkLabel(
            addressBox,
            text="Ulica: ",
            anchor="center",
            font=("arial", 16, "bold"),
            text_color="#F8FAFC",
            fg_color="transparent"
        )

        streetLabel.pack(side="top", pady=(10, 15))

        streetEntry = ctk.CTkEntry(
            addressBox,
            placeholder_text=address['STREET'],
            width=250,
            height=40,
            justify="center",
            fg_color="transparent",
            text_color="#F8FAFC",
            font=("arial", 16, "bold"),
            border_width=2,
            border_color="#3B82F6",
            corner_radius=20,
            placeholder_text_color="#939699"
        )

        streetEntry.pack(side="top", pady=(0, 15))

        cityLabel = ctk.CTkLabel(
            addressBox,
            text="Miasto: ",
            anchor="center",
            font=("arial", 16, "bold"),
            text_color="#F8FAFC",
            fg_color="transparent"
        )

        cityLabel.pack(side="top", pady=(0, 15))

        cityEntry = ctk.CTkEntry(
            addressBox,
            placeholder_text=address['CITY'],
            width=250,
            height=40,
            justify="center",
            fg_color="transparent",
            text_color="#F8FAFC",
            font=("arial", 16, "bold"),
            border_width=2,
            border_color="#3B82F6",
            corner_radius=20,
            placeholder_text_color="#939699"
        )

        cityEntry.pack(side="top", pady=(0, 15))

        countryLabel = ctk.CTkLabel(
            addressBox,
            text="Państwo: ",
            anchor="center",
            font=("arial", 16, "bold"),
            text_color="#F8FAFC",
            fg_color="transparent"
        )

        countryLabel.pack(side="top", pady=(0, 15))

        countryEntry = ctk.CTkEntry(
            addressBox,
            placeholder_text=address['COUNTRY'],
            width=250,
            height=40,
            justify="center",
            fg_color="transparent",
            text_color="#F8FAFC",
            font=("arial", 16, "bold"),
            border_width=2,
            border_color="#3B82F6",
            corner_radius=20,
            placeholder_text_color="#939699"
        )

        countryEntry.pack(side="top", pady=(0, 15))

        addressEditButton = ctk.CTkButton(
            addressBox,
            text="Edytuj Dane",
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

        addressEditButton.pack(side="top", pady=(15, 0))

#########################################

def makeUserInterface(window):
    '''
        funkcja tworzy interfejs panelu urzytkownika
        Args:
            window (TK): główne okno interfejsu
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
        text_color="#3a86ff",
        hover_color="#E69A9A",
        font=("arial", 20, "bold"),
        command=window.destroy
    )
    closeButton.pack(side="right", padx=10, pady=5)

    # przycisk do panelu urzytkownika


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

    historyButton = ctk.CTkButton(
        buttonBox,
        text="HISTORIA ZAKUPÓW",
        command=lambda :buyHistory(mainBox),
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

    historyButton.pack(side="left",padx=(0,50))

    adressButton = ctk.CTkButton(
        buttonBox,
        text="ADRES",
        command=lambda : address(mainBox),
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

    adressButton.pack(side="left", padx=(0, 50))

    deleteButton = ctk.CTkButton(
        buttonBox,
        text="USUŃ KONTO",
        command=lambda : deleteAccount(window),
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

    deleteButton.pack(side="left", padx=(0, 0))

    #################################

    buyHistory(mainBox)
