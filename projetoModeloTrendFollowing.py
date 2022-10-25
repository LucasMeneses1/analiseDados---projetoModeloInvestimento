#!/usr/bin/env python
# coding: utf-8

# # Projeto Modelo de Investimento - Trend Following

# - Projeto desenvolvido com objetivos meramente didáticos, para prática das tecnologias abordadas. Este projeto consiste em analisar um plano de investimento em ações que segue o método de trend following, baseado em comprar ações com tendência de alta e vender ações com tendência de queda.
# 
# - A estratégia do projeto consiste em todo mês compor uma carteira de investimentos com as 10 ações mais rentáveis do ibovespa nos últimos 6 meses. Todo mês a verificação dessa rentabilidade é realizada e a carteira é atualizada. Taxas que envolvem operações com ações não serão consideradas no cálculo da rentabilidade.
# 
# - Para realizar a análise dessa estrátegia, pegaremos o histórico de cotações de todas as ações que compuseram o ibovespa de dezembro de 2015 até agosto de 2022. Com essas cotações, calcularemos mês a mês como seria a rentabilidade dessa estratégia com relação ao índice ibovespa no mesmo período.
# 
# - Para isso, temos um banco de dados organizado mês a mês de dezembro de 2015 até agosto de 2022 com os tickers das ações que compuseram o ibovespa naquele mês, que será utilizado para obtermos as cotações.

# ### Bibliotecas Necessárias

# In[117]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import plotly.express as px
import seaborn as sns


# ### Composição Ibovespa dez/2015 - ago/2022

# In[118]:


# Importando as ações que compuseram o índice Ibovespa de dezembro de 2015 até agosto de 2022
df_acoes_ibov = pd.read_excel('composicao_ibov.xlsx')
lista_acoes = []

# Tratando os dados para adequá-los ao formato de pesquisa aceito pelo yahoo finance
for data in df_acoes_ibov:
    aux = df_acoes_ibov[data].dropna()
    aux = aux + '.SA'
    lista_acoes.append(aux)

# Salvando um dataframe com a lista de ações já tradadas
lista_acoes_final = pd.concat(lista_acoes)
lista_acoes_final = lista_acoes_final.drop_duplicates()
ibov = pd.Series(['^BVSP'])
display(lista_acoes_final)
display(ibov)


# ### Histórico das cotações das ações da lista e do índice Ibovespa de 30/06/2015 até 31/08/2022

# In[119]:


# O período de interesse para a análise da estratégia da carteira é de janeiro de 2015 até agosto de 2022.
# Porém, para definir a carteira de cada mês precisamos calcular o rendimento das ações nos últimos 6 meses.
# Logo, precisamos obter os dados dos rendimentos a partir de junho de 2015 para definirmos as primeiras carteiras do ano de 2015.    

cotacao_acoes = web.DataReader(lista_acoes_final, data_source='yahoo', start='2015-06-30', end='2022-08-31')['Adj Close']
display(cotacao_acoes)
cotacao_ibovespa = web.DataReader(ibov, data_source='yahoo', start='2015-12-30', end='2022-08-31')['Adj Close']
display(cotacao_ibovespa)


# ### Pegando a cotação do fechamento mensal de cada ação e do índice Ibovespa

# In[120]:


cotacao_acoes_mensal = cotacao_acoes.resample("M").last()
cotacao_ibov_mensal = cotacao_ibovespa.resample("M").last()
display(cotacao_acoes_mensal)
display(cotacao_ibov_mensal)


# ### Tratamento dos dados e cálculos de rendimento

# In[121]:


# preenchendo os valores NaN com 0 para realizar os cálculos do rendimento
cotacao_acoes_mensal = cotacao_acoes_mensal.fillna(0)
display(cotacao_acoes_mensal)


# In[122]:


# calculando o retorno mensal das ações e do indice Ibovespa
df_retorno_mensal_acoes = cotacao_acoes_mensal.pct_change().replace([np.inf, -np.inf, -1], 0)
display(df_retorno_mensal_acoes)
df_retorno_mensal_ibov = cotacao_ibov_mensal.pct_change().replace([np.inf, -np.inf, -1], 0)
display(df_retorno_mensal_ibov)

# calculando o retorno das ações a cada 6 meses
df_retorno_acoes_6m = cotacao_acoes_mensal.pct_change(periods=6).replace([np.inf, -np.inf, -1], 0)
display(df_retorno_acoes_6m)


# In[123]:


# Após a realização dos cálculos necessários, filtraremos o período temporal de análise das carteiras
df_retorno_mensal_acoes = df_retorno_mensal_acoes.loc['2015-12-31':]
df_retorno_acoes_6m = df_retorno_acoes_6m.loc['2015-12-31':]
display(df_retorno_mensal_acoes)
display(df_retorno_acoes_6m)
display(df_retorno_mensal_ibov)


# In[124]:


# Melhorando a estrutura dos dataframes - Ao invés de termos uma coluna para cada ação, teremos
# uma coluna contendo todas as ações
cotacao_acoes_mensal.reset_index(inplace=True)
df_retorno_mensal_acoes.reset_index(inplace=True)
df_retorno_acoes_6m.reset_index(inplace=True)
df_retorno_mensal_ibov.reset_index(inplace=True)

cotacao_acoes_mensal = pd.melt(cotacao_acoes_mensal, id_vars= "Date", var_name= "cod", value_name= "cotacao").dropna()
df_retorno_mensal_acoes = pd.melt(df_retorno_mensal_acoes, id_vars= "Date", var_name= "cod", value_name= "retorno_mensal").dropna()
df_retorno_acoes_6m = pd.melt(df_retorno_acoes_6m, id_vars= "Date", var_name= "cod", value_name= "retorno_6m").dropna()                 
df_retorno_mensal_ibov = pd.melt(df_retorno_mensal_ibov, id_vars= "Date", var_name= "cod", value_name= "retorno_mensal").dropna()                 

display(cotacao_acoes_mensal)
display(df_retorno_mensal_acoes)
display(df_retorno_acoes_6m)
display(df_retorno_mensal_ibov)


# ### Definindo a carteira mês a mês e calculando os resultados da estratégias

# In[125]:


# Definindo a carteira mês a mês

dic_meses = {12:'jan', 1:'fev', 2:'mar', 3:'abr', 4:'mai', 5:'jun', 6:'jul', 7:'ago', 8:'set', 9:'out', 10:'nov', 11:'dez'}
dic_carteira = {}
aux_mes = []
aux_rc = []
aux_ri = []
intervalo_datas_carteira = df_retorno_acoes_6m['Date'].drop_duplicates()

for i, mes in enumerate(intervalo_datas_carteira):
    # Definindo as carteiras mês a mês - As 10 ações de maior rendimento nos últimos 6 meses
    composicao_ibov_mes = list(df_acoes_ibov[mes].dropna())
    composicao_ibov_mes = [cod + '.SA' for cod in composicao_ibov_mes]
    #print(composicao_ibov_mes)
    df_retornos_6m_aux = df_retorno_acoes_6m.loc[
        (df_retorno_acoes_6m['Date'] == mes) &
        (df_retorno_acoes_6m['cod'].isin(composicao_ibov_mes))
    ]
    df_retornos_6m_aux = df_retornos_6m_aux.sort_values('retorno_6m', ascending=False).head(10)
    carteira = list(df_retornos_6m_aux['cod'])
    
    try:
        # Calculando o rendimento mensal das carteiras e comparando com o ibovespa
        
        # Filtrando o fechamento mensal das ações
        retorno_carteira = cotacao_acoes_mensal.loc[
            (cotacao_acoes_mensal['Date'] == intervalo_datas_carteira[i+1]) & 
            (cotacao_acoes_mensal['cod'].isin(carteira))
        ].copy()         
        
        # Filtrando a cotação do início do mês das ações
        df_aux = cotacao_acoes_mensal.loc[
            (cotacao_acoes_mensal['Date'] == mes) & 
            (cotacao_acoes_mensal['cod'].isin(carteira))
        ].copy()
        
        # Adicionando a cotação das ações do início do respectivo mês ao dataframe de retorno da carteira
        retorno_carteira['cotacao_inicial'] = list(df_aux['cotacao'])


        retorno_carteira = retorno_carteira.rename(columns = {'Date':'Mes', 'cod': 'Codigo', 'cotacao':'cotacao_final', 'cotacao_inicial':'cotacao_inicial'})
        
        # Cálculo do retorno mês a mês
        retorno_carteira['valorizacao'] = retorno_carteira['cotacao_final'] - retorno_carteira['cotacao_inicial']
        retorno_carteira['valorizacao_%'] = list(df_retorno_mensal_acoes['retorno_mensal'].loc[
            (df_retorno_mensal_acoes['cod'].isin(carteira)) & 
            (df_retorno_mensal_acoes['Date'] == intervalo_datas_carteira[i+1])
        ])

        # Filtrando o retorno do indice Ibovespa do mês
        retorno_ibov = df_retorno_mensal_ibov[(df_retorno_mensal_ibov['Date'] == intervalo_datas_carteira[i+1])]
        # display(retorno_ibov)
        
        # Considerando peso de investimento igual em todas as ações, o retorno da carteira será a média simples dos rendimentos de todas as ações da carteira
        rc = np.mean(retorno_carteira['valorizacao_%'])
        # Retorno do Ibovespa
        ri = retorno_ibov.iloc[0,-1]

        if mes.month == 12:
            aux_mes.append(f'{dic_meses[mes.month]}/{mes.year + 1}')
            aux_rc.append(rc)
            aux_ri.append(ri)     
        else:
            aux_mes.append(f'{dic_meses[mes.month]}/{mes.year}')
            aux_rc.append(rc)
            aux_ri.append(ri)
    except:
        pass
    
    #display(retorno_carteira)
dic_carteira['mes'] = aux_mes
dic_carteira['retorno_carteira'] = aux_rc
dic_carteira['retorno_ibovespa'] = aux_ri
#display(dic_carteira)
#display(retorno_carteira)


# In[126]:


# Dataframe com o rendimento mês a mês da carteira e do índice ibovespa
resultado = pd.DataFrame(data=dic_carteira)
resultado.set_index('mes', inplace=True)
display(
    
    resultado.style.format({
    'retorno_carteira': '{:,.2%}'.format,
    'retorno_ibovespa': '{:,.2%}'.format
})
    
)

# Dataframe com o rendimento ano a ano da carteira e do índice ibovespa
lista_meses = list(resultado.index)
lista_anos = [data[4:8] for data in lista_meses]

resultado_anual = resultado.copy()
resultado_anual['retorno_carteira'] = resultado_anual['retorno_carteira'] + 1 
resultado_anual['retorno_ibovespa'] = resultado_anual['retorno_ibovespa'] + 1
resultado_anual['ano'] = lista_anos
#display(resultado_anual)
resultado_anual['retorno_carteira_anual'] = resultado_anual.groupby('ano')['retorno_carteira'].cumprod() - 1
resultado_anual['retorno_ibovespa_anual'] = resultado_anual.groupby('ano')['retorno_ibovespa'].cumprod() - 1
resultado_anual = resultado_anual.groupby('ano').tail(1)[['ano','retorno_carteira_anual','retorno_ibovespa_anual']]
resultado_anual.set_index('ano', inplace=True)
display(
    
    resultado_anual.style.format({
    'retorno_carteira_anual': '{:,.2%}'.format,
    'retorno_ibovespa_anual': '{:,.2%}'.format
})
    
)

# Dataframe com o rendimento ano a ano cumulativo da carteira e do índice ibovespa
lista_meses = list(resultado.index)
lista_anos = [data[4:8] for data in lista_meses]

resultado_anual_cumulativo = resultado.copy()
resultado_anual_cumulativo['retorno_carteira'] = resultado_anual_cumulativo['retorno_carteira'] + 1 
resultado_anual_cumulativo['retorno_ibovespa'] = resultado_anual_cumulativo['retorno_ibovespa'] + 1
resultado_anual_cumulativo['ano'] = lista_anos
#display(resultado_anual)
resultado_anual_cumulativo['retorno_carteira_cumulativo'] = resultado_anual_cumulativo['retorno_carteira'].cumprod() - 1
resultado_anual_cumulativo['retorno_ibovespa_cumulativo'] = resultado_anual_cumulativo['retorno_ibovespa'].cumprod() - 1
resultado_anual_cumulativo = resultado_anual_cumulativo.groupby('ano').tail(1)[['ano','retorno_carteira_cumulativo','retorno_ibovespa_cumulativo']]

resultado_anual_cumulativo.set_index('ano', inplace=True)
display(
    
    resultado_anual_cumulativo.style.format({
    'retorno_carteira_cumulativo': '{:,.2%}'.format,
    'retorno_ibovespa_cumulativo': '{:,.2%}'.format
})
    
)


# ### Gráficos

# In[144]:


rac = list(resultado_anual['retorno_carteira_anual'])
rai = list(resultado_anual['retorno_ibovespa_anual'])
dra = list(resultado_anual['retorno_carteira_anual'] - resultado_anual['retorno_ibovespa_anual'])
daux = {'ano': ['2016', '2017', '2018', '2019', '2020', '2021', '2022']}  

aux = pd.DataFrame(data=dic_carteira)
aux['diferenca'] = aux['retorno_carteira'] - aux['retorno_ibovespa']

aux['ano'] = lista_anos = [data[4:8] for data in lista_meses]
aux['mes'] = lista_anos = [data[0:3] for data in lista_meses]
anos = ['2016', '2017', '2018', '2019', '2020', '2021', '2022']
meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

for mes in meses:
    lista_aux = list(aux.loc[(aux['mes'] == mes)]['retorno_carteira'])
    if len(lista_aux) == 7:
        daux[mes] = lista_aux
    else:
        a = 7 - len(lista_aux)
        for i in range(a):
            lista_aux.append(0)
        daux[mes] = lista_aux
aux2 = pd.DataFrame(data=daux)
aux2.set_index('ano', inplace=True)
aux2['Total'] = rac

# Mapa de calor representando o desempenho da carteira ao longo do período de tempo analisado
plt.figure(figsize=(16,9))

cbar_kws = {'format':lambda x, pos: '{:.0%}'.format(x)}
annot_kws={'fontsize':15}
ax = sns.heatmap(aux2, annot=True, vmin=-0.2, vmax=0.2, linewidths=0.8, fmt=".2%", annot_kws=annot_kws, cmap="RdYlGn", cbar=None, center = 0, robust = True, cbar_kws=cbar_kws)   
plt.title("Retorno da Carteira", fontsize=25, pad=30, weight='bold')
plt.yticks(rotation=0, fontsize=20)
plt.xticks(fontsize=20)
ax.set(xlabel=None,
      ylabel=None)


for mes in meses:
    lista_aux = list(aux.loc[(aux['mes'] == mes)]['retorno_ibovespa'])
    if len(lista_aux) == 7:
        daux[mes] = lista_aux
    else:
        a = 7 - len(lista_aux)
        for i in range(a):
            lista_aux.append(0)
        daux[mes] = lista_aux
        
aux2 = pd.DataFrame(data=daux)
aux2.set_index('ano', inplace=True)
aux2['Total'] = rai

# Mapa de calor representando o desempenho do Ibovespa ao longo do período de tempo analisado
plt.figure(figsize=(16,9))

cbar_kws = {'format':lambda x, pos: '{:.0%}'.format(x)}
annot_kws={'fontsize':15}
ax = sns.heatmap(aux2, annot=True, vmin=-0.2, vmax=0.2, linewidths=0.8, fmt=".2%", annot_kws=annot_kws, cmap="RdYlGn", cbar=None, center = 0, robust = True, cbar_kws=cbar_kws)   
plt.title("Retorno do Ibovespa", fontsize=25, pad=30, weight='bold')
plt.yticks(rotation=0, fontsize=20)
plt.xticks(fontsize=20)
ax.set(xlabel=None,
      ylabel=None)

for mes in meses:
    lista_aux = list(aux.loc[(aux['mes'] == mes)]['diferenca'])
    if len(lista_aux) == 7:
        daux[mes] = lista_aux
    else:
        a = 7 - len(lista_aux)
        for i in range(a):
            lista_aux.append(0)
        daux[mes] = lista_aux

aux2 = pd.DataFrame(data=daux)
aux2.set_index('ano', inplace=True)
aux2['Total'] = dra

# Mapa de calor representando o desempenho da carteira em relação ao Ibovespa ao longo do período de tempo analisado
plt.figure(figsize=(16,9))

cbar_kws = {'format':lambda x, pos: '{:.0%}'.format(x)}
annot_kws={'fontsize':15}
ax = sns.heatmap(aux2, annot=True, vmin=-0.1, vmax=0.1, linewidths=0.8, fmt=".2%", annot_kws=annot_kws, cmap="RdYlGn", cbar=None, center = 0, robust = True, cbar_kws=cbar_kws)   
plt.title("Diferença entre o retorno da carteira e o retorno do Ibovespa", fontsize=25, pad=30, weight='bold')
plt.yticks(rotation=0, fontsize=20)
plt.xticks(fontsize=20)
ax.set(xlabel=None,
      ylabel=None)

# Mapa de calor representando o desempenho da carteira em relação ao Ibovespa ao longo do período de tempo analisado
aux['ganhou'] = (aux['retorno_carteira'] > aux['retorno_ibovespa'])
aux['ganhou'] = aux['ganhou'].astype(int)
k = {}

for mes in meses:
    lista_aux = list(aux.loc[(aux['mes'] == mes)]['ganhou'])
    if len(lista_aux) == 7:
        daux[mes] = lista_aux
    else:
        a = 7 - len(lista_aux)
        for i in range(a):
            lista_aux.append(0.5)
        daux[mes] = lista_aux
aux2 = pd.DataFrame(data=daux)
aux2.set_index('ano', inplace=True)
aux2['Ano'] = (resultado_anual['retorno_carteira_anual'] > resultado_anual['retorno_ibovespa_anual']) 
aux2['Ano'] = aux2['Ano'].astype(int)
aux2['Ano'] = [0.5 + ret for ret in dra]

l2 = []
k['anos'] = anos
for mes in aux2:
    if mes != 'Ano':
        z = list(aux2[mes])
        l = []
        for item in z:
            if item == 1:
                l.append('Ganhou')
            elif item == 0.5:
                l.append('-')
            else:
                l.append('Perdeu')
        k[mes] = l

t = pd.DataFrame(data=k)

for item in aux2.index:
    if list(aux2.loc[item, :][:12])[-1] != 0.5:
        if sum(list(aux2.loc[item, :][:12])):
            l2.append(str(int(sum(list(aux2.loc[item, :][:12])))) + ' Vitórias')
    else:
        soma = 0
        for i in list(aux2.loc[item, :][:12]):
            if i != 0.5:
                soma += i
        l2.append(str(int(soma))  + ' vitórias')

t['Ano'] = l2
t.set_index('anos', inplace=True)

plt.figure(figsize=(16,9))

annot_kws={'fontsize':15, 'rotation':"45"}
ax = sns.heatmap(aux2, fmt='s', vmin=0, vmax=0.9, annot=t, linewidths=0.70, annot_kws=annot_kws, cmap="RdYlGn", cbar=None, center = 0.5, robust = True)   
plt.title("Meses em que a carteira ganhou do Ibovespa", fontsize=25, pad=30, weight='bold')
plt.yticks(rotation=0, fontsize=20)
plt.xticks(fontsize=20)
ax.set(xlabel=None,
      ylabel=None)


# In[138]:


# Comparação entre o retorno da carteira e do Ibovespa ano a ano
gb = resultado_anual.reset_index()

lista_carteira = list(gb['retorno_carteira_anual'])
lista_ibovespa = list(gb['retorno_ibovespa_anual'])
lista_retornos = lista_carteira + lista_ibovespa
lista_ano = list(gb['ano']) * 2
lista_rotulos = ['Carteira'] * 7 + ['Ibovespa'] * 7

dic_aux = {'Ano': lista_ano,'Retorno': lista_retornos,'Legenda': lista_rotulos}
df_aux = pd.DataFrame(data=dic_aux)

fig = px.bar(df_aux, x='Ano', text_auto=True, y='Retorno', 
             color="Legenda", barmode='group', template='seaborn', 
             title="Comparação entre o retorno da carteira e do Ibovespa ano a ano",
             labels={
        'Retorno': '',
        'Ano': ''
})
fig.update_yaxes(patch=dict(
        tickformat='.1%',
    ))
fig.update_layout(title={
    'font_family' : "Arial Black",
})
fig.show()

# Comparação entre o retorno acumulado da carteira e do Ibovespa  - gráfico de barras
gb = resultado_anual_cumulativo.reset_index()

lista_carteira = list(gb['retorno_carteira_cumulativo'])
lista_ibovespa = list(gb['retorno_ibovespa_cumulativo'])
lista_retornos = lista_carteira + lista_ibovespa
lista_ano = list(gb['ano']) * 2
lista_rotulos = ['Carteira'] * 7 + ['Ibovespa'] * 7

dic_aux = {'Ano': lista_ano,'Retorno': lista_retornos,'Legenda': lista_rotulos}
df_aux = pd.DataFrame(data=dic_aux)

fig = px.bar(df_aux, x='Ano', text_auto=True, y='Retorno', 
             color="Legenda", barmode='group', template='seaborn', 
             title="Comparação entre o retorno acumulado da carteira e do Ibovespa",
             labels={
        'Retorno': '',
        'Ano': ''
})
fig.update_yaxes(patch=dict(
        tickformat='.1%',
    ))
fig.update_layout(title={
    'font_family' : "Arial Black",
})
fig.show()

# Comparação entre o retorno acumulado da carteira e do Ibovespa - gráfico de linhas
import matplotlib.ticker as mtick

ax = resultado_anual_cumulativo.plot(marker='o', xlabel='')
vals = ax.get_yticks()
ax.set_yticklabels(['{:,.2%}'.format(x) for x in vals])

