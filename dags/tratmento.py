import datetime
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
import psycopg2
from psycopg2 import connect


url = "https://brapi.dev/api/quote/PETR4,^BVSP"
params = {
    'range': '5y',
    'interval': '3mo',
    'modules': 'balanceSheetHistory',
    'token': 'nyvMfdacbcxr6kSDu8nfM1',
}


#############################################################################################################
def indicadores(**kwargs):

    import psycopg2
from psycopg2 import sql


conn = psycopg2.connect(
    dbname="etl",  
    user="airflow",  
    password="airflow",  
    host="localhost",  
    port="5432"  
)


cursor = conn.cursor()


query = """
    SELECT
        id,
        enddate,
        COALESCE(cash, 0) AS cash,
        COALESCE(shortterminvestments, 0) AS shortterminvestments,
        COALESCE(netreceivables, 0) AS netreceivables,
        COALESCE(inventory, 0) AS inventory,
        COALESCE(othercurrentassets, 0) AS othercurrentassets,
        COALESCE(totalcurrentassets, 0) AS totalcurrentassets,
        COALESCE(longterminvestments, 0) AS longterminvestments,
        COALESCE(propertyplantequipment, 0) AS propertyplantequipment,
        COALESCE(goodwill, 0) AS goodwill,
        COALESCE(intangibleassets, 0) AS intangibleassets,
        COALESCE(otherassets, 0) AS otherassets,
        COALESCE(deferredlongtermassetcharges, 0) AS deferredlongtermassetcharges,
        COALESCE(totalassets, 0) AS totalassets,
        COALESCE(accountspayable, 0) AS accountspayable,
        COALESCE(shortlongtermdebt, 0) AS shortlongtermdebt,
        COALESCE(othercurrentliab, 0) AS othercurrentliab,
        COALESCE(longtermdebt, 0) AS longtermdebt,
        COALESCE(otherliab, 0) AS otherliab,
        COALESCE(minorityinterest, 0) AS minorityinterest,
        COALESCE(totalcurrentliabilities, 0) AS totalcurrentliabilities,
        COALESCE(totalliab, 0) AS totalliab,
        COALESCE(commonstock, 0) AS commonstock,
        COALESCE(retainedearnings, 0) AS retainedearnings,
        COALESCE(treasurystock, 0) AS treasurystock,
        COALESCE(otherstockholderequity, 0) AS otherstockholderequity,
        COALESCE(totalstockholderequity, 0) AS totalstockholderequity,
        COALESCE(nettangibleassets, 0) AS nettangibleassets
    FROM public.indicadores;
"""


cursor.execute(query)


rows = cursor.fetchall()


insert_query = """
    INSERT INTO dw.indicadores (
        id,
        enddate,
        cash,
        shortterminvestments,
        netreceivables,
        inventory,
        othercurrentassets,
        totalcurrentassets,
        longterminvestments,
        propertyplantequipment,
        goodwill,
        intangibleassets,
        otherassets,
        deferredlongtermassetcharges,
        totalassets,
        accountspayable,
        shortlongtermdebt,
        othercurrentliab,
        longtermdebt,
        otherliab,
        minorityinterest,
        totalcurrentliabilities,
        totalliab,
        commonstock,
        retainedearnings,
        treasurystock,
        otherstockholderequity,
        totalstockholderequity,
        nettangibleassets
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

conn.commit()


cursor.close()
conn.close()
###############################################################################################
def summary(**kwargs):

     conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Criar a tabela no schema 'dw'
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS dw.summaryprofile
        (
            id integer NOT NULL,
            address1 character varying(255),
            address2 character varying(255),
            city character varying(100),
            state character varying(2),
            zip character varying(10),
            country character varying(100),
            website character varying(255),
            industry character varying(100),
            industrykey character varying(50),
            industrydisp character varying(100),
            sector character varying(100),
            sectorkey character varying(50),
            sectordisp character varying(100),
            longbusinesssummary text,
            CONSTRAINT summaryprofile_pkey PRIMARY KEY (id)
        );
        '''
        cursor.execute(create_table_query)
        conn.commit()

        # Copiar e tratar os dados da tabela 'public.summaryprofile' para 'dw.summaryprofile'
        copy_data_query = '''
        INSERT INTO dw.summaryprofile (
            id, address1, address2, city, state, zip, country, website,
            industry, industrykey, industrydisp, sector, sectorkey, sectordisp, longbusinesssummary
        )
        SELECT
            id,
            COALESCE(address1, '0') AS address1,  -- Tratamento para NULL
            COALESCE(address2, '0') AS address2,  -- Tratamento para NULL
            COALESCE(city, '0') AS city,          -- Tratamento para NULL
            COALESCE(state, '0') AS state,        -- Tratamento para NULL
            COALESCE(zip, '0') AS zip,            -- Tratamento para NULL
            COALESCE(country, '0') AS country,    -- Tratamento para NULL
            COALESCE(website, '0') AS website,    -- Tratamento para NULL
            COALESCE(industry, '0') AS industry,  -- Tratamento para NULL
            COALESCE(industrykey, '0') AS industrykey,  -- Tratamento para NULL
            COALESCE(industrydisp, '0') AS industrydisp,  -- Tratamento para NULL
            COALESCE(sector, '0') AS sector,      -- Tratamento para NULL
            COALESCE(sectorkey, '0') AS sectorkey,  -- Tratamento para NULL
            COALESCE(sectordisp, '0') AS sectordisp,  -- Tratamento para NULL
            COALESCE(longbusinesssummary, '0') AS longbusinesssummary  -- Tratamento para NULL
        FROM public.summaryprofile;
        '''
        cursor.execute(copy_data_query)
        conn.commit()

        print("Dados migrados com sucesso!")

    except Exception as error:
        print(f"Erro: {error}")
        conn.rollback()

    finally:
        # Fechar a conexão
        cursor.close()
        conn.close()

# Executar a função para migrar os dados
indicadores()
#############################################################################################################################
def hisrorico(**kwargs):
    db_config = {
    'dbname': 'etl',  
    'user': 'airflow',  
    'password': 'airflow',  
    'host': 'localhost',  
    'port': '5432'  

    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        
        query = """
        INSERT INTO dw.historicoprecos (
            id,
            date,
            open,
            high,
            low,
            close,
            volume,
            adjustedclose
        )
        SELECT 
            id,
            -- Convertendo 'date' de bigint para timestamp
            to_timestamp(date),
            -- Substituindo NULL por 0
            COALESCE(open, 0) AS open,
            COALESCE(high, 0) AS high,
            COALESCE(low, 0) AS low,
            COALESCE(close, 0) AS close,
            COALESCE(volume, 0) AS volume,
            COALESCE(adjustedclose, 0) AS adjustedclose
        FROM public.historicoprecos;
        """

        
        cursor.execute(query)
        connection.commit()  

        print("Dados transferidos com sucesso!")

    except Exception as e:
        print(f"Erro ao transferir dados: {e}")
        connection.rollback()  

    finally:
        cursor.close()
        connection.close()


#################################################################################################################
def financial(**kwargs):
    
conn = psycopg2.connect(
    dbname="etl",
    user="airflow",
    password="airflow",
    host="localhost",
    port="5432"
)


cursor = conn.cursor()


create_table_query = """
    CREATE TABLE IF NOT EXISTS dw.financial_data (
        id integer,
        empresa_id integer NOT NULL,
        current_price numeric(10,2) DEFAULT 0,
        target_high_price numeric(10,2) DEFAULT 0,
        target_low_price numeric(10,2) DEFAULT 0,
        target_mean_price numeric(10,2) DEFAULT 0,
        target_median_price numeric(10,2) DEFAULT 0,
        recommendation_mean numeric(3,2) DEFAULT 0,
        recommendation_key character varying(10) COLLATE pg_catalog."default" DEFAULT '',
        number_of_analyst_opinions integer DEFAULT 0,
        total_cash bigint DEFAULT 0,
        total_cash_per_share numeric(10,2) DEFAULT 0,
        ebitda bigint DEFAULT 0,
        total_debt bigint DEFAULT 0,
        quick_ratio numeric(5,3) DEFAULT 0,
        current_ratio numeric(5,3) DEFAULT 0,
        total_revenue bigint DEFAULT 0,
        debt_to_equity numeric(5,2) DEFAULT 0,
        revenue_per_share numeric(10,2) DEFAULT 0,
        return_on_assets numeric(10,8) DEFAULT 0,
        return_on_equity numeric(10,8) DEFAULT 0,
        gross_profits bigint DEFAULT 0,
        free_cashflow bigint DEFAULT 0,
        operating_cashflow bigint DEFAULT 0,
        earnings_growth numeric(5,3) DEFAULT 0,
        revenue_growth numeric(5,3) DEFAULT 0,
        gross_margins numeric(10,8) DEFAULT 0,
        ebitda_margins numeric(10,8) DEFAULT 0,
        operating_margins numeric(10,8) DEFAULT 0,
        profit_margins numeric(10,8) DEFAULT 0,
        financial_currency character varying(3) COLLATE pg_catalog."default" DEFAULT ''
    );
"""
cursor.execute(create_table_query)


select_query = "SELECT * FROM public.financial_data"
cursor.execute(select_query)
rows = cursor.fetchall()


insert_query = """
    INSERT INTO dw.financial_data (
        id, empresa_id, current_price, target_high_price, target_low_price, 
        target_mean_price, target_median_price, recommendation_mean, 
        recommendation_key, number_of_analyst_opinions, total_cash, 
        total_cash_per_share, ebitda, total_debt, quick_ratio, 
        current_ratio, total_revenue, debt_to_equity, revenue_per_share, 
        return_on_assets, return_on_equity, gross_profits, free_cashflow, 
        operating_cashflow, earnings_growth, revenue_growth, gross_margins, 
        ebitda_margins, operating_margins, profit_margins, financial_currency
    ) VALUES (
        %s, %s, COALESCE(%s, 0), COALESCE(%s, 0), COALESCE(%s, 0), 
        COALESCE(%s, 0), COALESCE(%s, 0), COALESCE(%s, 0), 
        COALESCE(%s, ''), COALESCE(%s, 0), COALESCE(%s, 0), 
        COALESCE(%s, 0), COALESCE(%s, 0), COALESCE(%s, 0), COALESCE(%s, 0), 
        COALESCE(%s, 0), COALESCE(%s, 0), COALESCE(%s, 0), 
        COALESCE(%s, 0), COALESCE(%s, 0), COALESCE(%s, 0), 
        COALESCE(%s, 0), COALESCE(%s, 0), COALESCE(%s, 0), 
        COALESCE(%s, 0), COALESCE(%s, 0), COALESCE(%s, 0), COALESCE(%s, 0), COALESCE(%s, 0), COALESCE(%s, 0), %s
    );
"""


for row in rows:
    cursor.execute(insert_query, row)


conn.commit()


cursor.close()
conn.close()

#######################################################################################################################
dag = DAG(
    'tratamento',
    default_args={
        'owner': 'airflow',
        'retries': 1,
        'retry_delay': datetime.timedelta(minutes=1),
    },
    description='DAG para tratmento de indicadores  no PostgreSQL',
    schedule_interval=None,  
    start_date=datetime.datetime(2024, 11, 5),  
    catchup=False,  
)
#######################################################################################################################
summary = PythonOperator(
    task_id='tratar_summary',
    python_callable=summary,
    provide_context=True,
    dag=dag,
)

indicadores = PythonOperator(
    task_id='tratar_indicadores',
    python_callable=indicadores,
    provide_context=True,
    dag=dag,
)

hisrorico = PythonOperator(
    task_id='tratar_historico',
    python_callable=hisrorico,
    provide_context=True,
    dag=dag,
)

financial = PythonOperator(
    task_id='tratar_financial',
    python_callable=financial,
    provide_context=True,
    dag=dag,
)

summary >> hisrorico >> financial >> indicadores
