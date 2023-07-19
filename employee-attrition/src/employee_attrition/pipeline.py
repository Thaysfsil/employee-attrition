"""
This is a boilerplate pipeline
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import make_predictions, report_accuracy, split_data, train, preprocessing


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["data", "parameters"],
                outputs=["X_train", "X_test", "Y_train", "Y_test"],
                name="split",
            ),
            node(
                func=preprocessing,
                inputs=["X_train", "params:preprocessing"],
                outputs=["preprocess", "transformed_data"],
                name="preprocesing",
            ),
            node(
                func=train,
                inputs=["Y_train", "transformed_data", "params:train"],
                outputs="model",
                name="train",
            ),
            node(
                func=make_predictions,
                inputs=["X_test", "preprocess", "model"],
                outputs="test_result",
                name="make_predictions",
            ),
            node(
                func=report_accuracy,
                inputs=["Y_test", "test_result"],
                outputs=None,
                name="report_accuracy",
            ),
        ]
    )