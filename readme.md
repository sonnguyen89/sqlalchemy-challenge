Advanced SQL Challenge Repository

This repository contains 1 JUPYTER lab note and 1 python file.
they are using Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. 
Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib

## Table of Contents

- [Overview](#overview)
- [Usage](#usage)
- [Scripts](#scripts)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

* Design a query to calculate the total number of stations in the dataset.
* Design a query to find the most-active stations (that is, the stations that have the most rows).
* Design a query to get the previous 12 months of temperature observation (TOBS) data.
* design a Flask API based on the queries

## Usage

To run the Jupyter Note lab, follow these general steps:

1. Open Jupyterlab.
2. open the file climate_starter.ipynb and review each queries and result

To run the python file, follow these general steps:

1. Open terminal.
2. execute  the file app.py by enter "python app.py" to run the API system
3. open your web browser and you can enter following these urls:
* http://127.0.0.1:5000/
* http://127.0.0.1:5000/api/v1.0/precipitation
* http://127.0.0.1:5000/api/v1.0/stations
* http://127.0.0.1:5000/api/v1.0/tobs
* http://127.0.0.1:5000/api/v1.0/<start_date> (for example: http://127.0.0.1:5000/api/v1.0/2014-09-25)
* http://127.0.0.1:5000/api/v1.0/<start_date>/<end_date> (for example: http://127.0.0.1:5000/api/v1.0/2014-08-15/2014-09-25)
    

## Scripts

Feel free to explore and modify these files to suit your specific needs.

## Contributing

Contributions to this repository are welcome! If you have any useful SQL queries or improvements to existing ones, please feel free to submit a pull request.

Before contributing, please ensure that your code adheres to the repository's coding standards and practices.

## License

This repository is licensed under the [MIT License](LICENSE).

## Contact

If you have any questions, suggestions, or concerns regarding this repository, please don't hesitate to contact the repository owner:

- Email: [nam_son14@yahoo.com](mailto:nam_son14@yahoo.com
- GitHub: [songuyen89](https://github.com/sonnguyen89)