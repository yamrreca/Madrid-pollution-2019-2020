import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

def poincare_plot(bf, aft, reg_params_bf=None, reg_params_aft=None, bf_title=None, aft_title=None):
    """Creates a two-plot subplot showing the Poincaré plots of the measurements before and after
    some point in time.
    
    Arguments:
    -bf: Array-like with the measurements of the 'before' point in time. First column: original 
    measurements. Second column: shifted measurements-
    
    -aft: Array-like with the measurements of the 'after' point in time. Same column order as above.
    
    -reg_params_bf: Tuple or list with the parameters b0 and b1 from linear regression of the 'before'
    period. If None does not plot the lines.
    
    -reg_params_bf: Tuple or list with the parameters b0 and b1 from linear regression of the 'after'
    period.
    
    -bf_title: Title for the graph of the 'before' period
    
    -aft_title: Title for the graph of the 'after' period
    
    Returns:
    -None; plots the graphs."""
    
    #Preparing the regression parameters for plotting
    
    b0_bf, b1_bf = reg_params_bf
    b0_aft, b1_aft = reg_params_aft
    
    #Transforming to string for the legend
    str_b0_bf, str_b1_bf = str(round(b0_bf,2)), str(round(b1_bf,2))
    str_b0_aft, str_b1_aft = str(round(b0_aft,2)), str(round(b1_aft,2))
    
    #Extracting original and shifted columns
    bf_orig = bf[:,0]
    bf_shift = bf[:,1]
    aft_orig = aft[:,0]
    aft_shift = aft[:,1]

    fig, ax = plt.subplots(1,2, figsize = (15, 5))
    fig.suptitle('Poincaré Diagrams', fontsize=15)

    #Poincaré scatter plot
    ax[0].scatter(bf_orig,bf_shift)
    ax[1].scatter(aft_orig, aft_shift)
    
    if reg_params_bf is not None:
        #Linear regression
        ax[0].plot(bf_orig, b0_bf + b1_bf*bf_orig, color = 'red',
                     label = r'$x_{n + 1} = $' + str_b0_bf + ' + ' + str_b1_bf + r'$x_n$')
        #Identity line
        ax[0].plot(bf_orig, bf_orig, color='orange', label=r'$x_{n + 1} = x_n$')
        ax[0].legend()
        
    if reg_params_aft is not None:
        #Linear regression
        ax[1].plot(aft_orig, b0_aft + b1_aft*aft_orig, color = 'red',
                     label = r'$x_{n + 1} = $' + str_b0_aft + ' + ' + str_b1_aft + r'$x_n$')
        #Identity line
        ax[1].plot(aft_orig, aft_orig, color='orange', label=r'$x_{n + 1} = x_n$')
        ax[1].legend()
    
    
    ax[0].set_title(bf_title, fontsize=16)
    ax[1].set_title(aft_title, fontsize=16)

    for i in range(2):
        ax[i].set_xlabel(r'$x_n$')
        ax[i].set_ylabel(r'$x_{n + 1}$')
        
        
        
##################################################################################################################################################################################
        
def summ_stats_compare(bf, aft, bf_title='2019', aft_title='2020'):
    """Computes all summary statistics given in the describe method, plus the skew and kurtosis,
    for the two arguments and returns them as a single dataframe.
    
    Arguments:
    -bf: Pandas Series object containing measurements from the 'before' period.
    -aft: Pandas Series object containing measurements from the 'after' period.
    
    Returns:
    stats: Pandas Dataframe containing the summary statistics of both Series, rounded to two decimal 
    figures.
    """
    
    #Calculating the statistics for both Series
    bf_desc = bf.describe()
    bf_desc['skew'] = bf.skew()
    bf_desc['kurtosis'] = bf.kurtosis()
    
    aft_desc = aft.describe()
    aft_desc['skew'] = aft.skew()
    aft_desc['kurtosis'] = aft.kurtosis()
    
    #Creating the df
    
    stats = pd.DataFrame({bf_title:bf_desc, aft_title:aft_desc})
    
    return stats.round(2)


##################################################################################################################################################################################


def traj_matrix_SVD(X, window):
    """Calculates the trajectory matrix and performs SVD for the scree diagram.
    
    Arguments:
    X: Array-like containing pollutant measurements
    window: Int. The number of rows, corresponding to a specific period of time, by default
    24 for one day.
    
    Returns:
    U, V: The left and right matrices of SVD respectively
    S: The vector of singular values.
    """
     
    A = [] #The trajectory matrix
    col = len(X) - window #Number of columns
    for i in range(col):
        A.append(X[i:i+window])
    A = np.array(A)
    A = A.T
    
    assert A.shape == (window, col)
    
    U,S,V = np.linalg.svd(A)
    S = S.reshape(-1, 1)
    
    return U,S,V


##################################################################################################################################################################################


def half_month_ticks():
    """Creates a pandas index of tick positions at the 1st and 15th of every month, alongside a list 
    of their labels
    
    Returns:
    tick_pos: Pandas index object with tick positions.
    tick_labels = List with the labels corresponding to tick_pos.
    """
    
    #Craeating tick positions
    tick_dates = [[dt.datetime(2020,i,1), dt.datetime(2020,i,15)] for i in range(1,5)]
    tick_pos = [j for i in tick_dates for j in i]
    tick_pos.append(dt.datetime(2020,4,30)) #Last date for which there is data
    tick_pos = pd.Index(tick_pos) #Otherwise doesn't work well with matplotlib

    #Creating tick labels

    month_map = {1:'Jan', 
                 2:'Feb', 
                 3:'Mar',
                 4:'Apr'}

    tick_labels = []
    for i in tick_pos:
        mon_name = str(month_map [i.month])
        day = str(i.day)
        tick_labels.append(mon_name + '-' + day)
        
    return tick_pos, tick_labels



def seasonal_plot(res, axes, title=None):
    """Plots the results of the statsmodels seasonal_decompose function.
    
    Arguments:
    -res: The result of calling seasonal_decompose
    -axes: Matplotlib Axes object of length >=4
    -title: string. The title for the first column
    
    Returns:
    -axes: The axes with the plots
    """
    res.observed.plot(ax=axes[0], legend=False)
    axes[0].set_ylabel('Observed')
    axes[0].set_title(title)
    res.trend.plot(ax=axes[1], legend=False)
    axes[1].set_ylabel('Trend')
    res.seasonal.plot(ax=axes[2], legend=False)
    axes[2].set_ylabel('Seasonal')
    res.resid.plot(ax=axes[3], legend=False)
    axes[3].set_ylabel('Residual')
    
    return axes