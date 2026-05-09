# Interfejs graficzny głównej strony
'''

To do:
-kolory
-odstępy
-podpięcie funkcji (na koniec)

'''


import customtkinter as ctk
import pandas as pd
import GlobalVariables
import LoginInterface


'''
    Funkcja do przełączania interfejsu

    Args:
        window (tk): główne okno interfejsu
    Returns:
        Brak
'''
def openLoginInterface(window):
    for widget in window.winfo_children():
        widget.destroy()

    LoginInterface.makeLoginInterface(window)

'''
    przyszła funkcja do przekierowywania książki do kupna

    Args:
        bookID : id książki
    Returns:
        brak
'''
def buyBook(bookID):
    print(bookID)


'''
    funkcja tworzy główny interfejs programu, wyświetla książki z bazdy danych
    
    Args:
        window (TK): główne okno interfejsu
    Returns:
        brak 
'''
def makeDashboard(window):
    # Pasek nagłówkowy
    header = ctk.CTkFrame(window, fg_color="#DCDCDC")
    header.pack(side="top", fill="x")

    # Napis w nagłówku
    appNameLabel = ctk.CTkLabel(header, text="Internetowa Księgarnia", font=("arial", 16, "bold"), text_color="#3498db", fg_color="#DCDCDC")
    appNameLabel.pack(side="left", padx=10, pady=5)

    # Sprawdzanie czy użytkownik jest zalogowany
    if GlobalVariables.isLoggedIn == False:
        # przejście do logowania i rejsetracji
        loginButton = ctk.CTkButton(header, text="Zaloguj się", command= lambda x=window:openLoginInterface(x), fg_color="transparent", text_color="#334155", hover_color="#C8C8C8")
        loginButton.pack(side="right", padx=10, pady=5)

        # loginButton  = tk.Button(header, text="Zaloguj się", command=lambda x=window: openLoginInterface(x), relief="flat", font=("arial",12), background="#DCDCDC")
    else:
        # przejście do profilu użytkownika , albo cos innego (jeszcze nie wiem)
        profilButton = ctk.CTkButton(header, text="Twój profil", command="", fg_color="transparent", text_color="#334155", hover_color="#C8C8C8")
        profilButton.pack(side="right", padx=10, pady=5)

        # profilButton = tk.Button(header, text="Twój profil", command="", relief="flat", font=("arial",12), background="#DCDCDC")

    # główna sekcja dashbordu
    mainBox =  ctk.CTkFrame(window, fg_color="#DCDCDC")
    mainBox.pack(side="top", fill="both", expand=True)

    # dane pobrane z pliku
    data = pd.read_excel("DATABASE/bookNew.xlsx")

    # maksymalna ilośc kolumn
    maxColumns = 3

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
        bookFrame = ctk.CTkFrame(mainBox, width=200, height=250, fg_color="#FFFFFF", border_color="#334155", border_width=2, corner_radius=15,bg_color="#DCDCDC")
        bookFrame.pack_propagate(False)
        bookFrame.grid(row=rowGrid, column=columnGrid, padx=15, pady=15, sticky="nsew")

        #tytuł
        titleLabel = ctk.CTkLabel(bookFrame, text=f'Tytuł: \n{title}',
                              font=("arial",12,"bold"),
                              fg_color="transparent",
                              text_color="#334155")
        titleLabel.pack(side="top", pady=(15, 0))

        # autor
        authorLabel = ctk.CTkLabel(bookFrame, text=f'Autor: \n{author}',
                               font=("arial",12,"bold"),
                               fg_color="transparent",
                               text_color="#334155")
        authorLabel.pack(side="top", pady=10)

        # ilość
        quantityLabel = ctk.CTkLabel(bookFrame, text=f'Ilość: \n{quantity}',
                               font=("arial", 12, "bold"),
                               fg_color="transparent",
                               text_color="#334155")
        quantityLabel.pack(side="top", pady=5)

        # przycisk kup
        buyButton = ctk.CTkButton(bookFrame, text="Kup e-book", command=lambda  bookId=id:buyBook(bookId), fg_color="transparent", text_color="#334155", hover_color="#C8C8C8", font=("arial",12,"bold"), border_width=2, border_color="#000000")
        buyButton.pack(side="bottom", padx=5, pady=20)

        #buyButton =  tk.Button(bookFrame, text="Kup e-book", command=lambda bookId=id: buyBook(bookId), bd=1, relief="ridge", background="#FFFFFF", fg="#334155")

    # coś tam z pozycją, sam dokładnie nie wiem co to robi
    for i in range(maxColumns):
        mainBox.grid_columnconfigure(i, weight=1)
