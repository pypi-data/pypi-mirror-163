# Predict the Collision and Save the Earth
## About the Dataset
The official dataset is from NASA's official website https://cneos.jpl.nasa.gov/ca/ . And the modified version of this dataset is available on Kaggle. Link : https://www.kaggle.com/datasets/sameepvani/nasa-nearest-earth-objects 
The dataset consists of 90837 rows and 10 columns.

The models are used in this project,
- Adaboost Classifier
- Logistic Regression
- Multi-Layer Perceptron
- Stochastic Gradient Descent
- XGBoost Classifier
- Linear Perceptron Classifier
- Support Vector Classification
- Gradient Boosting Classifier
- K-Nearest Neighbors
- Random Forest Classifier
## Procedure


- First install the package using pip
```sh
pip install predict-the-collision
```

- import main_fun() from predict_collision

```sh
from predict_collision import main_fun
```
- The first parameter is "Data Path of CSV" and the second parameter is "Input Number of the prediction model"


| Model Name | User input |
| ------ | ------ |
| Adaboost Classifier | 1 |
| Logistic Regression | 2 |
| Multi-Layer Perceptron | 3 |
| Stochastic Gradient Descent | 4 |
| XGBoost Classifier | 5 |
| Linear Perceptron Classifier | 6 |
| Support Vector Classification | 7 |
| Gradient Boosting Classifier | 8 |
| K-Nearest Neighbors | 9 |
| Random Forest Classifier | 10 |

- Such as
```sh
main_fun("csv_path", 1)
```


