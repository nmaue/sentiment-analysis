# pyre-strict
import json
from argparse import ArgumentParser
from typing import Dict, Tuple


def score(predicted: int, answer: int) -> Tuple[int, int]:
    complete: int = 0
    binary: int = 0
    if predicted == answer:
        complete = 1

    if predicted >= 3 and answer >= 3:
        binary = 1

    if predicted < 3 and answer < 3:
        binary = 1

    return complete, binary


def get_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        "Score the predicted of a test file")

    parser.add_argument("test_file", required=True)
    parser.add_argument("answer_file", required=True)

    return parser


def inner_main(args) -> None:
    test_file: str = args.test_file
    answer_file: str = args.answer_file
    answers = open(answer_file)
    complete_total = 0
    binary_total = 0
    count = 0
    with open(test_file) as testbuffer:
        for line in testbuffer:
            test_line: str = line.strip()
            test_dict: Dict[str, int] = json.loads(test_line)
            answer_line: str = answers.readline()
            answer_dict: Dict[str, int] = json.loads(answer_line)

            if test_dict["id"] != answer_dict["id"]:
                raise Exception("Test ID on line does not match Answer ID")

            complete, binary = score(
                test_dict["predictedRating"], answer_dict["rating"])

            complete_total += complete
            binary_total += binary
            count += 1

    answers.close()
    print(
        """
5 Point Match Rating: {0} out of {1}
5 Point Accuracy: {2}

Binary Match Rating: {3} out of {1}
Binary Accuracy: {4}
""".format(
            complete_total,
            count,
            (complete_total / count),
            binary_total,
            (binary_total / count)
        )
    )


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    inner_main(args)


if __name__ == '__main__':
    main()
