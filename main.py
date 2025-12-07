from table import QueueTable
from connector import DataBaseConnection


def main_criterion_rank():
    pass


def task():
    # create connection
    db_conn = DataBaseConnection('./db/sqlite.db')

    # fill test values
    db_conn.load_test_data()

    # create Table model
    table_names = ['details', 'production_priority', 'criteria_trend']
    table = QueueTable(db_conn, *table_names)

    # load data from db to model
    table.load_data()


    # normalization form (132..-432..) -> (0-1)
    table.normalization()

    #
    table.queue_sorting(QueueTable.best_point_method)

    table.report(folder_path='./reports')


if __name__ == '__main__':
    task()