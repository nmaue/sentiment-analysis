# pyre-strict
import json
from argparse import ArgumentParser
from typing import List, Any, Dict
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier


def get_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        "Predict Ratings from training feature file and test feature file")

    parser.add_argument("training_file")
    parser.add_argument("test_file")
    parser.add_argument("output_file")
    parser.add_argument("-v", "--verbose", default=False,
                        required=False, action="store_true")

    return parser


def inner_main(args) -> None:
    """Train the model and predict each in test file"""
    training_file: str = args.training_file

    if args.verbose:
        print("Beginning to train model")
    model: OneVsRestClassifier = train_model(training_file, args.verbose)

    test_file: str = args.test_file
    output_file: str = args.output_file

    id_list: List[Any] = []
    feature_list: List[Any] = []
    prediction_list: List[float] = []

    if args.verbose:
        print("Starting testing")

    with open(test_file) as testing:
        for line in testing:
            testing_line: str = line.strip()
            testing_dict: Dict[str, Any] = json.loads(testing_line)

            id_list.append(testing_dict["id"])
            feature_list.append(testing_dict["features"])

    if args.verbose:
        print("Test file read, begin prediction")

    prediction_list = model.predict(feature_list)

    if args.verbose:
        print("All predictions made, writing to file!")

    with open(output_file, 'w') as outbuffer:
        i: int = 0
        for id in id_list:
            out_dict: Dict[str, Any] = dict()
            out_dict["id"] = id
            out_dict["predictedRating"] = float(prediction_list[i])
            i += 1
            outbuffer.write(json.dumps(out_dict) + "\n")


def train_model(training_file: str, verbose: bool) -> OneVsRestClassifier:
    """Iteralte over each line to add features to list and overall ratings"""
    scores: List[int] = []
    features_lists: List[List[int]] = []
    with open(training_file) as training:
        for line in training:
            training_line: str = line.strip()
            training_dict: Dict[str, Any] = json.loads(training_line)
            score: int = training_dict["overall"]
            scores.append(score)
            features: List[int] = training_dict["features"]
            features_lists.append(features)

    if verbose:
        print("Training file read, model fitting go!")

    # Create and fit model
    verbose_int: int = 1 if verbose else 0
    model: LinearSVC = OneVsRestClassifier(LinearSVC(verbose=verbose_int), 56)
    model.fit(features_lists, scores)

    if verbose:
        print("Model is fit!")

    return model


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    inner_main(args)


if __name__ == '__main__':
    main()
