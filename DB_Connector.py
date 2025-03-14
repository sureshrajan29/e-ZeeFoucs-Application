"""
This module is responsible for connect and access the database.

"""

import datetime
import itertools
import json
import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import text
import sys
import os
from logger import logger

# Use a breakpoint in the code line below to debug your script.
config = {
    'user': 'root',
    'password': 'e-consys',
    'host': 'localhost',
    'database': 'lens_gluing_automation',
    'port': 3306
}


class DBConnector:
    try:
        def __init__(self):
            try:
                self.cnx = mysql.connector.connect(**config)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error("Error at db main_init function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def insert_query(self, name, emp_id, role, biometric, password, previlege):
        try:
            """
              This method is used to insert the user details into db.
              param lists: name, emp_id, role, password, previlege all are str, biometric is array
              return: str
            """
            if not self.cnx.is_connected():
                self.cnx = mysql.connector.connect(**config)
            # insert the Query
            insert_query = "INSERT INTO user (name, emp_id, role, biometric, is_privilege, created_by, updated_by, " \
                           "password) " \
                           "VALUES ('{username}', '{emp_id}', '{role}', %s, '{previlege}',1, 1, '{password}')". \
                format(username=name, emp_id=emp_id, role=role, password=password, previlege=previlege)
            with self.cnx:
                with self.cnx.cursor() as cursor:
                    cursor.execute(insert_query, (biometric,))
                    cursor.nextset()
                    cursor.execute("set @counter = 0;")
                    cursor.nextset()
                    cursor.execute("update lens_gluing_automation.user set id  = (@counter := @counter + 1);")

                    # Close the cursor and the database connection
                    self.cnx.commit()
                    cursor.close()
                    self.cnx.close()
                    return "Query inserted"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at db insert query function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def update_query(self, name, password, user_permission, user_privilege, emp_id):
        try:
            """
              This method is used to update the user details.
              param lists: name, emp_id, user_permission, user_privilege all are str.
              return: str
            """
            if not self.cnx.is_connected():
                self.cnx = mysql.connector.connect(**config)
            with self.cnx:
                with self.cnx.cursor() as cursor:
                    cursor.execute("update lens_gluing_automation.user set name='{}', password='{}' , role='{}' , "
                                   "is_privilege='{}' "
                                   "where emp_id='{}';". format(name, password, user_permission, int(user_privilege), emp_id))
                    self.cnx.commit()
                    cursor.close()
                    self.cnx.close()
                    return "Query inserted"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at db update_query function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def delete(self, emp_id):
        try:
            """
              This method is used to delete the user details.
              param lists: emp_id is str.
              return: str
            """
            if not self.cnx.is_connected():
                self.cnx = mysql.connector.connect(**config)
            with self.cnx:
                with self.cnx.cursor() as cursor:
                    cursor.execute("update user set is_active = 0 where emp_id='{}';".format(emp_id))
                    self.cnx.commit()
                    cursor.nextset()
                    cursor.execute("set @counter = 0;")
                    cursor.nextset()
                    cursor.execute("update lens_gluing_automation.user set id  = (@counter := @counter + 1);")
                    self.cnx.commit()
                    cursor.close()
                    self.cnx.close()
                    return "Query inserted"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at db delete query function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def select_query(self, emp_id):
        try:
            """
              This method is used to get the user details using emp_id.
              param lists: emp_id is str.
              return: str
            """
            if not self.cnx.is_connected():
                self.cnx = mysql.connector.connect(**config)
            with self.cnx:
                with self.cnx.cursor() as cursor:
                    check = "SELECT role, is_privilege, password, biometric, is_active, name FROM " \
                            "lens_gluing_automation.user WHERE " \
                            "emp_id ={};".format(emp_id)
                    cursor.execute(check)
                    fetch = cursor.fetchall()
                    user_details = list(itertools.chain(*fetch))
                    cursor.close()
                    return user_details

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at db select_query function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def select_all(self):
        try:
            """
              This method is used to get all the user details.
              param lists: emp_id is str.
              return: user details in list
            """
            if not self.cnx.is_connected():
                self.cnx = mysql.connector.connect(**config)
            with self.cnx:
                with self.cnx.cursor() as cursor:
                    cursor.execute("SELECT * FROM lens_gluing_automation.user")
                    fetch = cursor.fetchall()
                    cursor.close()
                    return fetch

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at db select_all function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def fetch_biometric(self, emp_id):
        try:
            """
              This method is used to get the user fingerprint detail using emp_id.
              param lists: emp_id is str.
              return: str
            """
            if not self.cnx.is_connected():
                self.cnx = mysql.connector.connect(**config)
            with self.cnx:
                with self.cnx.cursor() as cursor:
                    check = "SELECT biometric FROM lens_gluing_automation.user WHERE emp_id ={};".format(emp_id)
                    cursor.execute(check)
                    fetch = cursor.fetchall()
                    user_details = list(itertools.chain(*fetch))
                    biometric = [user_details[0]]
                    fetch_biometric = []
                    for i, item in enumerate(biometric):
                        fetch_biometric.append(eval(item))
                    for y in fetch_biometric:
                        value = y
                    cursor.close()
                    return value

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at db fetch_biometric function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def fetch_emp_id(self):
        """
          This method is used to get the user emp_id.
          param lists: None.
          return: emp_id as str
        """
        if not self.cnx.is_connected():
            self.cnx = mysql.connector.connect(**config)
        with self.cnx:
            with self.cnx.cursor() as cursor:
                cursor.execute("SELECT emp_id FROM lens_gluing_automation.user")
                fetch = cursor.fetchall()
                emp_id = list(itertools.chain(*fetch))
                cursor.close()
                return emp_id


# if __name__ == '__main__':
#     var = DBConnector()
#     print(var.select_query(220500807))
#     print(var.fetch_emp_id())
# my_data = b'\x00\x01\x02\x03\x04'
# var.insert_query()
# var.insert_query(biometric=my_data, name='sgsrgh', emp_id=3, role='ADMIN', password='k')
# var.select_query()
#     print(datetime.datetime(2023, 3, 7, 5, 57, 45))
# var.insert_querys(my_data, 'Senthil', 3)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
