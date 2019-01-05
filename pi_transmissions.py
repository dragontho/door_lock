import socket
import time

class PI_Node:

    def __init__(self):
        self.pi_server = 'localhost'
        self.pi_port = 65432
        print("pi server node started at %s:%s" % (self.pi_server, self.pi_port))
        self.pc_server = 'localhost'
        self.pc_port = 65432
        print("pc server node targeted at %s:%s" % (self.pc_server, self.pc_port))

    def signal_door_state(self):
        # pc is client and pi is server
        door_state = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.pc_server, self.pc_port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    door_state = data
                    conn.sendall(data)
        return int(door_state.decode('utf-8'))

    def signal_motion(self, motion_state = "1"):
        # pc is server and pi is client
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.pc_server, self.pc_port))
            s.sendall(motion_state.encode("utf-8"))
            data = s.recv(1024)
        if int(data.decode("utf-8")):
            print("received signal for motion")
        else:
            print("signal for motion not received")

if __name__ == "__main__":
    pi_node = PI_Node()
    pi_node.signal_door_state()
    time.sleep(1)
    pi_node.signal_motion("0")

