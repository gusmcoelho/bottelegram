import sqlite3

def init_db():
    conn = sqlite3.connect('pedro.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos 
        (user_id INTEGER, produto TEXT, status TEXT)''')
    conn.commit()
    conn.close()

def salvar_pedido(user_id, produto):
    conn = sqlite3.connect('pedro.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pedidos (user_id, produto, status) VALUES (?, ?, 'pendente')", (user_id, produto))
    conn.commit()
    conn.close()