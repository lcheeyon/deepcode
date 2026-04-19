"""Shim entry for ``python3 -m apps.worker.main`` (repo root on ``PYTHONPATH``)."""

from deepguard_worker.run import run_worker_forever

if __name__ == "__main__":
    run_worker_forever()
