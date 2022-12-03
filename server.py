#Server
import socket
import select
from _thread import *
import sys
import time
import random


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Print in the following order : script, IP address, port number")
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

server.bind((IP_address, Port))
server.listen(3)

list_of_clients = []

Q = [" What is the Italian word for PIE? \n a.Mozarella b.Pasty c.Patty d.Pizza",
     " Water boils at 212 Units at which scale? \n a.Fahrenheit b.Celsius c.Rankine d.Kelvin",
     " Which sea creature has three hearts? \n a.Dolphin b.Octopus c.Walrus d.Seal",
     ]

A = ['d', 'a', 'b']

Count = []
client = ["address", -1]
bzr = [0, 0, 0]  


def clientthread(conn, addr):
    conn.send(bytes("Hello Genius!!!\n Welcome to this quiz! Answer any 5 questions correctly before your opponents do\n Press any key on the keyboard as a buzzer for the given question\n",'utf-8'))
    # Intro MSG
    while True:
        message = conn.recv(2048).decode()
        if message:
            if bzr[0] == 0:
                client[0] = conn
                bzr[0] = 1
                i = 0
                while i < len(list_of_clients):
                    if list_of_clients[i] == client[0]:
                        break
                    i += 1
                client[1] = i

            elif bzr[0] == 1 and conn == client[0]:
                bol = message[0] == A[bzr[2]][0]
                print(A[bzr[2]][0])
                if bol:
                    broadcast("player" + str(client[1] + 1) + " +1" + "\n\n")
                    Count[i] += 1
                    if Count[i] == 3:
                        broadcast("player" + str(client[1] + 1) + " WON" + "\n")
                        end_quiz()
                        sys.exit()

                else:
                    broadcast("player" + str(client[1] + 1) + " -1" + "\n\n")
                    Count[i] -= 1
                bzr[0] = 0
                if len(Q) != 0:
                    Q.pop(bzr[2])
                    A.pop(bzr[2])
                if len(Q) == 0:
                    end_quiz()
                quiz()

            else:
                conn.send(bytes(" player " + str(client[1] + 1) + " pressed buzzer first\n\n",'utf-8'))
        else:
            remove(conn)


def broadcast(message):
    for clients in list_of_clients:
        try:
            clients.send(bytes(message,'utf-8'))
        except:
            clients.close()
            remove(clients)


def end_quiz():
    broadcast("Game Over\n")
    bzr[1] = 1
    i = Count.index(max(Count))
    broadcast("player " + str(i + 1) + " wins!! by scoring " + str(Count[i]) + " points.")
    for x in range(len(list_of_clients)):
        list_of_clients[x].send(bytes("You scored " + str(Count[x]) + " points.",'utf-8'))

    # server.close()


def quiz():

    if len(Q) != 0:
        bzr[2] = random.randint(1, 10000) % len(Q)
        for connection in list_of_clients:
            connection.send(bytes(Q[bzr[2]],'utf-8'))


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    Count.append(0)
    print(addr[0] + " connected")

    start_new_thread(clientthread, (conn, addr))
    if (len(list_of_clients) == 3):
        quiz()
conn.close()
server.close()
