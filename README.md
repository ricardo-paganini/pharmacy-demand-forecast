# 💊 Farmácias Boa Dose: Previsão de Demanda

Estudo de caso de **previsão de vendas (série temporal)** para uma rede fictícia de farmácias, seguindo a metodologia **CRISP-DM**.

## Sobre o projeto

A **Farmácias Boa Dose** é uma rede fictícia com 5 lojas no Paraná (Curitiba, Londrina, Maringá e Ponta Grossa). As compras são centralizadas e o pedido semanal segue uma regra simples: **"pede o mesmo tanto que vendeu na semana passada"**.

A regra funciona na maior parte do ano, mas quebra justo quando importa: no inverno falta antigripal na prateleira, no fim do verão sobra protetor solar no estoque, e promoções e feriados distorcem o pedido da semana seguinte.

O objetivo do projeto é entender como as vendas se comportam ao longo do tempo e construir uma **previsão semanal por produto para as próximas 4 semanas** (janeiro de 2026) que erre menos que a regra atual, transformando a previsão numa **sugestão de pedido**.

**Dados:** 3 anos de vendas diárias (2023 a 2025), 5 lojas, 20 produtos e cerca de 108 mil linhas, com problemas propositais de base real (duplicados, nomes escritos de vários jeitos, vendas negativas e dias faltando).

## Perguntas de negócio

1. Como as vendas da rede evoluíram de 2023 a 2025? Existe tendência de crescimento?
2. Quais produtos têm sazonalidade forte e em quais meses ficam no pico?
3. Quanto as promoções e os feriados mexem nas vendas?
4. As lojas se comportam de forma parecida ou alguma foge do padrão?
5. Dá para prever as vendas semanais das próximas 4 semanas errando menos que a regra atual?
6. Quanto pedir de cada produto nas próximas 4 semanas?

## Principais resultados

| | Regra atual | Random Forest |
|---|---|---|
| Erro médio por semana e produto (MAE) | 43,0 unidades | **20,8 unidades** |
| Erro percentual (MAPE) | 15,2% | **7,8%** |

- 📉 **O modelo corta o erro pela metade** (−51,7%) no teste de julho a dezembro de 2025.
- 🌡️ **9 dos 20 produtos têm sazonalidade forte.** Os de inverno (gripe e resfriado) e os de verão (protetor solar e pós-sol) chegam a vender de 3 a 4 vezes mais no pico do que no mês mais fraco.
- 🏷️ **Promoção aumenta as vendas em cerca de 41%, e feriado derruba em cerca de 41%.** A regra atual não enxerga nenhuma das duas.
- 🏪 **A loja de Londrina caiu 16,4% a partir de abril de 2025**, enquanto as outras seguiram crescendo de 4% a 6%.
- 🎄 **Para janeiro de 2026, a regra atual pediria de menos em 18 dos 20 produtos**, porque a última semana conhecida teve o Natal. O modelo sugere um pedido de **24.355 unidades**, já com margem de segurança por produto.

## Ferramentas

- **Python** com pandas (tratamento e agregações), matplotlib e seaborn (gráficos) e scikit-learn (Random Forest, MAE e MAPE)
- **Jupyter Notebook**
- **Git e GitHub**

## Como reproduzir

No Prompt de Comando (Windows):

```bash
git clone https://github.com/ricardo-paganini/pharmacy-demand-forecast.git
cd pharmacy-demand-forecast
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name=pharmacy-venv --display-name="Python (pharmacy)"
jupyter notebook pharmacy_demand_forecast.ipynb
```

No Linux ou Mac, a ativação do ambiente é `source venv/bin/activate`. Se você não tiver o Jupyter instalado, rode antes `pip install notebook`.

No notebook, escolha o kernel **Python (pharmacy)** e rode **Kernel > Restart & Run All**.

Os arquivos `.csv` já estão no repositório. Para gerá-los de novo (o resultado é sempre o mesmo, por causa da semente fixa):

```bash
python generate_data.py
```

## Arquivos

| Arquivo | Descrição |
|---|---|
| `pharmacy_demand_forecast.ipynb` | Notebook com a análise completa (seções 1 a 9 do CRISP-DM) |
| `generate_data.py` | Script que gera as bases fictícias com semente fixa |
| `stores.csv` | Cadastro das 5 lojas |
| `products.csv` | Cadastro dos 20 produtos, com categoria e preço |
| `holidays.csv` | Feriados nacionais de 2023 a 2025 e o 01/01/2026 |
| `sales.csv` | Vendas diárias por loja e produto (2023 a 2025) |
| `requirements.txt` | Bibliotecas e versões do ambiente |

## Observação sobre os dados

Todos os dados são **fictícios**, gerados pelo `generate_data.py` para este estudo de caso. A empresa, as lojas e os números não representam nenhuma rede real. Os padrões de negócio (sazonalidade, promoções, feriados e a queda de uma loja) e os problemas de qualidade foram colocados de propósito, para a análise ter o que descobrir e tratar.
