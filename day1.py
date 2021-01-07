import glob, subprocess, random, time, threading, hashlib, os
# corpus is the set of files we preseeded with the fuzzer to give it valid inputs 
# these files will be parsed and handled by the fuzzer which will be ultimately mutated and spliced to try to find bugs

def fuzz(thr_id: int, inp: bytearray):
    assert isinstance(thr_id, int)
    assert isinstance(inp, bytearray)
    # write the input to a temporary file 
    tmpfn = f"tmpinput{thr_id}"
    with open(tmpfn, 'wb') as fd:
        fd.write(inp)
        sp = subprocess.Popen(["binutils-2.13.92/binutils/objdump", "-x", tmpfn], 
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
    #sp = subprocess.Popen(["binutils-2.13.92/binutils/objdump", "-d", tmpfn])

    ret = sp.wait()

    #assert that the program ran successfully
    if ret != 0:
        print(f'Exited with {ret}')
        if(ret == -11):
            #SIGSEGV
            dahash = hashlib.sha256(inp).hexdigest()
            open(os.path.join("crashes", f"crash_{dahash:64}"),"wb").write(inp)

# load all file names to corpus
corpus_filename= glob.glob("corpus/*")

corpus = set()
for filename in corpus_filename:
    corpus.add(open(filename, 'rb').read())

#after removing duplicate binaries it converts binaries back to list
corpus = list(corpus)

start = time.time()
cases = 0

def worker(thr_id):
    global start, corpus, cases
    while True:
        inp = bytearray(random.choice(corpus))
        for _ in range(random.randint(1, 8)):
            inp[random.randint(0,len(inp)-1)] = random.randint(0, 255)
        fuzz(thr_id, inp)
        elapsed = time.time() - start
        cases = cases+1
        fcps = float(cases)/elapsed
        print(f"[{elapsed:10.4f}] cases {cases:10} | fcps {fcps:10.4f}")
for thr_id in range(192):
    threading.Thread(target=worker, args=[thr_id]).start()

while threading.active_count() > 1:
    time.sleep(0.1)