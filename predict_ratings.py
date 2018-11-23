# pyre-strict
import json
from argparse import ArgumentParser
from typing import List, Any, Dict
from sklearn.svm import SVC


def get_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        "Predict Ratings from training feature file and test feature file")

    parser.add_argument("training_file", required=True)
    parser.add_argument("test_file", required=True)
    parser.add_argument("output_file", required=True)

    return parser


def inner_main(args) -> None:
    training_file: str = args.training_file
    model: SVC = train_model(training_file)

    test_file: str = args.test_file
    output_file: str = args.output_file
    outbuffer = open(output_file, 'w')

    with open(test_file) as testing:
        for line in testing:
            testing_line: str = line.strip()
            testing_dict: Dict[str, Any] = json.loads(testing_line)

            predictedRating = model.predict(testing_dict["features"])
            output_dict = dict()
            output_dict["id"] = testing_dict["id"]
            output_dict["predictedRating"] = predictedRating

            outbuffer.write(json.dumps(output_dict) + "\n")

    outbuffer.close()


def train_model(training_file: str) -> SVC:
    scores: List[int] = []
    features_lists: List[List[int]] = []
    with open(training_file) as training:
        for line in training:
            training_line: str = line.strip()
            training_dict: Dict[str, Any] = json.loads(training_line)
            score: int = training_dict["score"]
            scores.append(score)
            features: List[int] = training_dict["features"]
            features_lists.append(features)
    model: SVC = SVC()
    model.fit(scores, features_lists)
    return model


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    inner_main(args)


if __name__ == '__main__':
    main()
