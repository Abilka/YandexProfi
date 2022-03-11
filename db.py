import random
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
        people_id = len(self.cur.execute('SELECT * FROM participant WHERE promo_id=?', (promo_id,)).fetchall())
        self.cur.execute('INSERT INTO participant (id, name, promo_id) VALUES (?, ?, ?)', (people_id, name, promo_id))
        self.con.commit()
        return people_id

    def new_prize(self, promo_id: str, desc: str) -> int:
        prize_id = len(self.cur.execute('SELECT * FROM prize WHERE promo_id=?', (promo_id,)).fetchall())
        self.cur.execute('INSERT INTO prize (id, description, promo_id) VALUES (?, ?, ?)', (prize_id, desc, promo_id))
        self.con.commit()
        return prize_id

    def change_promo(self, name: str, desc: str, id: int or str) -> bool:
        print(id)
        self.cur.execute('UPDATE promo SET name=?, description=? WHERE id=?', (name, desc, int(id)))
        self.con.commit()
        return True

    def get_promo(self) -> typing.List[dict]:
        self.cur.execute("SELECT id, name, description FROM promo")
        return [{"id": i[0], "name": i[1], "description": i[2]} for i in self.cur.fetchall()]

    def del_promo(self, id: int or str) -> bool:
        select_prize = self.cur.execute('SELECT id FROM promo WHERE id=?', (id,)).fetchone()
        if select_prize:
            self.cur.execute('DELETE FROM promo WHERE id=?', (str(id)))
            self.con.commit()
            return True
        else:
            return False

    def del_prize(self, id_promo: int or str, id_prize) -> bool:
        select_prize = self.cur.execute('SELECT id FROM prize WHERE id=? AND promo_id=?', (str(id_prize), str(id_promo))).fetchone()
        if select_prize and len(select_prize) > 0:
            self.cur.execute('DELETE FROM prize WHERE id=? AND promo_id=?', (str(id_prize), str(id_promo)))
            self.con.commit()
            return True
        else:
            return False

    def info_promo(self, id: int or str) -> dict or bool:
        result = self.cur.execute("SELECT * FROM promo WHERE id=?", (str(id))).fetchone()
        if result:
            promo = list(self.cur.execute("SELECT * FROM promo WHERE id=?", (str(id))).fetchone())
            promo = dict({"id": promo[0], 'name': promo[1], 'description': promo[2]})
            parct = self.cur.execute("SELECT id, name FROM participant WHERE promo_id=?", (str(id))).fetchall()
            prize = self.cur.execute("SELECT id, description FROM prize WHERE promo_id=?", (str(id))).fetchall()
            promo.update({"prizes": [{"id": i[0], 'name': i[1]} for i in prize]})
            promo.update({"participants": [{"id": i[0], 'name': i[1]} for i in parct]})

            return promo
        else:
            return False

    def raffle(self, promo_id: int or str) -> dict or bool:
        promo_id = str(promo_id)
        promo = self.info_promo(promo_id)
        if promo and len(promo.get('participants')) >= len(promo.get('prizes')):
            return {'winner': promo.get('participants')[:len(promo.get('prizes'))+1], "prize": promo.get('prizes')}
        else:
            return False

    def truncate(self):
        self.cur.execute("DELETE FROM prize")
        self.cur.execute("DELETE FROM participant")
        self.cur.execute("DELETE FROM promo")
        self.cur.execute("DELETE FROM result")
        self.con.commit()



