# Phoenix Notes

## Creating an App
```bash
mix phx.new app_name
```

## Creating a Phoenix App
Start by installing Hex (Elixir's package manager) locally.  If you already have a version of Hex installed, you'll be asked whether you want to upgrade Hex to the latest version.
```bash
mix local.hex
```
Next, install the Phoenix archive.
```bash
mix archive.install hex phx_new
```
With Phoenix successfully installed, you can now create a Phoenix project (called `refuge` here).
```bash
mix phx.new project_name
```
Generate the scaffold HTML app using the `phx.gen.html` generator:
```bash
mix phx.gen.html Wildthings Bear bears name:string type:string hibernating:boolean
```
