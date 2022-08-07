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

use callback
```python
from win11toast import toast

toast('Hello Python', 'Click to open url', on_click=lambda args: print('clicked!', args))
# clicked! C:\Windows\Media\Alarm01.wav
```

### Jupyter

```python
from win11toast import toast_async

await toast_async('Hello Python', 'Click to open url', on_click='https://www.python.org')
```

![image](https://user-images.githubusercontent.com/12811398/183295534-82b0a6d1-8fa6-4ddc-bfb0-5021158b3cb0.png)

## Debug

[Notifications Visualizer](ms-windows-store://pdp/?ProductId=9NBLGGH5XSL1)

# Acknowledgements

- [winsdk_toast](https://github.com/Mo-Dabao/winsdk_toast)
- [Windows-Toasts](https://github.com/DatGuy1/Windows-Toasts)
- [MarcAlx/notification.py](https://gist.github.com/MarcAlx/443358d5e7167864679ffa1b7d51cd06)
