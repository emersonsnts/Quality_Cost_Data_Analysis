'''ANALYSIS OF QUALITY COSTS IN A MECHANICAL METAL INDUSTRY'''

'''Import of required libraries'''
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import style
import warnings
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter

warnings.filterwarnings('ignore')

'''Reading and processing data'''
Data_Base = pd.read_excel('Quality_Cost_Dataset.xlsx')
Data_Base.info()
Groupby_Cost_type = Data_Base.groupby(by='TIPO DE CUSTO').sum()
print(Groupby_Cost_type)
print(Groupby_Cost_type.loc['APPRAISAL COSTS'][1:-1]) #Finds and transforms the line into a series, whose index will be the labels of the dataframe from which it was extracted
#Renamed costs to facilitate graphical visualization
Abrevviation_Costs=['Supplier Audits',
                    'Suppliers Evaluation',
                    'Equipment Maintenance',
                    'Project Product Clinic',
                    'Legal Costs',
                    'Refunds for Quality Issues',
                    'Product Returns',
                    'Issuing and re-issuing Reports',
                    'Final Product Inspection',
                    'Engineering Labor',
                    'Quality Assurance Labor',
                    'Production System Labor',
                    'Warranty Labor',
                    'Reduction in Setups',
                    'Customer Market Research',
                    'Warranty Claims',
                    'Repairs to Finished Products',
                    'Reworks',
                    'Waste',
                    'Downtime',
                    'Overtime Work',
                    'Employees Training'

]

'''Creation of figure and style'''
plt.figure(figsize=(16, 9))
plt.style.use('seaborn-v0_8-darkgrid')
paleta = sns.color_palette('dark', 10)
plt.rc('font', family='Arial')

'''Scatter plot of all costs by total monetary amount'''
sns.scatterplot(data=Data_Base, x=Abrevviation_Costs, y='TOTAL', hue='TIPO DE CUSTO', palette=[paleta[2], paleta[3], paleta[8], paleta[0]], s=80) #palette=[paleta[2], paleta[3], paleta[8], paleta[0]], palette=['green', 'red', 'yellow', 'blue']
plt.tight_layout()
plt.xticks(rotation=45, ha='right', fontsize=11)
plt.title('Figure 1: Analysis of the Monetary Amount by Costs', fontsize=14)
plt.ylabel('Costs (USD)', fontsize=12) #opcional fontweight='bold'
plt.legend(
    loc='lower center',
    ncol=4,
    bbox_to_anchor=(0.5, -0.47),
    prop={'weight':'bold'}
)
plt.show()


'''Armezenagem por tipo de custo'''
value_ca = Groupby_Cost_type.loc['APPRAISAL COSTS'][1:-1]
value_fe = Groupby_Cost_type.loc['EXTERNAL FAILURE COSTS'][1:-1]
value_fi = Groupby_Cost_type.loc['INTERNAL FAILURE COSTS'][1:-1]
value_cp = Groupby_Cost_type.loc['PREVENTION COSTS'][1:-1]

#Groupby_Cost_type.columns[1:-1]
'''Stacked bar graph plot of cost types per quarter'''
plt.bar(value_fe.index,
        value_fe,
        color=paleta[3],
        edgecolor='white'
)
plt.bar(value_fi.index,
        value_fi,
        bottom=value_fe,
        color=paleta[8],
        edgecolor='white'
)
plt.bar(value_ca.index,
        value_ca,
        bottom=[A + B for A, B in zip(value_fe, value_fi)],
        color=paleta[0],
        edgecolor='white'
)
plt.bar(value_cp.index,
        value_cp,
        bottom=[A + B + C for A, B, C in zip(value_fe, value_fi, value_ca)],
        color=paleta[2],
        edgecolor='white'
)
plt.title('Quality Cost Analysis - Metal Mechanic Industry')
plt.xlabel('Time (Quarters)')
plt.ylabel('Costs (USD)')
plt.legend(
    [
        'EXTERNAL FAILURE COSTS',
        'INTERNAL FAILURE COSTS',
        'APPRAISAL COSTS',
        'PREVENTION COSTS'
    ],
    loc='lower center',
    ncol=4,
    bbox_to_anchor=(0.5, -0.15)
)
plt.show()


'''Bar graph plot of cost amounts for each type of quality cost'''
Groupby_Cost_type=Groupby_Cost_type.sort_values(by='TOTAL', ascending=False)
plt.bar(Groupby_Cost_type['TOTAL'].index, Groupby_Cost_type['TOTAL'], color=[paleta[3], paleta[8], paleta[2], paleta[0]], edgecolor='white')
plt.ticklabel_format(style='plain', axis='y')
plt.xticks(weight='bold', fontsize=12)
plt.title('Figure 2: Analysis of the Monetary Amount by Type of Quality Costs', fontsize=13)
plt.ylabel('Costs (USD)', fontsize=12)

for i, x in enumerate(Groupby_Cost_type['TOTAL']):
    plt.text(i,x,f'${x:,.2f}', ha='center', weight='bold', fontsize=12)
total_costs=sum(Groupby_Cost_type['TOTAL'])
for i, x in enumerate(Groupby_Cost_type['TOTAL']):
    plt.text(i,10000,f'{x/total_costs:,.0%}', ha='center', weight='bold', color='white', fontsize=12)
plt.show()


'''EXPONENTIAL REGRESSION'''
coq_value=Data_Base.groupby(by='TIPO DE CUSTO').sum()['TOTAL'][0] + Data_Base.groupby(by='TIPO DE CUSTO').sum()['TOTAL'][3]
copq_value=Data_Base.groupby(by='TIPO DE CUSTO').sum()['TOTAL'][1] + Data_Base.groupby(by='TIPO DE CUSTO').sum()['TOTAL'][2]

x1=[0, 60, 95]
y1=[100, coq_value/1000, 1500] #10^-3
x2=[50, 60, 95]
y2=[2000, copq_value/1000, 100] #10^-3
coefficients_coq= np.polyfit(x1, np.log(y1),1)
coefficients_copq= np.polyfit(x2, np.log(y2),1)

def coq(x):
    a=np.exp(list(coefficients_coq)[0])
    b=np.exp(list(coefficients_coq)[1])
    return b*(a**x)

def copq(x):
    a=np.exp(list(coefficients_copq)[0])
    b=np.exp(list(coefficients_copq)[1])
    return b*(a**x)

def total_costs(x):
    return coq(x)+ copq(x)

x=np.linspace(0,100,100)
plt.plot(x, coq(x))
plt.plot(x, copq(x))
plt.plot(x, total_costs(x))
plt.axvline(x=60)
plt.axvline(x=77.8)
plt.ylim(0,5000)
plt.show()

print(copq(77))
print(total_costs(77))
print(copq_value+coq_value)
plt.bar('Current Scenario (60% QUALITY)', sum(value_fe)+sum(value_fi), color=paleta[3])
plt.bar('Current Scenario (60% QUALITY)', sum(value_cp)+sum(value_ca), bottom=sum(value_fe)+sum(value_fi), color=paleta[2])
plt.bar('Projected Scenario (77% QUALITY)', copq(77)*1000, color=paleta[3])
plt.bar('Projected Scenario (77% QUALITY)', coq(77)*1000, bottom=copq(77)*1000, color=paleta[2])
plt.ticklabel_format(style='plain', axis='y')
plt.legend(
    [
        'COSTS OF POOR QUALITY',
        'COST OF QUALITY'
    ],
    loc='lower center',
    ncol=2,
    bbox_to_anchor=(0.5, -0.15))
plt.xticks(weight='bold', fontsize=12)
plt.title('Figure 5: Comparison between the current scenario and the projected scenario', fontsize=13)
plt.text(0,coq_value+copq_value*1.01,f'${coq_value+copq_value:,.2f}', ha='center', weight='bold', fontsize=12)
plt.text(1,total_costs(77)*1000*1.01,f'${total_costs(77)*1000:,.2f}', ha='center', weight='bold', fontsize=12)
plt.ylabel('Costs (USD)', fontsize=12)
plt.show()

