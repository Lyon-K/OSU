from cryptography.hazmat.primitives import hashes
import time
import string
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

first_n = 3 #each hex represents 2^8 so first 3 = first 2^24 bis

def get_randstr(length = 24):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length)).encode('ascii')

def weak_collision(data):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    source = digest.finalize()
    count = 0
    while(True):
        # keep generating hashes until we arrive at h(data) with the same initial bits
        count += 1
        digest = hashes.Hash(hashes.SHA256())
        digest.update(count.to_bytes(4,'big'))
        target = digest.finalize()

        # return count when collision of initial bits are found
        if target[:first_n] == source[:first_n]:
            return count

def strong_collision():
    hashmap = {}
    count = 0
    while(True):
        count += 1
        # generate a hash from random bytes
        digest = hashes.Hash(hashes.SHA256())
        digest.update(random.randbytes(4))
        target = digest.finalize()[:first_n]
        # save new hash in hashmap
        if hashmap.get(target) == None:
            hashmap[target] = count.to_bytes(4,'big')
        else:
            # when matching hash found, return count
            if hashmap.get(target) == count.to_bytes(4,'big'):
                # if we are using the same hashing value generated that is randomly(unlikely), dont count this hash
                # we are attempting to find different values that hashes to the same initial bits
                count -= 1
                continue
            return count

if __name__ == "__main__":
    num_runs = 20
    weak_collision_iterations = []
    strong_collision_iterations = 0
    # # create a thread pool with 4 threads
    with ThreadPoolExecutor(max_workers=4) as executor:
        # run weak_collition()
        future_to_collision = {executor.submit(weak_collision, randstr): randstr for randstr in [get_randstr() for _ in range(num_runs)]}
    for future in as_completed(future_to_collision):
        collision = future_to_collision[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (collision, exc))
        else:
            weak_collision_iterations.append(data)
    print(f"Weak collision: Average iterations for {num_runs} runs: {sum(weak_collision_iterations)/num_runs}")

    # run strong_collision()
    for _ in range(num_runs):
        strong_collision_iterations += strong_collision()
    print(f"Strong collision: Average iterations for {num_runs} runs: {strong_collision_iterations/num_runs}")

    # writes result in a text file
    with open('Q3.3_results.txt','w') as f:
        f.write(f"[{time.asctime()}]\n")
        f.write(f"Weak collision: Average iterations for {num_runs} runs: {sum(weak_collision_iterations)/num_runs}\n")
        f.write(f"Strong collision: Average iterations for {num_runs} runs: {strong_collision_iterations/num_runs}\n")

