import logging
import os
import sys

from unipipeline.args import CMD_INIT, CMD_CHECK, CMD_CRON, CMD_PRODUCE, CMD_CONSUME, parse_args, CMD_SCAFFOLD
from unipipeline.modules.uni import Uni


def run_check(u: Uni, args) -> None:  # type: ignore
    u.check()


def run_scaffold(u: Uni, args) -> None:  # type: ignore
    u.scaffold()


def run_cron(u: Uni, args) -> None:  # type: ignore
    u.start_cron()


def run_init(u: Uni, args) -> None:  # type: ignore
    u.initialize(everything=True)


def run_consume(u: Uni, args) -> None:  # type: ignore
    u.start_consuming(workers=list(args.consume_workers))


def run_produce(u: Uni, args) -> None:  # type: ignore
    u.send_to(args.produce_worker, args.produce_data, alone=args.produce_alone)


args_cmd_map = {
    CMD_INIT: run_init,
    CMD_CHECK: run_check,
    CMD_SCAFFOLD: run_scaffold,
    CMD_CRON: run_cron,
    CMD_PRODUCE: run_produce,
    CMD_CONSUME: run_consume,
}


def main() -> None:
    sys.path.insert(0, os.getcwdb().decode('utf-8'))
    args = parse_args()
    u = Uni(args.config_file, echo_level=logging.DEBUG if args.verbose else None)
    args_cmd_map[args.cmd](u, args)
    u.echo.success('done')
