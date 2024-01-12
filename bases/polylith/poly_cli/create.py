import typer

app = typer.Typer()


@app.command("base")
def base():
    print("create base")
