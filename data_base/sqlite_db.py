import sqlite3 as sq
from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect('italian_rest.db')
    cur = base.cursor()
    if base:
        print('Data base connected')
    base.execute('CREATE TABLE IF NOT EXISTS menu'
                 '(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    date = cur.execute('SELECT * FROM menu').fetchall()
    for ret in date:
        await bot.send_photo(message.from_user.id, ret[0],
                             f'{ret[1]}\nDescription: {ret[2]}\nPrice: {ret[-1]}$')


async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()


async def sql_delete(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()
