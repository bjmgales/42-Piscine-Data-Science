import pandas as pd
import sys
import os.path
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline


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


def voting_classifier(argv):
    df_train = pd.read_csv(argv[1])
    df_test = pd.read_csv(argv[2])
    train_data = df_train.drop('knight', axis=1)
    result_data = df_train['knight']

    x_train, x_test, y_train, y_test = train_test_split(train_data,
                                                        result_data,
                                                        test_size=0.2,
                                                        random_state=42)

    tree = DecisionTreeClassifier(random_state=42)
    KNN = Pipeline([
            ('scaler', StandardScaler()),
            ('model', KNeighborsClassifier(n_neighbors=4))
        ]
    )
    log_regr = Pipeline([
            ('scaler', StandardScaler()),
            ('model', LogisticRegression(random_state=42))
        ]
    )

    voting_clf = VotingClassifier(estimators=[
        ('log_regr', log_regr),
        ('KNN', KNN),
        ('tree', tree)],
        voting='hard'
    )

    voting_clf.fit(x_train, y_train)
    training_pred = voting_clf.predict(x_test)
    print(f'Voting Classifier => F1-Score: {f1_score(y_test, training_pred,
                                            pos_label='Jedi'):.2f}')

    with open('Voting.txt', 'w') as f:
        f.write('\n'.join(voting_clf.predict(df_test)))


def main():
    try:
        assertions(sys.argv)
        voting_classifier(sys.argv)
    except Exception as e:
        print(f'Error:{e}')


if __name__ == '__main__':
    main()
