from pathlib import Path

from setuptools import setup

setup(
    name='django-suit-v2-pm',
    version=__import__('suit').VERSION,
    description='Modern theme for Django admin interface.',
    long_description=(Path(__file__).parent / 'README.rst').read_text(encoding='utf-8'),
    long_description_content_type='text/x-rst',
    url='https://github.com/pulse-mind/django-suit',
    author='Kaspars Sprogis (darklow) forked by Pulse-Mind',
    author_email='pulse.mind.com@gmail.com',
    packages=['suit', 'suit.templatetags'],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 5.2',
        'License :: Free for non-commercial use',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Environment :: Web Environment',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ],
    python_requires='>=3.10',                # Minimum version requirement of the package
    install_requires=['Django>=5.2,<6.0'],
)
