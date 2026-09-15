'''
Please note:

The first file that you should run in this level is tests.py for database creation, with all tests passing.
Remember that running the hack.py will change the state of the database, causing some tests inside tests.py
to fail.

If you like to return to the initial state of the database, please delete the database (level-4.db) and run
the tests.py again to recreate it.
'''

import os
import re
import sqlite3
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    DB_CRUD_ops().get_stock_info(request.args["input"])
    DB_CRUD_ops().get_stock_price(request.args["input"])
    DB_CRUD_ops().update_stock_price(request.args["input"])
    DB_CRUD_ops().exec_multi_query(request.args["input"])
    DB_CRUD_ops().exec_user_script(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore


class Connect(object):

    # helper function creating database with the connection
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        return connection


class Create(object):

    def __init__(self):
        con = Connect()
        db_con = None
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            table_fetch = cur.execute(
                '''
                SELECT name
                FROM sqlite_master
                WHERE type='table'AND name='stocks';
                ''').fetchall()

            if table_fetch == []:
                cur.execute(
                    '''
                    CREATE TABLE stocks
                    (date text, symbol text, price real)
                    ''')
                cur.execute(
                    "INSERT INTO stocks VALUES (?, ?, ?)",
                    ('2022-01-06', 'MSFT', 300.00))
                db_con.commit()

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            if db_con is not None:
                db_con.close()


_SAFE_SYMBOL = re.compile(r"^[A-Za-z0-9._-]{1,32}$")
_LEADING_SYMBOL = re.compile(r"^[A-Za-z0-9._-]{1,32}")
_SELECT_QUERY = re.compile(
    r"^SELECT\s+(price|\*)\s+FROM\s+stocks\s+WHERE\s+symbol\s*=\s*'([A-Za-z0-9._-]{1,32})'\s*$",
    re.IGNORECASE,
)
_UPDATE_QUERY = re.compile(
    r"^UPDATE\s+stocks\s+SET\s+price\s*=\s*'?([0-9]+(?:\.[0-9]+)?)'?\s+WHERE\s+symbol\s*=\s*'([A-Za-z0-9._-]{1,32})'\s*$",
    re.IGNORECASE,
)


def _canonical_stock_symbol(value):
    if not isinstance(value, str):
        raise ValueError("invalid stock symbol")
    if _SAFE_SYMBOL.fullmatch(value):
        return value

    # Preserve the leading stock symbol while discarding appended SQL text.
    match = _LEADING_SYMBOL.match(value)
    if not match:
        raise ValueError("invalid stock symbol")
    return match.group(0)


def _execute_allowed_query(cur, query):
    stripped = query.strip()

    match = _SELECT_QUERY.fullmatch(stripped)
    if match:
        field, symbol = match.groups()
        if field.lower() == "price":
            cur.execute("SELECT price FROM stocks WHERE symbol = ?", (symbol,))
        else:
            cur.execute("SELECT * FROM stocks WHERE symbol = ?", (symbol,))
        return cur.fetchall(), False

    match = _UPDATE_QUERY.fullmatch(stripped)
    if match:
        price, symbol = match.groups()
        cur.execute(
            "UPDATE stocks SET price = ? WHERE symbol = ?",
            (float(price), symbol),
        )
        return [], True

    raise ValueError("unsupported query")


class DB_CRUD_ops(object):

    def get_stock_info(self, stock_symbol):
        Create()
        con = Connect()
        db_con = None
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] get_stock_info\n"
            query = "SELECT * FROM stocks WHERE symbol = '{0}'".format(stock_symbol)
            res += "[QUERY] " + query + "\n"

            restricted_chars = ";%&^!#-"
            has_restricted_char = any(char in query for char in restricted_chars)
            correct_number_of_single_quotes = query.count("'") == 2

            if has_restricted_char or not correct_number_of_single_quotes:
                res += "CONFIRM THAT THE ABOVE QUERY IS NOT MALICIOUS TO EXECUTE"
            else:
                cur.execute(
                    "SELECT * FROM stocks WHERE symbol = ?",
                    (stock_symbol,),
                )
                for result in cur.fetchall():
                    res += "[RESULT] " + str(result)
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            if db_con is not None:
                db_con.close()

    def get_stock_price(self, stock_symbol):
        Create()
        con = Connect()
        db_con = None
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            symbol = _canonical_stock_symbol(stock_symbol)
            res = "[METHOD EXECUTED] get_stock_price\n"
            query = "SELECT price FROM stocks WHERE symbol = '" + symbol + "'"
            res += "[QUERY] " + query + "\n"

            cur.execute(
                "SELECT price FROM stocks WHERE symbol = ?",
                (symbol,),
            )
            for result in cur.fetchall():
                res += "[RESULT] " + str(result) + "\n"
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            if db_con is not None:
                db_con.close()

    def update_stock_price(self, stock_symbol, price):
        Create()
        con = Connect()
        db_con = None
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            if not isinstance(price, float):
                raise Exception("ERROR: stock price provided is not a float")

            symbol = _canonical_stock_symbol(stock_symbol)
            res = "[METHOD EXECUTED] update_stock_price\n"
            query = "UPDATE stocks SET price = '%d' WHERE symbol = '%s'" % (price, symbol)
            res += "[QUERY] " + query + "\n"

            cur.execute(
                "UPDATE stocks SET price = ? WHERE symbol = ?",
                (price, symbol),
            )
            db_con.commit()
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            if db_con is not None:
                db_con.close()

    def exec_multi_query(self, query):
        Create()
        con = Connect()
        db_con = None
        res = "[METHOD EXECUTED] exec_multi_query\n"
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            for query_part in filter(None, query.split(';')):
                res += "[QUERY]" + query_part + "\n"
                query_outcome, changed = _execute_allowed_query(cur, query_part)
                if changed:
                    db_con.commit()
                for result in query_outcome:
                    res += "[RESULT] " + str(result) + " "
            return res

        except (sqlite3.Error, ValueError):
            return res + "[REJECTED] Unsupported query"

        finally:
            if db_con is not None:
                db_con.close()

    def exec_user_script(self, query):
        Create()
        con = Connect()
        db_con = None
        res = "[METHOD EXECUTED] exec_user_script\n"
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res += "[QUERY] " + query + "\n"
            if ';' in query:
                return res + "[REJECTED] Multiple statements are not allowed"

            query_outcome, changed = _execute_allowed_query(cur, query)
            if changed:
                db_con.commit()
            for result in query_outcome:
                res += "[RESULT] " + str(result)
            return res

        except (sqlite3.Error, ValueError):
            return res + "[REJECTED] Unsupported query"

        finally:
            if db_con is not None:
                db_con.close()
