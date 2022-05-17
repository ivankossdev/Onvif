import socket
for x in range(10):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
    sock.connect(('localhost', 55000))  # подключемся к серверному сокету
    sock.send(bytes(f'Hello, world {x}', encoding='UTF-8'))  # отправляем сообщение
    data = sock.recv(1024)  # читаем ответ от серверного сокета
    sock.close()  # закрываем соединение
    print(data)
