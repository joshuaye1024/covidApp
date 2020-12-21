import trileaf_db

def update_covid():
    """Function to update covid tables in sql table"""

    df = None

    sql = 'INSERT INTO {} ({fields}) VALUES ({values})'

    def createCursor(db):
        cursor = db.cursor()
        print('>>Connected database, processing. . .')
        return cursor

    createCursor(db).executemany(insert_sql, values)

