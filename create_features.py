# pyre-strict
import json
from argparse import ArgumentParser
from typing import List, Dict, Any


def get_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        "Build a feature file from a file with review text")

    parser.add_argument("in_file")
    parser.add_argument("out_file")
    parser.add_argument("-v", "--verbose", default=False,
                        required=False, action="store_true")

    return parser


def inner_main(args) -> None:
    in_file: str = args.in_file
    out_file: str = args.out_file

    with open(in_file, "r") as inbuffer:
        outbuffer = open(out_file, "w")
        for line in inbuffer:
            stripped_line: str = line.strip()
            input_dict: Dict[str, Any] = json.loads(stripped_line)
            output_dict = dict()
            reviewText: str = input_dict["reviewText"]
            output_dict["features"] = get_features(reviewText)
            output_dict["id"] = input_dict["id"]
            if ("rating" in input_dict):
                output_dict["rating"] = input_dict["rating"]
            outbuffer.write(json.dumps(output_dict) + "\n")
        outbuffer.close()


def get_features(review_text: str) -> List[int]:
    return [0 for x in range(10)]


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    inner_main(args)


if __name__ == '__main__':
    main()
