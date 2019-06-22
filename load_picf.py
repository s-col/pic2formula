from argparse import ArgumentParser
import pickle


def main():
    args = get_args()
    with open(args.path, 'rb') as f:
        x_picf, y_picf = pickle.load(f)
    print('x = ' + x_picf.str(showmax=None))
    print()
    print('y = ' + y_picf.str(showmax=None))

def get_args():
    parser = ArgumentParser()
    parser.add_argument('path', type=str)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
     main()