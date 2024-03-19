import os
import pathlib

import pandas 

"""You are welcome to use this structure as a starting point, or you can start from scratch.

The prefixed `get_` methods should not need any adjustment to read in the data.
Your solutions should be mostly contained within the prefixed `generate_` methods, and the `data_investigation()`

"""

# --- Fill in your details here ---
FIRST_NAME = "Hoa"
LAST_NAME = "Le"

# Gets current path
CURRENT_DIR = pathlib.Path(__file__).parent
DATA_DIR = os.path.join(CURRENT_DIR, "data")


def get_exchange_data():
    exchange_data = pandas.read_csv(
        os.path.join(DATA_DIR, "exchange.data"),
        delimiter="|",
    )
    return exchange_data


def get_stock_list():
    stock_list = pandas.read_csv(os.path.join(DATA_DIR, "stock.data"))
    return stock_list


def get_security_master():
    security_master = pandas.read_csv(
        os.path.join(DATA_DIR, "strong_oak_security_master.csv")
    )
    return security_master


def get_attributes():
    attributes = pandas.read_csv(os.path.join(DATA_DIR, "attributes.data"))
    return attributes


def generate_security_upload(
    security_master, full_stock_data, exchange_data
) -> pandas.DataFrame:
    
    security_master = security_master[~((security_master['Ticker'].isna()) & (security_master['QUEUESIP'].isna()))]

    security_master_t = security_master[(~security_master['Ticker'].isna()) & (security_master['QUEUESIP'].isna())]
    full_stock_data_s = full_stock_data[~((full_stock_data['Symbol'].isna()) & (~full_stock_data['QUEUESIP'].isna()))]

    security_master_q = security_master[(security_master['Ticker'].isna()) & (~security_master['QUEUESIP'].isna())]
    full_stock_data_q = full_stock_data[~((~full_stock_data['Symbol'].isna()) & (full_stock_data['QUEUESIP'].isna()))]

    security_master_tq = security_master[(~security_master['Ticker'].isna()) & (~security_master['QUEUESIP'].isna())]

    security_master_tm = pandas.merge(security_master_t, full_stock_data_s, left_on='Ticker', right_on='Symbol', how='inner')
    security_master_qm = pandas.merge(security_master_q, full_stock_data_q, on='QUEUESIP', how='inner')
    security_master_tqm = pandas.merge(security_master_tq, full_stock_data_q, on='QUEUESIP', how='inner')

    security_master_tm = security_master_tm[['MIC', 'QUEUESIP_y', 'Symbol', 'RequestId','Strong Oak Identifier']]
    security_master_tm.rename(columns={'QUEUESIP_y': 'QUEUESIP'}, inplace=True)

    security_master_qm = security_master_qm[['MIC', 'QUEUESIP', 'Symbol', 'RequestId','Strong Oak Identifier']]

    security_master_tqm = security_master_tqm[['MIC', 'QUEUESIP', 'Ticker', 'RequestId','Strong Oak Identifier']]
    security_master_tqm.rename(columns={'Ticker': 'Symbol'}, inplace=True)

    security_master_m = pandas.concat([security_master_tm, security_master_qm, security_master_tqm], axis=0)
    security_master_m.insert(0, 'EulerId', range(1, len(security_master_m) + 1))

    return security_master_m


def generate_attribute_upload(
    security_upload, attribute_data, full_stock_data, exchange_data
) -> pandas.DataFrame:
    final_merged = pandas.merge(security_upload, attribute_data, on="RequestId", how="left").merge(exchange_data, on="MIC", how="left")
    final_merged["Exchange Location"] = final_merged["domicile"] + "-" + final_merged["city"]
    final_merged.rename(columns={"name": "Exchange Name"}, inplace=True)
    final_merged = final_merged[[
        "EulerId", "Asset Class", "Inception Date", "Exchange Name", "Exchange Location", "Security Name",
        "Strong Oak Identifier", "Return Since Inception"
    ]]
    final_attribute = final_merged.melt(id_vars='EulerId', var_name='AttributeName', value_name='AttributeValue').dropna(subset=['AttributeValue'])

    return final_attribute


def data_investigation(security_upload, attribute_upload):
    pass


def main():
    security_master = get_security_master()
    full_stock_data = get_stock_list()
    exchange_data = get_exchange_data()

    # * Loading Securities into the platform * #

    # get security data...
    security_upload = generate_security_upload(
        security_master=security_master,
        full_stock_data=full_stock_data,
        exchange_data=exchange_data,
    )

    # * Uploading Attributes * #

    attribute_data = get_attributes()

    # get attribute data...
    attribute_upload = generate_attribute_upload(
        security_upload=security_upload,
        attribute_data=attribute_data,
        full_stock_data=full_stock_data,
        exchange_data=exchange_data,
    )

    # solutions go here.

    security_upload.to_csv(
        os.path.join(CURRENT_DIR, f"{FIRST_NAME}_{LAST_NAME}_section1.csv")
    )
    attribute_upload.to_csv(
        os.path.join(CURRENT_DIR, f"{FIRST_NAME}_{LAST_NAME}_section2.csv")
    )

    data_investigation(
        security_upload=security_upload, attribute_upload=attribute_upload
    )


if __name__ == "__main__":
    main()