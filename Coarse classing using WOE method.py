#!/usr/bin/env python
# coding: utf-8

# In[1]:


def calculate_woe_iv(dataset, faetures, target, cat):
    for feature in features:
        while dataset[feature].nunique() > cat:
            lst = []
            for i in range(dataset[faeture].nunique()):
                val = list(dataset[feature].unique())[i]
                lst.append({
                    'Value': val,
                    'All': dataset[dataset[feature] == val].count()[feature],
                    'Non_Responder': dataset[(dataset[feature] == val) & (dataset[target] == 0)].count()[feature],
                    'Responder': dataset[(dataset[feature] == val) & (dataset[target] == 1)].count()[feature]
                })

            dset = pd.DataFrame(lst)
            dset['Distr_Non_Responder'] = dset['Non_Responder'] / dset['Non_Responder'].sum()
            dset['Distr_Responder'] = dset['Responder'] / dset['Responder'].sum()
            dset['WoE'] = np.log(dset['Distr_Non_Responder'] / dset['Distr_Responder'])
            dset = dset.replace({'WoE': {np.inf: 0, -np.inf: 0}})
            dset['IV'] = (dset['Distr_Non_Responder'] - dset['Distr_Responder']) * dset['WoE']
            iv = dset['IV'].sum()
            dset = dset.sort_values(by='WoE')
            print(dset) #printing just to check the output
            dset['lag'] = dset['WoE'].shift(1)
            dset['WoE_diff'] = dset['WoE'] - dset['lag']
            dset1 = dset.nsmallest(1, ['WoE_diff'])
            woe_n = dset[(dset['WoE_diff'] == dset1['WoE_diff'].iloc[0]) | (dset['WoE'] == dset1['lag'].iloc[0])]['Value'].to_list()
            dataset[feature] = dataset[feature].replace(to_replace = woe_n, value = "_".join(woe_n)[:40])
    return dataset


'''
    function call
    
    #features are object columns in which we want to reduce the number of categories
    #data is the name of original dataframe
    #'target' is the name of target column
    #5 is the number of maximum categories required
'''

features = ['feature1', 'faeature2', 'feature3']
data = calculate_woe_iv(data, features, 'target', 5)

