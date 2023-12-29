# Go Snippets

## Check For Known Vulnerabilities

```
go run golang.org/x/vuln/cmd/govulncheck@latest ./...
```

## The `internal` directory

The directory name `internal` carries a special meaning and behavior in Go. Any packages which live under this directory can only be imported by code inside the parent of the `internal` directory.
