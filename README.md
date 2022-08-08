[![Python](https://img.shields.io/pypi/pyversions/win11toast.svg)](https://badge.fury.io/py/win11toast)
[![PyPI](https://badge.fury.io/py/win11toast.svg)](https://badge.fury.io/py/win11toast)

# win11toast
Toast notifications for Windows 10 and 11 based on [WinRT](https://docs.microsoft.com/en-us/windows/apps/design/shell/tiles-and-notifications/adaptive-interactive-toasts)

![image](https://user-images.githubusercontent.com/12811398/183295421-59686d68-bfb2-4d9d-ad61-afc8bd4e4808.png)

## Installation

```bash
pip install win11toast
```

## Usage

```python
from win11toast import toast

toast('Hello Python')
```

```python
from win11toast import toast

toast('Hello Python', 'Click to open url', on_click='https://www.python.org')
```

#### Use callback
```python
from win11toast import toast

toast('Hello Python', 'Click to open url', on_click=lambda args: print('clicked!', args))
# clicked! {'arguments': 'http:', 'user_input': {}}
```

#### Logo

```python
from win11toast import toast

toast('Hello', 'Hello from Python', logo='https://unsplash.it/64?image=669')
```

![image](https://user-images.githubusercontent.com/12811398/183359855-aa0a8d39-8249-4055-82cb-5968ab35e125.png)

#### Image

```python
from win11toast import toast

toast('Hello', 'Hello from Python', image='https://4.bp.blogspot.com/-u-uyq3FEqeY/UkJLl773BHI/AAAAAAAAYPQ/7bY05EeF1oI/s800/cooking_toaster.png')
```

![image](https://user-images.githubusercontent.com/12811398/183360063-36caef94-bb3e-4eef-ac15-d5d6c86e5d40.png)

#### Audio

```python
from win11toast import toast

toast('Hello', 'Hello from Python', audio='ms-winsoundevent:Notification.Looping.Alarm')
```

Available audio
https://docs.microsoft.com/en-us/uwp/schemas/tiles/toastschema/element-audio

#### Button

```python
from win11toast import toast

toast('Hello', 'Hello from Python', actions=['Dismiss'])
# {'arguments': 'dismiss', 'user_input': {}}
```

![image](https://user-images.githubusercontent.com/12811398/183361855-1269d017-5354-41db-9613-20ad2f22447a.png)

```python
from win11toast import toast

toast('Hello', 'Click a button', actions=['Approve', 'Dismiss', 'Other'])
```

![image](https://user-images.githubusercontent.com/12811398/183363035-af9e13cc-9bb1-4e25-90b3-9f6c1c00b3dd.png)

#### Input

```python
from win11toast import toast

toast('Hello', 'Type anything', inputs=['textbox'], actions=['Send'])
# {'arguments': 'dismiss', 'user_input': {'textbox': 'Hi there'}}
```

![image](https://user-images.githubusercontent.com/12811398/183361532-b554b9ae-e426-4fb1-8080-cc7c52d499d7.png)


#### Selection

```python
from win11toast import toast

toast('Hello', 'Which do you like?', selections=['Apple', 'Banana', 'Grape'], actions=['Submit'])
# {'arguments': 'dismiss', 'user_input': {'selection': 'Grape'}}
```

![image](https://user-images.githubusercontent.com/12811398/183361008-4cdd9445-683c-432e-8094-1c2193e959db.png)

![image](https://user-images.githubusercontent.com/12811398/183361138-2b81e8aa-bcbf-4764-a396-b7787518904b.png)

#### No arguments

```python
from win11toast import toast

toast()
```

![image](https://user-images.githubusercontent.com/12811398/183362441-8d865a74-f930-4c16-9757-22244d22a8e2.png)

#### Wrap text

```python
from win11toast import toast

toast('Hello', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Earum accusantium porro numquam aspernatur voluptates cum, odio in, animi nihil cupiditate molestias laborum. Consequatur exercitationem modi vitae. In voluptates quia obcaecati!')
```

![image](https://user-images.githubusercontent.com/12811398/183363789-e5a9c2bb-adf8-438d-9ebb-1e7693971a16.png)

### Jupyter

```python
from win11toast import toast_async

await toast_async('Hello Python', 'Click to open url', on_click='https://www.python.org')
```

![image](https://user-images.githubusercontent.com/12811398/183295534-82b0a6d1-8fa6-4ddc-bfb0-5021158b3cb0.png)

## Debug

[Notifications Visualizer](https://www.microsoft.com/store/apps/notifications-visualizer/9nblggh5xsl1)
![image](https://user-images.githubusercontent.com/12811398/183335533-33562c5c-d467-4acf-92a4-5e8f6ef05e1f.png)


# Acknowledgements

- [winsdk_toast](https://github.com/Mo-Dabao/winsdk_toast)
- [Windows-Toasts](https://github.com/DatGuy1/Windows-Toasts)
- [MarcAlx/notification.py](https://gist.github.com/MarcAlx/443358d5e7167864679ffa1b7d51cd06)
