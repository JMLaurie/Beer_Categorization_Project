# Beer Categorization Project

## Project Overview
This project analyzes a comprehensive beer dataset to explore various characteristics of different beer styles and brands. The analysis employs statistical methods, data visualization, and machine learning techniques to uncover patterns and relationships within beer data.

**Team Members:** Jake Laurie, Zach Lanter, Trevor Packan

## Dataset Description
The project utilizes a beer dataset containing multiple attributes including:
- Beer names and styles
- Brewery information
- Alcohol content (ABV)
- International Bitterness Units (IBU)
- Ounces (serving sizes)
- Additional beer characteristics

## Methodology

### 1. Data Loading and Preprocessing
- Imported necessary packages for data analysis (csv, os, numpy, pandas, matplotlib)
- Created custom data classes for different file types (CSV, Numpy arrays)
- Implemented abstract base classes for flexible data handling
- Loaded and structured beer data for analysis

### 2. Exploratory Data Analysis
- **Basic Statistics**: Calculated descriptive statistics for numerical features
- **Data Sorting**: Organized beers by various attributes to identify top performers
- **Visualization**: Created plots using matplotlib to visualize distributions and relationships

### 3. Machine Learning Approaches

#### Decision Tree Classification
- Implemented decision tree models to categorize beer styles
- Trained models on beer attributes to predict beer categories
- Evaluated classification performance

#### Principal Component Analysis (PCA)
- Applied PCA for dimensionality reduction
- Identified key components explaining variance in beer characteristics
- Visualized beer clusters in reduced dimensional space
- Used PCA for feature engineering and pattern recognition

### 4. Advanced Analysis
- Utilized typing annotations for code clarity and type safety
- Implemented functools for efficient data processing
- Applied the cmp_to_key function for custom sorting operations

## Key Findings
The analysis revealed patterns in beer characteristics across different styles, enabling:
- Classification of beers based on quantitative attributes
- Identification of key features distinguishing beer categories
- Understanding of relationships between ABV, IBU, and beer styles
- Dimensionality reduction for visualizing complex beer data

## Technologies Used
- **Python**: Core programming language
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **Scikit-learn**: Machine learning (Decision Trees, PCA)
- **Jupyter Notebook**: Interactive development environment

## Project Structure
```
Beer_Categorization_Project/
├── code/
│   └── plotter.py          # Visualization utilities
├── data/
│   └── beer.csv            # Beer dataset
├── output/
│   ├── eigs.svg            # Eigenvalue visualization
│   └── proj10.ipynb        # Main analysis notebook
├── README.md
└── run.bash                # Execution script
```

## How to Run
1. Ensure all required Python packages are installed
2. Execute `bash run.bash` to run the analysis
3. Or open `output/proj10.ipynb` in Jupyter Notebook for interactive exploration

## Results and Deliverables
- Comprehensive statistical analysis of beer characteristics
- Classification models for beer style prediction
- PCA visualizations showing beer clustering
- Eigenvalue analysis stored in output directory
- Detailed Jupyter notebook documenting all analysis steps

## Future Enhancements
- Integration of additional beer datasets
- Advanced ensemble methods for improved classification
- Web scraping for real-time beer data
- Interactive dashboard for beer exploration
- Recommendation system based on user preferences
