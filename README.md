# Análise de dados – Análise de modelo de investimento
<h4>Projeto desenvolvido em Python com o objetivo de praticar o uso das tecnologias nele aplicadas.</h4>

# 1.	Introdução
Este projeto consiste em analisar um plano de investimento em ações que segue o método de trend following, baseado em comprar ações com tendência de alta e vender ações com tendência de queda.
A estratégia do projeto consiste em todo mês compor uma carteira de investimentos com as 10 ações mais rentáveis do ibovespa nos últimos 6 meses. Todo mês a verificação dessa rentabilidade é realizada e a carteira é atualizada. Taxas que envolvem operações com ações não serão consideradas no cálculo da rentabilidade.

Para realizar a análise dessa estrátegia, pegaremos o histórico de cotações de todas as ações que compuseram o ibovespa de dezembro de 2015 até agosto de 2022. Com essas cotações, calcularemos mês a mês como seria a rentabilidade dessa estratégia com relação ao índice ibovespa no mesmo período.

Para isso, temos um banco de dados organizado mês a mês de dezembro de 2015 até agosto de 2022 com os tickers das ações que compuseram o ibovespa naquele mês, que será utilizado para obtermos as cotações.


# 2.	Métodos Utilizados
*	Manipulação e tratamento de dados; 
*	Criação de gráficos


# 3.	Tecnologias Utilizadas
*	Jupyter Notebook;
*	Python 3;
*	Biblioteca Numpy;
*	Biblioteca Matplotlib;
*	Biblioteca Plotly;
*	Biblioteca Seaborn


# 4.	Fonte dos dados
*	A base de dados com o histórico de ações do Ibovespa foi fornecida durante uma aula ao vivo oferecida pelo canal do Youtube EduFinance – Programação: https://www.youtube.com/channel/UC_00QQmsCRAC-6YVXesFcLQ. O histórico das cotações foi obtido pelo Yahoo Finance através de integração com a biblioteca Pandas.
