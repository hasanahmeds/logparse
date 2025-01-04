import logging

def configure(verbose: bool = False) -> None:
    logging.basicConfig(level=logging.DEBUG if verbose else logging.WARNING,
                        format="%(levelname)s: %(message)s", force=True)
