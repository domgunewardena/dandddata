import pandas as pd

def generate_skeleton_df(df,measure):
    
    date_columns = ['Date','Day','OrdDay']
    
    rev_df_columns = ['SiteName', 'LocationName', 'GenericLocation', 'Session', 'OrdSession', 'RevenueType', 'Wine', 'Date', 'Day', 'OrdDay', 'Revenue']
    cov_df_columns = ['SiteName', 'LocationName', 'GenericLocation', 'Session', 'Date', 'Day', 'OrdDay', 'Covers']    
    df_columns = rev_df_columns if measure=='Revenue' else cov_df_columns

    skeleton_df_columns = df_columns.copy()
    for col in [measure] + date_columns:
        skeleton_df_columns.remove(col)

    skeleton_df = df[skeleton_df_columns].groupby(skeleton_df_columns).sum().reset_index()

    if measure == 'Revenue':

        rows = [
            [
                row[0], 
                row[1], 
                row[2], 
                row[3], 
                row[4], 
                row[5], 
                row[6]
            ] for row in zip(
                skeleton_df[skeleton_df_columns[0]],
                skeleton_df[skeleton_df_columns[1]],
                skeleton_df[skeleton_df_columns[2]],
                skeleton_df[skeleton_df_columns[3]],
                skeleton_df[skeleton_df_columns[4]],
                skeleton_df[skeleton_df_columns[5]],
                skeleton_df[skeleton_df_columns[6]]
        )]

    else:

        rows = [
            [
                row[0], 
                row[1], 
                row[2], 
                row[3], 
            ] for row in zip(
                skeleton_df[skeleton_df_columns[0]],
                skeleton_df[skeleton_df_columns[1]],
                skeleton_df[skeleton_df_columns[2]],
                skeleton_df[skeleton_df_columns[3]],
        )]

    skeleton_dates = df[date_columns].groupby(date_columns).sum().reset_index()

    date_rows = [
        [
            row[0], 
            row[1], 
            row[2]
        ] for row in zip(
            skeleton_dates[date_columns[0]],
            skeleton_dates[date_columns[1]],
            skeleton_dates[date_columns[2]]
    )]

    skeleton = pd.DataFrame([row + date_row for row in rows for date_row in date_rows])
    skeleton.columns = df_columns.copy()[:-1]

    return pd.merge(skeleton,df,how='outer').fillna(0)
