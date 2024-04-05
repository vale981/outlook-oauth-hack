from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
  name='o365-authenticator',
  version='0.1.0',
  install_requires=install_requires,
  py_modules = [ 'config.py' ],
  scripts=[
    'get_token.py',
    'refresh_token.py'
  ],
)
