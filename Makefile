STA663_FinalReport_RadhikaAnand.pdf: STA663_FinalReport_RadhikaAnand.tex profiling.txt matlab_profile.png IBP.png CRP.png data_files/inversetimes.tex data_files/times_like.tex data_files/times.tex data_files/features.png data_files/data.png data_files/detected_features.png data_files/detected_total_features.png data_files/table_features.tex data_files/trace_plots.png data_files/figures.png
	pdflatex STA663_FinalReport_RadhikaAnand
	pdflatex STA663_FinalReport_RadhikaAnand
	pdflatex STA663_FinalReport_RadhikaAnand
    
data_files/times.tex: py_scripts/main.py data_files/X_orig.csv py_scripts/cython_functions.so
	python py_scripts/main.py
    
data_files/times_like.tex: py_scripts/likelihood_times.py data_files/X_orig.csv
	python py_scripts/likelihood_times.py 

data_files/inversetimes.tex: py_scripts/compare_inverse.py data_files/X_orig.csv
	python py_scripts/compare_inverse.py 

data_files/features.png data_files/data.png data_files/detected_features.png data_files/detected_total_features.png data_files/table_features.tex data_files/trace_plots.png data_files/figures.png: py_scripts/figures.py data_files/chain_Z.npy data_files/chain_K.npy data_files/chain_sigma_X.npy data_files/chain_sigma_A.npy data_files/chain_alpha.npy data_files/Z.npy data_files/A_orig.csv data_files/X_orig.csv data_files/Z_orig.csv
	python py_scripts/figures.py
    
data_files/A_orig.csv data_files/X_orig.csv data_files/Z_orig.csv: py_scripts/generate_data.py
	python py_scripts/generate_data.py

data_files/chain_Z.npy data_files/chain_K.npy data_files/chain_sigma_X.npy data_files/chain_sigma_A.npy data_files/chain_alpha.npy data_files/Z.npy: py_scripts/sampler_final.py
	python py_scripts/sampler_final.py

py_scripts/cython_functions.so:
	cd py_scripts ; python cython_setup.py build_ext --inplace; cd ..

all: STA663_FinalReport_RadhikaAnand.pdf
