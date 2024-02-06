import sqlite3, random, datetime
from models import Book

def getNewId():
    return random.getrandbits(28)

books = [
    # {
    #     'available': True,
    #     'title': 'Don Quixote',
    #     'timestamp': datetime.datetime.now()
    # },
    {
        'avaliable': True,
        'title': '',
        'timestamp': datetime.datetime.now()
    },
    {
        'avaliable': True,
        'title': '',
        'timestamp': datetime.datetime.now()
    },
    {
        'avaliable': True,
        'title': '',
        'timestamp': datetime.datetime.now()
    },
    {
        'avaliable': True,
        'title': '',
        'timestamp': datetime.datetime.now()
    },
    {
        'avaliable': True,
        'title': '',
        'timestamp': datetime.datetime.now()
    }
    
]

def connect():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, avaliable BOOLEAN, title TEXT, timestamp TEXT)')
    conn.commit()
    conn.close()
    for i in books:
        bk = Book(getNewId(), i['avaliable'], i['title'], i['timestamp'])
        insert(bk)

def insert(book):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books VALUES (?,?,?,?)', (
        book.id,
        book.available,
        book.title,
        book.timestamp
    ))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    rows = cursor.fetchall()
    books = []
    for i in rows:
        book = Book(i[0], True if i[1] == 1 else False, i[2], i[3])
        books.append(book)
    conn.close()
    return books

def update(book):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET avaliable=?, title=? WHERE id=?', (book.avaliable, book.title, book.id))
    conn.commit()
    conn.close()

def delete(theId):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id=?', (theId))
    conn.commit()
    conn.close()

def deleteAll():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books')
    conn.commit()
    conn.close()