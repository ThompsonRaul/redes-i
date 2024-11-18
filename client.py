import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))

    print("Connected to the server. Type commands to interact with the notes.")
    print("Commands: CREATE_NOTE <note>, EDIT_NOTE <note_id> <new_content>, DELETE_NOTE <note_id>, VIEW_NOTE <note_id>, LIST_NOTES")

    while True:
        try:
            command = input("> ")
            if command.strip().lower() == "exit":
                break

            client.send(command.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(response)
        
        except Exception as e:
            print(f"Error: {e}")
            break

    client.close()

if __name__ == "__main__":
    start_client()
