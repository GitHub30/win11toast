import asyncio
from winsdk.windows.data.xml.dom import XmlDocument
from winsdk.windows.foundation import IPropertyValue
from winsdk.windows.ui.notifications import (
    ToastNotificationManager,
    ToastNotification,
    NotificationData,
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


def add_text(msg, document):
    if isinstance(msg, str):
        msg = {
            'text': msg
        }
    binding = document.select_single_node('//binding')
    text = document.create_element('text')
    for name, value in msg.items():
        if name == 'text':
            text.inner_text = msg['text']
        else:
            text.set_attribute(name, value)
    binding.append_child(text)


def add_icon(icon, document):
    if isinstance(icon, str):
        icon = {
            'placement': 'appLogoOverride',
            'hint-crop': 'circle',
            'src': icon
        }
    binding = document.select_single_node('//binding')
    image = document.create_element('image')
    for name, value in icon.items():
        image.set_attribute(name, value)
    binding.append_child(image)


def add_image(img, document):
    if isinstance(img, str):
        img = {
            'src': img
        }
    binding = document.select_single_node('//binding')
    image = document.create_element('image')
    for name, value in img.items():
        image.set_attribute(name, value)
    binding.append_child(image)


def add_progress(prog, document):
    binding = document.select_single_node('//binding')
    progress = document.create_element('progress')
    for name in prog:
        progress.set_attribute(name, '{' + name + '}')
    binding.append_child(progress)


def add_audio(aud, document):
    if isinstance(aud, str):
        aud = {
            'src': aud
        }
    toast = document.select_single_node('/toast')
    audio = document.create_element('audio')
    for name, value in aud.items():
        audio.set_attribute(name, value)
    toast.append_child(audio)


def create_actions(document):
    toast = document.select_single_node('/toast')
    actions = document.create_element('actions')
    toast.append_child(actions)
    return actions


def add_button(button, document):
    if isinstance(button, str):
        button = {
            'activationType': 'protocol',
            'arguments': 'http:' + button,
            'content': button
        }
    actions = document.select_single_node(
        '//actions') or create_actions(document)
    action = document.create_element('action')
    for name, value in button.items():
        action.set_attribute(name, value)
    actions.append_child(action)


def add_input(id, document):
    if isinstance(id, str):
        id = {
            'id': id,
            'type': 'text',
            'placeHolderContent': id
        }
    actions = document.select_single_node(
        '//actions') or create_actions(document)
    input = document.create_element('input')
    for name, value in id.items():
        input.set_attribute(name, value)
    actions.append_child(input)


def add_selection(selection, document):
    if isinstance(selection, list):
        selection = {
            'input': {
                'id': 'selection',
                'type': 'selection'
            },
            'selection': selection
        }
    actions = document.select_single_node(
        '//actions') or create_actions(document)
    input = document.create_element('input')
    for name, value in selection['input'].items():
        input.set_attribute(name, value)
    actions.append_child(input)
    for sel in selection['selection']:
        if isinstance(sel, str):
            sel = {
                'id': sel,
                'content': sel
            }
        selection_element = document.create_element('selection')
        for name, value in sel.items():
            selection_element.set_attribute(name, value)
        input.append_child(selection_element)


def activated_args(_, event):
    e = ToastActivatedEventArgs._from(event)
    user_input = dict([(name, IPropertyValue._from(
        e.user_input[name]).get_string()) for name in e.user_input])
    return {
        'arguments': e.arguments,
        'user_input': user_input
    }


def notify(title=None, body=None, on_click=print, icon=None, image=None, progress=None, audio=None, input=None, inputs=[], selection=None, selections=[], button=None, buttons=[], xml=xml):
    notifier = ToastNotificationManager.create_toast_notifier()

    document = XmlDocument()
    document.load_xml(xml)

    if isinstance(on_click, str):
        set_attribute(document, '/toast', 'launch', on_click)

    if title:
        add_text(title, document)
    if body:
        add_text(body, document)
    if input:
        add_input(input, document)
    if inputs:
        for input in inputs:
            add_input(input, document)
    if selection:
        add_selection(selection, document)
    if selections:
        for selection in selections:
            add_selection(selection, document)
    if button:
        add_button(button, document)
    if buttons:
        for button in buttons:
            add_button(button, document)
    if icon:
        add_icon(icon, document)
    if image:
        add_image(image, document)
    if progress:
        add_progress(progress, document)
    if audio:
        add_audio(audio, document)

    notification = ToastNotification(document)
    if progress:
        data = NotificationData()
        for name, value in progress.items():
            data.values[name] = str(value)
        data.sequence_number = 1
        notification.data = data
        notification.tag = 'my_tag'
    notifier.show(notification)
    return notification


async def toast_async(title=None, body=None, on_click=print, icon=None, image=None, progress=None, audio=None, input=None, inputs=[], selection=None, selections=[], button=None, buttons=[], xml=xml, on_dismissed=print, on_failed=print):
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
        icon: <str> https://unsplash.it/64?image=669
        image: <str> https://4.bp.blogspot.com/-u-uyq3FEqeY/UkJLl773BHI/AAAAAAAAYPQ/7bY05EeF1oI/s800/cooking_toaster.png
        audio: <str> ms-winsoundevent:Notification.Looping.Alarm
        xml: <str>

    Returns:
        None
    """
    notification = notify(title, body, on_click, icon, image,
                          progress, audio, input, inputs, selection, selections, button, buttons, xml)
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


def update_progress(progress):
    data = NotificationData()
    for name, value in progress.items():
        data.values[name] = str(value)
    data.sequence_number = 2
    return ToastNotificationManager.create_toast_notifier().update(data, 'my_tag')
