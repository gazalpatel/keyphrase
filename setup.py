from setuptools import setup, find_packages

with open("README.md", mode="r", encoding="utf-8") as readme_file:
    readme = readme_file.read()



setup(
    name="top_ai",
    version="0.2021.7.1",
    author="Gazal Patel",
    author_email="gpatel@phigrc.com",
    description="Text processing and topic extraction library.",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    url="https://gazalpatel.wordpress.com/",
    download_url="https://github.com/gazalpatel/topic_ai/archive/refs/heads/main.zip",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'scipy',
        'nltk',
        'scipy',
        'unidecode',
        'contractions',
        'word2number',
        'bs4',
        'spacy'
    ],
    classifiers=[
        "Development Status :: Work in profress",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7.4",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    keywords="Topic modeling keyphrases text processing Transformer Networks BERT XLNet sentence embedding PyTorch NLP deep learning"
)
