import os
import sys

sys.path.append(os.pardir)

if __name__ == "__main__":
    from preprocessing import Preprocess
    from_dir = input("from_dir :")
    to_dir = input("to_dir: ")

    p = Preprocess(from_dir, to_dir)

    p.main()
    p.save()
    print("All Done")
