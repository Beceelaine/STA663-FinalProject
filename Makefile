final_report.pdf: final_report.tex profiling.txt data_files/times_like.tex data_files/times.tex data_files/features.png data_files/data.png data_files/detected_features.png data_files/detected_total_features.png data_files/table_features.tex data_files/trace_plots.png
	pdflatex final_report
	pdflatex final_report
	pdflatex final_report
    
data_files/times.tex: py_scripts/main.py data_files/X_orig.csv py_scripts/cython_function.so
	python py_scripts/main.py

py_scripts/cython_function.so:
	cd py_scripts ; python cython_setup.py build_ext --inplace; cd ..
    
data_files/times_like.tex: py_scripts/likelihood_times.py data_files/X_orig.csv
	python py_scripts/likelihood_times.py
    
py_scripts/figures.py: data_files/chain_Z.npy data_files/chain_K.npy data_files/chain_sigma_X.npy data_files/chain_sigma_A.npy data_files/chain_alpha.npy data_files/Z.npy data_files/A_orig.csv data_files/X_orig.csv data_files/Z_orig.csv
	python py_scripts/figures.py

data_files/features.png data_files/data.png data_files/detected_features.png data_files/detected_total_features.png data_files/table_features.tex data_files/trace_plots.png: py_scripts/figures.py
	python py_scripts/figures.py
    
data_files/A_orig.csv data_files/X_orig.csv data_files/Z_orig.csv: py_scripts/generate_data.py
	python py_scripts/generate_data.py

data_files/chain_Z.npy data_files/chain_K.npy data_files/chain_sigma_X.npy data_files/chain_sigma_A.npy data_files/chain_alpha.npy data_files/Z.npy: py_scripts/sampler_final.py
	python py_scripts/sampler_final.py
    
all: final_report.pdf
