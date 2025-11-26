# BASIC SHELL TCP SERVER ON PORT 33
# CODED BY IOSMEN (C) 2025
# https://github.com/iosmenq/TelnetShell?TelnetShell=source_code
import socket
import sys
import os
import subprocess

HOST = '192.168.1.107'
PORT = 33

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[OK] Port {PORT} opened successfully on {HOST}")
except Exception as e:
    print(f"[ERROR] Failed to open port {PORT}")
    print("Reason:", str(e))
    sys.exit(1)

print(f"[INFO] Waiting for connection on port {PORT}...")

while True:
    try:
        conn, addr = s.accept()
        print(f"[INFO] Connected by {addr}")
        conn.sendall(b"Connected to /bin/sh shell\n# ")

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                command = data.decode().strip()
                if command.lower() in ['exit', 'quit']:
                    break
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, executable='/bin/sh')
                    conn.sendall(output)
                except subprocess.CalledProcessError as e:
                    conn.sendall(e.output)
                conn.sendall(b"# ")
            except ConnectionResetError:
                print("[WARN] Client closed the connection unexpectedly.")
                break
        conn.close()
        print("[INFO] Connection closed.")
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped.")
        break


s.close()
