# Go Snippets

## Check For Known Vulnerabilities

```sh
go run golang.org/x/vuln/cmd/govulncheck@latest ./...
```

## The `internal` directory

The directory name `internal` carries a special meaning and behavior in Go. Any packages which live under this directory can only be imported by code inside the parent of the `internal` directory. This means that any packages under `internal` cannot be imported by code outside of that project.

## `http.FileServer`

-   Sanitizes all request paths by running them through the `path.Clean()` function before searching for a file. This removes any `.` and `..` elements from the URL path, which helps to stop directory traversal attacks.
-   The `Content-Type` is automatically set from the file extension using the `mime.TypeByExtension()` function. You can add your own custom extensions and content types using the `mime.AddExtensionType()` function if necessary.
-   Range requests are fully supported. This is great if your application is serving large files and you want to support resumable downloads. You can see this functionality in action if you use `curl` to request bytes 100-199 of a file.

```sh
$ curl -i -H "Range: bytes=100-199" --output - http://localhost:4000/static/img/logo.png
HTTP/1.1 206 Partial Content
Accept-Ranges: bytes
Content-Length: 100
Content-Range: bytes 100-199/1075
Content-Type: image/png
Last-Modified: Thu, 04 May 2017 13:07:52 GMT
Date: Tue, 05 Sep 2023 08:13:16 GMT
[binary data]
The Last-Modified and If-Modified-Since headers are transparently supported. If a file hasn’t changed since the user last requested it, then http.FileServer will send a 304 Not Modified status code instead of the file itself. This helps reduce latency and processing overhead for both the client and server.
```

## Boolean Flags

For flags defined with `flag.Bool()`, omitting a value when starting the application is the same as writing `-flag=true`. The following two commands are equivalent:

```sh
go run ./example -flag=true
go run ./example -flag
```

You must explicitly use `-flag=false` if you want to set a boolean flag value to `false`.

## Database Query Execution

Go provides three different methods for executing database queries:

-   `DB.Query()` is used for `SELECT` queries which return multiple rows.
-   `DB.QueryRow()` is used for `SELECT` queries which return a single row.
-   `DB.Exec()` is used for statements which don’t return rows (like `INSERT` and `DELETE`).

### Preventing SQL Injection

The `DB.Exec()` method works with placeholder `?` parameters in three steps:

-   It creates a new prepared statement on the database using the provided SQL statement. The database parses and compiles the statement, then stores it ready for execution.
-   In a second separate step, `DB.Exec()` passes the parameter values to the database. The database then executes the prepared statement using these parameters. Because the parameters are transmitted later, after the statement has been compiled, the database treats them as pure data. They can’t change the intent of the statement. So long as the original statement is not derived from untrusted data, injection cannot occur.
-   It then closes (or deallocates) the prepared statement on the database.

## Generate Self-Signed TLS Certificates

```sh
go run /usr/local/Cellar/go/1.21.5/libexec/src/crypto/tls/generate_cert.go --rsa-bits=2048 --host=localhost
```

## Testing

### Running Tests

```sh
# Test a specific package
go test ./cmd

# Run all tests
go test ./...

# Only run specific tests
go test -v -run="^TestRunMe$" ./cmd

# Skip specific tests
go test -v -skip="^TestSkipMe$" ./cmd

# Stops running tests after the first failure
go test -failfast ./cmd
```

#### Cached Tests

```sh
# Ignore the cache and force tests to run
go test -count=1 ./cmd

# Clear cached results for all tests
go clean -testcache
```

#### Test Coverage

```sh
go test -cover ./...

# Output a detailed breakdown of test coverage by method and function
go test -coverprofile=/tmp/profile.out ./...
go tool cover -func=/tmp/profile.out

# Open a browser window containing a navigable and highlighted representation of your code
go test -covermode=atomic -coverprofile=/tmp/profile.out ./...
go tool cover -html=/tmp/profile.out
```

### Parallel Testing

You can indicate that it’s OK for a test to be run concurrently alongside other tests by calling the `t.Parallel()` function at the start of the test.

```go
func TestPing(t *testing.T) {
    t.Parallel()

    ...
}
```

By default, the maximum number of tests that will be run simultaneously is the current value of [`GOMAXPROCS`](https://pkg.go.dev/runtime#pkg-constants).

```sh
go test -parallel=4 ./...
```

### Race Detector

If the code you’re testing leverages concurrency or you’re running tests in parallel, enabling [Go's race detector](https://go.dev/doc/articles/race_detector) can help flag race conditions that exist in your application.

```sh
go test -race ./cmd/
```
