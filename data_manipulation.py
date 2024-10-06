import pandas as pd
import numpy as np
import math

import matplotlib.pyplot as plt
# import seaborn as sns
import scipy.stats as stats
from scipy.stats import norm
from bokeh.palettes import Cividis256


def get_short_names(level, metric) -> dict:
    
    short_names_dict = { 
        'l1': {
            'default':{
                'Architecture and engineering occupations' : 'Arch & Eng',
                'Arts, design, entertainment, sports, and media occupations' : 'Ent',
                'Building and grounds cleaning and maintenance occupations' : 'Maintenance',
                'Business and financial operations occupations' : 'Financial',
                'Community and social service occupations' : 'Social Services',
                'Computer and mathematical occupations' : 'Comp & Math',
                'Construction and extraction occupations' : 'Construction',
                'Education, training, and library occupations' : 'Education',
                'Farming, fishing, and forestry occupations' : 'Natural Resources',
                'Food preparation and serving related occupations' : 'Food',
                'Healthcare practitioners and technical occupations' : 'Healthcare Practitioners',
                'Healthcare support occupations' : 'Healthcare',
                'Installation, maintenance, and repair occupations' : 'Facilities',
                'Legal occupations' : 'Legal',
                'Life, physical, and social science occupations' : 'Science',
                'Management occupations' : 'Management',
                'Office and administrative support occupations' : 'Office Admin',
                'Personal care and service occupations': 'Personal Care', 
                'Production occupations' : 'Production',
                'Protective service occupations': 'Security', 
                'Sales and related occupations' : 'Sales',
                'Transportation and material moving occupations' : 'Logistics'
            },            
            'number_of_workers':{
                'Architecture and engineering occupations' : 'Arch & Eng',
                'Arts, design, entertainment, sports, and media occupations' : 'Ent',
                'Building and grounds cleaning and maintenance occupations' : 'Maintenance',
                'Business and financial operations occupations' : 'Financial',
                'Community and social service occupations' : 'Social Srvcs',
                'Computer and mathematical occupations' : 'Comp & Math',
                'Construction and extraction occupations' : 'Construction',
                'Education, training, and library occupations' : 'Education',
                'Farming, fishing, and forestry occupations' : 'Ntrl Rsrcs',
                'Food preparation and serving related occupations' : 'Food',
                'Healthcare practitioners and technical occupations' : 'Healthcare Practitioners',
                'Healthcare support occupations' : 'Healthcare',
                'Installation, maintenance, and repair occupations' : 'Facilities',
                'Legal occupations' : 'Legal',
                'Life, physical, and social science occupations' : 'Sci',
                'Management occupations' : 'Management',
                'Office and administrative support occupations' : 'Office Admin',
                'Personal care and service occupations': 'Personal Care', 
                'Production occupations' : 'Production',
                'Protective service occupations': 'Security', 
                'Sales and related occupations' : 'Sales',
                'Transportation and material moving occupations' : 'Logistics'
            },
            'number_of_students':{
                'Architecture and engineering occupations' : 'Arch & Eng',
                'Arts, design, entertainment, sports, and media occupations' : 'Ent',
                'Building and grounds cleaning and maintenance occupations' : 'Maintenance',
                'Business and financial operations occupations' : 'Fin',
                'Community and social service occupations' : 'Social Services',
                'Computer and mathematical occupations' : 'Computer',
                'Construction and extraction occupations' : 'Construction',
                'Education, training, and library occupations' : 'Education',
                'Farming, fishing, and forestry occupations' : 'Natural Resources',
                'Food preparation and serving related occupations' : 'Food',
                'Healthcare practitioners and technical occupations' : 'Med Pract', # 'Med Pract' suppressed because it is near 0 for students
                'Healthcare support occupations' : 'Healthcare',
                'Installation, maintenance, and repair occupations' : 'Facilities',
                'Legal occupations' : 'Legal',
                'Life, physical, and social science occupations' : 'Science',
                'Management occupations' : 'Mgmt',
                'Office and administrative support occupations' : 'Office Admin',
                'Personal care and service occupations': 'Personal Care', 
                'Production occupations' : 'Production',
                'Protective service occupations': 'Security', 
                'Sales and related occupations' : 'Sales',
                'Transportation and material moving occupations' : 'Logistics'
            },            
        },
        'l2': {
            'default':{
                'Building and grounds cleaning and maintenance occupations' : 'Maint',
                'Construction and extraction occupations' : 'Construction',
                'Farming, fishing, and forestry occupations' : 'Natural Resources',
                'Food preparation and serving related occupations' : 'Food',
                'Healthcare support occupations' : 'Health',
                'Installation, maintenance, and repair occupations' : 'Facilities',
                'Management, business, and financial operations occupations' : 'Business',
                'Office and administrative support occupations' : 'Office Admin',
                'Personal care and service occupations': 'Personal Care', 
                'Production occupations' : 'Production',
                'Professional and related occupations' : 'Professional',
                'Protective service occupations' : 'Security',
                'Sales and related occupations' : 'Sales',
                'Transportation and material moving occupations' : 'Logistics'
            },            
            'number_of_workers':{
                'Building and grounds cleaning and maintenance occupations' : 'Maint',
                'Construction and extraction occupations' : 'Construction',
                'Farming, fishing, and forestry occupations' : 'Natural',
                'Food preparation and serving related occupations' : 'Food',
                'Healthcare support occupations' : 'Health',
                'Installation, maintenance, and repair occupations' : 'Facilities',
                'Management, business, and financial operations occupations' : 'Business',
                'Office and administrative support occupations' : 'Office Admin',
                'Personal care and service occupations': 'Personal Care', 
                'Production occupations' : 'Production',
                'Professional and related occupations' : 'Professional',
                'Protective service occupations' : 'Security',
                'Sales and related occupations' : 'Sales',
                'Transportation and material moving occupations' : 'Logistics'
            },
            'number_of_students':{
                'Building and grounds cleaning and maintenance occupations' : 'Maint',
                'Construction and extraction occupations' : 'Construction',
                'Farming, fishing, and forestry occupations' : 'Natural Resources',
                'Food preparation and serving related occupations' : 'Food',
                'Healthcare support occupations' : 'Health',  # 'Health' suppressed because it is near 0 for students
                'Installation, maintenance, and repair occupations' : 'Facilities',
                'Management, business, and financial operations occupations' : 'Bus',
                'Office and administrative support occupations' : 'Office',
                'Personal care and service occupations': 'Personal Care', 
                'Production occupations' : 'Production',
                'Professional and related occupations' : 'Professional',
                'Protective service occupations' : 'Security',
                'Sales and related occupations' : 'Sales',
                'Transportation and material moving occupations' : 'Logistics'
            },

        },
    }

    return short_names_dict[level][metric] if metric in short_names_dict[level].keys() else short_names_dict[level]['default']
    


def get_palette(number_of_groups) -> dict:

    Cividis = {
        'default': Cividis256[0:3] + Cividis256[64:67] + Cividis256[128:131]+ Cividis256[192: 195] + Cividis256[252: 255],
        14: Cividis256[0:3] + Cividis256[64:67] + Cividis256[128:131]+ Cividis256[192: 195] + Cividis256[252: 255],
        4: [Cividis256[0]] + [Cividis256[64]] + [Cividis256[192]] + [Cividis256[252]],
        2: Cividis256[0]  + Cividis256[255]
    }

    return Cividis[number_of_groups] if number_of_groups in Cividis.keys() else Cividis['default']


def get_format_parameters(metric, number_of_groups) -> dict:
    
    palette = get_palette(number_of_groups=number_of_groups)
    print(number_of_groups,' - ', palette)
    label_offset_dict = { 
        'default':{
                'block':{'line_width': 1, 
                         'line_color': 'white', 
                         'fill_alpha': 0.80, 
                         'palette': palette},
                'l2' : {'x_offset': 2, 
                        'y_offset': -35,
                        'text_font_size': "30pt",
                        'text_baseline': "top",
                        'text_color': 'black'
                        },
                'l1' : {'x_offset': 2, 
                        'y_offset': 35,
                        'text_font_size': "18pt",
                        'text_baseline': "top",
                        'text_color': 'black'
                        },
        },            

        'number_of_workers':{
            'block':{'line_width': 10, 
                        'line_color': 'white', 
                        'fill_alpha': 0.80, 
                        'palette': palette},
            'l2' : {'x_offset': 8, 
                    'y_offset': -15,
                    'text_font_size': "23pt",
                    'text_baseline': "top",
                    'text_color': 'black'
                    },
            'l1' : {'x_offset': 8, 
                    'y_offset': 4,
                    'text_font_size': "17pt",
                    'text_baseline': "top",
                    'text_color': 'white'
                    },
        },
        
        'number_of_students':{
                'block':{'line_width': 10, 
                         'line_color': 'white', 
                         'fill_alpha': 0.80, 
                         'palette': palette},
                'l2' : {'x_offset': 10, 
                        'y_offset': -35,
                        'text_font_size': "30pt",
                        'text_baseline': "top",
                        'text_color': 'black'
                        },
                'l1' : {'x_offset': 10, 
                        'y_offset': 4,
                        'text_font_size': "18pt",
                        'text_baseline': "top",
                        'text_color': 'white'
                        },
        },
    }
        
    return label_offset_dict[metric] if metric in label_offset_dict.keys() else label_offset_dict[metric]['default']


def get_student_record_df() -> pd.DataFrame:

    df_record = pd.read_csv('./assets/student.record.csv')
    df_term = pd.read_table('./assets/term.table.txt', delimiter="\t").fillna('Unknown')

    df_term.columns = ['TERM_ID', 'TERM_DESCRIPTION']
    terms = ['Fall', 'Winter', 'Summer', 'Spring', 'Unknown']
    df_term['TERM_NAME'] = df_term['TERM_DESCRIPTION'].apply(lambda x: list(filter(lambda y: y!='', [t if t in x else '' for t in terms]))[0])
    df_term['TERM_YEAR'] = df_term['TERM_DESCRIPTION'].apply(lambda x: int(x[-4:]) if x[-4:].isnumeric() else None)

    terms_student = ['ADMIT_TERM', 'MAJOR1_TERM', 'MAJOR2_TERM', 'MAJOR3_TERM']
    merge_record_df = df_record.copy()
    for term in terms_student:
        
        merge_record_df = pd.merge(
                            merge_record_df,
                            df_term, 
                            how='left',
                            left_on=term,
                            right_on='TERM_ID')
        
        merge_record_df.rename(columns={'TERM_ID': term + '_' + 'TERM_ID', 
                                'TERM_DESCRIPTION': term + '_' + 'TERM_DESCRIPTION', 
                                'TERM_NAME': term + '_' + 'TERM_NAME', 
                                'TERM_YEAR': term + '_' + 'TERM_YEAR'}, inplace=True)    


    merge_record_df['ADMIT_TERM_EQUALS_MAJOR1_TERM'] = merge_record_df['ADMIT_TERM'] == merge_record_df['MAJOR1_TERM']
    merge_record_df['MAJOR1_TERM_YEAR_MINUS_ADMIT_TERM_YEAR'] = merge_record_df['MAJOR1_TERM_TERM_YEAR'] - merge_record_df['ADMIT_TERM_TERM_YEAR']

    return merge_record_df


def get_df_record_occupation_level_grouped_by_year_filtered(merge_record_df) -> pd.DataFrame:


    term = 'MAJOR1_TERM_TERM_YEAR' # ADMIT_TERM_TERM_YEAR'
    merge_record_df['MAJOR1_DESCR'] = merge_record_df['MAJOR1_DESCR'].fillna('Undeclared')
    df_majors = pd.read_excel('./assets/majors.xlsx', sheet_name='majors', header=0)

    df_record_occupation = pd.merge(merge_record_df,
                                df_majors, 
                                how='left',
                                left_on='MAJOR1_DESCR',
                                right_on='MAJOR')

    df_record_occupation['number_of_students_all'] = 1
    df_record_occupation['number_of_students_men'] = df_record_occupation['SEX'].apply(lambda sex: 1 if sex == 'M' else 0) 
    df_record_occupation['number_of_students_women'] = df_record_occupation['SEX'].apply(lambda sex: 1 if sex == 'F' else 0)
    df_record_occupation['number_of_students_unknown'] = df_record_occupation['SEX'].apply(lambda sex: 1 if sex not in ['M', 'F'] else 0)
    df_record_occupation['MAJOR1_TERM_TERM_YEAR'] = df_record_occupation['MAJOR1_TERM_TERM_YEAR'].apply(lambda x: str(x)[0:4])

    df_record_occupation_grouped = df_record_occupation.groupby(['OCCUPATION',term]).sum().reset_index()

    df_occupation_level_mapping = pd.read_excel('./assets/bls_cpsaat39_2011_to_2015.xlsx', sheet_name='level_mapping_l0', header=0)
    df_occupation_level_mapping_distinct = df_occupation_level_mapping[['l4', 'l3', 'l2', 'l1']].drop_duplicates().reset_index()
    df_occupation_level_mapping_distinct = df_occupation_level_mapping_distinct[['l4', 'l3', 'l2', 'l1']]

    df_record_occupation_level_grouped = pd.merge(df_record_occupation_grouped,
                                                    df_occupation_level_mapping_distinct, 
                                                    how='left',
                                                    left_on='OCCUPATION',
                                                    right_on='l1')

    df_record_occupation_level_grouped = df_record_occupation_level_grouped[[term, 'OCCUPATION', 'number_of_students_all', 
                                                                            'number_of_students_men', 'number_of_students_women', 
                                                                            'number_of_students_unknown', 'l4', 'l3', 'l2', 'l1']].\
                                                                            sort_values(by=['OCCUPATION', term])

    df_record_occupation_level_grouped_by_year = df_record_occupation_level_grouped.groupby([term, 'l1']).sum().reset_index()
    df_record_occupation_level_grouped_by_year=df_record_occupation_level_grouped_by_year[[term, 'l4', 'l3', 'l2', 'l1', 
                                                                                        'number_of_students_all', 'number_of_students_men', 
                                                                                        'number_of_students_women', 'number_of_students_unknown']]
    df_record_occupation_level_grouped_by_year_filtered = df_record_occupation_level_grouped_by_year[df_record_occupation_level_grouped_by_year['MAJOR1_TERM_TERM_YEAR'].isin(['2011', '2012', '2013', '2014', '2015'])] 
    return df_record_occupation_level_grouped_by_year_filtered, df_occupation_level_mapping



# ###########################


def get_df_level_list(df_record_occupation_level_grouped_by_year_filtered, df_occupation_level_mapping):

    tabs = ['2015', '2014', '2013', '2012', '2011']

    df_bls_all = pd.DataFrame()
    for tab in tabs:
        df_bls_next = pd.read_excel('./assets/bls_cpsaat39_2011_to_2015.xlsx', 
                                    sheet_name=str(tab), 
                                    header=0, 
                                    ).fillna('Unknown')
        df_bls_next['year'] = str(tab)
        df_bls_all = pd.concat([df_bls_all, df_bls_next])


    df_level = pd.merge(df_bls_all,
                        df_occupation_level_mapping, 
                        how='left',
                        left_on='occupation',
                        right_on='l0')

    df_level = df_level[df_level['l0'].notnull()]


    df_level['year'] = df_level['year'].apply(lambda x: str(x))

    df_level = df_level.groupby(['year', 'l1'], sort=True).agg({
        'number_of_workers_all': 'sum',
        'median_weekly_earnings_all': 'mean',
        'number_of_workers_men': 'sum',
        'median_weekly_earnings_men': 'mean',
        'number_of_workers_women': 'sum',
        'median_weekly_earnings_women': 'mean',
        'occupation_x': 'first',
        'occupation_y': 'first',
        'l4': 'first',
        'l3': 'first',
        'l2': 'first',
        'l0': 'first'
    }).reset_index()

    df_merge_bls = pd.merge(df_level,
                        df_record_occupation_level_grouped_by_year_filtered, 
                        how='left',
                        left_on=['l1', 'year'],
                        right_on=['l1', 'MAJOR1_TERM_TERM_YEAR'])[[
                                    'year', 'occupation_x', 'l0','l1','l2_x','l3_x','l4_x',                                    
                                    'number_of_workers_all', 'median_weekly_earnings_all',
                                    'number_of_workers_men', 'median_weekly_earnings_men',
                                    'number_of_workers_women', 'median_weekly_earnings_women',
                                    'number_of_students_all', 'number_of_students_men',
                                    'number_of_students_women', 'number_of_students_unknown'
                        ]]

    new_column_names = {
        'year': 'year',
        'occupation_x': 'occupation',
        'l0': 'l0',
        'l1': 'l1',
        'l2_x': 'l2',
        'l3_x': 'l3',
        'l4_x': 'l4',
        'number_of_workers_all': 'number_of_workers_all_sum',
        'median_weekly_earnings_all': 'median_weekly_earnings_all_mean',
        'number_of_workers_men': 'number_of_workers_men_sum',
        'median_weekly_earnings_men': 'median_weekly_earnings_men_mean',
        'number_of_workers_women': 'number_of_workers_women_sum',
        'median_weekly_earnings_women': 'median_weekly_earnings_women_mean',
        'number_of_students_all': 'number_of_students_all_sum',
        'number_of_students_men': 'number_of_students_men_sum',
        'number_of_students_women': 'number_of_students_women_sum',
        'number_of_students_unknown': 'number_of_students_unknown_sum'
    }


    df_merge_bls.rename(columns=new_column_names, inplace=True)

    df_merge_bls


    df_level_list = []
    selected_levels = ['l1','l2','l3']
    for level in selected_levels:
        
        df_merge_bls_level = df_merge_bls[[level, 'year',                              
                            'number_of_students_all_sum',
                            'number_of_students_men_sum', 
                            'number_of_students_women_sum', 
                            'number_of_students_unknown_sum',
                            'number_of_workers_all_sum', 
                            'median_weekly_earnings_all_mean', 
                            'number_of_workers_men_sum', 
                            'median_weekly_earnings_men_mean', 
                            'number_of_workers_women_sum', 
                            'median_weekly_earnings_women_mean']
                            ]

        df_merge_bls_grouped = df_merge_bls_level.groupby(['year', level],  sort=True).sum().reset_index()
        df_level_list.append(df_merge_bls_grouped)
        # df_merge_bls_grouped.to_csv('./scratch/df_merge_bls_'+ level + '.csv', index=False)
    return df_level_list 


# print(len(df_level_list[0]))


def get_df_list_final():
    df_record_occupation_level_grouped_by_year_filtered, df_occupation_level_mapping = get_df_record_occupation_level_grouped_by_year_filtered(get_student_record_df())
    return get_df_level_list(df_record_occupation_level_grouped_by_year_filtered, df_occupation_level_mapping)