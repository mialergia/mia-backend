import onesignal as onesignal_sdk
import environ

env = environ.Env(
    ONESIGNAL_ANDROID_ID=str,
    ONESIGNAL_ANDROID_API_KEY=str,
    ONESIGNAL_IOS_ID=str,
    ONESIGNAL_IOS_API_KEY=str,
)
environ.Env.read_env()

onesignal_android_client = onesignal_sdk.Client(
    app_id=env('ONESIGNAL_ANDROID_ID'),
    app_auth_key=env('ONESIGNAL_ANDROID_API_KEY'),
)

onesignal_ios_client = onesignal_sdk.Client(
    app_id=env('ONESIGNAL_IOS_ID'),
    app_auth_key=env('ONESIGNAL_IOS_API_KEY'),
)


def send_push_notification(users_queryset, title, body):
    player_ids = []
    for user in users_queryset.exclude(onesignal_player_id=None):
        player_ids.append(user.onesignal_player_id)

    new_notification = onesignal_sdk.Notification(post_body={"contents": {'en': body}})
    new_notification.set_parameter("include_player_ids", player_ids)
    new_notification.set_parameter("headings", {'en': title})
    onesignal_response = onesignal_android_client.send_notification(new_notification)
    onesignal_response = onesignal_ios_client.send_notification(new_notification)

    return onesignal_response
