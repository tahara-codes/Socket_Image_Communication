import cv2
import socket
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 8010))
connection = client_socket.makefile("wb")

while True:
    frame = cv2.imread("./example.png")
    data = bytes(frame)
    size = len(data)
    client_socket.sendall(struct.pack(">L", size) + data)
