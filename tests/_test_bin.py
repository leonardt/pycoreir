import os
import subprocess


def test_bin():
    result = subprocess.run(
        "python bin/coreir -i tests/concat.json -p 'rungenerators; flatten'",
        shell=True, capture_output=True)
    assert not result.returncode, \
        "Got non-zero exit code ({result.returncode}): " + \
        result.stdout.decode() + result.stderr.decode()
