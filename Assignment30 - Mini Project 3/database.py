import sqlite3

con = sqlite3.connect('db/data.db')
my_cursor = con.cursor()

def add_employee(id, firstName, lastName, birthday, nationalCode, imagePath):
    my_cursor.execute(f'INSERT INTO employee(id, firstName, lastName, birthday, nationalCode, imagePath) VALUES("{id}", "{firstName}", "{lastName}", "{birthday}", "{nationalCode}", "{imagePath}")')
    con.commit()

def get_all_employee():
    my_cursor.execute('SELECT * FROM employee')
    result = my_cursor.fetchall()
    return result

def get_employee_detail(id):
    my_cursor.execute(f'SELECT * FROM employee WHERE id={id}')
    result = my_cursor.fetchall()
    return result

def delete_employee(id):
    my_cursor.execute(f'DELETE FROM employee WHERE id={id}')
    con.commit()

def update_employee(id, firstName, lastName, birthday, nationalCode, imagePath):
    my_cursor.execute(f'UPDATE employee SET (id, firstName, lastName, birthday, nationalCode, done, priority) VALUES("{id}", "{firstName}", "{lastName}", "{birthday}", "{nationalCode}", "{imagePath}") WHERE id={id}')
    con.commit()

def checkPassword(username, password):
    my_cursor.execute('SELECT * FROM admin')
    result = my_cursor.fetchall()
    if result[0][1]==username and result[0][2]==password:
        return True
    else:
        return False

def countEmployee():
    my_cursor.execute('SELECT * FROM employee')
    result = my_cursor.fetchall()
    return len(result)
