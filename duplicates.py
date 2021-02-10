import binascii
import os

def crc_of_file(fn):
    b = open(fn, 'rb').read()
    c = binascii.crc32(b) & 0xFFFFFFFF
    return c


def list_files(path):
    fs = []
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            f = os.path.join(root, name)
            fs.append((f, os.path.getsize(f)))
    return fs

def find_duplicates(path):
    fs = list_files(path)
    sizes = {}
    for f,s in fs:
        if s in sizes:
            sizes[s].append(f)
        else:
            sizes[s] = [f]

    crcs = {}
    for k in sizes.keys():
        if len(sizes[k])  > 1:
            for f in sizes[k]:
                c = crc_of_file(f)
                if c in crcs:
                    crcs[c].append(f)
                else:
                    crcs[c] = [f]

    dups = []
    for c in crcs.keys():
        if len(crcs[c]) > 1:
            dups.append(crcs[c])
    return dups


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        dups = find_duplicates(path)
        f = open('duplicates.txt', 'w')
        for d in dups:
            f.write(' '.join(d) + '\n')
        f.close()
    else:
        print("add a path to search as arg 1.")


if __name__ == '__main__':
    import sys
    main()
