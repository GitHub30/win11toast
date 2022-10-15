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

DEFAULT_APP_ID = 'Python'

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


async def play_sound(audio):
    from winsdk.windows.media.core import MediaSource
    from winsdk.windows.media.playback import MediaPlayer

    if audio.startswith('http'):
        from winsdk.windows.foundation import Uri
        source = MediaSource.create_from_uri(Uri(audio))
    else:
        from winsdk.windows.storage import StorageFile
        file = await StorageFile.get_file_from_path_async(audio)
        source = MediaSource.create_from_storage_file(file)

    player = MediaPlayer()
    player.source = source
    player.play()
    await asyncio.sleep(7)


async def speak(text):
    from winsdk.windows.media.core import MediaSource
    from winsdk.windows.media.playback import MediaPlayer
    from winsdk.windows.media.speechsynthesis import SpeechSynthesizer

    # print(list(map(lambda info: info.description, SpeechSynthesizer.get_all_voices())))

    stream = await SpeechSynthesizer().synthesize_text_to_stream_async(text)
    player = MediaPlayer()
    player.source = MediaSource.create_from_stream(stream, stream.content_type)
    player.play()
    await asyncio.sleep(7)


async def recognize(ocr):
    from winsdk.windows.media.ocr import OcrEngine
    from winsdk.windows.graphics.imaging import BitmapDecoder
    if isinstance(ocr, str):
        ocr = {'ocr': ocr}
    if ocr['ocr'].startswith('http'):
        from winsdk.windows.foundation import Uri
        from winsdk.windows.storage.streams import RandomAccessStreamReference
        ref = RandomAccessStreamReference.create_from_uri(Uri(ocr['ocr']))
        stream = await ref.open_read_async()
    else:
        from winsdk.windows.storage import StorageFile, FileAccessMode
        file = await StorageFile.get_file_from_path_async(ocr['ocr'])
        stream = await file.open_async(FileAccessMode.READ)
    decoder = await BitmapDecoder.create_async(stream)
    bitmap = await decoder.get_software_bitmap_async()
    if 'lang' in ocr:
        from winsdk.windows.globalization import Language
        if OcrEngine.is_language_supported(Language(ocr['lang'])):
            engine = OcrEngine.try_create_from_language(Language(ocr['lang']))
        else:
            class UnsupportedOcrResult:
                def __init__(self):
                    self.text = 'Please install. Get-WindowsCapability -Online -Name "Language.OCR*"'
            return UnsupportedOcrResult()
    else:
        engine = OcrEngine.try_create_from_user_profile_languages()
    # Avaliable properties (lines, angle, word, BoundingRect(x,y,width,height))
    # https://docs.microsoft.com/en-us/uwp/api/windows.media.ocr.ocrresult?view=winrt-22621#properties
    return await engine.recognize_async(bitmap)


def available_recognizer_languages():
    from winsdk.windows.media.ocr import OcrEngine
    for language in OcrEngine.get_available_recognizer_languages():
        print(language.display_name, language.language_tag)
    print('Run as Administrator')
    print('Get-WindowsCapability -Online -Name "Language.OCR*"')
    print('Add-WindowsCapability -Online -Name "Language.OCR~~~en-US~0.0.1.0"')


def notify(title=None, body=None, on_click=print, icon=None, image=None, progress=None, audio=None, dialogue=None, duration=None, input=None, inputs=[], selection=None, selections=[], button=None, buttons=[], xml=xml, app_id=DEFAULT_APP_ID):
    document = XmlDocument()
    document.load_xml(xml)

    if isinstance(on_click, str):
        set_attribute(document, '/toast', 'launch', on_click)

    if duration:
        set_attribute(document, '/toast', 'duration', duration)

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
        if isinstance(audio, str) and audio.startswith('ms'):
            add_audio(audio, document)
        elif isinstance(audio, dict) and 'src' in audio and audio['src'].startswith('ms'):
            add_audio(audio, document)
        else:
            add_audio({'silent': 'true'}, document)
    if dialogue:
        add_audio({'silent': 'true'}, document)

    notification = ToastNotification(document)
    if progress:
        data = NotificationData()
        for name, value in progress.items():
            data.values[name] = str(value)
        data.sequence_number = 1
        notification.data = data
        notification.tag = 'my_tag'
    if app_id == DEFAULT_APP_ID:
        try:
            notifier = ToastNotificationManager.create_toast_notifier()
        except Exception as e:
            notifier = ToastNotificationManager.create_toast_notifier(app_id)
    else:
        notifier = ToastNotificationManager.create_toast_notifier(app_id)
    notifier.show(notification)
    return notification


async def toast_async(title=None, body=None, on_click=print, icon=None, image=None, progress=None, audio=None, dialogue=None, duration=None, input=None, inputs=[], selection=None, selections=[], button=None, buttons=[], xml=xml, app_id=DEFAULT_APP_ID, ocr=None, on_dismissed=print, on_failed=print):
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
    if ocr:
        title = 'OCR Result'
        body = (await recognize(ocr)).text
        src = ocr if isinstance(ocr, str) else ocr['ocr']
        image = {'placement': 'hero', 'src': src}
    notification = notify(title, body, on_click, icon, image,
                          progress, audio, dialogue, duration, input, inputs, selection, selections, button, buttons, xml, app_id)
    loop = asyncio.get_running_loop()
    futures = []

    if audio and isinstance(audio, str) and not audio.startswith('ms'):
        futures.append(loop.create_task(play_sound(audio)))
    if dialogue:
        futures.append(loop.create_task(speak(dialogue)))

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


def update_progress(progress, app_id=DEFAULT_APP_ID):
    data = NotificationData()
    for name, value in progress.items():
        data.values[name] = str(value)
    data.sequence_number = 2
    if app_id == DEFAULT_APP_ID:
        try:
            notifier = ToastNotificationManager.create_toast_notifier()
        except Exception as e:
            notifier = ToastNotificationManager.create_toast_notifier(app_id)
    else:
        notifier = ToastNotificationManager.create_toast_notifier(app_id)
    return notifier.update(data, 'my_tag')
