import pandas as pd
import sys
import os.path
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt


def assertions(argv):
    assert len(argv) == 3, "format: py Tree.py arg1 arg2"

    assert os.path.isfile(argv[1]) is True, \
           f" {argv[1]} not found"
    assert os.path.isfile(argv[2]) is True, \
           f" {argv[2]} not found"
    print(argv[1])
    assert 'train_knight.csv' in argv[1].lower(), \
           "usage: 1st param path = **/Train_knight.csv"
    assert 'test_knight.csv' in argv[2].lower(), \
           "usage: 2nd param path = **/Test_knight.csv"


def tree_classifier(argv):
    df_train = pd.read_csv(argv[1])
    df_test = pd.read_csv(argv[2])

    train_data = df_train.drop('knight', axis=1)
    result_data = df_train['knight']
    x_train, x_test, y_train, y_test = train_test_split(train_data,
                                                        result_data,
                                                        test_size=0.2,
                                                        random_state=42)

    dt = DecisionTreeClassifier(random_state=42)
    # As seen in split.py, x_train/y_train represent
    # the data fed to the model for training.

    # During the training, the model will try to learn patterns from
    # x (features) to predict y (target).
    dt.fit(x_train, y_train)

    # After the training, we'll test out the model with
    # x_test/y_test.
    training_pred = dt.predict(x_test)

    print('Accuracy Score:', accuracy_score(y_test, training_pred))

    # pos_label = "Which is the positive class?"
    print('F1-Score:', f1_score(y_test, training_pred, pos_label='Jedi'))

    final_prediction = ('\n'.join(dt.predict(df_test)))
    with open('Tree.txt', 'w') as f:
        f.write(final_prediction)
    fig, ax = plt.subplots(figsize=(12, 8))
    plot_tree(dt, filled=True, ax=ax,
              feature_names=df_test.columns,
              class_names=['Jedi', 'Sith'])

    plt.show()


def main():
    try:
        assertions(sys.argv)
        tree_classifier(sys.argv)
    except Exception as e:
        print(f'Error:{e}')


if __name__ == '__main__':
    main()
