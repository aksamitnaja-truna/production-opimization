from collections import defaultdict
import pandas as pd
import os
from priority import str_prior



class QueueTable:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.details_table = None
        self.production_priority_table = None

        self.table =  None
        self.sorted_table = None
        self.trend = None
        self.value_map = None

        self.consensus_points = None

    def load_data(self):
        for table_name in ('details', 'production_priority'):
            try:
                self.db_conn.cursor.execute(f"SELECT * FROM {table_name}")
                rows = self.db_conn.cursor.fetchall()
                columns = [description[0] for description in self.db_conn.cursor.description]
                if table_name == 'details':
                    self.details_table = [columns, *rows]
                elif table_name == 'production_priority':
                    self.production_priority_table = [columns, *rows]
            except Exception as e:
                print(f"Ошибка при загрузке данных из таблицы '{table_name}': {e}")
                return None


        self.trend = {'priority': 'max',
                      'overdue': 'max',
                      'execution': 'min',
                      'profitability': 'max',
                      'bottleneck_load': 'min',
                      'turnover_rate': 'max',
                      'tech_readiness': 'max'}





    def normalization(self):
        self.table = []
        for index, row in enumerate(self.production_priority_table):
            self.table.append(list(row[2:]))

        # define min/max value in each feature
        bounds_values = defaultdict(list)
        for i, row in enumerate(self.table):
            if i == 0:
                continue
            for j, cell in enumerate(row, start=0):
                if j == 0:
                    continue
                feature = self.table[0][j]
                if len(bounds_values[feature]) == 0:
                    bounds_values[feature].extend([float(cell), float(cell)])
                if float(cell) < bounds_values[feature][0]:
                    bounds_values[feature][0] = float(cell)
                elif float(cell) > bounds_values[feature][1]:
                    bounds_values[feature][1] = float(cell)

        # normalization
        for i in range(1, len(self.table)):
            row = self.table[i]
            for j, cell in enumerate(row):
                if j == 0:
                    continue
                feature = self.table[0][j]
                min_v,  max_v = bounds_values[feature][0], bounds_values[feature][1]
                value = (float(cell) - min_v) / (max_v - min_v)
                if self.trend[feature] == 'min':
                    value = 1 - value
                row[j] = value

        for feature in self.trend:
            self.trend[feature] = "max"

        # print(self.table)

    @staticmethod
    def p1_less_then_p2(p1, p2):

        if len(p1) != len(p2):
            raise Exception
        size = len(p1)
        for i in range(size):
            if p1[i] >= p2[i]:
                return False
        return True


    def is_consensus_point(self, p1):
        iter_points = iter(self.table)
        header = next(iter_points)
        print(p1[3:])
        for p2  in iter_points:
            if  QueueTable.p1_less_then_p2(p1[3:], p2[1:]):
                self.consensus_points.add(p1[0])
                return True
        return False

    @staticmethod
    def best_point_method(p1, k=None):
        if k is None:
            k = [1 for _ in p1]
            total = 0
        else:
            pass
    # sum lambda = 1


        for i in range(len(p1)):
            total += k[i] * (1 - p1[i])**2
        return total**0.5

    @staticmethod
    def additive_method(point: list[float], factors=None) -> float:
        if factors is None:
            factors = {
                'priority': 0.25,
                'overdue': 0.20,
                'execution': 0.15,
                'profitability': 0.10,
                'bottleneck_load': 0.10,
                'turnover_rate': 0.10,
                'tech_readiness': 0.10
            }
        return  sum([value * factor for value, factor in zip(point, factors.values())])


    def queue_sorting(self, method, *args):
        self.consensus_points = set()

        priors_id, details_id = zip(*[(row[0], row[1]) for row in self.production_priority_table])
        self.sorted_table = [[prior_id, detail_id, *row] for prior_id, detail_id, row  in zip(priors_id, details_id, self.table)]
        header, rest = self.sorted_table[0], self.sorted_table[1:]
        rest.sort(
            key=lambda x: [
                x[self.table[0].index('priority') + 2],
                not self.is_consensus_point(x),
                method(x[2:], *args)
            ],
            reverse=True
        )
        self.sorted_table = [header] + rest
        print(self.consensus_points)



    def report(self, folder_path):


        hashed_details = {detail_id: [name] for detail_id, name in self.details_table[1:]}
        report_table = []
        sorted_table_iter = iter(self.sorted_table)
        header = next(sorted_table_iter)
        header.insert(2, 'name')
        report_table.append(header)
        for row in sorted_table_iter:
            is_consensus = row[0] in self.consensus_points
            report_table.append([*row[:2], *hashed_details[row[1]], str_prior(row[2], is_consensus), *row[3:]])

        # print(report_table)
        df = pd.DataFrame(report_table[1:], columns=report_table[0])
        excel_filename = 'production_report.xlsx'
        df.to_excel(os.path.join(folder_path, excel_filename), index=False, engine='openpyxl')

    def print_table(self):
        print(self.table)

    def get_table(self):
        return self.table

