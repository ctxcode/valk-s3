
# Documentation

Namespaces: [main](#main)

---

# main

## Aliases for 'main'

```js
// The SHA-256 of an empty body, as lowercase hex.
+ value EMPTY_SHA256 ("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
// The payload hash of a request whose body is not signed.
+ value UNSIGNED_PAYLOAD ("UNSIGNED-PAYLOAD")
```

### EMPTY_SHA256

The SHA-256 of an empty body, as lowercase hex.

### UNSIGNED_PAYLOAD

The payload hash of a request whose body is not signed.

## Errors for 'main'

```js
// Thrown by every operation of this package.
+ error Error (not_found, access_denied, response, connection, timeout, io, invalid, protocol) payload { message: String, s3_code: String (""), status: u16 (0), request_id: String ("") }
```

### Error

Thrown by every operation of this package.

- `not_found`: the bucket or the object does not exist (`NoSuchKey`, `NoSuchBucket`, or a
  404 answer without a body).
- `access_denied`: the credentials are wrong, or not allowed to do this (403).
- `response`: the server answered with any other error; `s3_code` says which.
- `connection`: the server could not be reached, or the connection broke.
- `timeout`: the server did not answer in time.
- `io`: reading the local file or stream, or writing the output, failed.
- `invalid`: an argument or the settings cannot be used, such as an empty bucket name.
- `protocol`: the server sent an answer this package cannot read.

`s3_code` holds the error code the server sent, such as `NoSuchKey` or `SlowDown`, `status`
the HTTP status, and `request_id` the id the server gave the request, for its logs.

## Functions for 'main'

```js
// Returns the time as `x-amz-date` writes it: `20130524T000000Z`.
+ fn amz_date(unix_seconds: uint) String
// Returns the query parameters encoded and sorted as a signature expects; also a valid query string to send.
+ fn canonical_query(query: Map[String]) String
// Returns the SHA-256 of `data` as lowercase hex, the form a payload hash takes in a signature.
+ fn sha256_hex(data: local &[u8]) String
// Returns `text` percent-encoded the way AWS signatures expect: everything but `A-Z a-z 0-9 - . _ ~` becomes `%XX`, and `/` too unless `keep_slash` is set, as for an object key in a path.
+ fn uri_encode(text: String, keep_slash: bool (false)) String
```

### amz_date

Returns the time as `x-amz-date` writes it: `20130524T000000Z`.

### canonical_query

Returns the query parameters encoded and sorted as a signature expects; also a valid query
string to send.

### sha256_hex

Returns the SHA-256 of `data` as lowercase hex, the form a payload hash takes in a signature.

### uri_encode

Returns `text` percent-encoded the way AWS signatures expect: everything but `A-Z a-z 0-9
- . _ ~` becomes `%XX`, and `/` too unless `keep_slash` is set, as for an object key in a path.

## Classes for 'main'

```js
// A connection to an S3-compatible service.
+ class Client {
    ~ config: Config

    // Returns whether the bucket exists and the credentials may use it.
    + fn bucket_exists(bucket: String) bool !Error
    // Returns this same client: it is a handle to connections, which cannot be copied. Lets `defer client.close()` and coroutines capture it.
    + fn clone() Client
    // Closes the connections kept open; the client stays usable.
    + fn close() void
    // Copies an object inside the service, without downloading it, and returns the ETag of the copy. Objects up to 5 GiB can be copied this way.
    + fn copy_object(from_bucket: String, from_key: String, bucket: String, key: String, options: ?PutOptions (null)) String !Error
    // Creates a bucket. In AWS regions other than `us-east-1` it is created in the client's region. Throws `response` with `s3_code` `BucketAlreadyOwnedByYou` or `BucketAlreadyExists` when the name is taken.
    + fn create_bucket(bucket: String) void !Error
    // Deletes a bucket, which must be empty.
    + fn delete_bucket(bucket: String) void !Error
    // Deletes the object `key`. Deleting a key that does not exist is not an error.
    + fn delete_object(bucket: String, key: String) void !Error
    // Deletes many objects, up to 1000 per request, and returns the keys that could not be deleted. Keys that do not exist count as deleted.
    + fn delete_objects(bucket: String, keys: Array[String]) Array[DeleteFailure] !Error
    // Downloads the object `key` into the file at `path`, and returns what is known about the object.
    + fn get_file(bucket: String, key: String, path: String, options: ?GetOptions (null)) ObjectInfo !Error
    // Returns the content of the object `key`.
    + fn get_object(bucket: String, key: String, options: ?GetOptions (null)) String !Error
    // Writes the content of the object `key` to `out` as it arrives, and returns what is known about the object.
    + fn get_object_into(bucket: String, key: String, out: Writer, options: ?GetOptions (null)) ObjectInfo !Error
    // Returns what is known about the object `key` without downloading it; throws `not_found` when there is no such object.
    + fn head_object(bucket: String, key: String) ObjectInfo !Error
    // Returns every key under `prefix`, reading page after page. With a `delimiter`, keys below it are grouped into `prefixes` instead.
    + fn list_all(bucket: String, prefix: String (""), delimiter: String ("")) ListPage !Error
    // Returns the names of the buckets the credentials own.
    + fn list_buckets() Array[String] !Error
    // Returns one page of the keys in `bucket`, at most 1000 (ListObjectsV2).
    + fn list_objects(bucket: String, options: ?ListOptions (null)) ListPage !Error
    // Returns a client for `config`. Throws `invalid` when the endpoint is not an `http` or `https` URL.
    + static fn new(config: Config) Client !Error
    // Returns whether the object `key` exists.
    + fn object_exists(bucket: String, key: String) bool !Error
    // Returns an iterator over the objects under `prefix`, which reads the next page when it needs it.
    + fn objects(bucket: String, prefix: String ("")) ObjectIterator
    // Returns a URL that downloads the object `key` without credentials until it expires, at most 7 days (604800 seconds) from now.
    + fn presign_get(bucket: String, key: String, expires_seconds: uint (3600)) String
    // Returns a URL that uploads the object `key` with a `PUT` request without credentials until it expires, at most 7 days (604800 seconds) from now.
    + fn presign_put(bucket: String, key: String, expires_seconds: uint (3600)) String
    // Uploads the file at `path` as the object `key` and returns its ETag.
    + fn put_file(bucket: String, key: String, path: String, options: ?PutOptions (null)) String !Error
    // Stores `data` as the object `key` and returns its ETag.
    + fn put_object(bucket: String, key: String, data: String, options: ?PutOptions (null)) String !Error
    // Uploads everything `reader` gives as the object `key` and returns its ETag.
    + fn put_stream(bucket: String, key: String, reader: Reader, options: ?PutOptions (null)) String !Error
}
```

### Client

A connection to an S3-compatible service.

Requests to the same host share kept-alive connections. A `Client` belongs to the thread
that made it; the coroutines of that thread can use it at the same time.

```valk
let client = s3.Client.new(s3.Config.from_env()) ! panic(E.message)
client.put_object("my-bucket", "hello.txt", "Hello world") ! panic(E.message)
let text = client.get_object("my-bucket", "hello.txt") ! panic(E.message)
```

#### bucket_exists

Returns whether the bucket exists and the credentials may use it.

#### clone

Returns this same client: it is a handle to connections, which cannot be copied. Lets
`defer client.close()` and coroutines capture it.

#### close

Closes the connections kept open; the client stays usable.

#### copy_object

Copies an object inside the service, without downloading it, and returns the ETag of the
copy. Objects up to 5 GiB can be copied this way.

The copy keeps the content type and metadata of the source, unless `options` is given:
then the copy gets those of `options` instead.

#### create_bucket

Creates a bucket. In AWS regions other than `us-east-1` it is created in the client's
region. Throws `response` with `s3_code` `BucketAlreadyOwnedByYou` or
`BucketAlreadyExists` when the name is taken.

#### delete_bucket

Deletes a bucket, which must be empty.

#### delete_object

Deletes the object `key`. Deleting a key that does not exist is not an error.

#### delete_objects

Deletes many objects, up to 1000 per request, and returns the keys that could not be
deleted. Keys that do not exist count as deleted.

#### get_file

Downloads the object `key` into the file at `path`, and returns what is known about the
object.

The file is created or replaced, and removed again when the download fails.

#### get_object

Returns the content of the object `key`.

`options` can ask for a byte range. The whole object is held in memory; use
`get_object_into` or `get_file` for large ones.

#### get_object_into

Writes the content of the object `key` to `out` as it arrives, and returns what is known
about the object.

When the request fails nothing is written to `out`; when the connection breaks halfway,
part of the object may have been.

#### head_object

Returns what is known about the object `key` without downloading it; throws `not_found`
when there is no such object.

#### list_all

Returns every key under `prefix`, reading page after page. With a `delimiter`, keys
below it are grouped into `prefixes` instead.

Holds all keys in memory; `objects` walks a large bucket one page at a time.

#### list_buckets

Returns the names of the buckets the credentials own.

#### list_objects

Returns one page of the keys in `bucket`, at most 1000 (ListObjectsV2).

```valk
let options = s3.ListOptions { prefix: "photos/" }
while true {
    let page = client.list_objects("my-bucket", options) ! panic(E.message)
    each page.objects as obj : println(obj.key + " " + obj.size)
    if !page.truncated : break
    options.continuation_token = page.next_token
}
```

#### new

Returns a client for `config`. Throws `invalid` when the endpoint is not an `http` or
`https` URL.

#### object_exists

Returns whether the object `key` exists.

#### objects

Returns an iterator over the objects under `prefix`, which reads the next page when it
needs it.

```valk
let iter = client.objects("my-bucket", "logs/")
while true {
    let obj = iter.next() ! panic(E.message)
    if !isset(obj) : break
    println(obj.key)
}
```

#### presign_get

Returns a URL that downloads the object `key` without credentials until it expires, at
most 7 days (604800 seconds) from now.

#### presign_put

Returns a URL that uploads the object `key` with a `PUT` request without credentials
until it expires, at most 7 days (604800 seconds) from now.

Only the host is signed, so the uploader chooses the content type and other headers.

#### put_file

Uploads the file at `path` as the object `key` and returns its ETag.

The content type comes from the file extension unless `options` sets one. A file larger
than `Config.multipart_threshold` goes up in parts, read one part at a time.

#### put_object

Stores `data` as the object `key` and returns its ETag.

Data larger than `Config.multipart_threshold` goes up in parts.

```valk
client.put_object("my-bucket", "notes/today.txt", "Hello", s3.PutOptions { content_type: "text/plain" }) ! panic(E.message)
```

#### put_stream

Uploads everything `reader` gives as the object `key` and returns its ETag.

The size need not be known: up to `Config.multipart_threshold` bytes are read first, and
a longer stream goes up in parts, so memory holds a few parts at a time.

```js
// The settings of a `Client`.
+ class Config {
    // The access key id; empty sends requests unsigned.
    + access_key: String
    // A PEM file with the certificate authority to check the server against, for a self-signed certificate.
    + ca_file: ?String
    // The URL of the service, such as `https://nyc3.digitaloceanspaces.com`. Empty uses AWS: `https://s3.<region>.amazonaws.com`.
    + endpoint: String
    // Uploads larger than this go in parts (multipart upload), at most 5 GiB.
    + multipart_threshold: uint
    // The size of each part of a multipart upload, at least 5 MiB. An upload has at most 10000 parts: `put_object` and `put_file` use larger parts when they need to, and `put_stream` stops at 10000 parts, about 78 GiB with the default.
    + part_size: uint
    // Puts the bucket in the path (`endpoint/bucket/key`) instead of in the host name (`bucket.endpoint/key`). MinIO and most self-hosted services need it.
    + path_style: bool
    // The region the requests are signed for. Services without regions, like MinIO, accept `us-east-1`; Backblaze B2 wants its own, such as `us-west-004`, and R2 wants `auto`.
    + region: String
    // How often a request is tried again when the connection fails or the server answers 500 or 503 (`SlowDown`), with a pause that doubles from 100 ms.
    + retries: uint
    // The secret access key.
    + secret_key: String
    // The token of temporary credentials, such as those of an AWS role.
    + session_token: String
    // Whether the body of an upload is part of the signature. Off sends `UNSIGNED-PAYLOAD`, which saves hashing the body; only do that over HTTPS.
    + sign_payload: bool
    // How long connecting, and each read and write on the connection, may take, in milliseconds.
    + timeout_ms: uint
    // How many parts of one multipart upload are sent at the same time.
    + upload_concurrency: uint
    // Whether the TLS certificate of the server is checked.
    + verify_tls: bool

    // Returns the settings from the standard AWS environment variables.
    + static fn from_env() Config
}
```

### Config

The settings of a `Client`.

For AWS, `region` and the keys are enough. Other S3-compatible services need their
`endpoint`, and most of them `path_style`:

```valk
// MinIO
let config = s3.Config { endpoint: "http://127.0.0.1:9000", path_style: true, access_key: "minioadmin", secret_key: "minioadmin" }
// Cloudflare R2
let config = s3.Config { endpoint: "https://<account-id>.r2.cloudflarestorage.com", region: "auto", access_key: key, secret_key: secret }
```

It holds the secret key, so keep it out of logs.

#### access_key

The access key id; empty sends requests unsigned.

#### ca_file

A PEM file with the certificate authority to check the server against, for a
self-signed certificate.

#### endpoint

The URL of the service, such as `https://nyc3.digitaloceanspaces.com`. Empty uses AWS:
`https://s3.<region>.amazonaws.com`.

#### multipart_threshold

Uploads larger than this go in parts (multipart upload), at most 5 GiB.

#### part_size

The size of each part of a multipart upload, at least 5 MiB. An upload has at most
10000 parts: `put_object` and `put_file` use larger parts when they need to, and
`put_stream` stops at 10000 parts, about 78 GiB with the default.

#### path_style

Puts the bucket in the path (`endpoint/bucket/key`) instead of in the host name
(`bucket.endpoint/key`). MinIO and most self-hosted services need it.

#### region

The region the requests are signed for. Services without regions, like MinIO, accept
`us-east-1`; Backblaze B2 wants its own, such as `us-west-004`, and R2 wants `auto`.

#### retries

How often a request is tried again when the connection fails or the server answers
500 or 503 (`SlowDown`), with a pause that doubles from 100 ms.

#### secret_key

The secret access key.

#### session_token

The token of temporary credentials, such as those of an AWS role.

#### sign_payload

Whether the body of an upload is part of the signature. Off sends `UNSIGNED-PAYLOAD`,
which saves hashing the body; only do that over HTTPS.

#### timeout_ms

How long connecting, and each read and write on the connection, may take, in
milliseconds.

#### upload_concurrency

How many parts of one multipart upload are sent at the same time.

#### verify_tls

Whether the TLS certificate of the server is checked.

#### from_env

Returns the settings from the standard AWS environment variables.

Reads `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_REGION`
(or `AWS_DEFAULT_REGION`) and `AWS_ENDPOINT_URL_S3` (or `AWS_ENDPOINT_URL`). Variables
that are not set keep the defaults; without keys, requests go out unsigned, which
public buckets accept.

```js
// A key that `delete_objects` could not delete, with the server's error code and message.
+ class DeleteFailure {
    + code: String
    + key: String
    + message: String
}
```

### DeleteFailure

A key that `delete_objects` could not delete, with the server's error code and message.

```js
// Settings for a download.
+ class GetOptions {
    // The number of bytes to download from `offset` on; 0 downloads up to the end.
    + length: uint
    // The first byte to download.
    + offset: uint
}
```

### GetOptions

Settings for a download.

#### length

The number of bytes to download from `offset` on; 0 downloads up to the end.

#### offset

The first byte to download.

```js
// Settings for one page of `list_objects`.
+ class ListOptions {
    // The `next_token` of the previous page, to read the page after it.
    + continuation_token: String
    // Groups keys that contain this after the prefix into `ListPage.prefixes`, like directories, usually `/`. Empty lists every key.
    + delimiter: String
    // The most keys in one page; the server sends at most 1000.
    + max_keys: uint
    // Only keys that start with this.
    + prefix: String
    // Only keys that sort after this one.
    + start_after: String
}
```

### ListOptions

Settings for one page of `list_objects`.

#### continuation_token

The `next_token` of the previous page, to read the page after it.

#### delimiter

Groups keys that contain this after the prefix into `ListPage.prefixes`, like
directories, usually `/`. Empty lists every key.

#### max_keys

The most keys in one page; the server sends at most 1000.

#### prefix

Only keys that start with this.

#### start_after

Only keys that sort after this one.

```js
// One page of keys from `list_objects`, or all of them from `list_all`.
+ class ListPage {
    + next_token: String
    + objects: Array[ObjectInfo]
    // The groups of keys `delimiter` made, each ending in the delimiter, like `photos/`.
    + prefixes: Array[String]
    // Whether more pages follow; pass `next_token` as `continuation_token` to read the next one.
    + truncated: bool
}
```

### ListPage

One page of keys from `list_objects`, or all of them from `list_all`.

#### prefixes

The groups of keys `delimiter` made, each ending in the delimiter, like `photos/`.

#### truncated

Whether more pages follow; pass `next_token` as `continuation_token` to read the next one.

```js
// What is known about a stored object.
+ class ObjectInfo {
    + content_type: String
    // The entity tag, without quotes. For a single upload the hex MD5 of the content; for a multipart upload it ends in `-` and the number of parts.
    + etag: String
    + key: String
    // As the server wrote it: an HTTP date for `head_object`, ISO 8601 in a listing.
    + last_modified: String
    // The user metadata (`x-amz-meta-*` headers), by lowercase name without the prefix.
    + metadata: Map[String]
    // The size in bytes; for a ranged download, the size of the part that was sent.
    + size: uint
    + storage_class: String
}
```

### ObjectInfo

What is known about a stored object.

`head_object` and the downloads fill in everything but `storage_class`; a listing fills in
`key`, `size`, `etag`, `last_modified` and `storage_class`.

#### etag

The entity tag, without quotes. For a single upload the hex MD5 of the content; for a
multipart upload it ends in `-` and the number of parts.

#### last_modified

As the server wrote it: an HTTP date for `head_object`, ISO 8601 in a listing.

#### metadata

The user metadata (`x-amz-meta-*` headers), by lowercase name without the prefix.

#### size

The size in bytes; for a ranged download, the size of the part that was sent.

```js
// Walks the objects of a bucket page by page; made by `Client.objects`.
+ class ObjectIterator {
    // Returns the next object in key order, or `null` after the last one.
    + fn next() ?ObjectInfo !Error
}
```

### ObjectIterator

Walks the objects of a bucket page by page; made by `Client.objects`.

#### next

Returns the next object in key order, or `null` after the last one.

```js
// Settings for an upload or a copy.
+ class PutOptions {
    // The `Content-Type` stored with the object. Empty lets `put_file` guess it from the file extension; the server stores `binary/octet-stream` or similar for the others.
    + content_type: String
    // Other headers to send, such as `Cache-Control`, `Content-Disposition`, `x-amz-acl` or `x-amz-storage-class`.
    + headers: Map[String]
    // User metadata, sent as `x-amz-meta-<name>` headers. Names are stored in lowercase.
    + metadata: Map[String]
}
```

### PutOptions

Settings for an upload or a copy.

#### content_type

The `Content-Type` stored with the object. Empty lets `put_file` guess it from the file
extension; the server stores `binary/octet-stream` or similar for the others.

#### headers

Other headers to send, such as `Cache-Control`, `Content-Disposition`, `x-amz-acl` or
`x-amz-storage-class`.

#### metadata

User metadata, sent as `x-amz-meta-<name>` headers. Names are stored in lowercase.

```js
// Signs requests with AWS Signature Version 4, in an `Authorization` header or in the query string of a presigned URL.
+ class Signer {
    + access_key: String
    + region: String
    + secret_key: String
    + service: String
    // The token of temporary credentials; sent as `x-amz-security-token` when set.
    + session_token: String

    // Returns the canonical request the signature is computed over; for comparing with what a server reports when it rejects a signature.
    + fn canonical_request(method: String, path: String, query: ?Map[String], headers: Map[String], payload_hash: String) String
    // Returns the query string of a presigned URL, signature included, without the `?`.
    + fn presign(method: String, host: String, path: String, query: ?Map[String], expires_seconds: uint, unix_seconds: uint) String
    // Returns the `Authorization` header value for a request.
    + fn sign(method: String, path: String, query: ?Map[String], headers: Map[String], payload_hash: String, unix_seconds: uint) String
}
```

### Signer

Signs requests with AWS Signature Version 4, in an `Authorization` header or in the query
string of a presigned URL.

`Client` signs its own requests; a `Signer` is for requests sent another way.

```valk
let signer = s3.Signer { access_key: "AKIA...", secret_key: "...", region: "eu-west-1" }
let headers = Map[String]{ "host" => "my-bucket.s3.eu-west-1.amazonaws.com", "x-amz-content-sha256" => s3.EMPTY_SHA256 }
let auth = signer.sign("GET", "/photo.jpg", null, headers, s3.EMPTY_SHA256, time.unix_ms() / 1000)
```

#### session_token

The token of temporary credentials; sent as `x-amz-security-token` when set.

#### canonical_request

Returns the canonical request the signature is computed over; for comparing with what a
server reports when it rejects a signature.

#### presign

Returns the query string of a presigned URL, signature included, without the `?`.

Only `host` is signed, so whoever holds the URL may send any other header with it.
`query` holds parameters of the request itself, such as `response-content-type`.

#### sign

Returns the `Authorization` header value for a request.

`path` is the URI-encoded path as sent (see `uri_encode`), `query` the decoded query
parameters, and `headers` the headers to sign, with at least `host`. `x-amz-date`, and
`x-amz-security-token` when there is a session token, are added to `headers`, so send
all of them. `payload_hash` is the hex SHA-256 of the body (see `sha256_hex`) or
`UNSIGNED_PAYLOAD`.
