import warnings # чтобы варнинги не мешали
warnings.filterwarnings("ignore")

from sklearn import tree # Само дерево решений
from sklearn.model_selection import train_test_split # функция разделяет выборку на обучающую и тестовую
import pandas as pd # для загрузки датасета

from graphviz import Source # для визуализации
from IPython.display import SVG, display, HTML # для красивого отображения в jupyter
style = "<style>svg{width: 50% !important; height: 50% !important;} </style>"
HTML(style)

df2 = pd.read_csv('train2.csv', index_col='idx')
X = df2[['Pclass', 'Age', 'Sex']] # признаки
y = df2['Survived'] # классы

# создаем и обучаем модель
clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=8)
clf.fit(X, y)

# делаем картинку (можно сохранить в файл и потом посмотреть)
graph = Source(tree.export_graphviz(clf, out_file=None, feature_names=list(X),
                                    class_names=['Died', 'Survived'], filled=True))
display(SVG(graph.pipe(format='svg'))) # выводим на экран (работает только в jupyter)


# разделяем выборку на обучающую и тестовую. Можно пропустить
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
clf.fit(X_train, y_train)

# делаем картинку
graph = Source(tree.export_graphviz(clf, out_file=None, feature_names=list(X),
                                    class_names=['Died', 'Survived'], filled=True))
display(SVG(graph.pipe(format='svg'))) # выводим на экран (работает только в jupyter)

# смотрим качество
clf.score(X_test, y_test)
clf.score(X, y)
clf.score(X_train, y_train)