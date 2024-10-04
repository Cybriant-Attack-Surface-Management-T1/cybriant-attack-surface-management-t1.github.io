
""" Imports """
import subprocess  # base
import queue  # base
import threading  # base
import time  # base
import sys  # base

def enqueue_output(out, queue):
    for line in iter(out.readline, ''):
        # print(f'Enqueuing line: {line.strip()}')
        queue.put(line)
    out.close()

def run_amass(flags: [str], timeout: int) -> [str]:
    results = []
    print(f'Running amass against the target with timeout set to {timeout}...')

    result = subprocess.Popen(flags, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True)

    # Creating a queue / thread combo for non-blocking I/O
    q = queue.Queue()
    t = threading.Thread(target=enqueue_output, args=(result.stdout, q))
    t.daemon = True  # Thread ends when subprocess ends
    t.start()

    # Caching start time
    start_time = time.time()

    while True:
        try:
            # print(f'Elapsed time: {time.time() - start_time:.2f}')
            line = q.get_nowait()
            print(f'Received line from queue: {line.strip()} at {time.time() - start_time:.2f} seconds')
        except queue.Empty:
            if result.poll() is not None:
                break
        else:
            results.append(line.strip())
        if time.time() - start_time > timeout:
            result.terminate()
            print(f'Timeout occurred after {timeout} seconds.')
            break

    return results

def main(domain: str):
    timeout = 60 * 5
    flags = ['amass', 'enum', '-d', domain]

    amass_results = run_amass(flags, timeout)
    print(f'Results from running amass: {amass_results}')


if __name__ == '__main__':
    domain = sys.argv[1]
    main(domain)
