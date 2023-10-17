from invoke import Collection, task

from taskgroups import db


@task(aliases=["test"])
def tests(c):
    """Run tests and validations"""
    c.run("./pytest.sh")


namespace = Collection(db, tests)

# @task
# def run(c):
#     """Run the game"""
#     c.run("python -m dungeon.main")
