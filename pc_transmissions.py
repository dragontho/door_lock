import socket
import time

class PC_Node:

    def __init__(self):
        self.pc_server = 'localhost'
        self.pc_port = 65432
        print("pc server node started at %s:%s" % (self.pc_server, self.pc_port))
        self.pi_server = 'localhost'
        self.pi_port = 65432
        print("pi server node targeted at %s:%s" % (self.pi_server, self.pi_port))

    def signal_door_state(self, door_state):
        # pc is client and pi is server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.pc_server, self.pc_port))
            s.sendall(door_state.encode('utf-8'))
            data = s.recv(1024)
        if int(data.decode('utf-8')):
            print("signal door to open")
        else:
            print("signal door to close")

    def signal_motion(self):
        # pc is server and pi is client
        motion_detected = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.pi_server, self.pi_port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    motion_detected = data
                    conn.sendall(data)
        return int(motion_detected.decode('utf-8'))

if __name__ == "__main__":
    pc_node = PC_Node()
    pc_node.signal_door_state('1')
    pc_node.signal_motion()
