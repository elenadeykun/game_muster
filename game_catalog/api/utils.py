def split(array, part_length):
    return [array[i:i + part_length] for i in range(0, len(array), part_length)]

