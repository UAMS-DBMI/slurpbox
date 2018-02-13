from hashlib import sha1 as SHA1


def sha1sum_from_file(filename):
    sha1 = SHA1()
    with open(filename, "rb") as inf:
        while True:
            buff = inf.read(1024 * 1024)
            if len(buff) == 0:
                break
            sha1.update(buff)

    return sha1.hexdigest()


if __name__ == '__main__':
    s = sha1sum_from_file('Summary.xls')
    print(s)
