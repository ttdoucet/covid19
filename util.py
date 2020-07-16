from scipy.signal import savgol_filter

case_color='#1f77b4'
death_color = '#e03b68' # framboise

def smooth(y):
    yhat = savgol_filter(y, 7, 1)
    return yhat

def calc_daily(df, src, dest):
    df[dest] = df[src] - df[src].shift(1)
    df.loc[:, dest] = df.loc[:, dest].fillna(0)    
    pass
