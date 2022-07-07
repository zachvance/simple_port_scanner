import argparse
import socket
from threading import Thread
from time import perf_counter

import numpy as np


class Menu:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="A simple port scanner written in python utilizing the socket and threading libraries."
        )

        self.parser.add_argument(
            "scan_type",
            default="l",
            nargs="?",
            choices=["l", "f"],
            help="The type of scan to perform.",
        )
        self.parser.add_argument(
            "-t",
            "--target",
            default="127.0.0.1",
            type=str,
            help="The host machine.",
        )
        self.parser.add_argument(
            "-p",
            "--ports",
            nargs="+",
            default=[21, 80, 110, 143, 443, 993, 8080],
            type=int,
            help="Specify the ports.",
        )


class ScanQuery:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port_list = [21, 80, 110, 143, 443, 993, 8080]
        self.open = []
        self.threads = []

    def full_scan(self):
        """~88 seconds to complete"""

        all_ports = range(65535)
        chunks = 5
        split = np.array_split(all_ports, chunks)
        for item in split:
            print(
                f"[+] Currently scanning ports {item[0] + 1} though {item[-1] + 1}..."
            )
            for i in item:
                port = i + 1
                thread = Thread(target=self.connect_to_port, args=(port,))
                self.threads.append(thread)
                thread.start()
            self.join_threads()

    def list_scan(self):
        """Attempts a connection to each port in self.port_list. Each attempt receives it's own thread."""
        for port in self.port_list:
            thread = Thread(target=self.connect_to_port, args=(port,))
            self.threads.append(thread)
            thread.start()

        self.join_threads()

    def connect_to_port(self, port):
        """Connect to a port; if it accepts the connection, append the port to the self.open attribute."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.host, port))
        if result == 0:
            self.open.append(port)
        sock.close()

    def join_threads(self):
        """Wait for the threads in self.threads to finish."""
        for thread in self.threads:
            thread.join()

    def results(self):
        if self.open:
            print("[+] Open ports:")
            for item in self.open:
                print(f"[+] {item}")
        else:
            print("[+] No open ports found.")


if __name__ == "__main__":

    m = Menu()
    args = m.parser.parse_args()

    start_time = perf_counter()
    sq = ScanQuery()
    sq.port_list = args.ports
    sq.host = args.target

    if args.scan_type == "l":
        print(f"[+] Scanning ports {sq.port_list} on {sq.host}.")
        sq.list_scan()
    elif args.scan_type == "f":
        print(f"[+] Scanning all ports on {sq.host}.")
        sq.full_scan()

    end_time = perf_counter()
    print(f"[+] Scan took {end_time - start_time: 0.2f} second(s) to complete.")
    sq.results()
