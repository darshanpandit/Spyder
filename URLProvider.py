'''
Uses two-queues to maintain BFS strategy.( We need to maintain depth.)
'''
from Queue import Queue

currentQueue= Queue()
nextQueue=Queue()
depth=0


def add_URL(url):
    global nextQueue
    nextQueue.put(url)
    
def time_To_Jump():
    global currentQueue
    if(currentQueue.qsize()==0):
        return True
    else:
        return False

def make_Jump():
    global currentQueue,nextQueue,depth
    currentQueue = nextQueue
    nextQueue = Queue()
    depth+=1
    
def get_URL():
    global currentQueue,depth
    if(time_To_Jump()):
        make_Jump()
    if(currentQueue.qsize()>=1):
        return (currentQueue.get(),depth)
    else:
        return (None, depth)
        
def isIncomplete():
    
    if(currentQueue.qsize()==0 and nextQueue.qsize()==0):
        return False
    else:
        return True
        
    