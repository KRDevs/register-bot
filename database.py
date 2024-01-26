import sqlite3 as sq

db = sq.connect('base.db')
cursor = db.cursor()


async def db_start():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS User("
        "user_id TEXT PRIMARY KEY,"
        "phone_number TEXT,"
        "name TEXT,"
        "description TEXT)"
    )
    db.commit()


async def create_user(user_id, phone_number, name, description):
    global cursor
    user = cursor.execute("SELECT 1 FROM User WHERE user_id=='{key}'".format(key=user_id)).fetchone()
    if not user:
        cursor.execute("INSERT INTO User VALUES(?,?,?,?)",
                       (user_id, phone_number, name, description))
        db.commit()


async def edit_user(state, user_id):
    state_data = await state.get_data()
    cursor.execute(
        "UPDATE User SET phone_number=?, name=?, description=? WHERE user_id=?",
        (state_data.get('phone_number', ''),
         state_data.get('name', ''),
         state_data.get('description', ''),
         user_id)
    )
    db.commit()
