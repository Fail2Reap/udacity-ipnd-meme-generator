# Meme Generator

<img src="https://i.gyazo.com/01038e6756a97109aec83842cc233f44.gif"/>

## Table of Contents
* [Project Overview](#project-overview)
    * [Directory Structure](#directory-structure)
    * [Modules](#modules)<br>
        * [MemeGenerator](#memegenerator)
        * [QuoteEngine](#quoteengine)
* [Getting Started](#getting-started)
    * [Overview of Key Dependencies](#overview-of-key-dependencies)
    * [Installing Dependencies](#installing-dependencies)
    * [Configuring Environment Variables](#configuring-environment-variables)
    * [Running the Flask Web App](#running-the-flask-web-app)
    * [Using the Command Line Tool](#using-the-command-line-tool)

## Project Overview
The Meme Generator is a small Flask web app that generates memes based on images and quotes provided. It also lets you generate a new meme by providing a URL for an image, a quote body and a quote author. Additionally, it comes with a command line tool to generate memes. This project was completed as part of the Udacity Intermediate Python Nanodegree.

### Directory Structure

```
.
├── __init__.py
├── app.py                      (Flask App)
├── main.py                     (Command Line Tool)
├── README.md
├── requirements.txt
├── MemeGenerator               (Module for generating memes)
│   ├── __init__.py
│   └── meme_engine.py
├── QuoteEngine                 (Module for ingesting quotes from files of various types)
│   ├── __init__.py
│   ├── Ingestor.py
│   ├── ingestor_interface.py
│   ├── Ingestors
│   │   ├── __init__.py
│   │   ├── csv_ingestor.py
│   │   ├── docx_ingestor.py
│   │   ├── pdf_ingestor.py
│   │   └── txt_ingestor.py
│   └── Models
│       ├── __init__.py
│       └── quote_model.py
├── static                      (Static content served by Flask)
│   ├── DogQuotes
│   │   ├── DogQuotesCSV.csv
│   │   ├── DogQuotesDOCX.docx
│   │   ├── DogQuotesPDF.pdf
│   │   └── DogQuotesTXT.txt
│   ├── SimpleLines
│   │   ├── SimpleLines.csv
│   │   ├── SimpleLines.docx
│   │   ├── SimpleLines.pdf
│   │   └── SimpleLines.txt
│   ├── fonts
│   │   └── OpenSans-Light.ttf
│   ├── images
│   │   └── no_meme.png         (Default image loaded if no other images exists yet)
│   └── photos
│       └── dog
│           ├── xander_1.jpg
│           ├── xander_2.jpg
│           ├── xander_3.jpg
│           └── xander_4.jpg
└── templates                   (HTML templates served by Flask)
    ├── base.html
    ├── meme.html
    └── meme_form.html
```

### Modules
#### MemeGenerator
This module exposes the MemeEngine class and its functions.

##### **Dependencies**
* [Pillow](https://pillow.readthedocs.io/en/stable/index.html) is a Python Imaging Library that adds image processing capabilities to your Python interpreter. This project uses it to manipulate and work with images to generate memes.

##### **Functions**
* [make_meme](./MemeGenerator/meme_engine.py#L28) function takes an instance of the [MemeEngine](./MemeGenerator/meme_engine.py#L8) class, an image source path, a quote body, a quote author and an optional width to resize the meme to. It then manipulates the image and adds the quote body and author to the image in the format of `"quote_body" - quote_author`. It then returns a file path to the saved meme.<br><br>
    Method signature:
    ```python
    make_meme(self, img_path: str, quote: str, author: str, width: int = 500) -> str
    ```

#### QuoteEngine
This module exposes:
* The generic [Ingestor](./QuoteEngine/Ingestor.py) class and associated functions.
* The specific file type ingestors and their functions under a nested [Ingestors](./QuoteEngine/Ingestors/__init__.py) module.
* The [QuoteModel](./QuoteEngine/Models/quote_model.py) class that encapsulates quote data.

Example imports:
```python
from QuoteEngine import Ingestor
from QuoteEngine.Ingestors import DocxIngestor
from QuoteEngine.Ingestors import TextIngestor
from QuoteEngine.Ingestors import PDFIngestor
from QuoteEngine.Ingestors import CSVIngestor
from QuoteEngine.Models import QuoteModel
```

##### **Dependencies**
* [pandas](https://pandas.pydata.org/) is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language. This project uses it to parse data from .csv files.

* [python-docx](https://python-docx.readthedocs.io/en/latest/) is a Python library for creating and updating Microsoft Word (.docx) files. This project uses it to parse data from .docx files.

* [XpdfReader](https://www.xpdfreader.com/index.html) is a free PDF viewer and toolkit, including a text extractor, image converter, HTML converter, and more. This project uses `pdftotext` that is part of the XpdfReader command line tools to parse data from .pdf files.


##### **Functions**
* [can_ingest](./QuoteEngine/ingestor_interface.py#L12) function takes an instance of the class and a file path as input. It attempts to determine whether we have an ingestor that can handle the file type which was passed. This function is only implemented at the Interface layer which all inheriting classes also have access to.<br><br>
    Method signature:
    ```python
    can_ingest(cls, path: str) -> bool
    ```

* [parse](./QuoteEngine/Ingestor.py#L25) function takes a file path as input, attempts to parse its contents and returns a List of QuoteModel's for consumption.<br><br>
    Method signature:
    ```python
    parse(cls, path: str) -> List[QuoteModel]
    ```

    >*note: The generic Ingestor and all specific file ingestors implement the [parse()]([IngestorInterface](./QuoteEngine/ingestor_interface.py#L25)) method of the [IngestorInterface](./QuoteEngine/ingestor_interface.py#L7) class.*


##### **Adding ingestors for other file types**
By default, the file types .docx, .txt, .pdf and .csv are supported. However, you may require quotes to be loaded from other types of files. To do so, simply follow the steps below:

1. Create a new file e.g. `my_new_ingestor` and place it in the [Ingestors](./QuoteEngine/Ingestors) directory.
2. Within the file:
    * Import the [IngestorInterface](./QuoteEngine/ingestor_interface.py#L7) and [QuoteModel](./QuoteEngine/Models/quote_model.py) classes.
    * Create a class for your new ingestor e.g. `MyNewIngestorClass` and ensure it inherits from the [IngestorInterface](./QuoteEngine/ingestor_interface.py#L7) class.
    * You will also need to ensure that your class implements any additional functions.<br><br>

    Your starter class code should now look something like this:

    ```python
    from typing import List

    from QuoteEngine.ingestor_interface import IngestorInterface
    from QuoteEngine.Models import QuoteModel

    # TODO: Add any additional packages you require for file ingestion

    class MyNewIngestorClass(IngestorInterface):
        """Subclass for ingesting csv files."""
        # TODO: Add the file extensions you anticipate ingesting with
        # this new class
        allowed_extensions = ['my_new_file_extension']

        @classmethod
        def parse(cls, path: str) -> List[QuoteModel]:
            """Method for parsing ingested file.

            Args:
                path (str): Path to the file to ingest.
            """
            # TODO: Ingest your file and create a list of QuoteModel's
            # to return
            return [QuoteModel("body", "author")]
    ```
3. Finally, import your new ingestor class in the Ingestors [\_\_init\_\_.py](./QuoteEngine/Ingestors/__init__.py) file as shown below:
    ```python
    from QuoteEngine.Ingestors.my_new_ingestor import MyNewIngestorClass
    ```
Your new class will also automatically become available for the generic Ingestor without any additional steps.


## Getting Started

### Overview of Key Dependencies
Here we have a quick overview of the key dependencies used in the creation of this web app project.
* [Python](https://www.python.org/) is a programming language that lets you work quickly and integrate systems more effectively.

* [Flask](https://flask.palletsprojects.com/en/2.0.x/) is a lightweight backend microservices framework for Python. Flask is required to handle requests and responses.

* [Pillow](https://pillow.readthedocs.io/en/stable/index.html) is a Python Imaging Library that adds image processing capabilities to your Python interpreter. This project uses it to manipulate and work with images to generate memes.

* [pandas](https://pandas.pydata.org/) is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language. This project uses it to parse data from .csv files.

* [python-docx](https://python-docx.readthedocs.io/en/latest/) is a Python library for creating and updating Microsoft Word (.docx) files. This project uses it to parse data from .docx files.

* [XpdfReader](https://www.xpdfreader.com/index.html) is a free PDF viewer and toolkit, including a text extractor, image converter, HTML converter, and more. This project uses `pdftotext` that is part of the XpdfReader command line tools to parse data from .pdf files.


### Installing Dependencies
Before we can run our Flask app, we need to ensure our environment is set up correctly.
1. **Python 3.9**<br>
    Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

2. **XpdfReader**<br>
    Next, we will install `XpdfReader` command line tools from the [XpdfReader](https://www.pdfreader.com/download.html) homepage.
    >*note:* Since there is no installer for the command line tools, you will need to extract them to a local directory and then ensure you add this directory to your systems PATH so that the tools are discoverable. Here you can find steps for [Windows](https://www.c-sharpcorner.com/article/add-a-directory-to-path-environment-variable-in-windows-10/) and [Ubuntu](https://opensource.com/article/17/6/set-path-linux).

3. **Virtual Environment**<br>
    It's recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/). [Conda](https://docs.conda.io/en/latest/) is another great alternative for managing virtual environments.

4. **Project Dependencies**<br>
    Once you have your virtual environment setup and running, install the required ependencies by naviging to the project root directory and running:
    ```bash
    pip install -r requirements.txt;
    ```
    This will install all of the required packages within the [requirements.txt](./requirements.txt) file including our key dependencies.


### Configuring Environment Variables
Once dependencies have been installed, we need to configure environment variables for our Flask app.

This can be done using the commands below:

```bash
export FLASK_APP=app;
export FLASK_ENV=development;
```
Through the `FLASK_APP` variable we are instructing `Flask` to start the app [app.py](./app.py).

Additionally we are setting the `FLASK_ENV` variable to indicate that the app should be started in development mode. More info on this can be found under [Environment and Debug Features](https://flask.palletsprojects.com/en/2.0.x/config/#environment-and-debug-features) in the Flask documentation.


### Running the Flask Web App
To run the app, navigate to the root directory and run:
```bash
flask run;
```
The web app will be available under [http://localhost:5000](http://localhost:5000) by default.
>*note:* Ensure the virtual environment you created earlier is currently active or dependency errors may occur.


### Using the Command Line Tool
This project also comes with a command line tool that generates a meme based on input provided.

Example Usage:
```bash
python3 main.py -p "/tmp/my_super_awesome_source_meme.png" -a "Mooncake" -b "Chookity"
```

Example Output:
```bash
/project/udacity-ipnd-meme-generator/tmp/meme-0xq1p0bj.png
```


Help Output:<br>
```
usage: main.py [-h] [-p PATH] [-b BODY] [-a AUTHOR]

Generates a meme and prints its file path.

optional arguments:
-h, --help                  show this help message and exit
-p PATH, --path PATH        file path of a specific image or folder path where one or more mages are stored
-b BODY, --body BODY        quote body to draw on the image
-a AUTHOR, --author AUTHOR  quote author to draw on the image
```
