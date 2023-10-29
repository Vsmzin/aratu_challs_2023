import socketserver
import jsonpickle
import base64
import threading

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
	
        class User:
            def __init__(self, username, password, age):
                self.username = username
                self.password = password
                self.age = age

        questions = ["username", "password", "idade"]

        self.request.settimeout(3)

        boita = '''
╦┌┬┐┌─┐┌─┐┬ ┬┬
║ │ ├─┤│  ├─┤│
╩ ┴ ┴ ┴└─┘┴ ┴┴
┌─┐┬─┐┌─┐┌─┐┬┌─┌─┐┬─┐┌─┐
│  ├┬┘├─┤│  ├┴┐├┤ ├┬┘ ┌┘
└─┘┴└─┴ ┴└─┘┴ ┴└─┘┴└─ o

IN DEVELOPMENT


OPTIONS: login and check_login

'''
        self.request.sendall(boita.encode())

        def login(username, password, age):
            user1 = User(username, password, age)
            logado = jsonpickle.encode(user1)
            user_base64 = base64.b64encode(logado.encode("utf-8"))
            return user_base64
        
        def who(tech):
            token = jsonpickle.decode(base64.urlsafe_b64decode(tech))
            user = token['username']
            return "Bem vindo " + user

        try:
            self.request.sendall("Selecione uma das options: ".encode())
            self.data = self.request.recv(1024).strip().decode('utf-8')

            if self.data.lower() == "login":
                user_info = {}
                for i in range(3):
                    self.request.sendall(f"Informe {questions[i]}: ".encode('utf-8'))
                    info = self.request.recv(1024).strip().decode('utf-8')
                    user_info[questions[i]] = info

                user_data = login(user_info['username'], user_info['password'], user_info['idade'])
                self.request.sendall(f"token: {user_data}".encode('utf-8'))

            elif self.data.lower() == "check_login":
                self.request.sendall("Insira o token: ".encode('utf-8'))
                info2 = self.request.recv(1024).strip().decode('utf-8')
                response = who(info2)
                self.request.sendall(response.encode('utf-8'))

        except socket.timeout:
            self.request.sendall("Tempo esgotado. Conexão encerrada.".encode('utf-8'))
        finally:
            self.request.close()

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1337


    server_thread = threading.Thread(target=lambda: socketserver.TCPServer((HOST, PORT), MyTCPHandler).serve_forever())
    server_thread.daemon = True
    server_thread.start()

    print(f"Servidor aguardando conexões em {HOST}:{PORT}")


    server_thread.join()



