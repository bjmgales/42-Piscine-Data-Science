from sklearn.model_selection import train_test_split
import pandas as pd
import sys
import os.path


def main():
    '''Split a file 80%/20% and create two new file with the result.'''
    try:
        assert len(sys.argv) == 2, "format: py split.py arg1"
        assert os.path.isfile(sys.argv[1]) is True, \
            " the file could not be found"
        df = pd.read_csv(sys.argv[1])
        train_knight, test_knight = train_test_split(df, test_size=0.2,
                                                     random_state=42)
        train_knight.to_csv('./Training_knight.csv',
                            index=False)
        test_knight.to_csv('./Testing_knight.csv',
                           index=False)
    except Exception as e:
        print(f'Error:{e}')
        return


if __name__ == '__main__':
    main()
