from collections import defaultdict
import pandas as pd
import os

from pandas.core.common import consensus_name_attr


class QueueTable:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.details_table = None
        self.production_priority_table = None

        self.table =  None
        self.trend = None
        self.value_map = None

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


    def convert_table_to_numeric(self):
        self.table = {}
        self.table['header'] = self.production_priority_table[0][1:]
        for row_idx in range(1, len(self.production_priority_table)):
            row = list(self.production_priority_table[row_idx][1:]).copy()
            for cell_idx in range(len(row)):
                if isinstance(row[cell_idx], str):
                    feature = self.production_priority_table[0][cell_idx + 1]
                    row[cell_idx] = self.velue_map[feature][row[cell_idx]]
            self.table[self.production_priority_table[row_idx][0]] = row


    def normalization(self):
        # define min/max value in each feature
        bounds_values = defaultdict(list)
        for id, row in self.table.items():
            if id == 'header':
                continue
            for j, cell in enumerate(row):
                feature = self.table['header'][j]
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
                feature = self.table['header'][j]
                min_v,  max_v = bounds_values[feature][0], bounds_values[feature][1]
                value = (float(cell) - min_v) / (max_v - min_v)
                if self.trend[feature] == 'min':
                    value = 1 - value
                row[j] = value

        for feature in self.trend:
            self.trend[feature] = "max"

        # print(self.table)

    @staticmethod
    def less_then(p1, p2):
        if len(p1) != len(p2):
            raise Exception
        size = len(p1)
        for i in range(size):
            if p1[i] >= p2[i]:
                return False
            return True


    def is_consensus_point(self, p1):
        iter_points = iter(self.table.values())
        header = next(iter_points)
        for p2  in iter_points:
            if  not QueueTable.less_then(p1, p2):
                return False
        return True


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

        res_table = [(detail_id, row) for detail_id, row  in self.table.items()  if detail_id != 'header']

        res_table.sort(
            key=lambda x: [
                x[1][self.table['header'].index('priority')], # high,normal, low
                not self.is_consensus_point(x[1]),
                method(x[1], *args)
            ],
            reverse=True
        )
        return [table_item[0] for table_item in res_table]


    def report(self, id_list, folder_path):
        report_table = []
        report_table.append([*self.details_table[0], *self.production_priority_table[0][1:]])
        hashed_details = {detail_id: [name] for detail_id, name in self.details_table[1:]}
        hashed_production_priority = {row[0]: row[1:] for row in self.production_priority_table[1:]}


        for detail_id in id_list:
            report_table.append([detail_id, *hashed_details[detail_id], *hashed_production_priority[detail_id]])

        df = pd.DataFrame(report_table[1:], columns=report_table[0])
        excel_filename = 'production_report.xlsx'
        df.to_excel(os.path.join(folder_path, excel_filename), index=False, engine='openpyxl')

    def print_table(self):
        print(self.table)

    def get_table(self):
        return self.table

