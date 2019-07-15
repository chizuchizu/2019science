from preprocessing import Preprocess

if __name__ == "__main__":
    from_dir = input("from_dir :")
    to_dir = input("to_dir: ")

    p = Preprocess(from_dir, to_dir)

    p.main()
    p.save()
    print("All Done")
