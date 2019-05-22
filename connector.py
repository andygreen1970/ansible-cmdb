# todo Проверить наличие mysql.connector
import mysql.connector


class ParserError(Exception):
    pass


class ConnError(Exception):
    pass


class Cmdb:

    def __init__(self, config=None, fields=None):
        # todo Возможно, надо сформировать error_msg
        # todo Заблокировать get и set item
        self.__config = {
            'type': 'MYSQL',
            'host': 'localhost',
            'port': '3306',
            'user': 'root',
            'password': '',
            'view': None,
            'where': None
            }
        # todo Проверить сам config
        for key in config:

            if key.lower().strip() in self.__config:
                self.__config[key] = config[key]
            else:
                raise ParserError("Неверный параметр config: {}.".format(key))
        # todo Сделать valid_connector переменной класса. Создать метод класса для ее модификации
        self.__valid_connector = {
            'MYSQL': mysql.connector.MySQLConnection
        }
        # todo Предусмотреть разбор строки в зависимости от типа соединения
        if self.__config['view'].count('.') == 1:
            self.__database, self.__view = self.__config['view'].split('.')
        else:
            raise ParserError("Неверный параметр config:view:{}. "
                              "Требуется указать строку в формате DATABASE.VIEW"
                              .format(self.__config['view']))

        if self.__config['type'] in self.__valid_connector:
            try:
                self.__conn = self.__valid_connector[self.__config['type']](
                    host=self.__config['host'], port=self.__config['port'],
                    database=self.__database, user=self.__config['user'],
                    password=self.__config['password'])

                self.__cursor = self.__conn.cursor()
                sql = "SHOW COLUMNS FROM {};".format(self.__view)
                self.__cursor.execute(sql)
                self.__fields = []
                row = self.__cursor.fetchone()

                while row is not None:
                    self.__fields.append(row[0])
                    row = self.__cursor.fetchone()

                self.__SQL = 'SELECT '

                for field in fields:
                    if field in self.__fields:
                        self.__SQL += field + ', '
                    else:
                        raise Exception("Поле {} отсутствует в CMDB.".format(str(field)))

                self.__SQL = self.__SQL[0:-2] + ' FROM ' + self.__view
                if self.__config['where']:
                    self.__SQL += ' WHERE={}'.format(self.__config['where'])
                    # todo Проверить синтаксис where
                self.__SQL += ';'
                self.__fields = list(fields)

            except Exception as err:
                self.close()
                raise ConnError("Ошибка соединения с базой: {}.".format(str(err)))
        else:
            raise ConnError("Параметр config:type:{} недоступен в этой версии.".format(self.__config['type']))

    def __iter__(self):
        try:
            self.__cursor.execute(self.__SQL)
        except Exception as err:
            self.close()
            raise ConnError("Ошибка выполнения запроса {}: {}.".format(self.__SQL, str(err)))
        return self

    def __next__(self):
        pair = dict()
        try:
            row = self.__cursor.fetchone()
        except Exception as err:
            self.close()
            raise ConnError("Ошибка получения данных: {}.".format(str(err)))
        if row:
            for i in range(len(self.__fields)):
                pair[self.__fields[i]] = row[i]
        else:
            raise StopIteration
        return pair

    def close(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__conn:
            self.__conn.close()

    def __del__(self):
        self.close()
