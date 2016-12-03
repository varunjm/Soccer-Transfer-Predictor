# Player-Transfer-Predictor

## Team members:

1. Aditya Bhardwaj
2. Satvik Shetty
3. Varun Jayathirtha

## Installation

The following python packages are needed:

* sqlite3
* pandas
* sklearn
  - manifold  
  - preprocessing  
  - cluster  
  - cluster  
* bokeh
  - plotting  
  - models  
* numpy  
* scipy  
* pylab  
* matplotlib.pyplot 

## Usage

* The repository includes meta data which is saved as .pkl files and utilized by the programs.
* To recalculate the meta data, place [this](https://drive.google.com/open?id=0BwgwzoTRFneJZHFhbF83b3NHVDA) dataset in the same directory. Execute the following programs in order.
  - [generate_DT_classifier.py](https://github.ncsu.edu/vjayath/Player-Transfer-Predictor/blob/master/generate_DT_classifier.py)
  - [fetch_teams_data.py](https://github.ncsu.edu/vjayath/Player-Transfer-Predictor/blob/master/fetch_teams_data.py)
* The main program is [Predict_transfers.py](https://github.ncsu.edu/vjayath/Player-Transfer-Predictor/blob/master/Predict_transfers.py)

    ``` python Predict_transfers.py ```
