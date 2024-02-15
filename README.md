# Flask Book API Server

## Visão geral:

Esse é um projeto em python, feito com Flask, para montar um CRUD de uma biblioteca.
Algumas modificações foram feitas em relações ao projeto original, como adição de dois campos para Email e nome do livro.

HTML e CSS já prontos, feitos por Hillary Wando (@Wandonium).

## Progresso:
- [x] ~~Criação de funções para ações no banco~~
- [x] ~~Criação de rotas e suas funções~~
- [ ] Documentação - 50%
- [ ] Testes
- [ ] Modificações e limpeza de código

## Rotas e funções:

### Página inicial:
<img src="./images/front_1.png" alt="Página inicial">

Nada muito complicado ao carregar a página, somente uma função padrão do Flask:
```python
def index():
  return render_template('index.html')
```
E uma funçao para verificação de email, utilizada mais para frente:
```python
def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        return True
    else:
        return False
```
***
### POST:
<img src="./images/post.png" alt="POST">

Contém a função postRequest(), onde ele:
<ul>
  <li>
  Recebe o request:
    
  ```python
    req_data = request.get_json()
  ```
    
  </li>
  <li>
  Verifica se o email é válido:
    
  ```python
    email = req_data['email']
    if not isValid(email):
        return jsonify({
            'status':'422',
            'res':'failure',
            'error':'Invalid email format. Please enter a valid email address.'
        })
  ```  
  </li>
  <li>
  Salva o email e verifica se o livro já existe:
  
  ```python
    title = req_data['title']
    bks = [b.serialize() for b in db.view()]
    for b in bks:
      if b['title'] == title:
          return jsonify({
              'res': f'Error! Book with title {title} is already in library!',
              'status': '404'
          })
  ```
  </li>
  <li>
  E insere o livro no banco:
  
  ```python
    bk = Book(db.getNewId(), True, title, datetime.datetime.now())
    db.insert(bk)
  
    return jsonify({
          'res': bk.serialize(),
          'status': '200',
          'msg': 'Success!'
      })
  ```
  </li>
</ul>

### GET all:
<img src="./images/get_no_id.png" alt="GET all">

Contém a função getRequest, onde puxamos todos os livros do banco:
```python
def getRequest():
  bks = [b.serialize() for b in db.view()]
  return jsonify({
      'res': bks,
      'status': '200',
      'msg': 'Success!',
      'no_of_books': len(bks)
  })
```
### GET id:
<img src="./images/get_id.png" alt="GET id">

Função getRequestId(id), dessa vez específicando o id do livro a ser buscado:
```python
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
            'res': '',
            'error': 'No arguments given',
            'status': '404'
        })
```
### PUT:
<img src="./images/put.png" alt="PUT">

Função putRequest(), para editar as informações de um livro:
```python
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
```

### DELETE id:
<img src="./images/delete.png" alt="DELETE id">

Função deleteRequest(id), para deletar um livro do banco utilizando seu id:
```python
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
```
## Link original:

https://medium.com/@hillarywando/how-to-create-a-basic-crud-api-using-python-flask-cd68ef5fd7e3
