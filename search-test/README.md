# search-test

This directory holds a self-contained Go application which can be used to run
randomized queries (to break the cache) against an ONI website, verifying that
the site is not only up and running, but properly responding to searches, as
those tend to invoke the most complex pieces of the ONI stack.

Go must be installed to build this, but the binary can be copied just about
anywhere post-build, or can be run against a remote URL directly, so there is
no need to have the Go toolchain in production.  Process:

```bash
cd search-test   # if you're not already here
make                    # or just run "go build" - I'm just really lazy
./search-test
```

You can configure the URL for the search request, enable printing out the
search results HTML locally, and maybe some other stuff We'll eventually add.
Just run `./search-test -h` for all options.

The exit status will be zero on success (defined below) and non-zero otherwise.
For a simple "it works" test, that's all that's needed.

Success is defined as hitting the search URL with random words and getting a
valid response body back which contains the text "\d\d\d+ results" somewhere.
We ensure three digits minimum because with any "or" query against five common
English words, we're guaranteed to have a huge result set.  If it's less than
100, something went horribly wrong.  Chances are if it's less than 10k,
something is wrong, but we don't want the cutoff to be too high.

STDERR gets a bit of useful JSON logging which may be handy for more advanced
monitoring someday, and could be captured to a file in the shorter term.
