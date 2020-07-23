def columns_to_datetime(df):
    """Creates a new df with a datetime columns and values corresponding to the concentration of a pollutant
    at said datetime.
    Arguments:
    df: A dataframe with different columns for pollutant concentration per hour of the day, named
    in the format h01, h02, etc."""
    
    import pandas as pd
    import numpy as np
    import datetime
    from warnings import filterwarnings
    filterwarnings('ignore')
    
    hours = ('h0'+str(i) if i<10 else 'h'+str(i) for i in range(1,25))
    df_hours = []
    df = df.reindex(np.sort(df.columns), axis = 1) #To prevent issues coming from columns
    #being in a different order when I pass a list of columns later on
    
    for hour, hour_str in enumerate(hours):
        hour = hour + 1
        
        #Creating a df with only the values of the corresponding hour
        columns = ['contaminante', 'estacion', 'fecha', hour_str]
        df_hour = df[columns]
        
        #The hour is appended to the date
        df_hour['dt'] = df_hour['fecha'].apply(lambda x:datetime.datetime(x.year, x.month, x.day, hour%24))
        df_hour.drop(columns=['fecha'], inplace=True)
        
        #Changing the name of the concentration column to avoid problems
        df_hour.rename(columns={hour_str:'concentracion'}, inplace = True)
        
        #The df is appended to the list
        df_hours.append(df_hour)
    
    new_df = pd.concat(df_hours).sort_values('dt').reset_index(drop=True)
    assert len(new_df) == 24*len(df)
    
    return new_df


def clean_data(csv_list):
    """Cleans the data in the csv file so that a dataframe with only a single column for
    the concentration of pollutants is created, and with the datetime info in another
    column. The function requires the data be downloaded in csv format from the official site https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=f3c0f7d512273410VgnVCM2000000c205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default.
    
    Arguments:
    csv_list: An iterable containing the paths to the files containing the data, one month per file.
    """
    
    import pandas as pd
    import numpy as np
    from warnings import filterwarnings
    filterwarnings('ignore')
    
    dfs = [pd.read_csv(csv, sep=';') for csv in csv_list]
    df = pd.concat(dfs)
    del dfs

    #The following columns will not be used and are removed
    df.drop(columns = ['PUNTO_MUESTREO', 'PROVINCIA', 'MUNICIPIO'], inplace = True)
    df.columns = df.columns.str.lower()

    #Some data are not validated, but that will be ignored
    df.drop(columns = ['v0'+str(i) if i<10 else 'v'+str(i) for i in range(1,25)], inplace = True)

    #Creating a date column
    anios = df['ano'].astype('str')
    meses = df['mes'].astype('str')
    dias = df['dia'].astype('str')
    fechas_str = anios + '-' + meses + '-' + dias

    df['fecha'] = pd.to_datetime(fechas_str, yearfirst=True)
    df.drop(columns=['ano','mes','dia'], inplace=True)

    #A column with the name of each pollutant is created
    used = {1:'SO2',
            6:'CO',
            8:'NO2',
            9:'PM2.5',
            10:'PM10',
            14:'O3'
            }

    not_used = {i:np.nan for i in (7,12,20,30,35,42,43,44)}
    pollutants_dict = {**used, **not_used}

    df['contaminante'] = df['magnitud'].apply(lambda x:pollutants_dict[x])
    df.drop(columns=['magnitud'], inplace = True)
    df = df.dropna().reset_index(drop=True)
    
    #The station located at Avda. La Guardia (station code 28079054) is set outside the urban
    #environment of the city and could therefore be registering outlier values. It will be 
    #removed.
    
    LaGuardia = df[df['estacion'] == 54].index
    df.drop(index=LaGuardia, inplace=True)
    df = df.reset_index(drop=True)
    
    #A new df is created with only one column for the pollutant concentration.
    #Another new column with the date and hour is created.

    clean_df = columns_to_datetime(df)
    
    return clean_df
    

def create_pollutant_csvs(clean_df):
    """Creates csv files containing the data for each pollutant individually.
    The resultant csv's first column will be a datetime index.
    
    IMPORTANT: The function assumes data from only one year. Otherwise the
    filename will be nonindicative of its true contents.
    
    Arguments:
    clean_df: The df obtained from the clean_data function."""
    
    import pandas as pd
    from os.path import join as pathjoin
    
    year = clean_df['dt'].dt.year.unique()[0].astype(str)
    save_dir = input('Write the path to the directory where the files will be saved.\n')

    for pollutant in clean_df['contaminante'].unique():
        pollut_df = clean_df[clean_df['contaminante'] == pollutant].copy()
        pollut_df.drop(columns=['contaminante'], inplace=True)
        pollut_df.set_index('dt', inplace = True)
        save_path = pathjoin(save_dir, f'{pollutant}-{year}.csv')
            
        pollut_df.to_csv(save_path)
            
            
if __name__ == '__main__':
    from sys import argv
    
    if len(argv) < 2:
        print('As arguments you must give the paths of the unprocessed csv files.')
        exit
        
    clean_df = clean_data(argv[1:])
    create_pollutant_csvs(clean_df)
        
    
