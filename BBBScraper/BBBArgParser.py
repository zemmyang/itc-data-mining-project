from argparse import ArgumentParser, Namespace
import sys
from BBBScraper import messages as M


def define_optional_args(parser: ArgumentParser) -> None:
    parser.add_argument("-v", "--verbose", help=M.VERBOSE_HELP, action="store_true")
    parser.add_argument("-c", "--config", help=M.CONFIG_HELP)
    parser.add_argument("-l", "--log", help=M.LOG_HELP, default='log.txt')
    parser.add_argument("-t", "--type", type=str, help=M.TYPE_HELP, default='SQL')


def define_required_args(parser: ArgumentParser) -> None:
    group = parser.add_argument_group("BBB scraper arguments")
    group.add_argument("--lim", type=int, help=M.LIM_HELP)
    group.add_argument("--loc", type=str, help=M.LOC_HELP, default="US")
    group.add_argument("--acc", help=M.ACC_HELP, action="store_true")
    group.add_argument("--all", help=M.ALL_HELP, action="store_true")
    group.add_argument('cats', nargs='*', help=M.CATS_HELP)

    define_optional_args(parser)

    check_if_no_args(parser)


def check_if_no_args(parser: ArgumentParser) -> None:
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)


def check_passed_args(args: Namespace) -> None:
    args.type.upper()  # it's uppercase whenever I check it...

    if args.all:
        raise NotImplementedError(M.SCRAPE_ALL_NOT_IMPLEMENTED_ERROR)
    elif args.config:
        raise NotImplementedError(M.CONFIG_NOT_IMPLEMENTED_ERROR)
    else:
        if len(args.cats) == 0:
            raise SyntaxError(M.NO_ALL_FLAG_BUT_NO_CAT_ERROR)
    # check_if_config_is_used(args)


def check_if_config_is_used(args: Namespace) -> None:
    if args.config:
        try:
            with open(args.config) as file:
                print(f"Using config file {file.name}")
        except FileNotFoundError:
            print(f"Specified config file {args.config} not found")

    else:
        print(M.NO_CONFIG_USED)
