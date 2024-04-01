import os

import click
import pendulum


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
    no_args_is_help=True,
    epilog="Specify one of these sub-commands and you can find more help from there.",
)
@click.pass_context
def cli(ctx, **kwargs):  # noqa:  # pylint: disable=unused-argument
    """
    Golf Muppet CLI
    """


@cli.command("get")
@click.pass_context
@click.option(
    "--booking-date",
    required=False,
    default=pendulum.now().to_date_string(),
    help="Booking date for which to get tee times.",
)
@click.option(
    "--club-id",
    required=True,
    help="Club ID from which to get tee times.",
)
@click.option(
    "--look-forward-days",
    required=False,
    default=7,
    help="Number of days to look forward for tee times.",
)
def get(ctx, **kwargs):  # noqa:  # pylint: disable=unused-argument
    """Get tee times for a given range of dates."""
    from get import get as get_tee_times

    booking_date = pendulum.parse(kwargs.pop("booking_date"), tz=os.getenv("BOOKING_TIMEZONE", "Pacific/Auckland"))
    look_forward_days: int = int(kwargs.pop("look_forward_days"))
    club_id: int = int(kwargs.pop("club_id"))

    for i in range(look_forward_days):
        get_tee_times(
            booking_date=booking_date.add(days=i + 1),
            club_id=club_id,
        )


@cli.command("list")
@click.pass_context
@click.option(
    "--fields",
    multiple=True,
    required=False,
    default=None,
)
def list(ctx, **kwargs):  # noqa:  # pylint: disable=unused-argument
    """List all available clubs."""
    from list import list_ as list_clubs

    list_clubs(**kwargs)


@cli.command("build")
@click.pass_context
def build(ctx, **kwargs):  # noqa:  # pylint: disable=unused-argument
    """Build required resources."""
    pass


@cli.command("destroy")
@click.pass_context
def destroy(ctx, **kwargs):  # noqa:  # pylint: disable=unused-argument
    """Destroy all resources."""
    pass


if __name__ == "__main__":
    cli()
