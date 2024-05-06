# TunnelTrafficCongestion


This repository belongs to the thesis that I did for my masters in Data Science at University of Stavanger
Supervisors: Associate Professor Naeem Khademi and Associate Professor Erlend Tøssebro
Spring 2024

Dependencies that must be installed before running the notebooks:
1. nvdbapi-v3. https://github.com/LtGlahn/nvdbapi-V3 Can be installed using pip install nvdbapi-v3. This repository has Copyright (c) 2020 Jan Kristian Jensen. 
2. Tensorflow. https://www.tensorflow.org/install 
3. Pandas, Numpy (recommended: Anaconda) https://www.anaconda.com/download 
4. Shapely https://pypi.org/project/shapely/ 

How to run: 
Download all the files to your local environment
- If you want to run the RNN model, plrease run the notebook called run_model.ipynb. This uses the .csv files in the folder 'data'.
- If you want to fetch the data for tunnels and registration points, please run the notebook called Get_tunnel_data.ipynb. This saved the output into Tunnels_with_points_data/tunnels_with_points.csv

The next step is not necessary to see results. The files necessary are already provided. 
- The output from the previous step is then added to the directory the QGIS is working in, and run the given files to visualize. The Get_category_of_tunnels.py will create a processed version of tunnel_with_points_processed.csv. (In the .qgz project file, change the directory adresses to your)


This repository includes the following folders: 

Data:
This folders includes the .csv files that the model is trained on. The files are downloaded from Trafikkdata Web interface at https://trafikkdata.atlas.vegvesen.no/#/eksport. The files are processed in Microsoft Excel, where the unnecessary columns are removed, traffic for only one lane is selected, and columns are renamed to English. 
One .csv file has data for one tunnel. 

Data visualization: 
This folder includes files necessary for data analysis and visualization 

Functions: 
This folder includes the .py files that the notebooks (.ipynb) use. These files contain the different functions that are imported into the notebooks. The files in this folder are as follows: 
- Get_data.py: Includes files that can fetch data from the APIs, and to find the nearest points 
- model.py: Includes the file that are necessary to prepare data for model, and to run the model

QGIS_files:
- These files are used for the geo analysis in QGIS
- Get_category_of_tunnels.py: This files reads in the .csv file tunnels_with_points.csv and finds the category (urban/sub-urban)
- Get_nvdbData.py: This file is used to fetch the tunnels from NVDB using the NVDB api version 3

Results: 
- This file includes the results and selected variables for each experiment. Each file is written to when the experiment is run in run_model.ipynb. 

Files:

Main.ipynb: This is to fetch the data via API and find the nearest points to tunnels 

Run_model.ipynb: This file runs the model on the files in the 'data' folder, and writes to the .txt files in Results. 
