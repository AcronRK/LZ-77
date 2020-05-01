import heapq
from collections import defaultdict


def encode(frequency):
    heap = [[weight, [symbol, '']] for symbol, weight in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def calculateBits(text):
    data = text
    frequency = defaultdict(int)
    for symbol in data:
        frequency[symbol] += 1
    dict = {}
    huff = encode(frequency)
    print("\nHuffman Encoding")
    print("Symbol".ljust(10) + "Weight".ljust(10) + "Huffman Code")
    for p in huff:
        print(p[0].ljust(10) + str(frequency[p[0]]).ljust(10) + p[1])
        # create a dictionary of symbol and its frequency
        dict[p[0]] = p[1]
    # calculating total number of bits
    total_bits = 0
    for symbol in text:
        total_bits += len(dict[symbol])
    return total_bits
