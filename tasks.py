from invoke import task
from tests.integration import harness


start_imposter = task(harness.start_imposter)

stop_imposter = task(harness.stop_imposter)
