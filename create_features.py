# pyre-strict
import json
from argparse import ArgumentParser
from typing import List, Dict, Any, Tuple, Set
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from collections import Counter

stopwords = set(stopwords.words('english'))

VOCAB_SIZE: int = 300


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

    cleaned_reviews, vocab = clean_reviews_and_get_vocab(in_file)

    with open(out_file, "w") as outbuffer:
        for review_dict in cleaned_reviews:
            output_dict = dict()
            output_dict["features"] = get_features(
                review_dict["reviewText"], vocab)
            output_dict["id"] = review_dict["id"]
            if "rating" in review_dict:
                output_dict["rating"] = review_dict["rating"]
            outbuffer.write(json.dumps(output_dict) + "\n")


def clean_reviews_and_get_vocab(
        in_file: str) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    ret: List[Dict[str, Any]] = []
    counter: Counter = Counter()
    with open(in_file, "r") as inbuffer:
        for line in inbuffer:
            stripped_line: str = line.strip()
            input_dict: Dict[str, Any] = json.loads(stripped_line)
            reviewText: str = input_dict["reviewText"]
            input_dict["reviewText"] = clean_and_tokenize_review(reviewText)

            counter.update(input_dict["reviewText"])
            ret.append(input_dict)

    elements = counter.most_common(VOCAB_SIZE)
    ret_vocab = dict()
    i = 0

    for word in elements:
        ret_vocab[word[0]] = i
        i += 1

    return ret, ret_vocab


def clean_and_tokenize_review(review_text: str) -> List[str]:
    tokens: List[str] = wordpunct_tokenize(review_text)

    return [token for token in tokens if token not in stopwords]


def get_features(review: List[str], vocab: Dict[str, int]) -> List[int]:
    ret: List[int] = [0 for x in range(len(vocab))]
    for token in review:
        if token in vocab:
            ret[vocab[token]] = 1

    return ret


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    inner_main(args)


if __name__ == '__main__':
    main()
