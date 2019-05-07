import socket, select

def handle_http(client, client_addr):
    client.send("HTTP/1.0 200 OK\r\n\r\nHelloWorld!!!\r\n  %s" % str(client_addr))
    client.close()

def serv(port=80):
    http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (socket.getaddrinfo("0.0.0.0", port))[0][-1]
    http.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    http.bind(addr)
    http.listen(4)

    while True:
        r, w, err = select.select((http,), (), (), 1)
        if r:
            for readable in r:
                client, client_addr = http.accept()
                handle_http(client, client_addr)

serv()