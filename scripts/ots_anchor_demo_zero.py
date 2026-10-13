import hashlib, subprocess, os, json

HASH = "281a9c6b944d30220be7b209492d2183d3931f94175d086b7cd90995cfe05593"
PATH = "demo_zero_hash.txt"

with open(PATH, "w") as f:
    f.write(HASH)

# Independent check: the file content must hash to itself
with open(PATH, "rb") as f:
    content_hash = hashlib.sha256(f.read()).hexdigest()
print("file_sha256:", content_hash)
print("target:     ", HASH)
print("MATCH:" , content_hash == HASH)

# Attempt ots stamp if the CLI is available
try:
    r = subprocess.run(["ots", "stamp", PATH], capture_output=True, text=True, timeout=30)
    print("ots_stamp_stdout:", r.stdout)
    print("ots_stamp_stderr:", r.stderr)
    print("ots_stamp_code:", r.returncode)
except FileNotFoundError:
    print("ots_cli_not_installed")
except Exception as e:
    print("ots_error:", e)
