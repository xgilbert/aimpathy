from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    README = readme_file.read()

with open("HISTORY.md", "r") as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name="aimpathy",
    version="0.1.1",
    author="Xavier Gilbert",
    author_email="",
    description="Basic NER using spaCy to parse abbreviated notes into structured data.",
    long_description=README + "\n\n" + HISTORY,
    long_description_content_type="text/mardown",
    license="MIT",
    # url="https://github.com/xgilbert/aimpathy",
    packages=find_packages(),
    keywords=["NER", "spaCy"],
    python_requires=">=3.8",
)

install_requires = [
    "spacy>=3.0.0"
]

if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires)