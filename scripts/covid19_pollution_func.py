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
    import matplotlib.pyplot as plt
    
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