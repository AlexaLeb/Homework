import psycopg2

class DataBase():
    def __init__(self, conn):
        self.conn = conn

    def create_db(self):
        with conn.cursor() as cur:
            cur.execute('''
            DROP TABLE tell;
            DROP TABLE client;
            ''')

            cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(40) NOT NULL,
                last_name VARCHAR(40) NOT NULL,
                email VARCHAR(40) NOT NULL,
                phones_amount INTEGER
            );
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS tell(
                id SERIAL PRIMARY KEY,
                number INTEGER NOT NULL,
                client_id INTEGER NOT NULL REFERENCES client(id)
            );
            """)
        print('Таблицы созданы')

    def add_client(self, first_name, last_name, email, phones=0):
        with conn.cursor() as cur:
            cur.execute('''
            INSERT INTO client(first_name, last_name, email, phones_amount) VALUES(%s, %s, %s, %s);
            ''', (first_name, last_name, email, phones))
        print('клиент добавлен')

    def add_phone(self, phone, client_id,):
        with conn.cursor() as cur:
            cur.execute('''
            INSERT INTO tell(number, client_id) VALUES(%s, %s);
            ''', (phone, client_id))
        print('телефон добавлен')

    def change_client(self, client_id, first_name=None, last_name=None, email=None, phones=None):
        with conn.cursor() as cur:
            point = input('''
            Какие данные о клиенте нужно изменить? Введите: 
            f - изменить имя
            l - изменить фамилию
            e - изменить почту
            t - изменить количество телефонов у клиента
            ''')
            if point == 'f':
                cur.execute('''
                UPDATE client SET first_name = %s
                WHERE id = %s;
                ''', (first_name, client_id))
                print('Успешно изменено')
            elif point == 'l':
                cur.execute('''
                UPDATE client SET last_name = %s
                WHERE id = %s;
                ''', (last_name, client_id))
                print('Успешно изменено')
            elif point == 'e':
                cur.execute('''
                UPDATE client SET email = %s
                WHERE id = %s;
                ''', (email, client_id))
                print('Успешно изменено')
            elif point == 't':
                cur.execute('''
                UPDATE client SET phones_amount = %s
                WHERE id = %s;
                ''', (phones, client_id))
                print('Успешно изменено')
            else:
                print('неизвестная команда')

    def delete_phone(self, client_id, phone):
        with conn.cursor() as cur:
            cur.execute('''
            SELECT number FROM tell
            WHERE client_id=%s
            LIMIT 1;
            ''', (client_id,)) #если такого клиента нет, то код выдаст ошибку

            cur.execute('''
            DELETE FROM tell 
            WHERE number=%s;
            ''', (phone,))
        print(f'телефон {phone} успешно удален')

    def delete_client(self, client_id):
        with conn.cursor() as cur:
            cur.execute('''
            DELETE FROM tell
            WHERE client_id=%s;
            ''', (client_id,))

            cur.execute('''
            DELETE FROM client
            WHERE id=%s;
            ''', (client_id,))
        print('Пользователь удален')

    def find_client(self, first_name=None, last_name=None, email=None, phone=None):
        pass


with psycopg2.connect(database="dvdrental", user="postgres", password="1207") as conn:
    data = DataBase(conn)
    # data.create_db()
    # data.add_client("sasha", "lebedev", 'email')
    # data.add_client("gerald", "witcher", 'emaill', 5)
    # data.add_phone(1111, 1)
    # data.add_phone(1121, 1)
    # data.add_phone(1131, 2)
    # data.add_phone(1541, 2)
    # data.change_client(2, 'Лютик')
    # data.change_client(2, last_name='Бард')
    # data.change_client(2, email='лютиклучший')
    # data.change_client(1, phones=4)
    # data.change_client(1, email='sasha')
    # data.delete_phone(2, 1131)
    # data.delete_client(2)

# conn.close()
