import binascii
import os
import sqlite3


class PicIdxr:
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = sqlite3.connect(db_file)
        self.c = self.db.cursor()
        self.c.execute(PicIdxr.create_statement)
        self.db.commit()
    
    def index_files(self, path):
        for root, _, files in os.walk(path, topdown=False):
            inserts = []
            print("Indexing:", root)
            for name in files:
                fn = os.path.join(root, name)
                sz = os.path.getsize(fn)
                crc = PicIdxr.crc_of_file(fn)
                inserts.append((fn, sz, crc))
            self.c.executemany(PicIdxr.insert_statement, inserts)
            self.db.commit()

    def check_duplicate(self, fn):
        crc = PicIdxr.crc_of_file(fn)
        c = self.db.cursor()
        c.execute(PicIdxr.select_statement, crc)
        res = c.fetchall()
        return res

    @staticmethod
    def crc_of_file(fn):
        b = open(fn, 'rb').read()
        c = binascii.crc32(b) & 0xFFFFFFFF
        return c

    create_statement = '''CREATE TABLE IF NOT EXISTS "pics" (
	"id"	INTEGER NOT NULL UNIQUE,
	"filename"	TEXT NOT NULL,
	"size"	INTEGER NOT NULL,
	"crc32"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
    );'''

    insert_statement = "INSERT INTO pics(filename, size, crc32) VALUES(?,?,?)"

    select_statement = "SELECT fn from pics WHERE crc32=?"

def main():
    if len(sys.argv) > 2:
        db = sys.argv[1]
        pi = PicIdxr(db)
        for p in sys.argv[2:]:
            print ("PATH is ", p)
            pi.index_files(p)
        pi.db.close()


if __name__ == '__main__':
    import sys
    main()
