class SomeModel:
    def predict(self, message: str) -> float:
        if not isinstance(message, str):
            raise TypeError(
                f"Parameter 'message' must be an str, "
                f"got {type(message).__name__} instead."
            )
        prediction = 0.5
        for ch_idx in range(len(message) - 1):
            if message[ch_idx: ch_idx + 2] == ":)":
                prediction += 0.1
            elif message[ch_idx: ch_idx + 2] == ":(":
                prediction -= 0.1
        return prediction


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    if not isinstance(message, str):
        raise TypeError(
            f"Parameter 'message' must be an str, "
            f"got {type(message).__name__} instead."
        )
    if not isinstance(bad_thresholds, float):
        raise TypeError(
            f"Parameter 'bad_thresholds' must be a float, "
            f"got {type(bad_thresholds).__name__} instead."
        )
    if not isinstance(good_thresholds, float):
        raise TypeError(
            f"Parameter 'good_thresholds' must be a float, "
            f"got {type(good_thresholds).__name__} instead."
        )
    if not isinstance(model, SomeModel):
        raise TypeError(
            f"Parameter 'model' must have type SomeModel, "
            f"got {type(model).__name__} instead."
        )
    if bad_thresholds > good_thresholds:
        raise ValueError(
            "Parameter 'bad_thresholds' must be less "
            "or equal then 'good_thresholds'."
        )

    prediction = model.predict(message)
    if prediction < bad_thresholds:
        return "неуд"
    if prediction > good_thresholds:
        return "отл"
    return "норм"
