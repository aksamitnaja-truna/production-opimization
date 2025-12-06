from json_handler import JsonHandler
from table import QueueTable
from connnector import DataBaseConnection


def main_criterion_rank():
    pass


def task():
    # create connection
    db_conn = DataBaseConnection('./db/sqlite.db')

    # fill test values
    db_conn.load_test_data()

    # create Table model
    table = QueueTable(db_conn)

    # load data from db to model
    table.load_data()

    # from str -> digit
    table.convert_table_to_numeric()

    # normalization form (132..-432..) -> (0-1)
    table.normalization()
    table.print_table()

    #
    id_list = table.queue_sorting(QueueTable.best_point_method)

    table.report(id_list, folder_path='./reports')


if __name__ == '__main__':
    task()