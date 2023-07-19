"""
This is a boilerplate pipeline
generated using Kedro 0.18.4
"""

import logging
import runpy
from typing import Any, Dict, Tuple
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, accuracy_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from .preprocessing import Preprocessing
global_preprocessing = runpy._run_module_as_main("employee_attrition.preprocessing")
Preprocessing = global_preprocessing["Preprocessing"]

print(globals())

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

def split_data(
    data: pd.DataFrame, 
    parameters: Dict[str, Any]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Splits data into features and target training and test sets

    Args:
        data: Data containing features and target.
        parameters: Parameters defined in parameters.yml.
    Returns:
        Split data.
    """
    
    df_target = data[parameters["target_column"]]
    df_target = df_target.eq(parameters["target_value"]).astype(int)
    data = data.drop(parameters["target_column"], axis=1)
    
    assert parameters["train_frac"] >= 0 and parameters["train_frac"] <= 1, "Invalid training set fraction"

    X_train, X_test, Y_train, Y_test = train_test_split(
                                        data, df_target, 
                                        train_size=parameters["train_frac"], stratify=df_target,random_state=parameters["random_state"])


    return X_train, X_test, Y_train, Y_test


def preprocessing(data: pd.DataFrame,  parameters: Dict[str, Any]):
    """Uses tfdf to vectorize text.
      Args:
        data: Training data of features.
        parameters: data parameters

    Returns:
        vectorizer: fitted TfidfVectorizer
        transformed_data: transformed data
    """
    preprocess = Preprocessing(parameters["categorical_cols"], parameters["number_cols"], parameters["expected_cols"])
    transformed_data = preprocess.transform(data)

    return  preprocess, transformed_data

def train(target: pd.DataFrame, transformed_data: pd.DataFrame ,  parameters: Dict[str, Any]):
    """Uses preprocessed data.
      Args:
        data: Training data of features.
        parameters: data parameters

    Returns:
        model: trained RandomForest
    """
    
    rf = RandomForestClassifier()
    rf_random = RandomizedSearchCV(estimator = rf,param_distributions = parameters["random_grid"],
               n_iter = parameters["n_iter"], cv = parameters["cv"],
               verbose = parameters["verbose"], random_state= parameters["random_state"],
               n_jobs = parameters["n_jobs"])
    rf_random.fit(transformed_data, target)

    logger.info(f'Best Parameters: {rf_random.best_params_} \n')

    model = RandomForestClassifier(**rf_random.best_params_)
    model.fit(transformed_data, target)
    return model



def make_predictions(
    test: pd.DataFrame,  preprocessing: Preprocessing,  model: RandomForestClassifier
) -> pd.Series:
    """Uses 1-nearest neighbour classifier to create predictions.

    Args:
        test: Training data of features.
        test: fitte TfIdf
        model: trained data
        parameters: data parameters

    Returns:
        y_pred: Prediction of the target variable.
    """

    test_input_model = preprocessing.transform(test)
    test_result = model.predict(test_input_model)

    return test_result


def report_accuracy(test: pd.Series, test_result: np.array):
    """Calculates and logs the accuracy.

    Args:
        y_pred: Predicted target.
        y_test: True target.
    """
    recall= recall_score(test,test_result)
    accuracy = accuracy_score(test, test_result)
    logger.info(f"Model has accuracy of {accuracy} on test data." )
    logger.info(f"Model has recall of {recall} on test data." )


