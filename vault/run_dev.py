import subprocess
import sys
import time

STORAGE_NODES = [
    ("node-1", 50051),
    ("node-2", 50052),
    ("node-3", 50053),
]

ADMIN_API = ("control_plane", "python -m control_plane.admin_api")


def start_storage_node(node_id: str, port: int) -> subprocess.Popen:
    cmd = [
        sys.executable, "-m", "storage_node.main",
        node_id, str(port),
    ]
    proc = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
    return proc


def start_admin_api() -> subprocess.Popen:
    cmd = [sys.executable] + ADMIN_API[1:]
    proc = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
    return proc


def main() -> None:
    procs = []

    for node_id, port in STORAGE_NODES:
        proc = start_storage_node(node_id, port)
        procs.append(proc)
        print(f"Started {node_id} on port {port} (pid={proc.pid})")

    proc = start_admin_api()
    procs.append(proc)
    print(f"Started admin API on port 8000 (pid={proc.pid})")

    print("\nAll components running. Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        for proc in procs:
            proc.terminate()
        for proc in procs:
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
        print("All processes terminated.")


if __name__ == "__main__":
    main()