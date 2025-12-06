import sqlite3
import random


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
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    detail_id INTEGER NOT NULL,
                    priority INTEGER NOT NULL,
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



        self.cursor.execute('DROP TABLE IF EXISTS details')
        self.cursor.execute('DROP TABLE IF EXISTS production_priority')


        # Данные для таблицы details
        details_data = [
            (0, 'Шестеренка ведущая',),
            (1, 'Муфта кулачковая',),
            (2, 'Вал промежуточный',),
            (3, 'Корпус редуктора',),
            (4, 'Подшипник упорный',),
            (5, 'Крышка защитная',),
            (6, 'Фланец соединительный',),
            (7, 'Втулка бронзовая',),
            (8, 'Колесо зубчатое',),
            (9, 'Ось вращения',),
        ]

        self.create_production_priority_table()
        self.create_details_table()

        # Вставляем данные в details
        self.cursor.executemany(
            'INSERT INTO details (id, name) VALUES (?, ?)',
            details_data
        )

        priority_data = [
            # priority, overdue, execution_time, profitability, bottleneck_load, turnover_rate, tech_readiness
            # Оригинальные данные
            (3, 5, 24, 1500.00, 85, 2.5, 100),
            (3, 2, 48, 2500.00, 90, 1.8, 100),
            (2, 0, 16, 800.00, 60, 3.2, 100),
            (2, 1, 36, 1200.00, 75, 2.1, 80),
            (1, 0, 8, 400.00, 40, 4.5, 100),
            (3, 7, 72, 3500.00, 95, 1.2, 90),
            (2, 0, 24, 950.00, 55, 2.8, 100),
            (1, 0, 12, 600.00, 45, 3.8, 95),
            (3, 3, 60, 2800.00, 88, 1.5, 85),
            (2, 1, 20, 1100.00, 65, 2.4, 100),

            # Новые данные - хаотичный порядок приоритетов (1-5)
            # Приоритет 4 - повышенный
            (4, 10, 96, 5000.00, 98, 0.8, 70),  # Очень срочный, но сложный
            (4, 1, 40, 4200.00, 85, 1.6, 100),  # Важный с хорошей готовностью
            (4, 8, 84, 4800.00, 92, 1.1, 85),  # Высокая прибыль, но просрочка

            # Приоритет 5 - критический
            (5, 15, 120, 8000.00, 99, 0.5, 60),  # Критический, большая просрочка
            (5, 0, 4, 3000.00, 70, 2.0, 100),  # Сверхсрочный, но быстрый
            (5, 3, 32, 6000.00, 96, 1.3, 95),  # Критически важный

            # Приоритет 1 - низкий (больше вариаций)
            (1, 0, 6, 300.00, 35, 5.0, 100),  # Простой и готовый
            (1, 2, 18, 350.00, 50, 4.2, 90),  # Низкая прибыль, небольшая просрочка
            (1, 0, 10, 450.00, 42, 4.8, 95),  # Стандартный низкий
            (1, 5, 30, 550.00, 58, 3.5, 75),  # Низкий, но с проблемами

            # Приоритет 2 - средний (разные сценарии)
            (2, 3, 28, 1300.00, 72, 2.7, 85),  # Средний с просрочкой
            (2, 0, 14, 900.00, 52, 3.0, 100),  # Стандартный средний
            (2, 6, 44, 1600.00, 80, 2.0, 65),  # Средний, но сложный
            (2, 1, 22, 1050.00, 68, 2.5, 90),  # Сбалансированный средний

            # Приоритет 3 - высокий
            (3, 4, 52, 3200.00, 87, 1.7, 88),  # Высокий, хорошая прибыль
            (3, 0, 20, 1800.00, 78, 2.3, 100),  # Высокий, без просрочки
            (3, 9, 68, 3800.00, 94, 1.0, 78),  # Высокий, но срочный
            (3, 2, 56, 2900.00, 83, 1.9, 92),  # Стабильный высокий

            # Приоритет 4 - пограничные случаи
            (4, 12, 100, 5500.00, 97, 0.7, 55),  # Очень сложный
            (4, 0, 12, 2000.00, 76, 1.8, 100),  # Быстрый, но важный

            # Приоритет 5 - экстремальные случаи
            (5, 20, 140, 10000.00, 100, 0.3, 40),  # Максимальные значения
            (5, 1, 8, 2500.00, 65, 1.5, 100),  # Критичный, но простой

            # Смешанные приоритеты - особые случаи
            (1, 10, 50, 700.00, 70, 2.9, 50),  # Низкий приоритет, но большая просрочка
            (5, 0, 2, 1500.00, 40, 3.0, 100),  # Критичный, но быстрый и легкий
            (3, 15, 80, 4200.00, 99, 0.9, 30),  # Высокий, но очень проблемный
            (2, 8, 64, 2000.00, 88, 1.8, 60),  # Средний с высокими показателями

            # Дополнительные для разнообразия
            (4, 6, 76, 4500.00, 91, 1.4, 82),
            (1, 1, 15, 500.00, 48, 4.0, 96),
            (3, 11, 92, 4100.00, 96, 0.6, 45),
            (2, 4, 38, 1400.00, 77, 2.2, 87),
            (5, 7, 56, 7000.00, 98, 1.0, 72),
            (4, 0, 24, 3000.00, 82, 1.9, 98),
            (1, 3, 25, 650.00, 55, 3.6, 88),
            (3, 8, 64, 3300.00, 89, 1.3, 79),
            (2, 9, 70, 1800.00, 84, 1.7, 68),
            (5, 4, 40, 5200.00, 92, 1.2, 89),
            (5, -1, 141, 299.00, 101, 0.29, 29)
        ]
        #
        # 'overdue': 'max',
        # 'execution': 'min',
        # 'profitability': 'max',
        # 'bottleneck_load': 'min',
        # 'turnover_rate': 'max',
        # 'tech_readiness': 'max'}
        worst = [min, max, min, max, min, min]
        min_p = [worst[i - 1](feature) for i, feature in  enumerate(zip(*priority_data)) if i >= 1]
        print(min_p)

        priority_data = [(i, random.sample(details_data, 1)[0][0], *row) for i, row in enumerate(priority_data)]


        # Вставляем данные в production_priority
        self.cursor.executemany(
            '''INSERT INTO production_priority 
            (id, detail_id, priority, overdue, execution, profitability, bottleneck_load, turnover_rate, tech_readiness) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            priority_data
        )

        self.conn.commit()
        print("Тестовые данные успешно загружены!")

