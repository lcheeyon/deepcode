"""``python3 -m deepguard_worker`` — Redis Streams consumer (Phase L4)."""

from deepguard_observability.runtime import configure_langsmith_env_defaults

from deepguard_worker.run import run_worker_forever

if __name__ == "__main__":
    configure_langsmith_env_defaults()
    run_worker_forever()
