from setuptools import find_packages, setup

setup(
    name='hedge_charts',
    version='0.1.0',
    author='Joel Brass',
    author_email='joel@jbrass.com',
    description='A package to generate stock charts',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hedge-design/hedge_charts',
    packages=find_packages(),
    install_requires=[
        'alpaca-py',
        'plotly',
        'kaleido',
        'python-dotenv'
    ],
    python_requires='>=3.7',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
