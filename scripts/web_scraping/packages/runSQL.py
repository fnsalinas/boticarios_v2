"""
Created on 28/09/2021
Author: Fabio Salinas (fabio.salinas1982@gmail.com)
Version: 1.0
"""

import pandas as pd
import psycopg2
from datetime import datetime as dt

def runSQL(
    SQL,
    user="postgres",
    password="A123",
    host="localhost",
    port="5432",
    database="postgres",
    sslcert=None,
    sslkey=None,
    sslrootcert=None,
    Select = True
    ):
    """
    Run SQL queries in postgreSQL with a Data Base conection

    Arguments:
        SQL         (String): Query to be executed on the Data Base.
        user        (String): Data base user. Default "postgres".
        password    (String): User password. Default "a123".
        host        (String): Data base Host. Default "localhost".
        port        (String): Data base Port. Default "5432".
        database    (String): Data base name. Default "postgres".
        sslcert     (String): Path to the ssl Cert (.crt).
        sslkey      (String): Path to the ssl Key (.key).
        sslrootcert (String): Path to the ssl Root Cert (.crt).
        Select      (Bool):   True for a "SELECT" Query (Default), False to run "INSERT, DELETE, DROP, TRUNCATE, UPDATE, etc"

    Returns (dict):
        {
            "result":  "Successful, Fail",
            "msg": "String with details about the result",
            "telapsed": <datetime.timedelta>,
            "dataFrame": <pandas.core.frame.DataFrame>,
            "query": "String sith the original query"
        }
    """

    start = dt.now()

    try:
        if sslcert!=None:
            db = psycopg2.connect(user=user, password=password, host=host, port=port, database=database, sslcert=sslcert, sslkey=sslkey, sslrootcert=sslrootcert)
        else:
            db = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
    except psycopg2.DatabaseError as error:
        print(error)
        return ({"result": "Fail", "msg": f"db Error: {error}", "telapsed": dt.now() - start, "DataFrame": pd.DataFrame(), "query": SQL})

    if Select:
        try:
            df = pd.read_sql(SQL, db)
            db.close()
            return ({"result": "Successful", "msg": f"Dataframe shape: {df.shape}", "telapsed": dt.now() - start, "DataFrame": df, "query": SQL})

        except psycopg2.DatabaseError as error:
            print(error)
            msg = f"{error}\n{'|'*25} Start Query {'|'*25}\n{SQL}\s{'|'*25} End Query {'|'*25}"
            return ({"result": "Fail", "msg": msg, "telapsed": dt.now() - start, "DataFrame": pd.DataFrame(), "query": SQL})

    else:
        try:
            cr = db.cursor()
            cr.execute(SQL)
            nrows = 0 if cr.rowcount is None else cr.rowcount
            db.commit()
            cr.close()
            msg = f"OK, {nrows:,.0f} rows affected."
            return ({"result": "Successful", "msg": msg, "telapsed": dt.now() - start, "DataFrame": pd.DataFrame(), "query": SQL})
        except psycopg2.DatabaseError as error:
            print(error)
            cr.close()
            msg = f"KO: {error}\n{'|'*25} Start Query {'|'*25}\n{SQL}\n,{'|'*25} End Query {'|'*25}"
            return ({"result": "Fail", "msg": msg, "telapsed": dt.now() - start, "DataFrame": pd.DataFrame(), "query": SQL})