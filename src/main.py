import argparse

from scenario import Scenario


def get_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", dest="username", required=True)
    parser.add_argument("-p", "--password", dest="password", required=True)
    parser.add_argument("-t", "--token", dest="token", required=True)

    return parser


def main(username, password, token):
    scenario = Scenario(username, password, token)
    scenario.play()


if __name__ == '__main__':
    args_parser = get_args_parser()
    args = args_parser.parse_args()

    main(username=args.username, password=args.password, token=args.token)
