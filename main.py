import threading
import random
import time

class Node:
    def __init__(self, node_id, total_nodes):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.active = True
        self.failed_nodes = set()
        self.suspected_nodes = set()
        self.replica_states = {}
        self.leader = None
        self.primary = False

    def send_message(self, target_node, message):
        print("Node {} sends message to Node {}: '{}'".format(self.node_id, target_node.node_id, message))
        target_node.receive_message(self, message)

    def receive_message(self, source_node, message):
        print("Node {} received message from Node {}: '{}'".format(self.node_id, source_node.node_id, message))

        if message == "Heartbeat":
            if not self.active:
                self.recover()
            self.send_message(source_node, "HeartbeatAck")

        elif message == "HeartbeatAck":
            if self.active and source_node in self.suspected_nodes:
                self.suspected_nodes.remove(source_node)
                print("Node {} removes suspicion on Node {}".format(self.node_id, source_node.node_id))

        elif message == "Replicate":
            if self.primary:
                replica_state = random.randint(1, 100)
                self.replica_states[source_node.node_id] = replica_state
                self.send_message(source_node, "ReplicateAck:{}".format(replica_state))

        elif message.startswith("ReplicateAck"):
            if self.leader is not None and self.leader != self and self.leader.active:
                replica_state = int(message.split(":")[1])
                self.leader.replica_states[source_node.node_id] = replica_state

        elif message.startswith("Fail"):
            failed_node_id = int(message.split(":")[1])
            if failed_node_id != self.node_id and failed_node_id != self.leader.node_id:
                self.fail_node(failed_node_id)

        elif message == "Recover":
            if self.active:
                self.send_message(source_node, "RecoverAck")

        elif message == "RecoverAck":
            if not self.active:
                self.recover()

    def heartbeat(self):
        while self.active:
            time.sleep(1)

            if random.random() < 0.1:
                self.detect_failed_nodes()

            if self.failed_nodes:
                self.recover_failed_nodes()

            if random.random() < 0.1:
                self.send_message(self.leader, "Heartbeat")

    def replicate(self):
        while self.active and self.primary:
            time.sleep(2)

            if random.random() < 0.2:
                for node in nodes:
                    if node != self and node.active and node not in self.failed_nodes and node not in self.suspected_nodes:
                        self.send_message(node, "Replicate")

    def fail_node(self, node_id):
        for node in nodes:
            if node.node_id == node_id:
                if node.active:
                    node.active = False
                    self.failed_nodes.add(node)
                    print("Node {} fails Node {}".format(self.node_id, node.node_id))
                break

    def recover(self):
        if not self.active:
            self.active = True
            self.failed_nodes.clear()
            self.suspected_nodes.clear()
            print("Node {} recovers".format(self.node_id))

    def detect_failed_nodes(self):
        for node in nodes:
            if node != self and node.active and node not in self.failed_nodes and node not in self.suspected_nodes:
                if random.random() < 0.5:
                    self.suspected_nodes.add(node)
                    print("Node {} suspects Node {}".format(self.node_id, node.node_id))

    def recover_failed_nodes(self):
        for node in self.failed_nodes.copy():
            if random.random() < 0.5:
                self.failed_nodes.remove(node)
                print("Node {} recovers Node {}".format(self.node_id, node.node_id))

                if self.leader is not None and self.leader != self and self.leader.active:
                    self.send_message(self.leader, "Recover")

    def run(self):
        heartbeat_thread = threading.Thread(target=self.heartbeat)
        heartbeat_thread.start()

        if self.node_id == 0:
            self.primary = True
            replicate_thread = threading.Thread(target=self.replicate)
            replicate_thread.start()

        heartbeat_thread.join()

if __name__ == "__main__":
    total_nodes = 5
    nodes = []

    for i in range(total_nodes):
        node = Node(i, total_nodes)
        nodes.append(node)

    # Start the threads
    threads = []
    for node in nodes:
        thread = threading.Thread(target=node.run)
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Determine the leader
    leader = None
    for node in nodes:
        if node.active and node.leader == node:
            leader = node
            break

    print("Elected leader: Node {}".format(leader.node_id))
