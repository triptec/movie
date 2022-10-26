from backend.setup.seed import Seed


# Currently this has concurrency issues if there is more than one worker.
# There's a data race checking if the db is empty, perhaps could be solved
# by preloading or perhaps using db transactions. Best would probably be to
# not run this on application initialization
def setup():
    seed = Seed()
    seed.movies()
