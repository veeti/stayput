from setuptools import setup, find_packages

requires = [
]

test_requires = [
]

setup(
    name='stayput',
    version='0.1.0',
    description="Static site generator",
    license='MIT',

    packages=find_packages(),
    test_suite='stayput.tests',

    install_requires=requires,
    tests_require=test_requires,

    entry_points={
        'console_scripts': [
            "stayput = stayput.cli:main",
        ]
    }
)
