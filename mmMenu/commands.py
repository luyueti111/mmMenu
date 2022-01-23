from mmMenu import app, db
import click
import os


@app.cli.command()
def initdb():
    db.drop_all()
    db.create_all()
    allImages = os.listdir(app.config['UPLOAD_PATH'])
    for img in allImages:
        os.remove(os.path.join(app.config['UPLOAD_PATH'], img))
    click.echo('Initialized database')
