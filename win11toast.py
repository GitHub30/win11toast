import asyncio
from turtle import onclick
from winsdk.windows.data.xml.dom import XmlDocument
from winsdk.windows.foundation import IPropertyValue
from winsdk.windows.ui.notifications import (
    ToastNotificationManager,
    ToastNotification,
    ToastActivatedEventArgs,
    ToastDismissedEventArgs,
    ToastFailedEventArgs
)


xml = """
<toast activationType="protocol" launch="http:">
    <visual>
        <binding template='ToastGeneric'></binding>
    </visual>
</toast>
"""


def set_attribute(document, xpath, name, value):
    attribute = document.create_attribute(name)
    attribute.value = value
    document.select_single_node(xpath).attributes.set_named_item(attribute)


def add_text(message, document):
    binding = document.select_single_node('//binding')
    text = document.create_element('text')
    text.inner_text = message
    binding.append_child(text)


def add_logo(logo, document):
    binding = document.select_single_node('//binding')
    image = document.create_element('image')
    image.set_attribute('placement', 'appLogoOverride')
    image.set_attribute('hint-crop', 'circle')
    image.set_attribute('src', logo)
    binding.append_child(image)


def add_image(src, document):
    binding = document.select_single_node('//binding')
    image = document.create_element('image')
    image.set_attribute('src', src)
    binding.append_child(image)


def add_audio(src, document):
    toast = document.select_single_node('/toast')
    audio = document.create_element('audio')
    audio.set_attribute('src', src)
    toast.append_child(audio)


def create_actions(document):
    toast = document.select_single_node('/toast')
    actions = document.create_element('actions')
    toast.append_child(actions)
    return actions


def add_action(action, document):
    actions = document.select_single_node(
        '//actions') or create_actions(document)
    action_element = document.create_element('action')
    action_element.set_attribute('activationType', 'system')
    action_element.set_attribute('arguments', 'dismiss')
    action_element.set_attribute('content', action)
    actions.append_child(action_element)


def add_input(id, document):
    actions = document.select_single_node(
        '//actions') or create_actions(document)
    input = document.create_element('input')
    input.set_attribute('id', id)
    input.set_attribute('type', 'text')
    actions.append_child(input)


def add_selections(selections, document):
    actions = document.select_single_node(
        '//actions') or create_actions(document)
    input = document.create_element('input')
    input.set_attribute('id', 'selection')
    input.set_attribute('type', 'selection')
    actions.append_child(input)
    for selection in selections:
        selection_element = document.create_element('selection')
        selection_element.set_attribute('id', selection)
        selection_element.set_attribute('content', selection)
        input.append_child(selection_element)


def activated_args(_, event):
    e = ToastActivatedEventArgs._from(event)
    user_input = dict([(name, IPropertyValue._from(
        e.user_input[name]).get_string()) for name in e.user_input])
    return {
        'arguments': e.arguments,
        'user_input': user_input
    }


async def toast_async(title=None, body=None, on_click=print, on_dismissed=print, on_failed=print, inputs=[], selections=[], actions=[], logo=None, image=None, audio=None, xml=xml):
    """
    Notify
    Args:
        title: <str>
        body: <str>
        on_click: <function>
        on_dismissed: <function>
        on_failed: <function>
        inputs: <list<str>> ['textbox']
        selections: <list<str>> ['Apple', 'Banana', 'Grape']
        actions: <list<str>> ['Button']
        logo: <str> https://unsplash.it/64?image=669
        image: <str> https://4.bp.blogspot.com/-u-uyq3FEqeY/UkJLl773BHI/AAAAAAAAYPQ/7bY05EeF1oI/s800/cooking_toaster.png
        audio: <str> ms-winsoundevent:Notification.Looping.Alarm
        xml: <str>

    Returns:
        None
    """
    notifier = ToastNotificationManager.create_toast_notifier()

    document = XmlDocument()
    document.load_xml(xml)

    if isinstance(on_click, str):
        set_attribute(document, '/toast', 'launch', on_click)

    if title:
        add_text(title, document)
    if body:
        add_text(body, document)
    if inputs:
        for input in inputs:
            add_input(input, document)
    if selections:
        add_selections(selections, document)
    if actions:
        for action in actions:
            add_action(action, document)
    if logo:
        add_logo(logo, document)
    if image:
        add_image(image, document)
    if audio:
        add_audio(audio, document)

    notification = ToastNotification(document)
    loop = asyncio.get_running_loop()
    futures = []

    if isinstance(on_click, str):
        on_click = print
    activated_future = loop.create_future()
    activated_token = notification.add_activated(
        lambda *args: loop.call_soon_threadsafe(
            activated_future.set_result, on_click(activated_args(*args))
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
