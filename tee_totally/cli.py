import json
import os
import sys
from typing import Optional

import click
import pendulum

# Period to time range mapping
PERIODS = {
    "dawn": ("05:00", "08:00"),
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
    from .get import get as get_tee_times

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
    from .list import list_ as list_clubs

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
    from .compare import compare_states

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
    multiple=True,
    type=int,
    help="Club ID(s) to search for tee times. Can specify multiple times (e.g., --club-id 341 --club-id 342).",
)
@click.option(
    "--club-name", 
    multiple=True,
    type=str,
    help="Club name(s) to search for tee times. Uses fuzzy matching. Can specify multiple times (e.g., --club-name 'Pupuke' --club-name 'Taupo').",
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
@click.option(
    "--notify",
    is_flag=True,
    help="Send SNS notification when tee times are found.",
)
@click.option(
    "--topic-name",
    default="tee-totally-notifications",
    help="SNS topic name for notifications (default: tee-totally-notifications).",
)
@click.option(
    "--region",
    default="ap-southeast-2",
    help="AWS region for SNS notifications (default: ap-southeast-2).",
)
def find(ctx, **kwargs):  # noqa:  # pylint: disable=unused-argument
    """Find available tee times for a club within a timestamp range."""
    from .find import find_available_tee_times
    from .clubs import find_club_ids_by_name, get_club_name_by_id
    
    club_ids = list(kwargs.pop("club_id")) if kwargs.get("club_id") else []
    club_names = kwargs.pop("club_name")
    
    # Handle club name lookups
    if club_names:
        for club_name in club_names:
            matched_ids = find_club_ids_by_name(club_name, max_matches=1)
            if matched_ids:
                matched_id = matched_ids[0]
                matched_club_name = get_club_name_by_id(matched_id)
                click.echo(f"Found club: {matched_club_name} (ID: {matched_id}) for search '{club_name}'")
                club_ids.append(matched_id)
            else:
                click.echo(f"Warning: No clubs found matching '{club_name}'")
    
    if not club_ids:
        click.echo("Error: At least one --club-id or --club-name is required.")
        return
        
    from_date_str = kwargs.pop("from_date")
    to_date_str = kwargs.pop("to_date")
    next_n_days = kwargs.pop("next_n_days")
    time_range = kwargs.pop("time_range")
    period = kwargs.pop("period")
    free_slots = kwargs.pop("free_slots")
    playing_partners = kwargs.pop("playing_partners")
    day_of_week = kwargs.pop("day_of_week")
    notify = kwargs.pop("notify")
    topic_name = kwargs.pop("topic_name")
    region = kwargs.pop("region")
    
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
    
    # Call find function and get results
    available_times = find_available_tee_times(club_ids, from_timestamp, to_timestamp, time_range, free_slots, playing_partners, day_of_week)
    
    # Send notification if requested and tee times were found
    if notify and available_times:
        from .notifications import send_tee_time_notification
        
        search_criteria = {
            'time_range': time_range,
            'day_of_week': day_of_week,
            'free_slots': free_slots,
            'playing_partners': playing_partners
        }
        
        click.echo(f"📲 Sending notification to SNS topic: {topic_name}")
        
        if send_tee_time_notification(available_times, search_criteria, topic_name, region):
            click.echo("✅ Notification sent successfully!")
        else:
            click.echo("❌ Failed to send notification")
    elif notify and not available_times:
        click.echo("📲 No tee times found - no notification sent")


@cli.group("build")
@click.pass_context
def build(ctx, **kwargs):  # noqa:  # pylint: disable=unused-argument
    """Build required resources."""
    pass


@build.command("sns")
@click.pass_context
@click.option(
    "--topic-name",
    default="tee-totally-notifications",
    help="Name of the SNS topic to create (default: tee-totally-notifications).",
)
@click.option(
    "--display-name",
    default="Tee Totally Notifications",
    help="Display name for the SNS topic.",
)
@click.option(
    "--phone-number",
    help="Phone number to subscribe for SMS notifications (E.164 format, e.g., +1234567890).",
)
@click.option(
    "--email",
    help="Email address to subscribe for email notifications.",
)
@click.option(
    "--region",
    default="ap-southeast-2",
    help="AWS region to create resources in (default: ap-southeast-2).",
)
def build_sns(ctx, **kwargs):  # noqa:  # pylint: disable=unused-argument
    """Build SNS topic for WhatsApp/SMS notifications."""
    from .notifications import SNSNotifier
    
    topic_name = kwargs.pop("topic_name")
    display_name = kwargs.pop("display_name")
    phone_number = kwargs.pop("phone_number")
    email = kwargs.pop("email")
    region = kwargs.pop("region")
    
    click.echo(f"Creating SNS resources in region: {region}")
    
    # Initialize SNS notifier
    notifier = SNSNotifier(region_name=region)
    
    if not notifier.is_available():
        click.echo("❌ SNS not available. Make sure boto3 is installed and AWS credentials are configured.")
        return
    
    # Check if topic already exists
    existing_topic_arn = notifier.get_topic_by_name(topic_name)
    if existing_topic_arn:
        click.echo(f"ℹ️  SNS topic '{topic_name}' already exists: {existing_topic_arn}")
        topic_arn = existing_topic_arn
    else:
        # Create topic
        click.echo(f"Creating SNS topic: {topic_name}")
        topic_arn = notifier.create_topic(topic_name, display_name)
        
        if not topic_arn:
            click.echo("❌ Failed to create SNS topic")
            return
        
        click.echo(f"✅ SNS topic created successfully: {topic_arn}")
    
    # Subscribe phone number if provided
    if phone_number:
        click.echo(f"Subscribing phone number: {phone_number}")
        
        if notifier.add_phone_subscription(topic_arn, phone_number):
            click.echo(f"✅ Phone number subscribed successfully")
            click.echo("📱 You should receive an SMS confirmation. Reply 'YES' to confirm the subscription.")
        else:
            click.echo("❌ Failed to subscribe phone number")
    
    # Subscribe email if provided
    if email:
        click.echo(f"Subscribing email address: {email}")
        
        if notifier.add_email_subscription(topic_arn, email):
            click.echo(f"✅ Email address subscribed successfully")
            click.echo("📧 You should receive an email confirmation. Click the confirmation link to confirm the subscription.")
        else:
            click.echo("❌ Failed to subscribe email address")
    
    # Show configuration info
    click.echo("\n🔧 Configuration:")
    click.echo(f"  Topic Name: {topic_name}")
    click.echo(f"  Topic ARN: {topic_arn}")
    click.echo(f"  Region: {region}")
    
    if phone_number:
        click.echo(f"  Phone: {phone_number}")
    if email:
        click.echo(f"  Email: {email}")
    
    click.echo("\n📝 Next steps:")
    steps = []
    if phone_number:
        steps.append("1. Confirm SMS subscription (reply 'YES' to the SMS)")
    if email:
        steps.append(f"{len(steps) + 1}. Confirm email subscription (click link in email)")
    steps.append(f"{len(steps) + 1}. Test notifications with: tee-totally build test-notification")
    steps.append(f"{len(steps) + 1}. Use --notify flag when running find commands")
    
    for step in steps:
        click.echo(f"  {step}")


@build.command("test-notification")
@click.pass_context
@click.option(
    "--topic-name",
    default="tee-totally-notifications",
    help="Name of the SNS topic to test (default: tee-totally-notifications).",
)
@click.option(
    "--region",
    default="ap-southeast-2",
    help="AWS region (default: ap-southeast-2).",
)
def test_notification(ctx, **kwargs):  # noqa:  # pylint: disable=unused-argument
    """Send a test notification to verify SNS setup."""
    from .notifications import send_test_notification
    
    topic_name = kwargs.pop("topic_name")
    region = kwargs.pop("region")
    
    click.echo(f"Sending test notification to SNS topic: {topic_name}")
    
    if send_test_notification(topic_name, region):
        click.echo("✅ Test notification sent successfully!")
        click.echo("📱 Check your phone/WhatsApp for the test message.")
    else:
        click.echo("❌ Failed to send test notification")
        click.echo("Check that:")
        click.echo("  - AWS credentials are configured")
        click.echo("  - SNS topic exists (create with: tee-totally build sns)")
        click.echo("  - Phone number is subscribed and confirmed")


@cli.command("destroy")
@click.pass_context
def destroy(ctx, **kwargs):  # noqa:  # pylint: disable=unused-argument
    """Destroy all resources."""
    pass


if __name__ == "__main__":
    cli()
