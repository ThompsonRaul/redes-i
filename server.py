import socket
import threading
import sqlite3
import os

# Configura o banco de dados SQLite
db_filename = 'notes.db'

# Função para inicializar o banco de dados e criar a tabela de notas, caso não exista
def init_db():
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_note_to_db(content):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    return note_id

def update_note_in_db(note_id, content):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET content = ? WHERE id = ?", (content, note_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

def delete_note_from_db(note_id):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

def get_note_from_db(note_id):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM notes WHERE id = ?", (note_id,))
    note = cursor.fetchone()
    conn.close()
    return note[0] if note else None

def list_notes_from_db():
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return notes

# Função para lidar com o cliente e os comandos
def handle_client(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8').strip()
            if not msg:
                break

            # Parseia o comando
            command = msg.split()
            action = command[0]

            if action == "CREATE_NOTE":
                note_content = " ".join(command[1:])
                note_id = save_note_to_db(note_content)
                response = f"NOTE_CREATED {note_id}"
                
            elif action == "EDIT_NOTE":
                note_id = int(command[1])
                new_content = " ".join(command[2:])
                if update_note_in_db(note_id, new_content):
                    response = "NOTE_UPDATED"
                else:
                    response = "ERROR Note not found"
                    
            elif action == "DELETE_NOTE":
                note_id = int(command[1])
                if delete_note_from_db(note_id):
                    response = "NOTE_DELETED"
                else:
                    response = "ERROR Note not found"
                    
            elif action == "VIEW_NOTE":
                note_id = int(command[1])
                content = get_note_from_db(note_id)
                if content:
                    response = f"NOTE {note_id}: {content}"
                else:
                    response = "ERROR Note not found"
                    
            elif action == "LIST_NOTES":
                notes = list_notes_from_db()
                if notes:
                    response = "\n".join([f"{note_id}: {content}" for note_id, content in notes])
                else:
                    response = "No notes available"
            else:
                response = "ERROR Unknown command"
            
            client_socket.send(response.encode('utf-8'))

        except Exception as e:
            print(f"Error handling client: {e}")
            break

    client_socket.close()

# Função para iniciar o servidor
def start_server():
    init_db()  # Inicializa o banco de dados
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9998))
    server.listen(5)
    print("Server listening on port 9998...")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()
