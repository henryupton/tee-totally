import json
import os
import sys
from typing import Optional

import click
import pendulum

# Period to time range mapping
PERIODS = {
    "dawn": ("05:00", "07:00"),
    "morning": ("07:00", "12:00"),
    "noon": ("11:00", "14:00"),
    "afternoon": ("12:00", "18:00"),
    "evening": ("17:00", "21:00")
}


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


@cli.command("compare")
@click.pass_context
@click.option(
    "--file-a",
    required=True,
)
@click.option(
    "--file-b",
    required=True,
)
@click.option(
    "--output-path",
    required=False,
    default=None,
    help="Path to output file.",
)
def compare(ctx, **kwargs):  # noqa:  # pylint: disable=unused-argument
    """Compare two files."""
    from compare import compare_states

    with open(kwargs.pop("file_a")) as a, open(kwargs.pop("file_b")) as b:
        state_a: dict = json.load(a)
        state_b: dict = json.load(b)

    diff: dict = compare_states(state_a, state_b)

    output_path: Optional[str] = kwargs.pop("output_path", None)
    if output_path:
        with open(output_path, "w") as f:
            json.dump(diff, f, indent=2, default=str)
    else:
        sys.stdout.write(json.dumps(diff, indent=2, default=str))


@cli.command("find")
@click.pass_context
@click.option(
    "--club-id",
    required=True,
    help="Club ID to search for tee times.",
)
@click.option(
    "--from",
    "from_date",
    required=False,
    help="Start date for search (YYYY-MM-DD).",
)
@click.option(
    "--to",
    "to_date",
    required=False,
    help="End date for search (YYYY-MM-DD).",
)
@click.option(
    "--next-n-days",
    required=False,
    type=int,
    help="Search next N days from today (alternative to --from/--to).",
)
@click.option(
    "--time-range",
    required=False,
    help="Time range filter (HH:MM-HH:MM, e.g., 08:00-12:00).",
)
@click.option(
    "--period",
    required=False,
    type=click.Choice(["dawn", "morning", "noon", "afternoon", "evening"]),
    help="Predefined time period filter.",
)
@click.option(
    "--free-slots",
    required=False,
    type=int,
    default=1,
    help="Minimum number of free slots required (default: 1).",
)
@click.option(
    "--playing-partners",
    required=False,
    type=int,
    help="Minimum number of slots already booked by other players.",
)
@click.option(
    "--day-of-week",
    multiple=True,
    type=click.Choice(["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]),
    help="Filter by day of week (can specify multiple).",
)
def find(ctx, **kwargs):  # noqa:  # pylint: disable=unused-argument
    """Find available tee times for a club within a timestamp range."""
    from find import find_available_tee_times
    
    club_id = int(kwargs.pop("club_id"))
    from_date_str = kwargs.pop("from_date")
    to_date_str = kwargs.pop("to_date")
    next_n_days = kwargs.pop("next_n_days")
    time_range = kwargs.pop("time_range")
    period = kwargs.pop("period")
    free_slots = kwargs.pop("free_slots")
    playing_partners = kwargs.pop("playing_partners")
    day_of_week = kwargs.pop("day_of_week")
    
    # Validate date/timestamp options
    if next_n_days is not None:
        if from_date_str or to_date_str:
            click.echo("Error: Cannot use --next-n-days with --from/--to. Choose one approach.")
            return
        if next_n_days <= 0:
            click.echo("Error: --next-n-days must be greater than 0.")
            return
        # Calculate timestamps from next_n_days
        now = pendulum.now()
        from_timestamp = now.start_of('day')
        to_timestamp = now.add(days=next_n_days).end_of('day')
    else:
        if not from_date_str or not to_date_str:
            click.echo("Error: Either use --next-n-days OR provide both --from and --to dates.")
            return
        # Convert dates to full day timestamps
        from_timestamp = pendulum.parse(from_date_str).start_of('day')
        to_timestamp = pendulum.parse(to_date_str).end_of('day')
    
    # Validate playing_partners constraint
    if playing_partners is not None:
        if playing_partners + free_slots > 4:
            click.echo(f"Error: playing-partners ({playing_partners}) + free-slots ({free_slots}) cannot exceed 4.")
            return
    
    # Convert period to time_range if specified
    if period and period in PERIODS:
        if time_range:
            click.echo("Warning: Both --time-range and --period specified. Using --time-range.")
        else:
            start_time, end_time = PERIODS[period]
            time_range = f"{start_time}-{end_time}"
    
    find_available_tee_times(club_id, from_timestamp, to_timestamp, time_range, free_slots, playing_partners, day_of_week)


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
