import argparse
from contextlib import ExitStack
import logging
from pathlib import Path
import sys
from . import __version__
from .config import Config
from .filters import Filters
from .logging_setup import configure
from .pipeline import analyze
from .output import atomic_output
from .reader import open_input
from .reports import write_csv, write_json
from .timestamps import iso_timestamp

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stream HTTP access logs into JSON or CSV analytics")
    parser.add_argument("inputs", nargs="+", help="Input paths, .gz files, or - for stdin")
    parser.add_argument("--input-format", choices=["auto", "json", "apache"], default="auto")
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--since")
    parser.add_argument("--until")
    parser.add_argument("--path-prefix", default="")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args(argv)
    configure(args.verbose)
    try:
        if args.inputs.count("-") > 1:
            raise ValueError("stdin may appear only once")
        filters = Filters(iso_timestamp(args.since) if args.since else None,
                          iso_timestamp(args.until) if args.until else None, args.path_prefix)
        config = Config.load(args.config) if args.config else Config()
        def streams():
            for path in args.inputs:
                with open_input(path) as stream:
                    yield path, stream
        report = analyze(streams(), config, filters, args.input_format, args.strict)
        writer = write_json if args.format == "json" else write_csv
        with ExitStack() as stack:
            output = stack.enter_context(atomic_output(args.output)) if args.output else sys.stdout
            writer(report, output)
        return 0
    except (OSError, ValueError, EOFError) as exc:
        logging.error("%s", exc)
        return 2
