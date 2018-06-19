# -*- coding: utf-8 -*-
import pymysql
import dbconn.auth as dbconn
import getpass

class DBConn:
    def __init__(self):

        while (True):
            print("--------------------------------")
            print("KONFIGURATOR CEN OSŁON OKIENNYCH")
            print("--------------------------------")
            quit = input('1.Logowanie, 2.Wyjście  ')

            if (quit == '2'):
                break
            self.connString()
            perm = self.login()
            if perm == 0:
                print('---------------------------------------------------------------')
                print('            ZALOGOWANO JAKO ADMINISTRATOR                      ')
                print('---------------------------------------------------------------')
                self.Admin()

            elif perm == 1:
                print('---------------------------------------------------------------')
                print('     WITAMY W KONFIGURATORZE ZALUZJI PLISOWANYCH i ROLET       ')
                print('---------------------------------------------------------------')
                self.User()

            else:
                print('Błąd logowania!')

    def connString(self):  # Ustanowienie połączenia z bazą mysql
        self.conn = pymysql.connect(host='localhost', user=dbconn.user, password=dbconn.user, db=dbconn.db, charset='utf8',
                                    use_unicode=True)
        self.c = self.conn.cursor()

    def login(self):  # logowanie - pobiera maila i hasło z mysql i sprawdza przypisane uprawnienia
        login = input('Podaj swój login: ')
        password = input('Podaj swoje hasło: ')
        self.c.execute('SELECT id_roli FROM Logowanie WHERE login=%s AND password=%s;', (login, password))
        try:
            perm = self.c.fetchall()[0][0]
        except:
            perm = -1
        return perm

    def User(self):  # Menu Usera
        while (True):
            dec = input('\n1. Konfiguruj produkt\n2. Wyjdź\n')
            if (dec == '1'):
                self.selectProduct()
                self.selectDim()
                self.selectModel()
                self.selectProfil()
                self.selectMaterial()
                self.selectMontaz()
                self.selectIlosc()
                self.insertall()
            elif (dec == '2'):
                self.connClose()
            else:
                print('Nieprawidłowy wybór')

    def selectProduct(self): # wyświetla listę produktów z wymiarami do wyboru
            self.c.execute('SELECT DISTINCT idnazwa, nazwa FROM Produkt')
            print('\n\t\t   PRODUKTY\n')
            print('%3s %20s' % ("ID", "Produkt"))
            print('________________________________________________')
            for row in self.c.fetchall():
                print('%3s %20s' % (row[0], row[1]))
            self.produktid = input("\nWybierz id produktu\t\t\t")
    def selectDim(self): # wyświetla listę dostępnych wymiarów
            self.c.execute('SELECT id,nazwa,szer,wys,cenabazowa FROM Produkt;')
            print('\n\t\tWYMIARY\n')
            print('%3s %20s %5s %5s' % ("ID", "Produkt", "Szer.", "Wys."))
            print('_________________________________________________')
            for row in self.c.fetchall():
                print('%3s %20s %5s %5s' % (row[0], row[1], row[2], row[3]))
            self.dimid = input("\nWybierz id wymiaru\t\t")
    def selectModel(self): # wyświetla listę modeli produktu
            self.c.execute('SELECT ID, nazwa_modelu FROM Model_produktu')
            print('\n\t\tMODEL PRODUKTU\n')
            print('%3s %22s' % ("ID", "Model Produktu"))
            print('__________________________________________')
            for row in self.c.fetchall():
                print('%3s %22s' % (row[0], row[1]))
            self.modelid = input("\nWybierz id modelu \t")
    def selectProfil(self):
            self.c.execute('SELECT ID, nazwy_k_p FROM Kolor_profili')
            print('\n\t\tKOLOR PROFILI\n')
            print('%3s %22s' % ("ID", "Kolor Profili"))
            print('__________________________________________')
            for row in self.c.fetchall():
                print('%3s %22s' % (row[0], row[1]))
            self.profilid = input("\nWybierz id koloru profili \t")
    def selectMaterial(self):
            self.c.execute('SELECT ID, nazwy_mat FROM Materialy')
            print('\n\t\tKOLOR MATERIAŁU\n')
            print('%3s %22s' % ("ID", "Kolor Materiału"))
            print('__________________________________________')
            for row in self.c.fetchall():
                print('%3s %22s' % (row[0], row[1]))
            self.materialid = input("\nWybierz id koloru materiału \t")
    def selectMontaz(self):
            self.c.execute('SELECT ID, nazwa_typu FROM Typy_montazu')
            print('\n\t\tTYP MONTAŻU\n')
            print('%3s %25s' % ("ID", "Typ montażu"))
            print('__________________________________________')
            for row in self.c.fetchall():
                print('%3s %25s' % (row[0], row[1]))
            self.montazid = input("\nWybierz id rodzaju montażu\t")


    def selectIlosc(self): # wyświetla ilość szt produktów do wpisania
            self.ilosc = input("\nWybierz ilość szt. do wyceny\t\t\t")

    def insertall(self):
            self.c.execute('INSERT INTO Konfigurator (Produkt_id, Kolor_id, Model_id, Typy_montazu_id, Materialy_id) VALUES (%s, %s, %s, %s, %s);',
                (self.produktid, self.profilid, self.modelid, self.montazid, self.materialid))
            self.conn.commit()

            self.c.execute('SELECT id FROM Konfigurator')
            KonfID = self.c.fetchall()[0][0]

            self.c.execute('SELECT * FROM Konfigurator WHERE `ID`=%s', (KonfID))
            for row in self.c.fetchall():
                print("\n\n----------------Dodano wycenę o nr ID = %s!--------------------" % (KonfID))
                print('%22s %15s %22s %15s %22s' % ("Produkt", "Profil","Model","Montaż","Materiał" ))
                print('%22s %15s %22s %15s %22s' % (row[0], row[1], row[2], row[3], row[4]))

    def Admin(self):  # Menu Administratora
        # logowanie admin
        while (True):
            dec = input('\n1. Wycena plis\n2. Usuń opcje wyboru żaluzji\n3. Dodaj nową opcję\n4. Wyjdź\n')
            if (dec == '1'):
                self.User()
            elif (dec == '2'):
                self.delete()
            elif (dec == '3'):
                self.insert()
            elif (dec == '4'):
                self.connClose()
            else:
                print('Nieprawidłowy wybór')

    def delete(self):  # Wybór: usunięcie poszczególnych elementów opcjonalnych do wyceny żaluzji
        print(
            '------------------------------------------------------------------------------------------------------------------')
        dec = input(
            '1.Usuń produkt | 2.Usuń wymiar | 3.Usuń Model | 4.Usuń profil | 5.Usuń materiał | 6.Usuń montaż | 7.Wyloguj ')
        print(
            '------------------------------------------------------------------------------------------------------------------')
        if (dec == '1'):
            self.deleteProduct()
        elif (dec == '2'):
            self.deleteDim()
        elif (dec == '3'):
            self.deleteModel()
        elif (dec == '4'):
            self.deleteProfil()
        elif (dec == '5'):
            self.deleteMaterial()
        elif (dec == '6'):
            self.deleteMontaz()
        elif (dec == '7'):
            self.connClose()
        else:
            print('Zły wybór')

    def deleteProduct(self):  # Usuwanie produktu o podanym ID z tabeli Produkt
        try:
            self.selectProduct()
            produktid = int(input('Podaj ID Produktu do usunięcia '))
            self.c.execute('DELETE FROM Produkt WHERE idnazwa=%s;', produktid)
            self.conn.commit()
            print('\n-------------- Usunięto produkt o ID=%s ---------------' % (produktid))
            self.selectProduct()
        except:
            print('Podałeś błędny id!')

    def deleteDim(self):  # Usuwanie wymiarów podanym ID z tabeli Produkt
        try:
            self.selectDim()
            dimid = int(input('Podaj ID wymiaru do usunięcia '))
            self.c.execute('DELETE FROM Produkt WHERE id=%s;', dimid)
            self.conn.commit()
            print('\n-------------- Usunięto wymiar o ID=%s ---------------' % (dimid))
            self.Admin()
        except:
            print('Podałeś błędny id!')

    def deleteModel(self):  # Usuwanie modelu z podanym ID
        try:
            self.selectModel()
            modelid = int(input('Podaj ID modelu do usunięcia '))
            self.c.execute('DELETE FROM Model_produktu WHERE id=%s;', modelid)
            self.conn.commit()
            print('\n-------------- Usunięto model o ID=%s ---------------' % (modelid))
            self.Admin()
        except:
            print('Podałeś błędny id!')

    def deleteProfil(self):  # Usuwanie profilu z podanym ID
        try:
            self.selectProfil()
            profilid = int(input('Podaj ID profilu do usunięcia '))
            self.c.execute('DELETE FROM Kolor_profili WHERE id=%s;', profilid)
            self.conn.commit()
            print('\n-------------- Usunięto profil o ID=%s ---------------' % (profilid))
            self.Admin()
        except:
            print('Podałeś błędny id!')

    def deleteMaterial(self):  # Usuwanie materiału z podanym ID
        try:
            self.selectMaterial()
            materialid = int(input('Podaj ID materialu do usunięcia '))
            self.c.execute('DELETE FROM Materialy WHERE id=%s;', materialid)
            self.conn.commit()
            print('\n-------------- Usunięto material o ID=%s ---------------' % (materialid))
            self.Admin()
        except:
            print('Podałeś błędny id!')

    def deleteMontaz(self):  # Usuwanie modelu z podanym ID
        try:
            self.selectMontaz()
            montazid = int(input('Podaj ID rodzaju montażu do usunięcia '))
            self.c.execute('DELETE FROM Typy_montazu WHERE id=%s;', montazid)
            self.conn.commit()
            print('\n-------------- Usunięto rodzaj montażu o ID=%s ---------------' % (montazid))
            self.Admin()
        except:
            print('Podałeś błędny id!')


    def insert(self):  # Wybór: dodanie poszczególnych elementów opcjonalnych do wyceny żaluzji
        print(
            '------------------------------------------------------------------------------------------------------------------')
        dec = input(
            '1.Dodaj produkt i wymiar | 2.Dodaj Model | 3.Dodaj profil | 4.Dodaj materiał | 5.Dodaj montaż | 6.Wyloguj ')
        print(
            '------------------------------------------------------------------------------------------------------------------')
        if (dec == '1'):
            self.insertProduct()
        elif (dec == '2'):
            self.insertModel()
        elif (dec == '3'):
            self.insertProfil()
        elif (dec == '4'):
            self.insertMaterial()
        elif (dec == '5'):
            self.insertMontaz()
        elif (dec == '6'):
            self.connClose()
        else:
            print('Zły wybór')

    def insertProduct(self): # Dodanie rekordu to tabeli Produkt
        try:
            nazwa = input('Nazwa produktu: ')
            szer = float(input('Szerokość w cm: '))
            wys = float(input('Wysokość w cm: '))
            cenabazowa = input('Cena podstawowa: ')
            idnazwa = input('Nr id dla produktu (1-Plisy | 2-Rolety : ')
            self.c.execute('INSERT INTO Produkt (nazwa,szer,wys,cenabazowa,idnazwa) VALUES (%s, %s, %s, %s, %s);', (nazwa,szer,wys,cenabazowa,idnazwa))
            self.conn.commit()
            print('\n-------------- Dodano nowy rodzaj produktu  ---------------')
        except:
            print('Podałeś niepoprawne dane! ')
    def insertModel(self): # Dodanie rekordu to tabeli Model
        try:
            nazwamodelu = input('Wpisz nazwę modelu: ')
            doplatadomodelu = input('Dopłata do modelu w %(zmiennoprzecinkowo): ')
            self.c.execute('INSERT INTO Model_produktu (nazwa_modelu, doplata_do_modelu) VALUES (%s, %s);', (nazwamodelu,doplatadomodelu))
            self.conn.commit()
            print('\n-------------- Dodano nowy rodzaj modelu  ---------------')
        except:
            print('Podałeś niepoprawne dane! ')
    def insertProfil(self): # Dodanie rekordu to tabeli Kolor_Profil
        try:
            profil = input('Wpisz kolor profili: ')
            doplatadoprofili = input('Dopłata do profili w %(zmiennoprzecinkowo): ')
            self.c.execute('INSERT INTO Kolor_profili (nazwy_k_p,doplata_do_k_p) VALUES (%s, %s);', (profil,doplatadoprofili))
            self.conn.commit()
            print('\n-------------- Dodano nowy rodzaj profilu  ---------------')
        except:
            print('Podałeś niepoprawne dane! ')

    def insertMaterial(self): # Dodanie rekordu to tabeli Materialy
        try:
            material = input('Podaj nazwę materiału: ')
            doplatamaterial = input('Dopłata do materiału w %(zmiennoprzecinkowo: ')
            self.c.execute('INSERT INTO Materialy (nazwy_mat,doplata_mat) VALUES (%s, %s);', (material,doplatamaterial))
            self.conn.commit()
            print('\n-------------- Dodano nowy rodzaj materiału  ---------------')
        except:
            print('Podałeś niepoprawne dane! ')

    def insertMontaz(self): # Dodanie rekordu to tabeli Typy_Montazu
        try:
            montaz = input('Podaj typ montażu: ')
            doplatamontaz = input('Dopłata do typu montazu w %(zmiennoprzecinkowo): ')
            self.c.execute('INSERT INTO Typy_montazu (nazwa_typu,doplata_m) VALUES (%s, %s);', (montaz,doplatamontaz))
            self.conn.commit()
            print('\n-------------- Dodano nowy typ montażu  ---------------')
        except:
            print('Podałeś niepoprawne dane! ')

    def connClose(self):  # Zamknięcie połączenia z bazą mysql
        self.conn.close()
        print('\n\n\t\t***** ZOSTAŁEŚ WYLOGOWANY Z SYSTEMU *****\n\n\t\tProjekt i wykonanie: Marcin Tomaszewski 2018')
        while (True):
            dec = input('\nAby ponownie zalogować wybierz 1\n')
            if (dec == '1'):
                self.__init__()

db = DBConn()
