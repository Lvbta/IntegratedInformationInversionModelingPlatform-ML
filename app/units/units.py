import logging

import numpy as np
from hyperopt import hp


def create_hyperopt_space(param_space):
    space = {}
    for param, settings in param_space.items():
        try:
            logging.info(f"Processing parameter '{param}' with settings: {settings}")

            if settings.startswith('range'):
                settings = settings.strip('range()')
                parts = settings.split(',')
                if len(parts) == 3:
                    start, stop, step = map(int, parts)
                    space[param] = hp.quniform(param, start, stop, step)
                else:
                    raise ValueError(f"Expected 3 values for 'range', got {len(parts)}")
            elif settings.startswith('loguniform'):
                settings = settings.strip('loguniform()')
                parts = settings.split(',')
                if len(parts) == 2:
                    min_val, max_val = map(float, parts)
                    space[param] = hp.loguniform(param, np.log(min_val), np.log(max_val))
                else:
                    raise ValueError(f"Expected 2 values for 'loguniform', got {len(parts)}")
            elif settings.startswith('uniform'):
                settings = settings.strip('uniform()')
                parts = settings.split(',')
                if len(parts) == 2:
                    min_val, max_val = map(float, parts)
                    space[param] = hp.uniform(param, min_val, max_val)
                else:
                    raise ValueError(f"Expected 2 values for 'uniform', got {len(parts)}")
            elif settings.startswith('choice'):
                settings = settings.strip('choice([').strip('])')
                options = settings.split(', ')
                space[param] = hp.choice(param, [opt.strip("'") for opt in options])
            else:
                raise ValueError(f"Unknown settings format for parameter '{param}': {settings}")
        except Exception as e:
            logging.error(f"Error creating hyperopt space for parameter '{param}': {e}")
            raise
    return space


# Convert numpy types to standard Python types
def convert_np_types(obj):
    if isinstance(obj, dict):
        return {k: convert_np_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_np_types(i) for i in obj]
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.int64):
        return int(obj)
    elif isinstance(obj, np.float64):
        return float(obj)
    else:
        return obj


def create_time_series_data(df, independent_vars, dependent_var, time_steps):
    X, y = [], []
    for i in range(len(df) - time_steps):
        X.append(df[independent_vars].iloc[i:i + time_steps].values)
        y.append(df[dependent_var].iloc[i + time_steps])
    return np.array(X), np.array(y)