# db_utils.py
import pandas as pd
from sqlalchemy import create_engine
import os

def get_engine(user, password, host, db_name):
    engine_str = f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}"
    return create_engine(engine_str)

def load_and_insert_csv(csv_path, table_name, db_user, db_password, db_host, db_name):
    try:
        from sqlalchemy import create_engine
        import pandas as pd
        import os

        if not os.path.exists(csv_path):
            print(f"❌ File not found: {csv_path}")
            return

        # ✅ NEW ENGINE PER INSERT
        engine_str = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
        engine = create_engine(engine_str)

        df = pd.read_csv(csv_path)
        df = df.loc[:, ~df.columns.isna()]
        df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("-", "_")

        df.to_sql(table_name, con=engine, if_exists="append", index=False)
        print(f"✅ Inserted into `{table_name}` ({len(df)} rows)")
    except Exception as e:
        print(f"❌ Error inserting into `{table_name}`:", e)
