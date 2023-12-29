# Go Snippets

## Check For Known Vulnerabilities

```
go run golang.org/x/vuln/cmd/govulncheck@latest ./...
```

## The `internal` directory

The directory name `internal` carries a special meaning and behavior in Go. Any packages which live under this directory can only be imported by code inside the parent of the `internal` directory. This means that any packages under `internal` cannot be imported by code outside of that project.

## `http.FileServer`

- Sanitizes all request paths by running them through the `path.Clean()` function before searching for a file. This removes any . and .. elements from the URL path, which helps to stop directory traversal attacks.
- The `Content-Type` is automatically set from the file extension using the `mime.TypeByExtension()` function. You can add your own custom extensions and content types using the `mime.AddExtensionType()` function if necessary.
- Range requests are fully supported. This is great if your application is serving large files and you want to support resumable downloads. You can see this functionality in action if you use curl to request bytes 100-199 of a file.

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
