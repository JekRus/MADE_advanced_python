from contextlib import nullcontext as does_not_raise
from unittest.mock import patch
import pytest

import sentiment
from sentiment import predict_message_mood, SomeModel


@pytest.mark.parametrize(
    "bad_thresholds,good_thresholds,prediction,expected_answer",
    [
        (0.1, 0.9, 0.0, "неуд"),
        (0.1, 0.9, 0.5, "норм"),
        (0.1, 0.9, 1.0, "отл"),
        (0.3, 0.5, 0.0, "неуд"),
        (0.3, 0.5, 0.5, "норм"),
        (0.3, 0.5, 1.0, "отл"),
        (0.3, 0.4, 0.0, "неуд"),
        (0.3, 0.4, 0.5, "отл"),
        (0.3, 0.4, 1.0, "отл"),
        (0.8, 0.9, 0.0, "неуд"),
        (0.8, 0.9, 0.5, "неуд"),
        (0.8, 0.9, 1.0, "отл"),
    ],
)
def test_predict_message_mood_basic(
    bad_thresholds, good_thresholds, prediction, expected_answer
):
    sample_message = "Message"
    with patch.object(sentiment.SomeModel, "predict") as mpredict:
        mpredict.return_value = prediction
        model = sentiment.SomeModel()
        answer = predict_message_mood(
            sample_message, model, bad_thresholds, good_thresholds
        )
        assert answer == expected_answer


@pytest.mark.parametrize(
    "message,bad_thresholds,good_thresholds,exp_exception",
    [
        (42, 0.1, 0.9, TypeError),
        (42.2, 0.1, 0.9, TypeError),
        ([1, 2, 3], 0.1, 0.9, TypeError),
        ({"a": 1, "b": 2}, 0.1, 0.9, TypeError),
        (set(), 0.1, 0.9, TypeError),
        ("valid message", "string", 0.9, TypeError),
        ("valid message", "", 0.9, TypeError),
        ("valid message", 10, 0.9, TypeError),
        ("valid message", [1, 2, 3], 0.9, TypeError),
        ("valid message", {"a": 1, "b": 2}, 0.9, TypeError),
        ("valid message", 0.1, "string", TypeError),
        ("valid message", 0.1, "", TypeError),
        ("valid message", 0.1, 10, TypeError),
        ("valid message", 0.1, [1, 2, 3], TypeError),
        ("valid message", 0.1, {"a": 1, "b": 2}, TypeError),
        ("valid message", 0.9, 0.1, ValueError),
        ("valid message", 0.5, 0.49, ValueError),
        ("valid message", 100.0, -100.0, ValueError),
    ],
)
def test_predict_message_mood_wrong_arguments(
    message, bad_thresholds, good_thresholds, exp_exception
):
    with patch.object(sentiment.SomeModel, "predict") as mpredict:
        mpredict.return_value = 1
        with pytest.raises(exp_exception):
            model = sentiment.SomeModel()
            predict_message_mood(message, model, bad_thresholds, good_thresholds)


@pytest.mark.parametrize(
    "message", ["message1", "message2", "", "MESSAGE3", "MESSage4", "3232"]
)
def test_predict_message_mood_default_params(message):
    with patch.object(sentiment.SomeModel, "predict") as mpredict:
        ret_vals = [-100.0, 0.29, 0.3, 0.31, 0.5, 0.8, 0.81, 0.9, 100.0]
        expected_answers = [
            "неуд",
            "неуд",
            "норм",
            "норм",
            "норм",
            "норм",
            "отл",
            "отл",
            "отл",
        ]
        mpredict.side_effect = ret_vals
        model = sentiment.SomeModel()
        for ans in expected_answers:
            assert predict_message_mood(message, model) == ans


def test_predict_message_mood_wrong_model_type():
    message, bad_thresholds, good_thresholds = ("valid message", 0.1, 0.9)
    wrong_models = [42, "not a model", {"a": 1}, [1, 2, 3]]
    for model in wrong_models:
        with pytest.raises(TypeError):
            predict_message_mood(message, model, bad_thresholds, good_thresholds)


@pytest.mark.parametrize(
    "message,bad_thresholds,good_thresholds,model_retval,expected_answer",
    [
        ("message1", 0.1, 0.9, 0.09, "неуд"),
        ("message1", 0.1, 0.9, 0.1, "норм"),
        ("message1", 0.1, 0.9, 0.9, "норм"),
        ("message1", 0.1, 0.9, 0.91, "отл"),
        ("message1", 0.2, 0.3, 0.19, "неуд"),
        ("message1", 0.2, 0.3, 0.2, "норм"),
        ("message1", 0.2, 0.3, 0.3, "норм"),
        ("message1", 0.2, 0.3, 0.31, "отл"),
        ("message1", 0.5, 0.5, 0.49, "неуд"),
        ("message1", 0.5, 0.5, 0.5, "норм"),
        ("message1", 0.5, 0.5, 0.51, "отл"),
    ],
)
def test_predict_message_mood_corner_case(
    message, bad_thresholds, good_thresholds, model_retval, expected_answer
):
    with patch.object(sentiment.SomeModel, "predict") as mpredict:
        mpredict.return_value = model_retval
        model = sentiment.SomeModel()
        answer = predict_message_mood(message, model, bad_thresholds, good_thresholds)
        assert answer == expected_answer


@pytest.mark.parametrize(
    'message,expectation',
    [
        ('any_string', does_not_raise()),
        ('UPPER and lower case and digits 021943', does_not_raise()),
        ('\t\t\n\t', does_not_raise()),
        (42, pytest.raises(TypeError)),
        (-127.3, pytest.raises(TypeError)),
        (0, pytest.raises(TypeError)),
        (None, pytest.raises(TypeError)),
        ({'a': 1, 'b': 2}, pytest.raises(TypeError)),
        ({3, 4, -12}, pytest.raises(TypeError)),
    ]
)
def test_model_predict_wrong_argument(message, expectation):
    model = SomeModel()
    with expectation:
        assert model.predict(message) is not None
