import asyncio
from winsdk.windows.data.xml.dom import XmlDocument
from winsdk.windows.ui.notifications import (
    ToastNotificationManager,
    ToastNotification,
    ToastActivatedEventArgs,
    ToastDismissedEventArgs,
    ToastFailedEventArgs
)


async def toast_async(title='Hello', body='Hello from Python', on_click=print, on_dismissed=print, on_failed=print):
    """
    Notify
    Args:
        title: <str>
        body: <str>
        on_click: <function>
        on_dismissed: <function>
        on_failed: <function>

    Returns:
        None
    """
    notifier = ToastNotificationManager.create_toast_notifier()
    launch = on_click if isinstance(on_click, str) else 'http:'
    # https://docs.microsoft.com/en-us/windows/uwp/launch-resume/launch-default-app
    # http: or file:
    tString = f"""
<toast activationType="protocol" launch="{launch}">
    <visual>
        <binding template='ToastGeneric'>
            <text>{title}</text>
            <text>{body}</text>
        </binding>
    </visual>
    <actions>
        <action content="Play" activationType="protocol" arguments="C:\Windows\Media\Alarm01.wav"/>
    </actions>
</toast>
"""

    document = XmlDocument()
    document.load_xml(tString)
    notification = ToastNotification(document)
    loop = asyncio.get_running_loop()
    futures = []

    if isinstance(on_click, str):
        on_click = print
    activated_future = loop.create_future()
    activated_token = notification.add_activated(
        lambda _, event_args: loop.call_soon_threadsafe(
            activated_future.set_result, on_click(
                ToastActivatedEventArgs._from(event_args).arguments)
        )
    )
    futures.append(activated_future)

    dismissed_future = loop.create_future()
    dismissed_token = notification.add_dismissed(
        lambda _, event_args: loop.call_soon_threadsafe(
            dismissed_future.set_result, on_dismissed(ToastDismissedEventArgs._from(event_args).reason))
    )
    futures.append(dismissed_future)

    failed_future = loop.create_future()
    failed_token = notification.add_failed(
        lambda _, event_args: loop.call_soon_threadsafe(
            failed_future.set_result, on_failed(ToastFailedEventArgs._from(event_args).error_code))
    )
    futures.append(failed_future)

    notifier.show(notification)
    try:
        _, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
        for p in pending:
            p.cancel()
    finally:
        if activated_token is not None:
            notification.remove_activated(activated_token)
        if dismissed_token is not None:
            notification.remove_dismissed(dismissed_token)
        if failed_token is not None:
            notification.remove_failed(failed_token)


def toast(*args, **kwargs):
    asyncio.run(toast_async(*args, **kwargs))


if __name__ == '__main__':
    url = 'https://www.python.org'
    toast('Hello Python', 'Click to open url', on_click=url)
