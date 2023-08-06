from setuptools import find_packages, setup

setup(
    name='bert-classifier',
    packages=find_packages(where='src.bert_classifier'),
    package_dir={'': 'src'},
    version='0.1.1',
    description='Bert based NLP classification models',
    author='ming_gao@outlook.com',
    license='MIT',
    install_requires=[
        'torch',
        'transformers',
    ]
)