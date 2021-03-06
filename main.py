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
        self.hosts_list: list = ["127.0.0.1"]
        self.port_list: list = [21, 80, 110, 143, 443, 993, 8080]
        self.open: list = []
        self.threads: list = []

    def create_port_list(self) -> None:
        all_ports = range(65535)
        chunks = 5
        li = np.array_split(all_ports, chunks)
        self.port_list = li

    def full_scan(self) -> None:
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

    def list_scan(self) -> None:
        """Attempts a connection to each port in self.port_list. Each attempt receives it's own thread."""
        for port in self.port_list:
            thread = Thread(target=self.connect_to_port, args=(port,))
            self.threads.append(thread)
            thread.start()

        self.join_threads()

    def connect_to_port(self, port: int) -> None:
        """Connect to a port; if it accepts the connection, append the port to the self.open attribute."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.host, port))
        if result == 0:
            self.open.append(port)
        sock.close()

    def join_threads(self) -> None:
        """Wait for the threads in self.threads to finish."""
        for thread in self.threads:
            thread.join()

    def create_hosts_list(self, starting_address, ending_address) -> None:
        """Todo: Split this method up."""
        self.hosts_list = []  # Clear hosts list

        start = starting_address.split(".")
        end = ending_address.split(".")

        # Get the two "network" sections of the IP address
        network1 = start[0]
        network2 = start[1]

        # Get the first part of the "host" section of the IP address
        s = limit(int(start[-2]), 255)
        e = limit(int(end[-2]) + 1, 255)
        host1 = list(range(s, e))

        # Get the second part of the "host" section of the IP address
        s = limit(int(start[-1]), 255)
        e = limit(int(end[-1]) + 1, 255)
        host2 = list(range(s, e))

        # Loop through the requested ranges and append the range of IP addresses to self.hosts_list
        for i in host1:
            for j in host2:
                address = f"{network1}.{network2}.{i}.{j}"
                self.hosts_list.append(address)

    def results(self) -> None:
        if self.open:
            print("[+] Open ports:")
            for item in self.open:
                print(f"[+] {item}")
        else:
            print("[+] No open ports found.")


def limit(input_value: int, limit_value: int) -> int:
    if input_value > limit_value:
        return limit_value
    else:
        return input_value


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
