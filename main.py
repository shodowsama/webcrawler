from crawler import search_web
from config import Config
import pandas as pd


if __name__ == "__main__":
    result = search_web()
    df = pd.DataFrame(result)
    df.to_csv(Config.save_place,encoding='utf-8',index=False)







