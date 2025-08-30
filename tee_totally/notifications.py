#!/usr/bin/env python3
"""
Notification system for sending alerts when tee times are found using AWS SNS.
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

from .logger import log

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False


class NotificationError(Exception):
    """Exception raised for notification-related errors."""
    pass


class SNSNotifier:
    """SNS notification handler for WhatsApp and other messaging."""
    
    def __init__(self, region_name: str = 'ap-southeast-2'):
        self.client = None
        self.region_name = region_name
        self.topic_arn = None
        self._initialize()
    
    def _initialize(self):
        """Initialize SNS client with AWS credentials."""
        if not AWS_AVAILABLE:
            log.warning("Boto3 library not installed. Install with: pip install boto3")
            return
            
        try:
            self.client = boto3.client('sns', region_name=self.region_name)
            
            # Test credentials by listing topics
            self.client.list_topics()
            log.info(f"SNS client initialized successfully in region {self.region_name}")
            
        except NoCredentialsError:
            log.error("AWS credentials not found. Configure with AWS CLI, environment variables, or IAM roles.")
        except Exception as e:
            log.error(f"Failed to initialize SNS client: {e}")
            raise NotificationError(f"Failed to initialize SNS client: {e}")
    
    def is_available(self) -> bool:
        """Check if SNS notifications are available."""
        return self.client is not None and AWS_AVAILABLE
    
    def create_topic(self, topic_name: str, display_name: str = None) -> Optional[str]:
        """
        Create an SNS topic.
        
        Args:
            topic_name: Name of the SNS topic
            display_name: Display name for the topic
            
        Returns:
            Topic ARN if created successfully, None otherwise
        """
        if not self.is_available():
            log.error("SNS client not available")
            return None
        
        try:
            response = self.client.create_topic(Name=topic_name)
            topic_arn = response['TopicArn']
            
            if display_name:
                self.client.set_topic_attributes(
                    TopicArn=topic_arn,
                    AttributeName='DisplayName',
                    AttributeValue=display_name
                )
            
            log.info(f"SNS topic created successfully: {topic_arn}")
            return topic_arn
            
        except ClientError as e:
            log.error(f"Failed to create SNS topic: {e}")
            return None
    
    def list_topics(self) -> List[Dict[str, str]]:
        """
        List all SNS topics.
        
        Returns:
            List of topic dictionaries with TopicArn
        """
        if not self.is_available():
            return []
        
        try:
            response = self.client.list_topics()
            return response.get('Topics', [])
        except Exception as e:
            log.error(f"Failed to list SNS topics: {e}")
            return []
    
    def get_topic_by_name(self, topic_name: str) -> Optional[str]:
        """
        Get topic ARN by name.
        
        Args:
            topic_name: Name of the topic to find
            
        Returns:
            Topic ARN if found, None otherwise
        """
        topics = self.list_topics()
        for topic in topics:
            arn = topic['TopicArn']
            if arn.split(':')[-1] == topic_name:
                return arn
        return None
    
    def publish_message(self, topic_arn: str, message: str, subject: str = None) -> bool:
        """
        Publish a message to an SNS topic.
        
        Args:
            topic_arn: ARN of the SNS topic
            message: Message to publish
            subject: Optional subject for the message
            
        Returns:
            True if message published successfully, False otherwise
        """
        if not self.is_available():
            log.error("SNS client not available")
            return False
        
        try:
            publish_args = {
                'TopicArn': topic_arn,
                'Message': message
            }
            
            if subject:
                publish_args['Subject'] = subject
            
            response = self.client.publish(**publish_args)
            message_id = response['MessageId']
            
            log.info(f"Message published successfully. MessageId: {message_id}")
            return True
            
        except Exception as e:
            log.error(f"Failed to publish SNS message: {e}")
            return False
    
    def add_phone_subscription(self, topic_arn: str, phone_number: str) -> bool:
        """
        Subscribe a phone number to an SNS topic for SMS.
        
        Args:
            topic_arn: ARN of the SNS topic
            phone_number: Phone number in E.164 format (e.g., +1234567890)
            
        Returns:
            True if subscription created successfully, False otherwise
        """
        if not self.is_available():
            return False
        
        try:
            # Ensure phone number is in E.164 format
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number
            
            response = self.client.subscribe(
                TopicArn=topic_arn,
                Protocol='sms',
                Endpoint=phone_number
            )
            
            subscription_arn = response['SubscriptionArn']
            log.info(f"Phone subscription created: {subscription_arn}")
            return True
            
        except Exception as e:
            log.error(f"Failed to create phone subscription: {e}")
            return False
    
    def add_email_subscription(self, topic_arn: str, email_address: str) -> bool:
        """
        Subscribe an email address to an SNS topic for email notifications.
        
        Args:
            topic_arn: ARN of the SNS topic
            email_address: Email address to subscribe
            
        Returns:
            True if subscription created successfully, False otherwise
        """
        if not self.is_available():
            return False
        
        try:
            response = self.client.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint=email_address
            )
            
            subscription_arn = response['SubscriptionArn']
            log.info(f"Email subscription created: {subscription_arn}")
            return True
            
        except Exception as e:
            log.error(f"Failed to create email subscription: {e}")
            return False


def format_tee_time_notification(tee_times: List[Dict[str, Any]], search_criteria: Dict[str, Any]) -> str:
    """
    Format tee time results into a readable notification message.
    
    Args:
        tee_times: List of found tee time dictionaries
        search_criteria: Dictionary of search parameters used
        
    Returns:
        Formatted message string
    """
    if not tee_times:
        return "No tee times found matching your criteria."
    
    message_parts = [
        "🏌️ TEE TIME ALERT!",
        "",
        f"Found {len(tee_times)} tee time(s) matching your criteria:",
        ""
    ]
    
    for i, tee_time in enumerate(tee_times[:3], 1):  # Limit to 3 for SMS length
        club_name = tee_time.get('club_name', 'Unknown Club')
        tee_time_str = tee_time.get('tee_time', 'Unknown Time')
        date_str = tee_time.get('date', 'Unknown Date')
        available_slots = tee_time.get('available_slots', 0)
        booking_links = tee_time.get('booking_links', [])
        
        # Parse the datetime for better formatting
        try:
            dt = datetime.fromisoformat(tee_time_str.replace('Z', '+00:00'))
            time_str = dt.strftime('%H:%M')
        except:
            time_str = tee_time_str
        
        # Get the first booking link if available
        first_booking_url = None
        if booking_links and len(booking_links) > 0:
            first_booking_url = booking_links[0].get('booking_url')
        
        message_parts.extend([
            f"{i}. {club_name}",
            f"   {date_str} at {time_str}",
            f"   {available_slots} slot(s) available"
        ])
        
        # Add booking link if available
        if first_booking_url:
            message_parts.append(f"   Book: {first_booking_url}")
        
        message_parts.append("")  # Empty line between entries
    
    if len(tee_times) > 3:
        message_parts.append(f"...and {len(tee_times) - 3} more")
    
    return "\n".join(message_parts)


def send_tee_time_notification(
    tee_times: List[Dict[str, Any]], 
    search_criteria: Dict[str, Any],
    topic_name: str = 'tee-totally-notifications',
    region_name: str = 'ap-southeast-2'
) -> bool:
    """
    Send tee time notification via SNS.
    
    Args:
        tee_times: List of found tee times
        search_criteria: Search parameters used
        topic_name: SNS topic name to publish to
        region_name: AWS region
        
    Returns:
        True if notification sent successfully, False otherwise
    """
    if not tee_times:
        log.info("No tee times to notify about")
        return True
    
    # Initialize notifier
    notifier = SNSNotifier(region_name=region_name)
    
    if not notifier.is_available():
        log.error("SNS notifications not available")
        return False
    
    # Get topic ARN
    topic_arn = notifier.get_topic_by_name(topic_name)
    if not topic_arn:
        log.error(f"SNS topic '{topic_name}' not found. Create it first with: tee-totally build sns")
        return False
    
    # Format and send message
    message = format_tee_time_notification(tee_times, search_criteria)
    subject = f"Tee Times Found - {len(tee_times)} match(es)"
    
    log.info(f"Sending SNS notification to topic: {topic_name}")
    return notifier.publish_message(topic_arn, message, subject)


def send_test_notification(
    topic_name: str = 'tee-totally-notifications',
    region_name: str = 'ap-southeast-2'
) -> bool:
    """
    Send a test SNS notification.
    
    Args:
        topic_name: SNS topic name
        region_name: AWS region
        
    Returns:
        True if test message sent successfully, False otherwise
    """
    notifier = SNSNotifier(region_name=region_name)
    
    if not notifier.is_available():
        log.error("SNS notifications not available")
        return False
    
    topic_arn = notifier.get_topic_by_name(topic_name)
    if not topic_arn:
        log.error(f"SNS topic '{topic_name}' not found")
        return False
    
    test_message = (
        "🏌️ Tee Totally Test Notification\n\n"
        "This is a test notification from your golf tee time finder.\n\n"
        "If you receive this message, SNS notifications are working correctly!\n\n"
        f"Sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    log.info(f"Sending test SNS notification to topic: {topic_name}")
    return notifier.publish_message(topic_arn, test_message, "Test Notification")