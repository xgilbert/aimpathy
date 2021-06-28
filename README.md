# Problem

* Turn abbreviated notes (unstructured data) to structured data  
* Plain text (string) into json/dictionary  
* NER  


# Model

* NER model  
* spaCy  
  * spaCy NER already supports the entity types like `PERSON`, `DATE`, etc. Limitations are that is lack of case specific tags necessary to solve the problem (e.g. type of contact, identification of project name)  
  * custom: trained model on synthetic data (`./data/training.txt`), following a [BIO](https://natural-language-understanding.fandom.com/wiki/Named_entity_recognition) type tagging  


# Requirements

Although the application can be installed locally, it is setup to run on Docker. If you want to run the application outside of Docker, make sure to install spaCy (>=3.0) and flask.  

```
DATA_PATH = "../data"
MODEL_PATH = "../model"
```


# Install (Unix)

```
cd ~/my/install/directory

git clone https://github.com/xgilbert/aimpathy.git

cd aimpathy

# make sure your Docker daemon is running
docker build -t aimpathy-api .
```

# Run

```
# start the application
docker run -d -p 5000:5000 aimpathy-api
```

Once the container is running, the app should be accessible from your web browser at `http://127.0.0.1:5000`.  


# Training the model

* The repository contains training data as well as a pre-trained model in `./model/model.pickle`  
* To retrain the model (e.g. add new notes)  
  *  edit `./data/training.txt` (tsv) file following BIO tagging  
  *  rebuild the container  
  *  access endpoint `http://127.0.0.1:5000/api/v1/train`  
* Tags  
  * ContType : contact type (phone, call, email, mail, meet, ...)  
  * ProjName : project name


# Testing

A basic test is implemented in the API to check that spaCy has been loaded correctly and that the control string has been parsed correctly

```
http://127.0.0.1:5000/api/v1/test
```

output

```json
{
  "status":"spacy and en_core_web_sm loaded successfully",
  "test":"passed"
}
```

> This is a simple test, not a production unit test. The aim of this test is a simple indication that everything is running correctly.

The test, based on dictionary equality, checks that the string  

```
Jan 21: mail John S about signing them up for phase 3 of project Beta.  
```

is parsed into  

```json
{
    "contact_name": "John S",
    "contact_type": "mail",
    "date": "Jan 21",
    "project": "Beta"
}
```


# Usage

In your web browser, paste the url below  

```
http://127.0.0.1:5000/api/v1/note?note="Jan 21: mail John S about signing them up for phase 3 of project Beta."
```

Expected output  

```json
{
  "contact_name":"John S",
  "contact_type":"mail",
  "date":"Jan 21",
  "project":"Beta"
}
```


# Limitations

* Non capitalized month will result into missing date. E.g. `march 13 mail John S ...` will not return a `DATE`.  
* Non capitalized names will not return a `PERSON`.  


# Necessary improvements

* Deal with capitalization  
* Test performance of custom tagging of `DATE` and `PERSON` in traning data as opposed to relying on spaCy off-the-shelf capabilities  
* Test/compare alternative models (BERT?)  
* Test `datefinder` for dates  
* Add unit tests for `aimpathy` (lib) & API testing  
* Enrich training dataset (more notes, more cases)  


# Time split

* research + build training data : ~ 1h
* model : ~1h
* api : ~1h
* packaging + docker : ~ 1h
* documentation : ~ .5h
* testing : ~ .5h

* total time : ~5h