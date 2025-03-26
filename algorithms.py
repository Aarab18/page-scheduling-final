def fifo(reference_string, frame_size):
    frames = []
    page_faults = 0
    for page in reference_string:
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
            page_faults += 1
    return page_faults

def lru(reference_string, frame_size):
    frames = []
    page_faults = 0
    for page in reference_string:
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
            page_faults += 1
        else:
            frames.remove(page)
            frames.append(page)
    return page_faults

def optimal(reference_string, frame_size):
    frames = []
    page_faults = 0
    for i, page in enumerate(reference_string):
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
            else:
                future = reference_string[i+1:]
                replace = max(frames, key=lambda x: future.index(x) if x in future else float('inf'))
                frames[frames.index(replace)] = page
            page_faults += 1
    return page_faults

def second_chance(reference_string, frame_size):
    frames = []
    ref_bits = []
    pointer = 0
    page_faults = 0
    for page in reference_string:
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
                ref_bits.append(1)
            else:
                while ref_bits[pointer]:
                    ref_bits[pointer] = 0
                    pointer = (pointer + 1) % frame_size
                frames[pointer] = page
                ref_bits[pointer] = 1
                pointer = (pointer + 1) % frame_size
            page_faults += 1
        else:
            ref_bits[frames.index(page)] = 1
    return page_faults

def clock(reference_string, frame_size):
    frames = [None] * frame_size
    ref_bits = [0] * frame_size
    pointer = 0
    page_faults = 0
    for page in reference_string:
        if page not in frames:
            while ref_bits[pointer]:
                ref_bits[pointer] = 0
                pointer = (pointer + 1) % frame_size
            frames[pointer] = page
            ref_bits[pointer] = 1
            pointer = (pointer + 1) % frame_size
            page_faults += 1
        else:
            ref_bits[frames.index(page)] = 1
    return page_faults

if __name__ == "__main__":
    ref_string = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    frame_size = 3
    print(f"FIFO: {fifo(ref_string, frame_size)}")
    print(f"LRU: {lru(ref_string, frame_size)}")
    print(f"Optimal: {optimal(ref_string, frame_size)}")
    print(f"Second Chance: {second_chance(ref_string, frame_size)}")
    print(f"Clock: {clock(ref_string, frame_size)}")