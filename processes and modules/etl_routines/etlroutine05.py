import pandas as pd
import numpy as np
from plconfig import MachineInfo as machine_info
from datetimetools import Alternative_date_variables as ad
from verifiers import send_message

machine_info = machine_info()
try: 
    vendas_por_sku  = r'G:'+machine_info.pathlang0+r'\Data & Performance\Relatórios\2 - SUPPLY DASHBOARD\Bases Metabase\venda_por_sku_diario_'+str(ad().year_month)+r'.csv'
    master_catalogo = r'G:'+machine_info.pathlang0+r'\Data & Performance\Relatórios\0 - BASES UNIVERSAIS\Master Catálogo - Brasil.xlsx'
    destination = r'G:'+machine_info.pathlang0+r'\Data & Performance\Relatórios Justo Insights\UNILEVER\unilever_'+str(ad().year_month)+r'.csv'
    df1 = pd.read_csv(vendas_por_sku)
    df1 = df1[
        [
            "Delivery_date",
            "Product_id",
            "GMV",
            "Order_Status",
            "Qty_Ordered",
            "price",
            "order_creation_date",
            "discount_percentage"        
        ]
    ]
    df2 = df1[["Product_id"]]
    df2 = df2.drop_duplicates(subset=["Product_id"])
    df3 = pd.read_excel(master_catalogo)
    df3.columns = df3.iloc[1]
    df3 = df3.drop([0, 1, 2])
    df3 = df3.reset_index(drop=True)
    df3 = df3[["Código SKU", "Nome do Item", "EAN 13", "Fabricante"]]
    df3 = df3.sort_values("Código SKU")
    df3 = df3.drop_duplicates(subset=["Código SKU"])
    df2 = df2.reset_index(drop=True)
    df4 = pd.merge(df2, df3, how="left", left_on=["Product_id"], right_on=["Código SKU"])
    df4 = df4[["Product_id", "Nome do Item", "EAN 13", "Fabricante"]]
    df5 = pd.merge(df1, df4, how="left", left_on=["Product_id"], right_on=["Product_id"])
    df5["Manufacturer"] = np.where(
        df5["Fabricante"] == "UNILEVER", "UNILEVER", "Other Manufacturer"
    )
    df5["Item_name"] = np.where(
        df5["Fabricante"] == "UNILEVER", df5["Nome do Item"], "Other Manufacturer"
    )
    df5 = df5[
        [
            "Delivery_date",
            "Product_id",
            "GMV",
            "Order_Status",
            "price",
            "Qty_Ordered",
            "order_creation_date",
            "discount_percentage",
            "EAN 13",
            "Manufacturer",
            "Item_name",
        ]
    ]
    df5 = df5.rename(columns={"price": "Price"})
    df5 = df5.rename(columns={"order_creation_date": "Order_creation_date"})
    df5 = df5.rename(columns={"discount_percentage": "Discount_percentage"})
    df5 = df5.rename(columns={"EAN 13": "EAN"})
    df5.to_csv(destination, index=False)
except:
    emsg='<!channel> Error while doing the Unilever sales ETL (etl5).'
    print(emsg)
    send_message(emsg,'#bot_channel')