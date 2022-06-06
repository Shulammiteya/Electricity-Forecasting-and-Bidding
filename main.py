import pandas as pd
import numpy as np
import traceback
import logging
from keras.models import load_model
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler


scaler = StandardScaler(with_mean=False)

def normalize(data):
  return scaler.fit_transform(data)

def inverse_normalize(data):
  return scaler.inverse_transform(data)

# You should not modify this part.
def config():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="./sample_data/consumption.csv", help="input the consumption data path")
    parser.add_argument("--generation", default="./sample_data/generation.csv", help="input the generation data path")
    parser.add_argument("--bidresult", default="./sample_data/bidresult.csv", help="input the bids result path")
    parser.add_argument("--output", default="output.csv", help="output the bids path")

    return parser.parse_args()


def output(path, data):
    import pandas as pd

    df = pd.DataFrame(data, columns=["time", "action", "target_price", "target_volume"])
    df.to_csv(path, index=False)

    return


if __name__ == "__main__":
    args = config()

    try:
        model = load_model('./lstm.h5')
        df_consumption = pd.read_csv(args.consumption)
        df_generation = pd.read_csv(args.generation)
        df_generation['time'] = pd.to_datetime(df_generation['time'])

        df_input = pd.DataFrame()
        df_input['time'] = df_generation['time']
        df_input['diff'] = df_generation['generation'] - df_consumption['consumption']
        df_input['hour'] = [timestamp.hour for timestamp in df_input['time']]
        df_input['month'] = [timestamp.month for timestamp in df_input['time']]

        # Creating the cyclical daily feature
        df_input['hour_cos_index'] = [np.cos(x * (2 * np.pi / 24)) for x in df_input['hour']]
        df_input['hour_sin_index'] = [np.sin(x * (2 * np.pi / 24)) for x in df_input['hour']]

        # Creating the cyclical yearly feature
        sec_in_a_year = 365.25 * 24 * 60 * 60
        df_input['month_cos_index'] = [np.cos(x.timestamp() * (2 * np.pi / sec_in_a_year)) for x in df_input['time']]
        df_input['month_sin_index'] = [np.sin(x.timestamp() * (2 * np.pi / sec_in_a_year)) for x in df_input['time']]

        df_input.drop(['time', 'hour',	'month'], axis=1, inplace=True)
        df_input['diff'] = normalize( np.array(df_input['diff']).reshape(-1, 1) )

        pred = model.predict(df_input.to_numpy().reshape(-1, 168, 5))
        pred = inverse_normalize(pred).squeeze()

        data = []
        for i in range(24):
            if pred[i] > 0:
                data.append([df_generation.iloc[i]['time'] + timedelta(days=7), 'sell', 0.01, abs(pred[i])])
            else:
                data.append([df_generation.iloc[i]['time'] + timedelta(days=7), 'buy', 2.54, abs(pred)[i]])

    except Exception as e:
        logging.error(traceback.format_exc())
        data = []
    
    output(args.output, data)
