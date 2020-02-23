from constituents.msci import MSCI

if __name__ == "__main__":
    indices = open("config.txt").readlines()
    print(MSCI(indices))