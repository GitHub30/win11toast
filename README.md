[![Python](https://img.shields.io/pypi/pyversions/win11toast.svg)](https://badge.fury.io/py/win11toast)
[![PyPI](https://badge.fury.io/py/win11toast.svg)](https://badge.fury.io/py/win11toast)

# win11toast
Toast notifications for Windows 10 and 11

![image](https://user-images.githubusercontent.com/12811398/183295421-59686d68-bfb2-4d9d-ad61-afc8bd4e4808.png)

## Installation

```bash
pip install win11toast
```

## Usage

```python
from win11toast import toast

toast('Hello Python', 'Click to open url', on_click='https://www.python.org')
```

### Jupyter

```python
from win11toast import toast_async

await toast_async('Hello Python', 'Click to open url', on_click='https://www.python.org')
```

![image](https://user-images.githubusercontent.com/12811398/183295534-82b0a6d1-8fa6-4ddc-bfb0-5021158b3cb0.png)
