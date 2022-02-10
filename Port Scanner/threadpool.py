from multiprocessing.pool import ThreadPool
from rich.console import Console
import os

console = Console()
#https://docs.python.org/3/library/multiprocessing.html
def threadpool(function, ports_bulk, bulk_length):
    num_of_threads = 200
    print("recomndate number of threads",os.cpu_count())
    print(f"\n {num_of_threads} Threads are in use.\n")
    tpool = ThreadPool(num_of_threads)
    #print("tpool = ",tpool)
    for loop_index, _ in enumerate(tpool.imap_unordered(function, ports_bulk), 1):
        #print("loop",loop_index)
        animation_bar(loop_index, bulk_length)

#https://www.programcreek.com/python/?CodeExample=print+progress+bar
#Idea from here for the animation bar
def animation_bar(loop_index_iteration, bulk_length):
    bar_width = 50  # chars
    bar_current_width = bar_width * loop_index_iteration // bulk_length
    bar = "█" * bar_current_width + "-" * (bar_width - bar_current_width)
    progress = "%.1f" % (loop_index_iteration / bulk_length * 100)
    console.print(f"|{bar}| {progress} %", end="\r", style="green")
    if loop_index_iteration == bulk_length:
        print()




