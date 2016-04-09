from invoke import task
from tests.integration import harness


start_mb = task(harness.start_mb)

stop_mb = task(harness.stop_mb)
