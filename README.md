# B-SERS: Books Search Engine and Recommendation System
![home](https://raw.githubusercontent.com/kevin-wijaya/resources/main/images/books-search-engine-and-recommendation-system/home.png)

## Table of Contents
+ [About](#about)
+ [Tech Stack](#techstack)
+ [Getting Started](#getting_started)
+ [Usage](#usage)
+ [Screenshots](#screenshots)
+ [Author](#author)

## About <a name = "about"></a>

<b>B-SERS: Books Search Engine and Recommendation System</b>. This system combines the functionalities of a search engine and a recommendation system to effectively address the challenges of finding and suggesting books. By leveraging advanced algorithms and indexing techniques, B-SERS allows users to perform detailed searches across a large database of books.

The search engine uses the BM25 Okapi method for ranking, ensuring highly relevant search results. The recommendation system employs a <b>multi-features weighting content-based recommendation</b> method, specifically applied to the title and description of the books.

The dataset used for B-SERS comes from <a href="https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset" target="_blank">Kaggle</a>. To complete the book details, I utilized ISBN data to scrape book descriptions from Amazon. In about a week, I successfully <b>scraped descriptions for 79,436 books</b> using a server that ran 24 hours a day.

## Tech Stack <a name = "techstack"></a>

- Web Application: JQuery, Tailwind CSS, Axios, Webpack
- Experiment: Poetry, Numpy, Pandas, Scikit-learn, rank_bm25

## Getting Started <a name = "getting_started"></a>

These instructions will guide you through installing the project on your local machine for testing purposes. There are two methods of installation, with docker or manually using Linux and macOS commands.

### Requirements

This project requires Python 3.10.


### Installation (Docker)

Clone this repository
``` sh
git clone https://github.com/kevin-wijaya/Books-Search-Engine-and-Recommendation-System.git
```

Change the directory to the `cloned repository`
``` sh
cd Books-Search-Engine-and-Recommendation-System/
```

Run docker compose
``` sh
docker compose up --build
```

Open your web browser and go to the following URL
``` python
# http://localhost:5500
```

### Installation (Linux or MacOS)

Clone this repository
``` sh
git clone https://github.com/kevin-wijaya/Books-Search-Engine-and-Recommendation-System.git
```

Change the directory to the cloned repository and then navigate to the `server` directory
``` sh
cd Books-Search-Engine-and-Recommendation-System/server/
```

Initialize the python environment to ensure isolation
``` sh
python -m venv .venv
```

Activate the python environment
``` sh
source .venv/bin/activate
```

Install prerequisite python packages
``` sh
 pip install --no-cache-dir -r requirements.txt
```

Run the uvicorn server
``` sh
sh -c "uvicorn run:app --reload --port=8001 --host=0.0.0.0
```

Open new terminal and change the directory to the cloned repository and then navigate to the `client` directory
``` sh
# replace the /path/to/your/ with the path where your cloned repository is located
cd /path/to/your/Books-Search-Engine-and-Recommendation-System/client/
```

Change the directory to the production folder
``` sh
cd .dist/
```

Run the Python HTTP server
``` sh
python -m http.server 5500
```

Open your web browser and go to the following URL
``` python
# http://localhost:5500
```

## Usage <a name = "usage"></a>

To use this web application is easy, follow these 3 steps:

1. **Insert Text**: Enter your text into the search field.
2. **Search**: Press Enter or click the search icon to process the query. The system will then provide recommendations.
3. **Adjust Weight Parameters**: Optionally, adjust the weights for the title or description parameters to see different results.

## Screenshots <a name = "screenshots"></a>

Here are some screenshots of the application:

![test#1](https://raw.githubusercontent.com/kevin-wijaya/resources/main/images/books-search-engine-and-recommendation-system/test%20%231.png)

![params#1](https://raw.githubusercontent.com/kevin-wijaya/resources/main/images/books-search-engine-and-recommendation-system/params%20%231.png)

![params#2](https://raw.githubusercontent.com/kevin-wijaya/resources/main/images/books-search-engine-and-recommendation-system/params%20%232.png)

![test#2](https://raw.githubusercontent.com/kevin-wijaya/resources/main/images/books-search-engine-and-recommendation-system/test%20%232.png)

![test#3](https://raw.githubusercontent.com/kevin-wijaya/resources/main/images/books-search-engine-and-recommendation-system/test%20%233.png)

![test#4](https://raw.githubusercontent.com/kevin-wijaya/resources/main/images/books-search-engine-and-recommendation-system/test%20%234.png)

![detail](https://raw.githubusercontent.com/kevin-wijaya/resources/main/images/books-search-engine-and-recommendation-system/detail.png)

![about](https://raw.githubusercontent.com/kevin-wijaya/resources/main/images/books-search-engine-and-recommendation-system/about.png)

## Author <a name = "author"></a>
- **Kevin Wijaya** 