import bitio
import sys
import huffman
import pickle


def read_tree(tree_stream):
    # Reading the description of huffman tree from the input argument
    # of the function and using pickle.load(input) to make the tree
    # object and return it
    tree = pickle.load(tree_stream)
    return tree


def decode_byte(tree, bitreader):
    # While the leaf is not reached when traversing tree,
    # keep going by reading bits left and right, and check
    # if instances match. When they do, return the leaf value
    while True:
        if isinstance(tree, huffman.TreeLeaf):
            return tree.getValue()
        my_bit = bitreader.readbit()
        if my_bit == 0:
            tree = tree.getLeft()
        elif my_bit == 1:
            tree = tree.getRight()


def decompress(compressed, uncompressed):
    # Reading the compressed tree using the read_tree function
    # and using the treet to decode the entire stream, writing
    # all the symbols to the uncompressed stream
    # if theres an end of file, exit
    newTree = read_tree(compressed)
    bitWrite = bitio.BitWriter(uncompressed)
    bitRead = bitio.BitReader(compressed)
    decodeBit = decode_byte(newTree, bitRead)
    try:
        while decodeBit is not None:
            bitWrite.writebits(decodeBit, 8)
            decodeBit = decode_byte(newTree, bitRead)
    except EOFError:
        sys.exit()


def write_tree(tree, tree_stream):
    # Writing the tree to the input argument tree_stream
    pickle.dump(tree, tree_stream)


def compress(tree, uncompressed, compressed):
    # Compressing the file by writing all symbols into corresponding
    # bits and padding.
    # writing the tree using write_tree function
    # to the compressed stream
    write_tree(tree, compressed)
    entable = huffman.make_encoding_table(tree)
    bitWrite = bitio.BitWriter(compressed)
    bitRead = bitio.BitReader(uncompressed)
    noteof = True
    while noteof:
        try:
            encode = entable[bitRead.readbits(8)]
            for i in encode:
                bitWrite.writebit(i)
        except EOFError:
            noteof = False
            encode = entable[None]
            for i in encode:
                bitWrite.writebit(i)
    bitWrite.flush()
