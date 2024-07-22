<h1 align="center">SEWAA TRAINING ON EVALUATION OF THE CGAN and WRF Models ICPAC Headquarters, Ngong, Kenya
22- 26 July 2024</h1>
<h2 align="center">22<sup>nd</sup> to 26<sup>th</sup> July 2024, ICPAC, Nairobi, Kenya</h2>

### Python Introduction  On 11:00-13:00, 16th November 2023:

## Agenda:
* Introduction to Python
* Introduction to ChatGPT for learning Python
* Climate data analysis with Python Modifying and selecting variables using xarray 
* Setting up a map with cartopy, plotting contour and filled contour
* Plotting wind vector, overlaying with cartopy

## Hands on

* The workshop dataset is stored in the google drive link [https://drive.google.com/file/d/1Dad7mUn4CLVRUjOtCZ1JBOm_Knwf_sCx/view](https://drive.google.com/file/d/1Dad7mUn4CLVRUjOtCZ1JBOm_Knwf_sCx/view)

* To login to the computer with Jupyter enabled, open the port with desired number between 6000-8888 in seperate terminal
```
ssh -NL 8888:localhost:8888 country@168.168.168.168
```

* In another terminal, ssh into the machine by 
```
ssh -X country@168.168.168.168
```
* to setup an python environment, micromamba is an options,  
https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html

```
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)
micromamba self-update
micromamba activate base
micromamba install python pip -c conda-forge
micromamba install -c conda-forge xarray zarr 

```

* To start Jupyter notebook
```
git clone https://github.com/icpac-igad/python-workshop.git
conda activate pycpt_env
cd python-workshop
jupyter notebook --no-browser --port=8888
```

* To access the Jupyter notebook from your computer, in firefox/Chromium borwser, type ```http://localhost:8888```


