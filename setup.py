from setuptools import setup, find_packages

setup(
    name="codest",
    version="0.1.4",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=[
        "pyperclip>=1.8.0",
    ],
    entry_points={
        'console_scripts': [
            'codest=codest.__main__:run',
        ],
    },
)