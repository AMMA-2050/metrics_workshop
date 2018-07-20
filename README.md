# metrics_workshop
Scripts developed at the metrics workshop, 12-16.12.2016

ToDo:
- PET formula is incorrect and needs to be updated
- Dry spells/wet spells are based on rolling windows, which should be changed to index difference approach or image label
- additional rainy season calculations could be added
- Check annual mean rainy day 
- SPI calculation should average rainfall instead of averaging SPI for time series
- Above files should be rerun to update the atlases accordingly


Packages:

dev_code: code under development for workshop preparation

example_code: all kinds of nice example code that you can use for your scripts!

shared: shared package of the workshop participants. All scripts developed at the workshop go here

your folder: where all your personal examples and changes go. A sandbox for you!

Teacher: teacher example folder

visitor: sandbox for external people


MASTER SCRIPT STRUCTURE:

- load_file_names
- load_data
- calculate_data
- plot for one model 
- make multi model
- plot multi model
- statistics
- plot anomalies
