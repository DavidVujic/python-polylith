import typer

app = typer.Typer()


@app.command()
def base():
    print("create base")


if __name__ == "__main__":
    app()
