# Signs requests with botocore and prints the signatures, to cross-check the valk signer.
# Usage: python3 tests/sigv4_botocore.py  (needs boto3/botocore installed)
import datetime
from unittest import mock
from botocore.auth import SigV4Auth, S3SigV4Auth, S3SigV4QueryAuth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials

def sign(auth_cls, creds, service, region, when, method, url, headers, body=b"", expires=None):
    req = AWSRequest(method=method, url=url, headers=headers, data=body)
    with mock.patch("botocore.auth.get_current_datetime", return_value=when):
        if expires is None:
            auth = auth_cls(creds, service, region)
        else:
            auth = auth_cls(creds, service, region, expires=expires)
        auth.add_auth(req)
    if expires is not None:
        return req.url
    return req.headers["Authorization"]

suite = Credentials("AKIDEXAMPLE", "wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY")
t15 = datetime.datetime(2015, 8, 30, 12, 36, 0)
print("get-vanilla", sign(SigV4Auth, suite, "service", "us-east-1", t15, "GET", "https://example.amazonaws.com/", {}))
print("get-vanilla-query-order-key-case", sign(SigV4Auth, suite, "service", "us-east-1", t15, "GET", "https://example.amazonaws.com/?Param2=value2&Param1=value1", {}))
print("post-vanilla", sign(SigV4Auth, suite, "service", "us-east-1", t15, "POST", "https://example.amazonaws.com/", {}))
print("get-header-value-trim", sign(SigV4Auth, suite, "service", "us-east-1", t15, "GET", "https://example.amazonaws.com/", {"My-Header1": " value1", "My-Header2": ' "a   b   c"'}))
print("post-x-www-form-urlencoded", sign(SigV4Auth, suite, "service", "us-east-1", t15, "POST", "https://example.amazonaws.com/", {"Content-Type": "application/x-www-form-urlencoded"}, b"Param1=value1"))

s3c = Credentials("AKIAIOSFODNN7EXAMPLE", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")
t13 = datetime.datetime(2013, 5, 24, 0, 0, 0)
e = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
print("s3-get-object", sign(S3SigV4Auth, s3c, "s3", "us-east-1", t13, "GET", "https://examplebucket.s3.amazonaws.com/test.txt", {"Range": "bytes=0-9", "x-amz-content-sha256": e}))
print("s3-list", sign(S3SigV4Auth, s3c, "s3", "us-east-1", t13, "GET", "https://examplebucket.s3.amazonaws.com/?max-keys=2&prefix=J", {"x-amz-content-sha256": e}))
print("s3-presign", sign(S3SigV4QueryAuth, s3c, "s3", "us-east-1", t13, "GET", "https://examplebucket.s3.amazonaws.com/test.txt", {}, expires=86400))

# Random-ish key with characters that need encoding, a session token and a body
tok = Credentials("AKIAEXAMPLE2", "secret/with+chars=", "session-token-123")
t26 = datetime.datetime(2026, 10, 4, 13, 5, 9)
body = b"hello world"
import hashlib
h = hashlib.sha256(body).hexdigest()
print("s3-put-token", sign(S3SigV4Auth, tok, "s3", "eu-west-1", t26, "PUT", "http://127.0.0.1:9100/my-bucket/dir/a%20b%2Bc%C3%A9.txt?partNumber=3&uploadId=abc%2Fdef", {"x-amz-content-sha256": h, "Content-Type": "text/plain", "x-amz-meta-owner": "ada"}, body))
print("s3-presign-token", sign(S3SigV4QueryAuth, tok, "s3", "eu-west-1", t26, "PUT", "http://127.0.0.1:9100/my-bucket/dir/a%20b.txt", {}, expires=600))
