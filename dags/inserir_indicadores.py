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


def inserir_dados_indicadores(**kwargs):
    response = requests.get(url, params=params)

    
    conn = psycopg2.connect(
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
            summary_id = 8  

            for entry in historical_data:
                endDate = entry.get('date', '1970-01-01 00:00:00+00') 
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

                
                endDate = datetime.datetime.fromisoformat(endDate)  

                
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


def inserir_historrico_precos(**kwargs):
    response = requests.get(url, params=params)

    if response.status_code == 200:
    data = response.json()
    print(data)  

    results = data.get('results', [])
    print(results)
    if results:
        historical_data = results[0].get('historicalDataPrice', [])
        summary_id = 1  

        for entry in historical_data:
            
            name = "TRAD3"
            date = entry.get('date', 0)
            open_price = entry.get('open', 0.0)
            high_price = entry.get('high', 0.0)
            low_price = entry.get('low', 0.0)
            close_price = entry.get('close', 0.0)
            volume = entry.get('volume', 0)
            adjusted_close = entry.get('adjustedClose', 0.0)

            
            insert_query = '''
                INSERT INTO historicoprecos (
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

def inserir_dados_summary(**kwargs):
    response = requests.get(url, params=params)

    
    conn = connect(
        dbname="etl",
        user="airflow",
        password="airflow",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    data = response.json()  

    results = data.get('results', [])
    if results:
        summary_profile = results[0].get('summaryProfile', {})
        summary_id = 1 
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


def dadosfinanceiros(**kwargs):
    response = requests.get(url, params=params)

    if response.status_code == 200:
    data = response.json()
    results = data.get('results', [])
    print(results)

    if results:
        
        financial_data = results[0]  
        summary_id = 1  

        
        current_price = financial_data.get('regularMarketPrice', 0)
        target_high_price = financial_data.get('financialData', {}).get('targetHighPrice', 0)
        target_low_price = financial_data.get('financialData', {}).get('targetLowPrice', 0)
        target_mean_price = financial_data.get('financialData', {}).get('targetMeanPrice', 0)
        target_median_price = financial_data.get('financialData', {}).get('targetMedianPrice', 0)
        recommendation_mean = financial_data.get('financialData', {}).get('recommendationMean', 0)
        recommendation_key = financial_data.get('financialData', {}).get('recommendationKey', '')
        number_of_analyst_opinions = financial_data.get('financialData', {}).get('numberOfAnalystOpinions', 0)
        total_cash = financial_data.get('financialData', {}).get('totalCash', 0)
        total_cash_per_share = financial_data.get('financialData', {}).get('totalCashPerShare', 0)
        ebitda = financial_data.get('financialData', {}).get('ebitda', 0)
        total_debt = financial_data.get('financialData', {}).get('totalDebt', 0)
        quick_ratio = financial_data.get('financialData', {}).get('quickRatio', 0)
        current_ratio = financial_data.get('financialData', {}).get('currentRatio', 0)
        total_revenue = financial_data.get('financialData', {}).get('totalRevenue', 0)
        debt_to_equity = financial_data.get('financialData', {}).get('debtToEquity', 0)
        revenue_per_share = financial_data.get('financialData', {}).get('revenuePerShare', 0)
        return_on_assets = financial_data.get('financialData', {}).get('returnOnAssets', 0)
        return_on_equity = financial_data.get('financialData', {}).get('returnOnEquity', 0)
        gross_margins = financial_data.get('financialData', {}).get('grossMargins', 0)
        ebitda_margins = financial_data.get('financialData', {}).get('ebitdaMargins', 0)
        operating_margins = financial_data.get('financialData', {}).get('operatingMargins', 0)
        profit_margins = financial_data.get('financialData', {}).get('profitMargins', 0)
        financial_currency = financial_data.get('currency', '')

        
        conn = connect(
            dbname="etl",
            user="airflow",
            password="airflow",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        
        insert_query = '''
            INSERT INTO financial_data (
                empresa_id, current_price, target_high_price, target_low_price, target_mean_price,
                target_median_price, recommendation_mean, recommendation_key, number_of_analyst_opinions,
                total_cash, total_cash_per_share, ebitda, total_debt, quick_ratio, current_ratio, total_revenue,
                debt_to_equity, revenue_per_share, return_on_assets, return_on_equity, gross_margins, 
                ebitda_margins, operating_margins, profit_margins, financial_currency
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        # Inserir os dados na tabela
        cursor.execute(insert_query, (
            summary_id, current_price, target_high_price, target_low_price, target_mean_price,
            target_median_price, recommendation_mean, recommendation_key, number_of_analyst_opinions,
            total_cash, total_cash_per_share, ebitda, total_debt, quick_ratio, current_ratio, total_revenue,
            debt_to_equity, revenue_per_share, return_on_assets, return_on_equity, gross_margins,
            ebitda_margins, operating_margins, profit_margins, financial_currency
        ))

        
        conn.commit()

        print("Dados inseridos com sucesso.")
    else:
        print("A lista de resultados está vazia.")
else:
    print(f"Request failed with status code {response.status_code}")


cursor.close()
conn.close()



dag = DAG(
    'inserirdados',
    default_args={
        'owner': 'airflow',
        'retries': 1,
        'retry_delay': datetime.timedelta(minutes=1),
    },
    description='DAG para inserir dados indicadores de uma API no PostgreSQL',
    schedule_interval=None,  
    start_date=datetime.datetime(2024, 11, 5),  
    catchup=False,  
)


inserir_dados_indicadores_task = PythonOperator(
    task_id='inserir_dados_indicadores',
    python_callable=inserir_dados_indicadores,
    provide_context=True,
    dag=dag,
)
inserir_historrico_precos = PythonOperator(
    task_id='inserir_historico_precos',
    python_callable=inserir_historico_precos,
    provide_context=True,
    dag=dag,
)
inserir_dados_summary = PythonOperator(
    task_id='inserir_dados_summary',
    python_callable=inserir_dados_summary,
    provide_context=True,
    dag=dag,
)
dadosfinanceiros = PythonOperator(
    task_id='dadosfinancieros',
    python_callable=dadosfinanceiros,
    provide_context=True,
    dag=dag,
)



inserir_dados_summary >> inserir_dados_indicadores_task >> inserir_historrico_precos >> dadosfinanceiros
