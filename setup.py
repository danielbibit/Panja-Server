from setuptools import setup, find_packages

install_requires = [
    'sqlalchemy>=1.1.13',
    'passlib>=1.7.1'
]

setup(name='panja',
      version='0.0.1',
      description='Home automation server',
      author='Daniel Moraes dos Santos',
      author_email='danielbibit@gmail.com',
      url='https://github.com/danielbibit/Panja-Server',
      license='GNU General Public License v3.0',
      packages=find_packages(),
      entry_points={
            'console_scripts': [
                  'panja = panja.__main__:main'
            ]
      },
      keywords=['automation', 'home automation', 'smart home']
     )
