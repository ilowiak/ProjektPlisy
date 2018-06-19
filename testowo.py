import pymysql


class DBConn:
    def __init__(self):
        print('Witamy w konfiguratorze żaluzji plisowanych !')
        self.conn()
    def conn(self):
        import secret.auth as nowy
        try:
            # obiekt połączenia
            print('POŁĄCZENIE Z BAZĄ DANYCH ')
            self.conn = pymysql.connect('localhost',nowy.user,nowy.passwd, nowy.db,charset='utf8')
            print('Połączenie ustanowione')
            # obekt na którym wykonujemy zapytania SQL
            self.c = self.conn.cursor()
        except:
            print( 'Błędne dane logowania')
    def logowanie(self):
        self.a = 3
        while self.a:
            self.login = input('Podaj login')
            self.passwd = input ('Podaj hasło')
            self.loginAdmin = self.login
            self.c.execute('SELECT id FROM Logowanie WHERE login=%s AND password=%s',(self.login,self.passwd))
            wynik = self.c.fetchall()
            if(len(wynik) > 0):
                if(wynik[0][4] == 'A'):
                    self.login = '%'
                    self.passwd = '%'
                    print('Admin')
                    while(True):
                        dec = input ('S-wybierz, I-Wprowadz, U-Aktualizuj, D- Usun, R-Raport, Q- wyjście').upper()
                        if(dec == 'S'):
                            self.select()
                        elif(dec == 'I'):
                            self.insert()
                        elif(dec == 'U'):
                            self.update()
                        elif(dec == 'D'):
                            self.delete()
                        elif (dec == 'R'):
                            self.report()
                        elif(dec == 'Q'):
                            print('Wyjście')
                            self.conn.close()
                            self.a = 0
                            break
                        else:
                            print('Błędne dane')
                else:
                    print('User')
                    while (True):
                        dec = input('S-wybierz, Q- wyjście').upper()
                        if (dec == 'S'):
                            self.select()
                        elif (dec == 'Q'):
                            print('Wyjście')
                            self.conn.close()
                            self.a = 0
                            break
                        else:
                            print('Błędne dane')
            else:
                print('Błędne dane logowania')
                self.a -=1

db = DBConn()
