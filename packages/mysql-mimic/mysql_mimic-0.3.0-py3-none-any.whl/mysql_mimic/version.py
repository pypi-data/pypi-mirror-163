"""mysql-mimic version information"""

__version__ = "0.3.0"


def main(name):
    if name == "__main__":
        print(__version__)


main(__name__)
