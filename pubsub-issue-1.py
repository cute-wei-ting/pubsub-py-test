from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from datetime import datetime, timezone
from db import add

# TODO(developer)
project_id = "skye-personal"
subscription_id = "pubsub-issue-1"
table = "ordering" 
test=0

# project_id = "your-project-id"
# subscription_id = "your-subscription-id"
# Number of seconds the subscriber should listen for messages
timeout = 300.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    print(f"{message.publish_time}")
    message.subscribe_time = datetime.now(timezone.utc)
    add(table,message)
    message.ack()
    # nack test
    
    # global test
    # if test == 2:
    #     print(f"nack {message.data}.")
    #     message.nack()
    # else:
    #     message.ack()
    # test+= 1
    

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.