import itertools
import random
import logging
from multiprocessing import Pool, Process, get_start_method, Queue

from .config import CONFIG

# Needs to be global so we can call it from a child process
_global_solver_ref = None

# Magic from https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
def split(a, n):
    k, m = divmod(len(a), n)
    # Listify this so we check the lengths here
    return list(
        list(a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)]) for i in range(n)
    )

# Fake Pool for profiling with py-spy
class FakePool:
    def __init__(self):
        pass

    def map(self, func, args):
        return list(map(func, args))

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        pass


def getPool(cores):
    if cores <= 1:
        return FakePool()
    else:
        return ProcessPool(processes=cores)
    #    return Pool(processes=cores)

global_process_counter = 0


def getGlobalProcessCounter():
    global global_process_counter
    global_process_counter += 1
    return global_process_counter


def doprocess(id, inqueue, outqueue):
    count = 0
    while True:
        # print("! {} Waiting for task".format(id))
        (func, msg) = inqueue.get()
        # print("! {} Got task {}".format(id,count))
        if func is None:
            if msg == "stats":
                outqueue.put()
            # print("! {} exit".format(id))
            break
        outqueue.put(func(msg))
        # print("! {} Done task {}".format(id,count))
        count += 1

class ProcessPool:
    def __init__(self, processes):
        assert processes > 1
        self._processcount = processes

    def map(self, func, args):
        # Make this repeatable, but shuffled differently on each call
        random.Random(getGlobalProcessCounter()).shuffle(args)
        # TODO: This can be unbalanced
        chunks = split(args, self._processcount)
        logging.info("Chunked %s in %s", len(args), [len(c) for c in chunks])
        # print("!A ", chunks)
        # Push all the work
        for i, chunk in enumerate(chunks):
            for c in chunk:
                # print("! Putting task {} for {}".format(i, c))
                self._inqueues[i].put((func, c))

        results = []
        for i, q in enumerate(self._outqueues):
            l = []
            # Get one answer for each thing in the chunk
            for _ in chunks[i]:
                x = q.get()
                # print("!X got ", i, x)
                l.append(x)
            results.append(l)

        # print("!Ax {} {} {} {} {}".format(len(args), sum([len(c) for c in chunks]), sum([len(r) for r in results]), [len(c) for c in chunks], [len(r) for r in results]))
        if len(list(itertools.chain(*results))) != len(args):
            logging.error(
                "Missing answers: {} {} {} {}".format(
                    [len(r) for r in results],
                    [len(c) for c in chunks],
                    sum([len(c) for c in chunks]),
                    len(args),
                )
            )
            assert len(list(itertools.chain(*results))) == len(args)
        # print("!B ", results)
        # print("!C", list(itertools.chain(*results)))
        return list(itertools.chain(*results))

    def __enter__(self):
        assert get_start_method() == "fork"
        ## print("! enter")
        self._inqueues = [Queue() for i in range(self._processcount)]
        self._outqueues = [Queue() for i in range(self._processcount)]
        self._processes = [
            Process(target=doprocess, args=(getGlobalProcessCounter(), self._inqueues[i], self._outqueues[i]))
            for i in range(self._processcount)
        ]
        for p in self._processes:
            p.start()
        return self

    # Clean up
    def __exit__(self, a, b, c):
        ## print("! exit")
        for q in self._inqueues:
            q.put((None, None))
        for p in self._processes:
            p.join()
        return False