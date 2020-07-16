from scipy.signal import savgol_filter

case_color='#1f77b4'
death_color = '#e03b68' # framboise

def smooth(y):
    yhat = savgol_filter(y, 7, 1)
    return yhat

