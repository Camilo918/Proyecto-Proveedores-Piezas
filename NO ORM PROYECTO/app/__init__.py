import os
import sqlite3
from flask import Flask, g

DB_FILENAME = 'data.sqlite'


def get_db():
    """Return a sqlite3 connection for the current app context (cached in g)."""
    db = getattr(g, '_database', None)
    if db is None:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, '..', DB_FILENAME)
        need_init = not os.path.exists(db_path)

        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON;')

        g._database = conn
        db = conn

        if need_init:
            _init_db_schema(db)

    return db


def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        g._database = None


def _init_db_schema(conn):
    """Create tables if they don't exist."""
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS provider (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            city TEXT,
            province TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS piece (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS supply (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider_id INTEGER NOT NULL,
            piece_id INTEGER NOT NULL,
            price REAL NOT NULL DEFAULT 0.0,
            quantity INTEGER NOT NULL DEFAULT 0,
            color TEXT,
            category TEXT,
            FOREIGN KEY(provider_id) REFERENCES provider(id) ON DELETE CASCADE,
            FOREIGN KEY(piece_id) REFERENCES piece(id) ON DELETE CASCADE,
            UNIQUE(provider_id, piece_id)
        );
    """)

    conn.commit()


def create_app(test_config=None):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SQLITE_DB'] = DB_FILENAME
    app.secret_key = 'dev-key'

    
    app.teardown_appcontext(close_db)

    
    from . import models, views
    app.register_blueprint(views.bp)

    
    with app.app_context():
        get_db()

    return app
