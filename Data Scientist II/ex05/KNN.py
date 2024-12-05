import pandas as pd
import sys
import os.path
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score
import matplotlib.pyplot as plt


def assertions(argv):
    assert len(argv) == 3, "format: py Tree.py arg1 arg2"

    assert os.path.isfile(argv[1]) is True, \
           f" {argv[1]} not found"
    assert os.path.isfile(argv[2]) is True, \
           f" {argv[1]} not found"
    print(argv[1])
    assert 'train_knight.csv' in argv[1].lower(), \
           "usage: 1st param path = **/Train_knight.csv"
    assert 'test_knight.csv' in argv[2].lower(), \
           "usage: 2nd param path = **/Test_knight.csv"


def KNN_classifier(argv):
    df_train = pd.read_csv(argv[1])
    df_test = pd.read_csv(argv[2])

    train_data = df_train.drop('knight', axis=1)
    result_data = df_train['knight']
    x_train, x_test, y_train, y_test = train_test_split(train_data,
                                                        result_data,
                                                        test_size=0.2,
                                                        random_state=42)
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    df_test = scaler.transform(df_test)
    accuracy = []
    fOne_score = []
    precision = []

    for k in range(1, 31):
        neigh = KNeighborsClassifier(n_neighbors=k)
        neigh.fit(x_train, y_train)
        training_pred = neigh.predict(x_test)
        accuracy.append(accuracy_score(y_test, training_pred))
        fOne_score.append(f1_score(y_test, training_pred, pos_label='Jedi'))
        precision.append(precision_score(y_test, training_pred,
                                         pos_label='Jedi'))
        print(f'k{k} ===> Accuracy Score:{accuracy[-1]:.2f} | \
F1-Score:{fOne_score[-1]:.2f} | Precision Score:{precision[-1]:.2f}')

    sum_score = [accuracy[i] + precision[i] + fOne_score[i]
                 for i in range(len(accuracy))]
    best_k = sum_score.index(max(sum_score))
    neigh = KNeighborsClassifier(n_neighbors=best_k + 1)
    neigh.fit(x_train, y_train)
    with open("KNN.txt", 'w') as f:
        for pred in neigh.predict(df_test):
            f.write(pred + '\n')
    plt.plot(accuracy)
    plt.ylabel('accuracy')
    plt.xlabel('k values')
    plt.show()


def main():
    try:
        assertions(sys.argv)
        KNN_classifier(sys.argv)
    except Exception as e:
        print(f'Error:{e}')


if __name__ == '__main__':
    main()
