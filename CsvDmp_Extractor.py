import pandas as pd
import glob

folder_path = 'folderEnd/*/DUMP/*.csv'

csv_file_paths = glob.glob(folder_path)[0]
# filetoRead = 'HFS_20230406191801_noa1_469 - HFS_20230406191801_noa1_469.csv'

for csv_file_path in csv_file_paths:
    print(f'Opening {csv_file_path}')   
    #df = pd.read_csv(csv_file_path, header=41, index_col='NDX')
    df = pd.read_csv(csv_file_path)

    # # df = df[df['PASS/FAIL'] == 'PASS']
    # # #print(df)
    # # passRows = df.loc[df["PASS/FAIL"] == "PASS", ['yyyy-MM-DD', 'Elev', 'Azim', 'Signal', 'PASS/FAIL']]
    # # print(passRows)

    # # Permanently changes the pandas settings
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.width', None)

    # # Find the indices of the PASS rows
    # pass_indices = df[df['PASS/FAIL'] == 'PASS'].index

    # # Find the first and last FAIL rows before the PASS rows
    # fail_indices = []
    # last_fail_idx = None
    # for idx in pass_indices:
    #     fail_indices_before = df.loc[:idx][df.loc[:idx, 'PASS/FAIL'] == 'FAIL'].index
    #     if len(fail_indices_before) > 0:
    #         fail_idx_before = fail_indices_before[-1]
    #         if fail_idx_before != last_fail_idx and fail_idx_before not in pass_indices:
    #             fail_indices.append(fail_idx_before)
    #             last_fail_idx = fail_idx_before
    #     fail_indices_after = df.loc[idx:][df.loc[idx:, 'PASS/FAIL'] == 'FAIL'].index
    #     if len(fail_indices_after) > 0:
    #         fail_idx_after = fail_indices_after[0]
    #         if fail_idx_after != last_fail_idx and fail_idx_after not in pass_indices and fail_idx_after not in fail_indices:
    #             fail_indices.append(fail_idx_after)
    #             last_fail_idx = fail_idx_after

    # # Include the first and last FAIL rows before the PASS rows in the dataframe
    # included_indices = list(pass_indices) + fail_indices
    # included_indices.sort()
    # df_included = df.loc[included_indices]

    # # Print the resulting dataframe
    # # print(df_included.drop_duplicates(keep='first'))

    # df_included.drop_duplicates(keep='first').to_csv(f'{fileToRead}_export')



