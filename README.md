# Word2Vec AI Search Engine

This search engine is dedicated to IMDb's local database which was downloaded using IMDbPY. It uses the Word2Vec model to determine words similar to input. These input data are entered on a website, which was built using Django.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

None, project is fully portable, unless you want your own DB - then you have to built it like our sample **dataset.csv**

### Installing

None, project is fully portable.

### Running

* Run **run.bat** file located in **searchengine** folder
* Open your browser
* Go to [Search](http://localhost:8000/search)
* Type something in search field
* Wait for search results

## Deployment

Standard Django deployment.

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [IMDb Dataset](https://www.imdb.com/interfaces/) - Dataset shared by IMDb
* [IMDbPY](https://imdbpy.sourceforge.io/) - Used to download more info using IMDb Dataset
* [Word2Vec](https://radimrehurek.com/gensim/models/word2vec.html) - Used to model and train data a neural network

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is an university project, it is free to use it without any consequences.
Remember about licences of **Build With** modules.

### IMDb
Information courtesy of [IMDb](http://www.imdb.com).
Used with permission.