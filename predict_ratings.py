# pyre-strict
import json
from argparse import ArgumentParser
from typing import List, Any, Dict
from sklearn.svm import LinearSVC


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
    model: LinearSVC = train_model(training_file, args.verbose)

    test_file: str = args.test_file
    output_file: str = args.output_file
    outbuffer = open(output_file, 'w')

    with open(test_file) as testing:
        for line in testing:
            testing_line: str = line.strip()
            testing_dict: Dict[str, Any] = json.loads(testing_line)

            predictedRating = model.predict([testing_dict["features"]])[0]
            output_dict = dict()
            output_dict["id"] = testing_dict["id"]
            output_dict["predictedRating"] = float(predictedRating)
            print(output_dict)

            outbuffer.write(json.dumps(output_dict) + "\n")

    outbuffer.close()


def train_model(training_file: str, verbose: bool) -> LinearSVC:
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

    # Create and fit model
    verbose_int: int = 1 if verbose else 0
    model: LinearSVC = LinearSVC(verbose=verbose_int)
    model.fit(features_lists, scores)
    return model


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    inner_main(args)


if __name__ == '__main__':
    main()
