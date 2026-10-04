# The same transfers as main.valk with boto3, for comparison. Needs boto3.
import sys, time, boto3
from boto3.s3.transfer import TransferConfig

size_mib = int(sys.argv[1]) if len(sys.argv) > 1 else 256
threads = int(sys.argv[2]) if len(sys.argv) > 2 else 10
s3 = boto3.client("s3", endpoint_url="http://127.0.0.1:9100", aws_access_key_id="valktest",
                  aws_secret_access_key="valktest-secret", region_name="us-east-1")
cfg = TransferConfig(max_concurrency=threads)
path = "/tmp/valk-s3-bench.bin"

def report(name, ms):
    print(f"{name}: {size_mib} MiB in {ms:.0f} ms = {size_mib / (ms / 1000):.0f} MiB/s")

t = time.monotonic()
s3.upload_file(path, "valk-s3-bench", "boto.bin", Config=cfg)
report("upload_file", (time.monotonic() - t) * 1000)
t = time.monotonic()
s3.download_file("valk-s3-bench", "boto.bin", "/tmp/valk-s3-bench.boto", Config=cfg)
report("download_file", (time.monotonic() - t) * 1000)
t = time.monotonic()
body = s3.get_object(Bucket="valk-s3-bench", Key="boto.bin")["Body"].read()
report("get_object", (time.monotonic() - t) * 1000)
small = b"x" * 1024
t = time.monotonic()
for i in range(1000):
    s3.put_object(Bucket="valk-s3-bench", Key=f"small/{i}", Body=small)
put_ms = (time.monotonic() - t) * 1000
t = time.monotonic()
for i in range(1000):
    s3.get_object(Bucket="valk-s3-bench", Key=f"small/{i}")["Body"].read()
print(f"1000 x 1 KiB: put {put_ms:.0f} ms, get {(time.monotonic() - t) * 1000:.0f} ms")
# Cross-check: the object valk uploaded reads back the same through boto3
v = s3.get_object(Bucket="valk-s3-bench", Key="big.bin")["Body"].read()
print("valk upload matches via boto3:", v == open(path, "rb").read())
