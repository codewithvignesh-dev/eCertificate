from contextlib import contextmanager
import pymysql
from flask import current_app

class MySQL:
    def init_app(self, app):
        app.extensions["mysql"] = self

    def connection(self):
        return pymysql.connect(
            host=current_app.config["DB_HOST"],
            port=current_app.config["DB_PORT"],
            user=current_app.config["DB_USERNAME"],
            password=current_app.config["DB_PASSWORD"],
            database=current_app.config["DB_NAME"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
            connect_timeout=current_app.config["DB_CONNECT_TIMEOUT"],
            read_timeout=current_app.config["DB_READ_TIMEOUT"],
            write_timeout=current_app.config["DB_WRITE_TIMEOUT"]
        )

    @contextmanager
    def transaction(self):
        connection = self.connection()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def fetchone(self, sql, params=()):
        connection = self.connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()
        finally:
            connection.close()

    def fetchall(self, sql, params=()):
        connection = self.connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        finally:
            connection.close()

    def execute(self, sql, params=()):
        connection = self.connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                result = cursor.lastrowid
            connection.commit()
            return result
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def executemany(self, sql, params):
        connection = self.connection()
        try:
            with connection.cursor() as cursor:
                cursor.executemany(sql, params)
                result = cursor.rowcount
            connection.commit()
            return result
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def test_connection(self):
        connection = self.connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return cursor.fetchone() is not None
        finally:
            connection.close()
