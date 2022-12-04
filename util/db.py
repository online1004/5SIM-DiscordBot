import sqlite3

def user_data(user_id:int):
    con = sqlite3.connect(f'./DB/database.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM user WHERE id == ?;", (user_id,))
    result = cur.fetchone()
    return result

def data_create(user_id:int):
    con = sqlite3.connect(f'./DB/database.db')
    cur = con.cursor()
    cur.execute("INSERT INTO user VALUES(?, ?, ?)", (user_id, "0", "0"))
    con.commit()
    con.close()

def add_money(user_id:int, money:int):
    con = sqlite3.connect(f'./DB/database.db')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM user WHERE id = {user_id}')
    result = cur.fetchone()
    last_m = result[1]
    new_m = int(last_m) + int(money)
    cur.execute("UPDATE user SET money = ? WHERE id == ?;", (new_m, user_id))
    con.commit()
    cur.execute(f'SELECT * FROM user WHERE id = {user_id}')
    result = cur.fetchone()
    con.close()
    return result[1]

def sub_money(user_id:int, money:int):
    con = sqlite3.connect(f'./DB/database.db')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM user WHERE id = {user_id}')
    result = cur.fetchone()
    last_m = result[1]
    new_m = int(last_m) - int(money)
    buylog = int(result[2]) + 1
    cur.execute("UPDATE user SET money = ?, buylog = ? WHERE id == ?;", (new_m, buylog, user_id))
    con.commit()
    cur.execute(f'SELECT * FROM user WHERE id = {user_id}')
    result = cur.fetchone()
    con.close()
    return result[1]
