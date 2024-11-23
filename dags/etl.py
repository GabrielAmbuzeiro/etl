from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import requests
import datetime
from airflow.utils.dates import days_ago
from psycopg2 import connect


url = "https://brapi.dev/api/quote/PETR4,^BVSP"
params = {
    'range': '5y',
    'interval': '1d',
    'dividends': 'true',
    'modules': 'summaryProfile,balanceSheetHistory',
    'token': 'nyvMfdacbcxr6kSDu8nfM1',
}




create_table_query_historico = '''
CREATE TABLE IF NOT EXISTS HistoricoPrecos (
    id INT,
    date BIGINT,  -- Armazena a data como um timestamp
    open DECIMAL(10, 2),
    high DECIMAL(10, 2),
    low DECIMAL(10, 2),
    close DECIMAL(10, 2),
    volume BIGINT,
    adjustedClose DECIMAL(10, 2),
    FOREIGN KEY (id) REFERENCES SummaryProfile(id)
);
'''
create_table_query_summary = '''
CREATE TABLE IF NOT EXISTS SummaryProfile (
    id INT PRIMARY KEY,
    address1 VARCHAR(255),
    address2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(2),
    zip VARCHAR(10),
    country VARCHAR(100),
    website VARCHAR(255),
    industry VARCHAR(100),
    industryKey VARCHAR(50),
    industryDisp VARCHAR(100),
    sector VARCHAR(100),
    sectorKey VARCHAR(50),
    sectorDisp VARCHAR(100),
    longBusinessSummary TEXT
);
'''
create_table_historico_indicadores = '''
CREATE TABLE  IF NOT EXISTS indicadores (
    id int ,
    endDate integer,
    cash BIGINT,
    shortTermInvestments BIGINT,
    netReceivables BIGINT,
    inventory BIGINT,
    otherCurrentAssets BIGINT,
    totalCurrentAssets BIGINT,
    longTermInvestments BIGINT,
    propertyPlantEquipment BIGINT,
    goodWill BIGINT,
    intangibleAssets BIGINT,
    otherAssets BIGINT,
    deferredLongTermAssetCharges BIGINT,
    totalAssets BIGINT,
    accountsPayable BIGINT,
    shortLongTermDebt BIGINT,
    otherCurrentLiab BIGINT,
    longTermDebt BIGINT,
    otherLiab BIGINT,
    minorityInterest BIGINT,
    totalCurrentLiabilities BIGINT,
    totalLiab BIGINT,
    commonStock BIGINT,
    retainedEarnings BIGINT,
    treasuryStock BIGINT,
    otherStockholderEquity BIGINT,
    totalStockholderEquity BIGINT,
    netTangibleAssets BIGINT,
    FOREIGN KEY ( id ) REFERENCES SummaryProfile( id )
);
'''

create_table_historico_dadosfinanceiros = '''
CREATE TABLE IF NOT EXISTS financial_data (
    id int ,                           -- ID único do registro
    empresa_id INT NOT NULL,                         -- Chave estrangeira para a tabela 'empresas'
    current_price DECIMAL(10, 2),                    -- Preço atual
    target_high_price DECIMAL(10, 2),                -- Preço alvo alto
    target_low_price DECIMAL(10, 2),                 -- Preço alvo baixo
    target_mean_price DECIMAL(10, 2),                -- Preço alvo médio
    target_median_price DECIMAL(10, 2),              -- Preço alvo mediano
    recommendation_mean DECIMAL(3, 2),               -- Recomendação média (em formato decimal)
    recommendation_key VARCHAR(10),                   -- Recomendação (ex: 'buy', 'hold', 'sell')
    number_of_analyst_opinions INT,                   -- Número de opiniões de analistas
    total_cash BIGINT,                               -- Caixa total
    total_cash_per_share DECIMAL(10, 2),             -- Caixa total por ação
    ebitda BIGINT,                                   -- EBITDA (Lucro antes de juros, impostos, depreciação e amortização)
    total_debt BIGINT,                               -- Dívida total
    quick_ratio DECIMAL(5, 3),                       -- Liquidez imediata
    current_ratio DECIMAL(5, 3),                     -- Liquidez corrente
    total_revenue BIGINT,                            -- Receita total
    debt_to_equity DECIMAL(5, 2),                    -- Dívida / Patrimônio líquido
    revenue_per_share DECIMAL(10, 2),                -- Receita por ação
    return_on_assets DECIMAL(10, 8),                 -- Retorno sobre ativos
    return_on_equity DECIMAL(10, 8),                 -- Retorno sobre patrimônio líquido
    gross_profits BIGINT,                            -- Lucro bruto
    free_cashflow BIGINT,                            -- Fluxo de caixa livre
    operating_cashflow BIGINT,                       -- Fluxo de caixa operacional
    earnings_growth DECIMAL(5, 3),                   -- Crescimento dos lucros
    revenue_growth DECIMAL(5, 3),                    -- Crescimento da receita
    gross_margins DECIMAL(10, 8),                    -- Margem bruta
    ebitda_margins DECIMAL(10, 8),                    -- Margem EBITDA
    operating_margins DECIMAL(10, 8),                -- Margem operacional
    profit_margins DECIMAL(10, 8),                   -- Margem de lucro
    financial_currency VARCHAR(3),                   -- Moeda (ex: 'BRL', 'USD')
    FOREIGN KEY ( id ) REFERENCES SummaryProfile( id )
);
'''

# criar tabelas no DW
create_schema= '''
CREATE SCHEMA IF NOT EXISTS dw;

'''

create_table_query_historicodw = '''
CREATE TABLE IF NOT EXISTS dw.HistoricoPrecos (
    id INT,
    date BIGINT,  -- Armazena a data como um timestamp
    open DECIMAL(10, 2),
    high DECIMAL(10, 2),
    low DECIMAL(10, 2),
    close DECIMAL(10, 2),
    volume BIGINT,
    adjustedClose DECIMAL(10, 2),
    FOREIGN KEY (id) REFERENCES SummaryProfile(id)
);
'''
create_table_query_summarydw = '''
CREATE TABLE IF NOT EXISTS dw.SummaryProfile (
    id INT PRIMARY KEY,
    address1 VARCHAR(255),
    address2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(2),
    zip VARCHAR(10),
    country VARCHAR(100),
    website VARCHAR(255),
    industry VARCHAR(100),
    industryKey VARCHAR(50),
    industryDisp VARCHAR(100),
    sector VARCHAR(100),
    sectorKey VARCHAR(50),
    sectorDisp VARCHAR(100),
    longBusinessSummary TEXT
);
'''
create_table_historico_indicadoresdw = '''
CREATE TABLE  IF NOT EXISTS dw.indicadores (
    id int ,
    endDate integer,
    cash BIGINT,
    shortTermInvestments BIGINT,
    netReceivables BIGINT,
    inventory BIGINT,
    otherCurrentAssets BIGINT,
    totalCurrentAssets BIGINT,
    longTermInvestments BIGINT,
    propertyPlantEquipment BIGINT,
    goodWill BIGINT,
    intangibleAssets BIGINT,
    otherAssets BIGINT,
    deferredLongTermAssetCharges BIGINT,
    totalAssets BIGINT,
    accountsPayable BIGINT,
    shortLongTermDebt BIGINT,
    otherCurrentLiab BIGINT,
    longTermDebt BIGINT,
    otherLiab BIGINT,
    minorityInterest BIGINT,
    totalCurrentLiabilities BIGINT,
    totalLiab BIGINT,
    commonStock BIGINT,
    retainedEarnings BIGINT,
    treasuryStock BIGINT,
    otherStockholderEquity BIGINT,
    totalStockholderEquity BIGINT,
    netTangibleAssets BIGINT,
    FOREIGN KEY ( id ) REFERENCES SummaryProfile( id )
);
'''

create_table_historico_dadosfinanceirosdw = '''
CREATE TABLE IF NOT EXISTS dw.financial_data (
    id int ,                           -- ID único do registro
    empresa_id INT NOT NULL,                         -- Chave estrangeira para a tabela 'empresas'
    current_price DECIMAL(10, 2),                    -- Preço atual
    target_high_price DECIMAL(10, 2),                -- Preço alvo alto
    target_low_price DECIMAL(10, 2),                 -- Preço alvo baixo
    target_mean_price DECIMAL(10, 2),                -- Preço alvo médio
    target_median_price DECIMAL(10, 2),              -- Preço alvo mediano
    recommendation_mean DECIMAL(3, 2),               -- Recomendação média (em formato decimal)
    recommendation_key VARCHAR(10),                   -- Recomendação (ex: 'buy', 'hold', 'sell')
    number_of_analyst_opinions INT,                   -- Número de opiniões de analistas
    total_cash BIGINT,                               -- Caixa total
    total_cash_per_share DECIMAL(10, 2),             -- Caixa total por ação
    ebitda BIGINT,                                   -- EBITDA (Lucro antes de juros, impostos, depreciação e amortização)
    total_debt BIGINT,                               -- Dívida total
    quick_ratio DECIMAL(5, 3),                       -- Liquidez imediata
    current_ratio DECIMAL(5, 3),                     -- Liquidez corrente
    total_revenue BIGINT,                            -- Receita total
    debt_to_equity DECIMAL(5, 2),                    -- Dívida / Patrimônio líquido
    revenue_per_share DECIMAL(10, 2),                -- Receita por ação
    return_on_assets DECIMAL(10, 8),                 -- Retorno sobre ativos
    return_on_equity DECIMAL(10, 8),                 -- Retorno sobre patrimônio líquido
    gross_profits BIGINT,                            -- Lucro bruto
    free_cashflow BIGINT,                            -- Fluxo de caixa livre
    operating_cashflow BIGINT,                       -- Fluxo de caixa operacional
    earnings_growth DECIMAL(5, 3),                   -- Crescimento dos lucros
    revenue_growth DECIMAL(5, 3),                    -- Crescimento da receita
    gross_margins DECIMAL(10, 8),                    -- Margem bruta
    ebitda_margins DECIMAL(10, 8),                    -- Margem EBITDA
    operating_margins DECIMAL(10, 8),                -- Margem operacional
    profit_margins DECIMAL(10, 8),                   -- Margem de lucro
    financial_currency VARCHAR(3),                   -- Moeda (ex: 'BRL', 'USD')
    FOREIGN KEY ( id ) REFERENCES SummaryProfile( id )
);

'''


# Função para inserir dados no banco de dados
def inserir_dados_historico(**kwargs):
    response = requests.get(url, params=params)

  
    conn = connect(
        dbname="ETL",
        user="airflow",
        password="airflow",
        host="postgres",
        port="5432"
    )
    cursor = conn.cursor()

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        if results:
            historical_data = results[0].get('historicalDataPrice', [])
            summary_id = 1 

            for entry in historical_data:
                date = entry.get('date', 0)
                open_price = entry.get('open', 0.0)
                high_price = entry.get('high', 0.0)
                low_price = entry.get('low', 0.0)
                close_price = entry.get('close', 0.0)
                volume = entry.get('volume', 0)
                adjusted_close = entry.get('adjustedClose', 0.0)

               
                insert_query = '''
                INSERT INTO HistoricoPrecos (
                    id, date, open, high, low, close, volume, adjustedClose
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(insert_query, (
                    summary_id, date, open_price, high_price, low_price,
                    close_price, volume, adjusted_close
                ))

            conn.commit()
        else:
            print("A lista de resultados está vazia.")
    else:
        print(f"Request failed with status code {response.status_code}")

    cursor.close()
    conn.close()


def inserir_dados_indicadores(**kwargs):
    response = requests.get(url, params=params)

  
    conn = connect(
        dbname="ETL",
        user="airflow",
        password="airflow",
        host="postgres",
        port="5432"
    )
    cursor = conn.cursor()

    if response.status_code == 200:
        data = response.json()  
        results = data.get('results', [])
        
        if results:
            historical_data = results[0].get('historicalDataPrice', [])
            summary_id = 1  

            for entry in historical_data:
                endDate = entry.get('date', 0)  
                cash = entry.get('cash', 0)
                shortTermInvestments = entry.get('shortTermInvestments', 0)
                netReceivables = entry.get('netReceivables', 0)
                inventory = entry.get('inventory', 0)
                otherCurrentAssets = entry.get('otherCurrentAssets', 0)
                totalCurrentAssets = entry.get('totalCurrentAssets', 0)
                longTermInvestments = entry.get('longTermInvestments', 0)
                propertyPlantEquipment = entry.get('propertyPlantEquipment', 0)
                goodWill = entry.get('goodWill', 0)
                intangibleAssets = entry.get('intangibleAssets', 0)
                otherAssets = entry.get('otherAssets', 0)
                deferredLongTermAssetCharges = entry.get('deferredLongTermAssetCharges', 0)
                totalAssets = entry.get('totalAssets', 0)
                accountsPayable = entry.get('accountsPayable', 0)
                shortLongTermDebt = entry.get('shortLongTermDebt', 0)
                otherCurrentLiab = entry.get('otherCurrentLiab', 0)
                longTermDebt = entry.get('longTermDebt', 0)
                otherLiab = entry.get('otherLiab', 0)
                minorityInterest = entry.get('minorityInterest', 0)
                totalCurrentLiabilities = entry.get('totalCurrentLiabilities', 0)
                totalLiab = entry.get('totalLiab', 0)
                commonStock = entry.get('commonStock', 0)
                retainedEarnings = entry.get('retainedEarnings', 0)
                treasuryStock = entry.get('treasuryStock', 0)
                otherStockholderEquity = entry.get('otherStockholderEquity', 0)
                totalStockholderEquity = entry.get('totalStockholderEquity', 0)
                netTangibleAssets = entry.get('netTangibleAssets', 0)


              
                insert_query = '''
                INSERT INTO indicadores (
                    id, endDate, cash, shortTermInvestments, netReceivables, inventory, otherCurrentAssets,
                    totalCurrentAssets, longTermInvestments, propertyPlantEquipment, goodWill, intangibleAssets,
                    otherAssets, deferredLongTermAssetCharges, totalAssets, accountsPayable, shortLongTermDebt,
                    otherCurrentLiab, longTermDebt, otherLiab, minorityInterest, totalCurrentLiabilities, totalLiab,
                    commonStock, retainedEarnings, treasuryStock, otherStockholderEquity, totalStockholderEquity,
                    netTangibleAssets
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''

                cursor.execute(insert_query, (
                    summary_id, 
                    endDate,  
                    cash, shortTermInvestments, netReceivables, inventory, otherCurrentAssets, totalCurrentAssets,
                    longTermInvestments, propertyPlantEquipment, goodWill, intangibleAssets, otherAssets,
                    deferredLongTermAssetCharges, totalAssets, accountsPayable, shortLongTermDebt, otherCurrentLiab,
                    longTermDebt, otherLiab, minorityInterest, totalCurrentLiabilities, totalLiab, commonStock,
                    retainedEarnings, treasuryStock, otherStockholderEquity, totalStockholderEquity, netTangibleAssets
                ))

            conn.commit()
        else:
            print("A lista de resultados está vazia.")
    else:
        print(f"Request failed with status code {response.status_code}")

    cursor.close()
    conn.close()

def inserir_dados_summary(**kwargs):
    response = requests.get(url, params=params)

   
    conn = connect(
        dbname="ETL",
        user="airflow",
        password="airflow",
        host="postgres",
        port="5432"
    )
    cursor = conn.cursor()
    data = response.json()  

    results = data.get('results', [])
    if results:
        summary_profile = results[0].get('summaryProfile', {})
        summary_id = 1 
        # Extração dos dados do perfil
        address1 = summary_profile.get('address1', '')
        address2 = summary_profile.get('address2', '')
        city = summary_profile.get('city', '')
        state = summary_profile.get('state', '')
        zip_code = summary_profile.get('zip', '')
        country = summary_profile.get('country', '')
        website = summary_profile.get('website', '')
        industry = summary_profile.get('industry', '')
        industry_key = summary_profile.get('industryKey', '')
        industry_disp = summary_profile.get('industryDisp', '')
        sector = summary_profile.get('sector', '')
        sector_key = summary_profile.get('sectorKey', '')
        sector_disp = summary_profile.get('sectorDisp', '')
        long_business_summary = summary_profile.get('longBusinessSummary', '')

     
        insert_query = '''
        INSERT INTO SummaryProfile (
            id,address1, address2, city, state, zip, country,
            website, industry, industryKey,
            industryDisp, sector, sectorKey, sectorDisp,
            longBusinessSummary
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        cursor.execute(insert_query, (
            summary_id,address1, address2, city, state, zip_code, country,
            website, industry, industry_key,
            industry_disp, sector, sector_key, sector_disp,
            long_business_summary
        ))

        
        conn.commit()
        print("Dados do SummaryProfile inseridos com sucesso!")
    


        cursor.close()
        conn.close()




# Definir o DAG
dag = DAG(
    'criar_tabelas',
    default_args={
        'owner': 'airflow',
        'retries': 1,
        'retry_delay': datetime.timedelta(minutes=1),
    },
    description='DAG para inserir dados históricos de uma API no PostgreSQL',
    schedule_interval=None,  
    start_date=datetime.datetime(2024, 11, 5),  
    catchup=False, 
)


create_table_query_historico = PostgresOperator(
    task_id='create_table_historico',
    postgres_conn_id='postgres-airflow',  
    sql=create_table_query_historico,  
    dag=dag,
)
create_table_query_summary = PostgresOperator(
    task_id='create_table_query_summary',
    postgres_conn_id='postgres-airflow',  
    sql=create_table_query_summary,  
    dag=dag,
)
create_table_historico_indicadores = PostgresOperator(
    task_id='create_table_historico_indicadores',
    postgres_conn_id='postgres-airflow',  
    sql=create_table_historico_indicadores,  
    dag=dag,
)
create_table_historico_dadosfinanceiros = PostgresOperator(
    task_id='create_table_historico_dadosfinanceiros',
    postgres_conn_id='postgres-airflow',  
    sql=create_table_historico_dadosfinanceiros,  
    dag=dag,
)
########### definir task do dw

create_table_query_historicodw = PostgresOperator(
    task_id='create_table_historicodw',
    postgres_conn_id='postgres-airflow',  
    sql=create_table_query_historicodw,  
    dag=dag,
)
create_table_query_summarydw = PostgresOperator(
    task_id='create_table_query_summarydw',
    postgres_conn_id='postgres-airflow',  
    sql=create_table_query_summarydw,  
    dag=dag,
)
create_table_historico_indicadoresdw = PostgresOperator(
    task_id='create_table_historico_indicadoresdw',
    postgres_conn_id='postgres-airflow',  
    sql=create_table_historico_indicadoresdw,  
    dag=dag,
)
create_table_historico_dadosfinanceirosdw = PostgresOperator(
    task_id='create_table_historico_dadosfinanceirosdw',
    postgres_conn_id='postgres-airflow',  
    sql=create_table_historico_dadosfinanceirosdw,  
    dag=dag,
)

create_schema = PostgresOperator(
    task_id='create_schema',
    postgres_conn_id='postgres-airflow',  
    sql=create_schema,  
    dag=dag,
)



inserir_dados_task = PythonOperator(
    task_id='inserir_dados_historico',
    python_callable=inserir_dados_historico,
    provide_context=True,
    dag=dag,
)

inserir_dados_indicadores_task = PythonOperator(
    task_id='inserir_dados_indicadores',
    python_callable=inserir_dados_indicadores,
    provide_context=True,
    dag=dag,
)
inserir_dados_summary = PythonOperator(
    task_id='inserir_dados_summary',
    python_callable=inserir_dados_summary,
    provide_context=True,
    dag=dag,
)


create_table_query_summary  >> create_table_query_historico >> create_table_historico_indicadores >> create_table_historico_dadosfinanceiros >> create_schema >> create_table_query_summarydw  >> create_table_query_historicodw >> create_table_historico_indicadoresdw >> create_table_historico_dadosfinanceirosdw >> inserir_dados_summary >> inserir_dados_task >> inserir_dados_indicadores_task 
