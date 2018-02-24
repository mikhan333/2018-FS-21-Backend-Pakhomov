# -*- coding: utf-8 -*-
import socket

import os
import re

def get_response(request):

    all = request.split("\n")
    method, address, protocol = all[0].split(" ")


    result = re.match(r'/test\d+.txt/', address)



    if address == "/":  #обработка пути /
        answer = "HTTP/1.1 200 OK\n\n"
        answer += "Hello mister!\nYou are:"
        for i in range(len(all)):
            if all[i].find("User-Agent:")!=-1:
                answer+=all[i].split("User-Agent:")[1]
                return answer


    elif address == "/test/":  #обработка пути /test/
        answer = "HTTP/1.1 200 OK\n\n"
        answer+="http://localhost:8000"+address
        return answer


    elif address == "/media/":  #обработка пути /media/
        directory = '/home/mikhan/Downloads/ProjectWeb/lesson1/files'
        files = os.listdir(directory)

        answer = "HTTP/1.1 200 OK\n\n"
        answer+='\n'.join(files)
        return answer


    elif result!=None:  #обработка пути /test\d+.txt/
        directory = '/home/mikhan/Downloads/ProjectWeb/lesson1/files'
        files = os.listdir(directory)
        result2 = re.search(r'test\d+.txt', address)
        result2 = result2.group(0)

        for i in range(len(files)):
            if files[i]==result2:  #обработка пути, если файл существует
                f = open('../files/'+result2)
                l = [line.strip() for line in f]

                answer = "HTTP/1.1 200 OK\n\n"
                answer += '\n'.join(l)
                return answer

          #обработка пути, если файла нет
        answer = "HTTP/1.1 404 Not found\n\n"
        answer+="File not found"
        return answer


    else:  #обработка любого другого пути
        answer = "HTTP/1.1 404 Not found\n\n"
        answer+="Page not found"
        return answer


    #return 'WRITE YOU RESPONSE HERE\n'


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  #привязываем сокет с имеющимся у компьютера хостом и свободным портом: в данном случае
                                         # локальный сервер на порту 8000
server_socket.listen(0)  #переключаем сокет в режим прослушивания, "0" - максимальная длина очереди

print 'Started'
while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print 'Got new client', client_socket.getsockname()  #получаем имя локального хоста(адрес сокета на "нашем конце" соединения)(хост+порт) и выводим
        request_string = client_socket.recv(2048)  #читаем данные порциями по 2048байт
        client_socket.send(get_response(request_string))  #отправляем данные: строку, которую мы получим из функции get_response(request)
        client_socket.close()
    except KeyboardInterrupt:  #обработаем прерывание программы на сервере(Ctrl+C)
        print 'Stopped'
        server_socket.close()  #закрываем сокет
        exit()

