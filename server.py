import numpy as np
import struct
import socket
import PIL.Image
import cv2


class ImageServer:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(("", 8010))
        self.s.listen(10)
        print("Socket now listening")

        self.conn, _ = self.s.accept()
        self.data = b""
        self.image_size = (256, 256)

    def receive(self):

        payload_size = struct.calcsize(">L")

        while len(self.data) < payload_size:
            self.data += self.conn.recv(4096)
        packed_msg_size = self.data[:payload_size]
        self.data = self.data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        while len(self.data) < msg_size:
            self.data += self.conn.recv(4096)
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]

        # preprocess
        pilImage = PIL.Image.frombytes("RGB", self.image_size, frame_data)
        npImage = np.array(pilImage)
        cvImage = cv2.cvtColor(npImage, cv2.COLOR_RGB2BGR)
        cvImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
        cv2.imshow("image", cvImage)
        cv2.waitKey(1)


if __name__ == "__main__":
    image_server = ImageServer()
    while True:
        image_server.receive()
