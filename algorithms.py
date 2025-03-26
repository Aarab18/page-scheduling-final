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
    pass

def second_chance(reference_string, frame_size):
    pass

def clock(reference_string, frame_size):
    pass