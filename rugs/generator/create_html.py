import argparse
from os import listdir
from os.path import isfile, join

def main():
    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--input_models', metavar='path', required=True,
                        help='Path to models directory')
    parser.add_argument('--output_html', metavar='path', required=True,
                        help='Path to the output HTML file')
    args = parser.parse_args()

    onlyfiles = [f for f in listdir(args.input_models) if join(args.input_models, f).endswith('.gltf')]
    print(onlyfiles)



if __name__ == "__main__":
    main()
