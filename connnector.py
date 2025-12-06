import sqlite3


class DataBaseConnection:
    def __init__(self, file_path):
        self.conn = sqlite3.connect(file_path)
        self.cursor = self.conn.cursor()

    def create_details_table(self):
        self.cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT not null
                    )
            ''')

    def create_production_priority_table(self):
        self.cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS production_priority (
                    id INTEGER  PRIMARY KEY AUTOINCREMENT,
                    priority TEXT NOT NULL,
                    overdue INTEGER NOT NULL,
                    execution time INTEGER NOT NULL,
                    profitability DECIMAL (10,2) NOT NULL,
                    bottleneck_load INTEGER NOT NULL,
                    turnover_rate DECIMAL (5,2) NOT NULL,
                    tech_readiness INTEGER NOT NULL
                    )
            ''')

    def load_test_data(self):
        # Сначала создаем таблицы
        self.create_details_table()
        self.create_production_priority_table()

        # Очищаем предыдущие данные
        self.cursor.execute('DELETE FROM details')
        self.cursor.execute('DELETE FROM production_priority')

        # Сбрасываем автоинкремент (опционально, но рекомендуется)
        self.cursor.execute('DELETE FROM sqlite_sequence WHERE name IN ("details", "production_priority")')

        # Данные для таблицы details
        details_data = [
            ('Шестеренка ведущая',),
            ('Вал промежуточный',),
            ('Корпус редуктора',),
            ('Подшипник упорный',),
            ('Крышка защитная',),
            ('Фланец соединительный',),
            ('Втулка бронзовая',),
            ('Колесо зубчатое',),
            ('Ось вращения',),
            ('Муфта кулачковая',)
        ]

        # Вставляем данные в details
        self.cursor.executemany(
            'INSERT INTO details (name) VALUES (?)',
            details_data
        )

        # Данные для таблицы production_priority
        priority_data = [
            # priority, overdue, execution_time, profitability, bottleneck_load, turnover_rate, tech_readiness
            (3, 5, 24, 1500.00, 85, 2.5, 100),
            (3, 2, 48, 2500.00, 90, 1.8, 100),
            (2, 0, 16, 800.00, 60, 3.2, 100),
            (2, 1, 36, 1200.00, 75, 2.1, 80),
            (1, 0, 8, 400.00, 40, 4.5, 100),
            (3, 7, 72, 3500.00, 95, 1.2, 90),
            (2, 0, 24, 950.00, 55, 2.8, 100),
            (1, 0, 12, 600.00, 45, 3.8, 95),
            (3, 3, 60, 2800.00, 88, 1.5, 85),
            (2, 1, 20, 1100.00, 65, 2.4, 100)
        ]

        # Вставляем данные в production_priority
        self.cursor.executemany(
            '''INSERT INTO production_priority 
            (priority, overdue, execution, profitability, bottleneck_load, turnover_rate, tech_readiness) 
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            priority_data
        )

        self.conn.commit()
        print("Тестовые данные успешно загружены!")

