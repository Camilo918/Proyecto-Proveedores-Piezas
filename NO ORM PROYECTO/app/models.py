from typing import List, Optional, Dict, Any
from . import get_db


# ---------------------------
# PROVIDERS
# ---------------------------

def get_all_providers() -> List[Dict[str, Any]]:
    db = get_db()
    cur = db.execute("SELECT * FROM provider ORDER BY id")
    rows = cur.fetchall()
    return [dict(row) for row in rows]


def get_provider(provider_id: int) -> Optional[Dict[str, Any]]:
    db = get_db()
    cur = db.execute("SELECT * FROM provider WHERE id = ?", (provider_id,))
    row = cur.fetchone()
    return dict(row) if row else None


def create_provider(name: str, address: str, city: str, province: str) -> int:
    db = get_db()
    cur = db.execute(
        "INSERT INTO provider (name, address, city, province) VALUES (?, ?, ?, ?)",
        (name, address, city, province)
    )
    db.commit()
    return cur.lastrowid


def update_provider(provider_id: int, name: str, address: str, city: str, province: str) -> None:
    db = get_db()
    db.execute(
        "UPDATE provider SET name = ?, address = ?, city = ?, province = ? WHERE id = ?",
        (name, address, city, province, provider_id)
    )
    db.commit()


def delete_provider(provider_id: int) -> None:
    db = get_db()
    db.execute("DELETE FROM provider WHERE id = ?", (provider_id,))
    db.commit()


# ---------------------------
# PIECES
# ---------------------------

def get_all_pieces() -> List[Dict[str, Any]]:
    db = get_db()
    cur = db.execute("SELECT * FROM piece ORDER BY id")
    rows = cur.fetchall()
    return [dict(row) for row in rows]


def get_piece(piece_id: int) -> Optional[Dict[str, Any]]:
    db = get_db()
    cur = db.execute("SELECT * FROM piece WHERE id = ?", (piece_id,))
    row = cur.fetchone()
    return dict(row) if row else None


def create_piece(name: str) -> int:
    db = get_db()
    cur = db.execute("INSERT INTO piece (name) VALUES (?)", (name,))
    db.commit()
    return cur.lastrowid


def update_piece(piece_id: int, name: str) -> None:
    db = get_db()
    db.execute("UPDATE piece SET name = ? WHERE id = ?", (name, piece_id))
    db.commit()


def delete_piece(piece_id: int) -> None:
    db = get_db()
    db.execute("DELETE FROM piece WHERE id = ?", (piece_id,))
    db.commit()



def get_supplies_by_provider(provider_id: int) -> List[Dict[str, Any]]:
    db = get_db()
    cur = db.execute("""
        SELECT s.*, p.name AS piece_name
        FROM supply s
        JOIN piece p ON p.id = s.piece_id
        WHERE s.provider_id = ?
        ORDER BY s.id
    """, (provider_id,))
    rows = cur.fetchall()
    return [dict(row) for row in rows]


def get_supply(provider_id: int, piece_id: int) -> Optional[Dict[str, Any]]:
    db = get_db()
    cur = db.execute(
        "SELECT * FROM supply WHERE provider_id = ? AND piece_id = ?",
        (provider_id, piece_id)
    )
    row = cur.fetchone()
    return dict(row) if row else None


def get_supply_by_id(supply_id: int) -> Optional[Dict[str, Any]]:
    db = get_db()
    cur = db.execute("SELECT * FROM supply WHERE id = ?", (supply_id,))
    row = cur.fetchone()
    return dict(row) if row else None


def upsert_supply(provider_id: int, piece_id: int, price: float, quantity: int, color: str, category: str) -> int:
    db = get_db()
    existing = get_supply(provider_id, piece_id)

    if existing:
        db.execute("""
            UPDATE supply
            SET price = ?, quantity = ?, color = ?, category = ?
            WHERE provider_id = ? AND piece_id = ?
        """, (price, quantity, color, category, provider_id, piece_id))
        db.commit()
        return existing["id"]
    else:
        cur = db.execute("""
            INSERT INTO supply (provider_id, piece_id, price, quantity, color, category)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (provider_id, piece_id, price, quantity, color, category))
        db.commit()
        return cur.lastrowid


def delete_supply_by_id(supply_id: int) -> None:
    db = get_db()
    db.execute("DELETE FROM supply WHERE id = ?", (supply_id,))
    db.commit()
