<h1 align="center">6<sup>th</sup> Foundational Climate Prediction Training Workshop for ICPAC Member States Forecasters ICPAC</h1>
<h2 align="center">13<sup>th</sup> to 24<sup>th</sup> November 2023, ICPAC, Nairobi, Kenya</h2>

### Python Introduction  On 11:00-13:00, 16th November 2023:

## Agenda:
* Introduction to Python
* Introduction to ChatGPT for learning Python
* Climate data analysis with Python Modifying and selecting variables using xarray 
* Setting up a map with cartopy, plotting contour and filled contour
* Plotting wind vector, overlaying with cartopy

## Hands on

* To login to the computer with Jupyter enabled, open the port with desired number 8888 in seperate terminal
```
ssh -NL 8888:localhost:8888 country@168.168.168.168
```

* In another terminal, ssh into the machine by 
```
ssh -X country@168.168.168.168
```

* To start Jupyter notebook
```
git clone https://github.com/icpac-igad/python-workshop.git
conda activate pycpt_env
cd python-workshop
jupyter notebook --no-browser --port=8888
```

* To access the Jupyter notebook from your computer, in firefox/Chromium borwser, type ```http://localhost:8888```


