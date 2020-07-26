from __future__ import print_function
import argparse

def main(): 
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--name', action='store', default='james')
    parser.add_argument('--num', action='store', default=3)

    results = parser.parse_args()
    
    print(results.name)

if __name__ == "__main__":
    main()