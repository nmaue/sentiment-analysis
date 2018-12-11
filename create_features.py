"""
Handles Negation and uses binary bag

Vocab 10000
"""
# pyre-strict
import json
from argparse import ArgumentParser
from typing import List, Dict, Any, Tuple
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from collections import Counter
from nltk.sentiment.util import mark_negation

stopwords = set(stopwords.words('english'))

# Max size of vocab
VOCAB_SIZE: int = 10000


def get_parser() -> ArgumentParser:
    """Define the command line args (verbose unused for now)"""

    parser: ArgumentParser = ArgumentParser(
        "Build a feature file from a file with review text")

    parser.add_argument("in_file")
    parser.add_argument("out_file")
    parser.add_argument("-v", "--verbose", default=False,
                        required=False, action="store_true")
    parser.add_argument("--build-vocab", "-bv", required=False,
                        default=None, dest="vocab_out")
    parser.add_argument("--read-vocab", "-rv", required=False,
                        default=None, dest="vocab_in")

    return parser


def inner_main(args) -> None:
    """Run the main function"""

    in_file: str = args.in_file
    out_file: str = args.out_file
    build_vocab = args.vocab_out is not None

    if args.verbose:
        print("Starting to clean reviews")

    # Get cleaned reviews and vocab dict
    cleaned_reviews, vocab = clean_reviews_and_get_vocab(in_file, build_vocab)

    if args.verbose:
        print("Reviews cleaned")

    if args.vocab_in is not None:
        # Read vocab in and overwrite
        vocab_file: str = args.vocab_in
        vocab = read_vocab(vocab_file)
        if args.verbose:
            print("Vocab read in")

    if args.vocab_out is not None:
        # Write vocab to file
        vocab_file: str = args.vocab_out
        store_vocab(vocab_file, vocab)
        if args.verbose:
            print("Vocab file written")

    with open(out_file, "w") as outbuffer:
        if args.verbose:
            print("Starting to build features")

        # For each review get featires and write to file
        for review_dict in cleaned_reviews:
            output_dict = dict()
            output_dict["features"] = get_features(
                review_dict["reviewText"], vocab)
            output_dict["id"] = review_dict["id"]
            if "overall" in review_dict:
                output_dict["overall"] = review_dict["overall"]
            outbuffer.write(json.dumps(output_dict) + "\n")

    if args.verbose:
        print("Features written")


def clean_reviews_and_get_vocab(
    in_file: str,
    build_vocab: bool
) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """
    Iterate over the input file
        Tokenize review
        add all tokens to counter
        add review dict to cleaned review list

    Get most common tokens and assign them an index

    returns list of cleaned review dicts and the vocab dict
    """

    ret: List[Dict[str, Any]] = []
    counter: Counter = Counter()
    with open(in_file, "r") as inbuffer:
        for line in inbuffer:
            stripped_line: str = line.strip()
            input_dict: Dict[str, Any] = json.loads(stripped_line)
            reviewText: str = input_dict["reviewText"]

            # Clean and tokenize this review
            input_dict["reviewText"] = clean_and_tokenize_review(reviewText)

            # add tokens to counter
            counter.update(input_dict["reviewText"])

            # add to return list
            ret.append(input_dict)

    ret_vocab = None

    if build_vocab:
        ret_vocab = dict()

        # Get most common tokens
        elements = counter.most_common(VOCAB_SIZE)
        i = 0

        # Assign each an index
        for word in elements:
            ret_vocab[word[0]] = i
            i += 1

    return ret, ret_vocab


def clean_and_tokenize_review(review_text: str) -> List[str]:
    """
    Uses wordpunct_tokenize to keep punctuation groups together
    # https://www.nltk.org/api/nltk.tokenize.html#nltk.tokenize.regexp.WordPunctTokenizer

    Removes nltk stopwords from token list
    """
    tokens: List[str] = wordpunct_tokenize(review_text)
    mark_negation(tokens, shallow=True)
    return [token for token in tokens if token.lower() not in stopwords]


def get_features(review: List[str], vocab: Dict[str, int]) -> List[int]:
    """Check if token in vocab, if yes set index to 1"""
    ret: List[int] = [0 for x in range(len(vocab))]
    for token in review:
        if token in vocab:
            ret[vocab[token]] = 1

    return ret


def read_vocab(vocab_file: str) -> Dict[str, int]:
    """Create vocab dict from file, to be consistent"""
    ret_dict: Dict[str, int] = dict()
    with open(vocab_file, 'r') as vocabbuffer:
        vocab_string = vocabbuffer.read().strip()
        ret_dict: Dict[str, int] = json.loads(vocab_string)
    return ret_dict


def store_vocab(vocab_file: str, vocab: Dict[str, int]) -> None:
    """Write the vocab dict to a file"""
    vocab_string: str = json.dumps(vocab)
    with open(vocab_file, 'w') as vocabbuffer:
        vocabbuffer.write(vocab_string)


def validate_args(args) -> bool:
    if args.vocab_in is None and args.vocab_out is None:
        print("Must include either build or read vocab file")
        return False

    if args.vocab_in is not None and args.vocab_out is not None:
        print("Only include either build or read voacb file")
        return False

    return True


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    if validate_args(args):
        inner_main(args)


if __name__ == '__main__':
    main()
