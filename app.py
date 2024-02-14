from flask import Flask, render_template, request, jsonify
import os, re, datetime
import db
from models import Book
app = Flask(__name__)

if not os.path.isfile('books.db'):
    db.connect()

@app.route('/')
def index():
    return render_template('index.html')

def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        return True
    else:
        return False
    
@app.route('/request', methods=['POST'])
def postRequest():
    req_data = request.get_json()
    email = req_data['email']
    if not isValid(email):
        return jsonify({
            'status':'422',
            'res':'failure',
            'error':'Invalid email format. Please enter a valid email address.'
        })
    title = req_data['title']
    bks = [b.serialize() for b in db.view()]
    for b in bks:
        if b['title'] == title:
            return jsonify({
                'res': f'Error! Book with title {title} is already in library!',
                'status': '404'
            })
        
    bk = Book(db.getNewId(), True, title, datetime.datetime.now())
    db.insert(bk)

    return jsonify({
        'res': bk.serialize(),
        'status': '200',
        'msg': 'Success!'
    })

@app.route('/request', methods=['GET'])
def getRequest():
    content_type = request.headers.get('Content-Type')
    bks = [b.serialize() for b in db.view()]
    if (content_type == 'application/json'):
        json = request.json
        for b in bks:
            if b['id'] == int(json['id']):
                return jsonify({
                    'res': b,
                    'status': '200',
                    'msg': 'Success!'
                })
        return jsonify({
            'error': f'Error! Book with id "{json["id"]}" not found!',
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            'res': bks,
            'status': '200',
            'msg': 'Success!',
            'no_of_books': len(bks)
        })

@app.route('/request/<id>', methods=['GET'])
def getRequestId(id):
    req_args = request.view_args
    bks = [b.serialize() for b in db.view()]
    if req_args:
        for b in bks:
            if b['id'] == int(req_args['id']):
                return jsonify({
                    'res': b,
                    'status': '200',
                    'msg': 'Success!'
                })
        return jsonify({
            'error': f'Error! Book with id {req_args["id"]} was not found!',
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            'res': bks,
            'status': '200',
            'msg': 'Success getting book by ID!',
            'no_of_books': len(bks)
        })
    
@app.route('/request', methods=['PUT'])
def putRequest():
    req_data = request.get_json()
    try:
        title = req_data['title']
        book_id = req_data['id']
        availability = True
        books = [b.serialize() for b in db.view()]
        for b in books:
            if b['id'] == book_id:
                book = Book(
                    book_id,
                    availability,
                    title,
                    datetime.datetime.now()
                )
                db.update(book)
                return jsonify({
                    'res': book.serialize(),
                    'status': '200',
                    'msg': 'Success updating the book.'
                })
    except:
        return jsonify({
                'error': f'Error! Book not found!',
                'res': '',
                'status': '404'
            })

@app.route('/request/<id>', methods=['DELETE'])
def deleteRequest(id):
    req_args = request.view_args
    bks = [b.serialize() for b in db.view()]
    if req_args:
        for b in bks:
            if b['id'] == int(req_args['id']):
                db.delete(b['id'])
                updated_bks = [b.serialize() for b in db.view()]
                return jsonify({
                    'res': updated_bks,
                    'status': '200',
                    'msg': 'Success deleting book!',
                    'no_of_books': len(updated_bks)
                })
    else:
        return jsonify({
            'error': 'Error! No book id sent!',
            'res': '',
            'status': '404'
        })
    
if __name__ == '__main__':
    app.run()