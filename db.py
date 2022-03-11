import sqlite3
import typing


class DB:
    """Класс взаимодействия с БД"""

    def __init__(self):
        self.con = sqlite3.connect('base.db')
        self.cur = self.con.cursor()

    def new_promo(self, name: str, desc: str) -> int or str:
        self.cur.execute('INSERT INTO promo (name, description) VALUES (?, ?)', (name, desc))
        id = self.cur.lastrowid
        self.con.commit()
        return id

    def new_participant(self, name: str, promo_id: int) -> int or str:
        self.cur.execute('INSERT INTO participant (name, promo_id) VALUES (?, ?)', (name, promo_id))
        id = self.cur.lastrowid
        self.con.commit()
        return id

    def new_prize(self, promo_id: str, desc: str) -> int:
        self.cur.execute('INSERT INTO prize (description, promo_id) VALUES (?, ?)', (desc, promo_id))
        id = self.cur.lastrowid
        self.con.commit()
        return id


    def change_promo(self, name: str, desc: str, id: int or str) -> bool:
        print(id)
        self.cur.execute('UPDATE promo SET name=?, description=? WHERE id=?', (name, desc, int(id)))
        self.con.commit()
        return True

    def get_promo(self) -> typing.List[dict]:
        self.cur.execute("SELECT id, name, description FROM promo")
        return [{"id": i[0], "name": i[1], "description": i[2]} for i in self.cur.fetchall()]

    def del_promo(self, id: int or str) -> bool:
        self.cur.execute('DELETE FROM promo WHERE id=?', (str(id)))
        self.con.commit()
        return True

    def info_promo(self, id: int or str) -> dict:
        promo = list(self.cur.execute("SELECT * FROM promo WHERE id=?", (str(id))).fetchone())
        promo = dict({"id": promo[0], 'name': promo[1], 'description': promo[2]})
        parct = self.cur.execute("SELECT id, name FROM participant WHERE promo_id=?", (str(id))).fetchall()
        prize = self.cur.execute("SELECT id, description FROM prize WHERE promo_id=?", (str(id))).fetchall()
        promo.update({"prizes": [{"id": i[0], 'name': i[1]} for i in prize]})
        promo.update({"participants": [{"id": i[0], 'name': i[1]} for i in parct]})

        return promo

