# valk-s3

An S3 client for [Valk](https://valk-lang.dev): AWS S3 and the S3-compatible services, such as
MinIO, Cloudflare R2, DigitalOcean Spaces and Backblaze B2. Uploads, downloads, listings,
multipart uploads, presigned URLs and buckets, signed with AWS Signature Version 4.

Requires Valk 0.7.8 or newer.

## Install

```
vman install github.com/ctxcode/valk-s3
```

## Example

```rust
use s3

let client = s3.Client.new(s3.Config {
    region: "eu-west-1"
    access_key: "AKIA..."
    secret_key: "..."
}) ! panic(E.message)

client.put_object("my-bucket", "notes/hello.txt", "Hello world", s3.PutOptions {
    content_type: "text/plain"
    metadata: .{ "author" => "ada" }
}) ! panic(E.message)

let text = client.get_object("my-bucket", "notes/hello.txt") ! panic(E.message)

let info = client.head_object("my-bucket", "notes/hello.txt") ! panic(E.message)
println("%{info.size} bytes, %{info.content_type}")

client.delete_object("my-bucket", "notes/hello.txt") ! panic(E.message)
```

## Services

`Config` has the endpoint, region and credentials. Without an `endpoint` it talks to AWS in
`region`. Most other services need `path_style`, which puts the bucket in the path instead of in
the host name:

```rust
// MinIO
s3.Config { endpoint: "http://127.0.0.1:9000", path_style: true, access_key: "minioadmin", secret_key: "minioadmin" }
// Cloudflare R2
s3.Config { endpoint: "https://<account-id>.r2.cloudflarestorage.com", region: "auto", access_key: key, secret_key: secret }
// DigitalOcean Spaces
s3.Config { endpoint: "https://ams3.digitaloceanspaces.com", region: "ams3", access_key: key, secret_key: secret }
// Backblaze B2
s3.Config { endpoint: "https://s3.us-west-004.backblazeb2.com", region: "us-west-004", access_key: key, secret_key: secret }
```

`s3.Config.from_env()` reads `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`,
`AWS_REGION` and `AWS_ENDPOINT_URL`. Without keys, requests go out unsigned, which public
buckets accept. Other settings: `timeout_ms`, `retries` (on a broken connection, 500 and 503),
`verify_tls` and `ca_file`, and the multipart settings below.

## Uploads

```rust
client.put_object(bucket, key, data, options)     // a String
client.put_file(bucket, key, "video.mp4", options) // content type from the extension
client.put_stream(bucket, key, reader, options)    // any io.Reader; the size need not be known
client.copy_object(from_bucket, from_key, bucket, key)
```

Each returns the ETag. `PutOptions` sets the `content_type`, user `metadata` (`x-amz-meta-*`)
and other `headers` such as `Cache-Control` or `x-amz-storage-class`.

Anything larger than `multipart_threshold` (16 MiB) goes up as a multipart upload, in parts of
`part_size` (8 MiB), `upload_concurrency` (4) parts at a time. A file or stream is read one part
at a time, so memory holds a few parts, never the whole upload. A failed multipart upload is
aborted, so no parts are left behind.

## Downloads

```rust
let data = client.get_object(bucket, key)                 // into memory
let info = client.get_file(bucket, key, "out.bin")        // into a file
let info = client.get_object_into(bucket, key, writer)    // to any io.Writer, as it arrives
let part = client.get_object(bucket, key, s3.GetOptions { offset: 100, length: 50 })
```

A failed download writes nothing to the writer, and `get_file` removes the file again.
`head_object` returns the `ObjectInfo` (size, ETag, content type, last modified, metadata)
without the content, and `object_exists` says whether there is one.

## Listing

`list_objects` returns one page of up to 1000 keys, and `next_token` to read the next one:

```rust
let options = s3.ListOptions { prefix: "photos/", delimiter: "/" }
while true {
    let page = client.list_objects("my-bucket", options) ! panic(E.message)
    each page.objects as obj : println(obj.key + " " + obj.size)
    each page.prefixes as dir : println(dir)
    if !page.truncated : break
    options.continuation_token = page.next_token
}
```

`list_all(bucket, prefix, delimiter)` reads every page into one `ListPage`. `objects(bucket,
prefix)` walks a large bucket one page at a time:

```rust
let iter = client.objects("my-bucket", "logs/")
while true {
    let obj = iter.next() ! panic(E.message)
    if !isset(obj) : break
    println(obj.key)
}
```

## Deleting

`delete_object` deletes one key. `delete_objects(bucket, keys)` deletes any number, 1000 per
request, and returns a `DeleteFailure` for each key the server refused.

## Presigned URLs

```rust
let download = client.presign_get("my-bucket", "report.pdf", 3600) // valid for an hour
let upload = client.presign_put("my-bucket", "uploads/photo.jpg")
```

Anyone with the URL can download or upload that one key until it expires (at most 7 days).
`s3.Signer` signs requests that are sent some other way.

## Buckets

`create_bucket`, `delete_bucket`, `bucket_exists` and `list_buckets`.

## Errors

Every method throws `s3.Error`, with `s3_code` (such as `NoSuchKey`), `status`, `request_id` and
a `message`:

| code | when |
| --- | --- |
| `not_found` | the bucket or the object does not exist |
| `access_denied` | the credentials are wrong or not allowed to do this |
| `response` | any other error answer of the server; see `s3_code` |
| `connection` | the server could not be reached, or the connection broke |
| `timeout` | the server did not answer in time |
| `io` | reading the local file or stream, or writing the output, failed |
| `invalid` | an argument or a setting cannot be used |
| `protocol` | the server sent an answer that cannot be read |

## Benchmarks

A 256 MiB object against MinIO in docker on the same machine (12 cores, Linux), median of five
runs, next to boto3 1.43 with its default 10 threads:

| | valk-s3 | boto3 |
| --- | --- | --- |
| upload a file (multipart, 8 MiB parts) | 477 MiB/s | 637 MiB/s |
| upload, `upload_concurrency: 10` | 587 MiB/s | |
| download into a file | 1219 MiB/s | 1310 MiB/s |
| download into memory | 453 MiB/s | 1467 MiB/s |
| 1000 GETs of 1 KiB, one at a time | 0.24 s | 0.91 s |

1000 PUTs of 1 KiB take 14 s with either client; that is MinIO writing each object to disk.
`make bench` runs the valk side; `bench/boto3_bench.py` the boto3 side.

## Development

`make server` starts MinIO in docker on port 9100 (`make server-down` removes it), and
`make test` runs the suite against it. `tests/sigv4_botocore.py` prints the signatures botocore computes for the requests the
signing tests check. `make example` runs the example against the same server, `make lint` checks
the sources and `make docs` regenerates the API documentation. Override the compiler with
`make vc=/path/to/valk test`.

## Not supported

Copying objects larger than 5 GiB (that needs `UploadPartCopy`), parallel ranged downloads,
object versions, ACL and bucket policy calls, server-side encryption headers beyond passing them
in `PutOptions.headers`, and the `aws-chunked` streaming signature. Credentials come from the
config or the environment only, not from `~/.aws` files or instance roles.
