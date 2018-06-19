# -*- coding: utf-8 -*-
import pymysql

class DBConn:
    def __init__(self):
        
        while(True):
            quit = input('1.Logowanie, 2.Wyjście  ')
            if(quit == '2'):
                break
            self.connString()
            perm = self.login()
            if perm == 0:
                print('---------------------------------------------------------------')
                print('            ZALOGOWANO JAKO ADMINISTRATOR                      ')
                print('---------------------------------------------------------------')                
                self.Admin()
                
            elif perm == 1 :
                print('---------------------------------------------------------------')
                print('     WITAMY W KONFIGURATORZE ZALUZJI PLISOWANYCH i ROLET       ')
                print('---------------------------------------------------------------')                
                self.User()
                            
            else:
                print('Błąd logowania!')

    def connString(self):  # Ustanowienie połączenia z bazą mysql
        self.conn = pymysql.connect(host='localhost', user='user', password='user', db='mydb', charset='utf8',
                                    use_unicode=True)
        self.c = self.conn.cursor()

                        
    def login(self): # logowanie - pobiera maila i hasło z mysql i sprawdza przypisane uprawnienia
        login = input('Podaj swój login: ')
        password = input('Podaj swoje hasło: ')
        self.c.execute('SELECT id_roli FROM Logowanie WHERE login=%s AND password=%s;', (login, password))
        try:
            perm = self.c.fetchall()[0][0]
        except:
            perm = -1
        return perm

    def User(self): # Menu Usera
            while(True):
                dec = input('\n1. Konfiguruj produkt\n2. Wyjdź\n')
                if(dec == '1'):
                    self.selectAll()
                elif(dec == '2'):
                    self.connClose()
                else:
                    print('Nieprawidłowy wybór')

    def selectAll(self):


            self.c.execute('SELECT idnazwa, nazwa FROM Produkt')
            print('\n\t\t   PRODUKTY\n')
            print('%3s %20s' % ("ID", "Produkt"))
            print('________________________________________________')
            for row in self.c.fetchall():
                print('%3s %20s' % (row[0], row[1]))
            produktid = input("\nWybierz nr produktu\t\t\t")

            self.c.execute('SELECT id,nazwa,szer,wys FROM Produkt;')
            print('\n\t\tWYMIARY\n')
            print('%3s %20s %5s %5s' % ("ID", "Produkt", "Szer.", "Wys."))
            print('_________________________________________________')
            for row in self.c.fetchall():
                print('%3s %20s %5s %5s' % (row[0], row[1], row[2], row[3]))
            dimid = input("\nWybierz nr wymiaru\t\t")

            self.c.execute('SELECT ID, nazwa_modelu FROM Model_produktu')
            print('\n\t\tMODEL PRODUKTU\n')
            print('%3s %22s' % ("ID", "Model Produktu"))
            print('__________________________________________')
            for row in self.c.fetchall():
                print('%3s %22s' % (row[0], row[1]))
            modelid = input("\nWybierz nr modelu \t")

            self.c.execute('SELECT ID, nazwy_k_p FROM Kolor_profili')
            print('\n\t\tKOLOR PROFILI\n')
            print('%3s %22s' % ("ID", "Kolor Profili"))
            print('__________________________________________')
            for row in self.c.fetchall():
                print('%3s %22s' % (row[0], row[1]))
            profilid = input("\nWybierz nr koloru profili \t")

            self.c.execute('SELECT ID, nazwy_mat FROM Materialy')
            print('\n\t\tKOLOR MATERIAŁU\n')
            print('%3s %22s' % ("ID", "Kolor Materiału"))
            print('__________________________________________')
            for row in self.c.fetchall():
                print('%3s %22s' % (row[0], row[1]))
            materialid = input("\nWybierz nr koloru materiału \t")

            self.c.execute('SELECT ID, nazwa_typu FROM Typy_montazu')
            print('\n\t\tTYP MONTAŻU\n')
            print('%3s %22s' % ("ID", "Typ montażu"))
            print('__________________________________________')
            for row in self.c.fetchall():
                print('%3s %22s' % (row[0], row[1]))
            montazid = input("\nWybierz rodzaj montażu\t")

            self.c.execute(
                'INSERT INTO Konfigurator (Produkt_id, Kolor_id, Model_id, Typy_montazu_id, Materialy_id) VALUES (%s, %s, %s, %s, %s);',
                (produktid, dimid, modelid, profilid, materialid, montazid))
            self.conn.commit()



    def Admin(self): # Menu Administratora
        #logowanie admin
            while(True):
                dec = input('\n1. Wycena plis\n2. Usuń opcje wyboru żaluzji\n3. Dodaj nową opcję\n4. Wyjdź\n')
                if(dec == '1'):
                    self.selectAll()
                elif(dec == '2'):
                    self.delete()
                elif(dec == '3'):
                    self.insert()
                elif(dec == '4'):
                    self.connClose()
                else:
                    print('Nieprawidłowy wybór')


    def delete(self): #Wybór: usunięcie poszczególnych elementów opcjonalnych do wyceny żaluzji
        print('------------------------------------------------------------------------------------------------------------------')
        dec = input('1.Usuń produkt | 2.Usuń wymiar | 3.Usuń Model | 4.Usuń profil | 5.Usuń materiał | 6.Usuń montaż | 7.Wyloguj ')
        print('------------------------------------------------------------------------------------------------------------------')
        if(dec == '1'):
            self.deleteProdukt(prod)
        elif(dec == '2'):
            self.deleteShowing(id)
        elif(dec == '3'):
            self.connClose()
        else:
            print('Zły wybór')

    def deleteProdukt(self, prod): # Usuwanie rekordu o podanym ID z tabeli Produkt
        try:
            self.selectAll(produktid)
            prod = int(input('Podaj ID Produktu do usunięcia '))
            self.c.execute('DELETE FROM Produkt WHERE id=%s;', id)
            self.conn.commit()
            self.selectMovie()
            print('\n-------------- Usunięto produkt o ID=%s ---------------'  % (prod))
        except:
            print('Podałeś błędny id!')

            
    def connClose(self):   # Zamknięcie połączenia z bazą mysql
        self.conn.close()
        print('\n\n\t\t***** ZOSTAŁEŚ WYLOGOWANY Z SYSTEMU *****\n\n\t\tProjekt i wykonanie: Marcin Tomaszewski 2018')
        while(True):
            dec = input('\nAby ponownie zalogować wybierz 1\n')
            if(dec == '1'):
                self.__init__()        
    
    
db = DBConn()
