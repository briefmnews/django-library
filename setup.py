from setuptools import setup

from django_library import __version__

setup(
    name="django-library",
    version=__version__,
    description="Handle login and ticket validation for french library connectors (Archimed, GMInvent and C3RB)",
    url="https://github.com/briefmnews/django-library",
    author="Brief.me",
    author_email="tech@brief.me",
    license="MIT",
    packages=["django_library", "django_library.migrations"],
    python_requires=">=3.7",
    install_requires=[
        "Django>=3.2",
        "python-cas>=1.4.0",
        "lxml>=4.6",
        "requests>=2.19.1",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data=True,
    zip_safe=False,
)
