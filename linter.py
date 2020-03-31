# coding=utf-8

import logging
import sys
from pylint.lint import Run

logger = logging.getLogger('linter')

exit_code = 0
cmd_line_args = sys.argv[1:]

if cmd_line_args:
    if "--fail-under" in cmd_line_args:
        fail_under_index = cmd_line_args.index("--fail-under")
        fail_under_value = float(cmd_line_args[fail_under_index + 1])
        del cmd_line_args[fail_under_index:fail_under_index + 2]
    else:
        logger.warning("no fail_under argument provided, defaulting to 10.0")
        fail_under_value = 10.0


    results = Run(args=cmd_line_args, do_exit=False)
    sys.stdout.flush()

    try:
        score = results.linter.stats["global_note"]
    except KeyError:
        logger.warning("no score parsed from Pylint output")
        exit_code = 1
    else:
        if score < fail_under_value:
            logger.error("score %s is less than fail-under value %s", score, fail_under_value)
            exit_code = 1
else:
    print("usage: pylint-fail-under [--fail_under SCORE] [Pylint Command Line Arguments]")

sys.exit(exit_code)
