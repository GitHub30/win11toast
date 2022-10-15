from setuptools import setup

setup(
    name='win11toast',
    version='0.30',
    description='Toast notifications for Windows 10 and 11',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/GitHub30/win11toast',
    project_urls={ 'Bug Tracker': 'https://github.com/GitHub30/win11toast/issues' },
    author='Tomofumi Inoue',
    author_email='funaox@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        "Topic :: Utilities",
        'Operating System :: Microsoft',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11'
    ],
    install_requires=['winsdk'],
    py_modules=['win11toast']
)

# Publish commands
# https://packaging.python.org/tutorials/packaging-projects/
#pip install --upgrade pip build twine
#python -m build
#python -m twine upload dist/*
