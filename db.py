import sqlite3
from flask import g
from sqlite3 import Error
import os


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("crate.db")
        db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def change_db(query, args=()):
    db = get_db()
    db.execute(query, args)
    db.commit()

def get_users():
    query = "SELECT * FROM users WHERE role='User'"
    return query_db(query)

def get_admins():
    query = "SELECT * FROM users WHERE role='Admin'"
    return query_db(query)


def delete_user(name):
    query = "DELETE FROM users WHERE name = (?)"
    return change_db(query, (name,))

def add_user(name, age, password, role):
    query = "INSERT INTO users(name, age, password, role) VALUES (?, ?, ?, ?)"
    return change_db(query, (name, age, password, role))

