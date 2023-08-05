from edulint.linting.problem import ProblemEncoder
from edulint.config.config import get_config
from edulint.linting.linting import lint
import argparse
import json


def setup_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint provided code.")
    parser.add_argument("file", metavar="FILE", help="the file to lint")
    parser.add_argument("--json", action="store_true",
                        help="should output problems in json format")
    return parser.parse_args()


def main() -> int:
    args = setup_argparse()
    config = get_config(args.file)
    result = lint(args.file, config)
    if args.json:
        print(json.dumps(result, indent=1, cls=ProblemEncoder))
    else:
        for problem in result:
            print(problem)
    return 0
