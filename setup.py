import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name='cs-battleground',
    version='0.0.1',
    author='Eduard Konanau & Dzmitry Zavaliony',
    author_email='aduard.kononov@gmail.com',
    description='CoppeliaSim based robot battleground',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/ekon-university/8_sem_labs/pis/battleground',
    packages=setuptools.find_packages(),
    package_data={
        'cs_battleground.remote_api': [
            'bin/*.so',
            'bin/*.dll',
        ],
        'cs_battleground.cli': [
            'template_dir/**',
            'template_dir/wrappers/**',
        ],
        'cs_battleground': [
            'arena_files/coppelia/battleground.ttt',
            'arena_files/coppelia/robot.ttm',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=required,
    entry_points={
        'console_scripts': [
            'cs-battleground=cs_battleground.cli.__main__:main',
        ],
    },
)
