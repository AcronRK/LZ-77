import os
import huffman

dictionary = []


def compress(text, output_file):
    index = 0
    cnt = 0
    while index < len(text):
        length = 0
        windowlen = -1
        count = -1
        notFound = 1
        cnt += 1
        for i in range(index, len(text)):
            count = text.rfind(text[index:index + length + 1], 0, index)
            if count >= 0:
                length += 1
                windowlen = count
                notFound = 0

        if notFound:
            dictionary.append([0, 0, text[index]])
            index += 1
        else:
            if index + length < len(text):
                dictionary.append([index - windowlen, length, text[index + length]])
                index += length + 1
            else:
                dictionary.append([index - windowlen, length - 1, text[index + length - 1]])
                break

    # Create Dictionary
    f2 = open(output_file, "w")
    for d in dictionary:
        f2.write(str(d) + "\n")
    f2.close()
    # return the number of tuples
    return cnt


def decompress(text, decompressedFile):
    # Decompression Part
    newText = ""
    for i in range(0, len(dictionary)):
        if dictionary[i][0] == 0 and dictionary[i][1] == 0:
            newText = newText + dictionary[i][2]
        else:
            index = dictionary[i][0]
            length = dictionary[i][1]
            newText = newText + newText[len(newText) - index: len(newText) - index + length] + dictionary[i][2]
    f3 = open(decompressedFile, "w")
    f3.write(newText)

    # check if decompressed text is same to the input
    if text == newText:
        print("Decompression made successfully")
    else:
        print("Decompression error: Decompressed text is not equal to the input file")
    dictionary.clear()
    f3.close()


# create a file containing the reverse input of the original file and returns name/path of the file
def reverseFile(text):
    str = ""
    for i in text:
        str = i + str
    path = "reversed_input.txt"
    f1 = open(path, "w")
    f1.write(str)
    f1.close()
    return path


def compressionRatio(inputFile, compressedFile):
    # multiplying by 8 converts the size into bits
    inputSize = os.stat(inputFile).st_size
    dictSize = os.stat(compressedFile).st_size
    return (dictSize / inputSize) * 100


# open the input file
f = open("input.txt", "r")
# save the input in text
text = f.read()
f.close()
# compress returns the number of tuples created from the algo (input, output file)
tuples = compress(text, "dictionaryText.txt")
# decompress gets as input the text and the destination file for decompression
decompress(text, "output.txt")
print("Number of tuples created by the compression: " + str(tuples))
# calculating compression ratio, gets the size of both files
compressRatio = compressionRatio("input.txt", "dictionaryText.txt")
print("Compressed by: " + str(compressRatio) + " %")

# doing the same thing for the reversed file
print("Reverse input")
# func creates the file and returns its path
reversed_path = reverseFile(text)
# open the file and read its content
reverse_file = open(reversed_path, "r")
reversed_text = reverse_file.read()
# create dictionary and calculate number of tuples
reversed_tuples = compress(reversed_text, "reversedDictionary.txt")
print("Number of tuples in reversed file is: " + str(reversed_tuples))
# decompress the dictionary file and save it to another destination
decompress(reversed_text, "reversedDecompress.txt")
# calculate compression ratio
reverseCompressRatio = compressionRatio(reversed_path, "reversedDictionary.txt")
print("Reverse file compressed by: " + str(reverseCompressRatio) + "%")

# comparing to huffman encoding
# calculating the number of bits for lz77
lz77_bits = tuples * 3 * 8
# calculating the number of bits in huffman encoding
huffman_bits = huffman.calculateBits(text)
print("Number of bits from LZ77 algortihm:" + str(lz77_bits))
print("Number of bits from huffman: " + str(huffman_bits))
