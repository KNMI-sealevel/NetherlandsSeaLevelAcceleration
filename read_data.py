import xarray as xr

path_data = '/Users/iriskeizer/Documents/Wind effect/paper/code check/data/'
path_pres_data = f'{path_data}'

output_dir = './data_atmosphere'


def tide_gauge_obs(interp=True):
    '''
    Read a list of tide gauge data and compute the average. 
    Set `interp` to True for a linear interpolation of missing values.
    By default use the 6 tide gauges from the Zeespiegelmonitor.
    The unit of the output is cm. ''' 
    tg_id=[20, 22, 23, 24, 25, 32]
    
    tg_data_dir = path_data + 'tide gauges/rlr_annual'
    names_col = ('id', 'lat', 'lon', 'name', 'coastline_code', 'station_code', 'quality')
    filelist_df = pd.read_csv(tg_data_dir + '/filelist.txt', sep=';', 
                              header=None, names=names_col)
    filelist_df = filelist_df.set_index('id')

    names_col2 = ('time', 'height', 'interpolated', 'flags')

    for i in range(len(tg_id)):
        tg_data = pd.read_csv(f'{tg_data_dir}/data/{tg_id[i]}.rlrdata', 
                              sep=';', header=None, names=names_col2)
        tg_data = tg_data.set_index('time')
        tg_data.height = tg_data.height.where(~np.isclose(tg_data.height,-99999))
        tg_data.height = tg_data.height - tg_data.height.mean()

        if i==0:
            tg_data_df = pd.DataFrame(data=dict(time=tg_data.index, 
                                                col_name=tg_data.height))
            tg_data_df = tg_data_df.set_index('time')
            tg_data_df.columns  = [str(tg_id[i])] 
        else:
            tg_data_df[str(tg_id[i])] = tg_data.height

    if interp:
        tg_data_df = tg_data_df.interpolate(method='slinear')
        
    tg_data_df['Average'] = tg_data_df.mean(axis=1)
    tg_data_df = tg_data_df * 0.1 # Convert from mm to cm
    
    # Rename columns to station names
    tg_data_df = tg_data_df.rename(columns={"20": stations[0], 
                                            "22": stations[1],
                                            "23": stations[2],
                                            "24": stations[3],
                                            "25": stations[4],
                                            "32": stations[5]})
    
    return tg_data_df


def prep_pres_data_obs(data_type = 'era5'):
    """ Function to prepare the observational pressure data for the analysis. For data_type choose ['era5', '20cr']  """
    
    if data_type == 'era5':
        
        # Define the path to code
        path_fp = f'{path_pres_data}ERA5/ERA5_be_msl.nc' # Path to surface pressure 1950-1978
        path_sp = f'{path_pres_data}ERA5/ERA5_msl.nc' # Path to surface pressure 1979-present
        
        # Open data file
        dataset_fp = xr.open_dataset(path_fp)
        dataset_sp = xr.open_dataset(path_sp) 
        
        # Add the two datasets
        dataset = xr.concat([dataset_fp, dataset_sp], dim='time')

        # Change coordinate and variable names
        dataset = dataset.rename({'longitude': 'lon','latitude': 'lat','msl': 'pressure'})

        # Sort latitudes increasing
        dataset = dataset.sortby('lat')

        
    elif data_type == '20cr':
        

        # Open data file
        dataset = xr.open_dataset(path_pres_data + '20CR/prmsl.mon.mean.nc') 

        # Shift longitudes to -180-180 
        dataset.coords['lon'] = (dataset.coords['lon'] + 180) % 360 - 180
        dataset = dataset.sortby(dataset.lon)

        # Change coordinate and variable names
        dataset = dataset.rename({'prmsl': 'pressure'})
    
        #Drop 'time_bnds' variables
        dataset = dataset.drop('time_bnds')
        
        # Select smaller area of data 
        dataset = dataset.where((dataset.lat >= 0) & (dataset.lat <= 90) & (dataset.lon >= -90) & (dataset.lon <= 90), drop=True)

    else: print('Given data_type not correct, choose era5 or 20cr')

        
    # Calculate annual averages 
    dataset_annual = dataset.groupby('time.year').mean('time')
   
    # Save annual data as netcdf4  
    #dataset_annual.to_netcdf(f'{path_pres}pres_annual_{data_type}')
    
    return dataset_annual