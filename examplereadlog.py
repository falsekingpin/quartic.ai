import time
def tail(theFile):
    theFile.seek(0,2)   # Go to the end of the file
    while True:
        line = theFile.readline()
        if not line:
            time.sleep(10)    # Sleep briefly for 10sec
            continue
        yield line

if __name__ == '__main__':
    fd = open('/home/user/Personal-Work/log_problem/out.log', 'r+')
    for line in tail(fd):
        print(line)