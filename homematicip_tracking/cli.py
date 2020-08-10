"""Console script for homematicip_tracking."""
import sys
import click
from prometheus_client import start_http_server
from time import sleep

from .homematicip_tracking import HomematiIP


@click.command()
@click.argument('config', type=click.Path())
@click.argument('port', type=click.INT)
@click.option('--wait', default=5*60,
              help='Waiting time between metric polls'
)
@click.option('--print/--no-print', 'prnt', default=False)
def main(config, port, wait, prnt):
    """Console script for homematicip_tracking."""

    hmip = HomematiIP(config)
    start_http_server(port)

    while True:
        metrics = hmip.poll_thermostats()
        if prnt:
            print(metrics.head())
        sleep(wait)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
