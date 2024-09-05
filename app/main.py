import logging
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from hyperopt import fmin, tpe, Trials, STATUS_OK, rand

from app.units.data_Normlization import normalize_data, denormalize_data

import paddle
from paddle.nn import Sequential, LSTM, Linear, Dropout
import paddle.nn.functional as F

from units.units import create_hyperopt_space, convert_np_types
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('ggplot')



app = Flask(__name__)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}})


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Paths for storing data
UPLOAD_FOLDER = 'upload_data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create directory if it doesn't exist

# Global variable to store the file path and config
data_file_path = None
config = None

# Load config
try:
    with open('./config/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
except Exception as e:
    logging.error(f'Error loading config file: {e}')
    raise


@app.route('/upload', methods=['POST'])
def upload_file():
    global data_file_path

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    data_file_path = file_path  # Save the path to the global variable

    file_extension = data_file_path.split('.')[-1].lower()
    if file_extension == 'csv':
        df = pd.read_csv(data_file_path)
    elif file_extension in ['xls', 'xlsx']:
        df = pd.read_excel(data_file_path)

    # Remove rows with NaN or empty values
    df.dropna(inplace=True)

    preview = df.head(5).to_dict(orient='records')
    return jsonify(preview)


@app.route('/optimize_and_train', methods=['POST'])
def optimize_and_train():
    global data_file_path, config
    print(data_file_path)
    now = datetime.now()
    formatted_time = now.strftime('%Y%m%d_%H%M%S')

    if not data_file_path:
        return jsonify({'error': 'No data uploaded'}), 400

    json_data = request.get_json()
    model_type = json_data.get('model')
    process_Method = json_data.get('processMethod')
    independent_vars = json_data.get('independentVars')
    dependent_var = json_data.get('dependentVar')
    optimization_algorithm = json_data.get('optimizationAlgorithm', 'tpe')  # Default to TPE
    print(f'模型名称：{model_type}/n;优化算法：{optimization_algorithm};/n数据处理方式:{process_Method}/n;')

    if model_type not in config['models']:
        return jsonify({'error': 'Invalid model type'}), 400

    # Load the data from file
    try:
        file_extension = data_file_path.split('.')[-1].lower()
        if file_extension == 'csv':
            df = pd.read_csv(data_file_path)
        elif file_extension in ['xls', 'xlsx']:
            df = pd.read_excel(data_file_path)
        else:
            return jsonify({'error': 'Unsupported file format'}), 400
    except Exception as e:
        logging.error(f'Error reading data file: {e}')
        return jsonify({'error': 'Error reading data file'}), 500

    if not all(var in df.columns for var in independent_vars):
        return jsonify({'error': 'One or more independent variables are missing'}), 400

    if dependent_var not in df.columns:
        return jsonify({'error': 'Dependent variable is missing'}), 400

    df_clean = df.dropna(subset=independent_vars + [dependent_var])

    X = df_clean[independent_vars].values
    y = df_clean[dependent_var].values

    if process_Method in ['L2', '对数', '不处理']:
        X, _, _ = normalize_data(X, process_Method)
        y, _, _ = normalize_data(y, process_Method)
    else:
        X, *xdataparams = normalize_data(X, process_Method)
        y, *ydataparams = normalize_data(y, process_Method)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True , random_state=42)

    # Check if the model is a linear model
    linear_models = ['线性回归', '岭回归', '拉索回归']
    if model_type in linear_models:
        # Train the model without hyperparameter optimization
        model_class = globals().get(config['models'][model_type]['class'])
        model = model_class()
        model.fit(X_train, y_train)

        joblib.dump(model, './models/' + formatted_time + '_' + dependent_var + model_type + '_' + optimization_algorithm + '_' + os.path.basename(data_file_path).replace(data_file_path.split('.')[-1].lower(),'.pkl'))
        # To load the model later
        # loaded_model = joblib.load(model_filename)

        predictions = model.predict(X_test)

        if process_Method in ['L2', '对数', '不处理']:
            predictions = predictions
            y_test = y_test
        else:
            predictions = denormalize_data(predictions, process_Method, ydataparams)
            y_test = denormalize_data(y_test, process_Method, ydataparams)

        # 打开文件用于写入
        # np.savetxt('./result/' + formatted_time + '_' + dependent_var +  model_type +'process_Method'+ '_预处理参数.txt', ydataparams, fmt='%.6f')

        mse = mean_squared_error(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predictions)
        best_predictions = convert_np_types(predictions)
        y_test = convert_np_types(y_test)  # Convert y_test to list

        # Create a new DataFrame with independent variables, true values, and predictions
        result_df = pd.DataFrame(X_test, columns=independent_vars)
        result_df['True_' + dependent_var] = y_test
        result_df['Predicted_' + dependent_var] = predictions

        # Save the DataFrame to a new Excel file
        result_filename = './result/' + formatted_time + '_' + dependent_var +  model_type + '_predictions.xlsx'
        result_df.to_excel(result_filename, index=False)

        # Plot true vs predicted values
        plt.figure(figsize=(14, 7))
        plt.plot(y_test, label='真实值')
        plt.plot(best_predictions, label='预测值')
        plt.xlabel('样本序号')
        plt.ylabel(dependent_var)
        plt.title(f'测试集{dependent_var}真实值与预测值折线图')
        plt.legend()

        # Display metrics on the plot
        metrics_text = f'MSE: {mse:.2f}\nRMSE: {rmse:.2f}\nMAE: {mae:.2f}\nR²: {r2:.2f}'
        plt.text(0.95, 0.01, metrics_text, verticalalignment='bottom', horizontalalignment='right',
                 transform=plt.gca().transAxes, color='black', fontsize=12,
                 bbox=dict(facecolor='white', alpha=0.5))

        plot_filename = './result/' + formatted_time + '_' + dependent_var + model_type + '_test.png'
        plt.savefig(plot_filename)

        return jsonify({
            'params': '线性模型不作优化',
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'r2': r2,
            'ture_data': y_test,
            'predictions': best_predictions
        }), 200


    model_config = config['models'][model_type]
    model_class = globals().get(model_config['class'])
    param_space = model_config.get('params', {})  # Default to empty dictionary

    if model_class is None:
        return jsonify({'error': 'Model class not found in globals'}), 500

    try:
        space = create_hyperopt_space(param_space)
    except Exception as e:
        logging.error(f"Error creating hyperopt space: {e}")
        return jsonify({'error': 'Error creating hyperopt space'}), 500

    kernel_options = ['linear', 'poly', 'rbf', 'sigmoid']
    weights_options = ['distance', 'uniform']
    activation_options = ['tanh', 'relu', 'identity', 'logistic']
    def objective(params):
        try:
            # 调试打印
            print(f"接收到的参数: {params}")

            # 将参数转换为合适的类型
            if model_type == '随机森林':
                if 'max_depth' in params:
                    params['max_depth'] = int(params['max_depth'])
                if 'min_samples_split' in params:
                    params['min_samples_split'] = int(params['min_samples_split'])
                if 'n_estimators' in params:
                    params['n_estimators'] = int(params['n_estimators'])

            elif model_type == '支持向量机':
                if 'C' in params:
                    params['C'] = float(params['C'])
                if 'epsilon' in params:
                    params['epsilon'] = float(params['epsilon'])
                if 'kernel' in params:
                    params['kernel'] = kernel_options[int(params['kernel'])]

            elif model_type == '梯度提升':
                if 'n_estimators' in params:
                    params['n_estimators'] = int(params['n_estimators'])
                if 'max_depth' in params:
                    params['max_depth'] = int(params['max_depth'])

            elif model_type == '决策树回归':
                if 'max_depth' in params:
                    params['max_depth'] = int(params['max_depth'])
                if 'min_samples_split' in params:
                    params['min_samples_split'] = int(params['min_samples_split'])

            elif model_type == 'K近邻回归':
                if 'n_neighbors' in params:
                    params['n_neighbors'] = int(params['n_neighbors'])

            elif model_type == '多层感知器回归':
                if 'hidden_layer_sizes' in params:
                    # 确保hidden_layer_sizes是元组形式
                    sizes = params['hidden_layer_sizes']
                    if isinstance(sizes, str) and ',' in sizes:
                        sizes = tuple(map(int, sizes.replace('(', '').replace(')', '').split(',')))
                    elif isinstance(sizes, str):
                        sizes = (int(sizes.replace('(', '').replace(')', '')),)
                    params['hidden_layer_sizes'] = sizes
                if 'alpha' in params:
                    params['alpha'] = float(params['alpha'])

            elif model_type in ['岭回归', '拉索回归']:
                if 'alpha' in params:
                    params['alpha'] = float(params['alpha'])

            model = model_class(**params)
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            mse = mean_squared_error(y_test, predictions)

            return {'loss': mse, 'status': STATUS_OK}
        except Exception as e:
            logging.error(f"模型拟合或评估时出错: {e}")
            return {'loss': float('inf'), 'status': STATUS_OK}

    trials = Trials()
    try:
        if optimization_algorithm == 'tpe':
            best_params = fmin(objective, space, algo=tpe.suggest, max_evals=50, trials=trials)
        elif optimization_algorithm == 'random_search':
            best_params = fmin(objective, space, algo=rand.suggest, max_evals=50, trials=trials)
        else:
            return jsonify({'error': 'Invalid optimization algorithm'}), 400
    except Exception as e:
        logging.error(f"Error during hyperparameter optimization: {e}")
        return jsonify({'error': 'Error during hyperparameter optimization'}), 500
    # print(best_params)
    # Use the best parameters to train the final model
    try:
        # Convert parameters to appropriate types
        if model_type == '随机森林':
            if 'max_depth' in best_params:
                best_params['max_depth'] = int(best_params['max_depth'])
            if 'min_samples_split' in best_params:
                best_params['min_samples_split'] = int(best_params['min_samples_split'])
            if 'n_estimators' in best_params:
                best_params['n_estimators'] = int(best_params['n_estimators'])

        elif model_type == '支持向量机':
            if 'C' in best_params:
                best_params['C'] = float(best_params['C'])
            if 'epsilon' in best_params:
                best_params['epsilon'] = float(best_params['epsilon'])
            if 'kernel' in best_params:
                if int(best_params['kernel']) > 3:
                    best_params['kernel'] = kernel_options[3]
                else:
                    best_params['kernel'] = kernel_options[int(best_params['kernel'])]

        elif model_type == '梯度提升':
            if 'n_estimators' in best_params:
                best_params['n_estimators'] = int(best_params['n_estimators'])
            if 'max_depth' in best_params:
                best_params['max_depth'] = int(best_params['max_depth'])

        elif model_type == '决策树回归':
            if 'max_depth' in best_params:
                best_params['max_depth'] = int(best_params['max_depth'])
            if 'min_samples_split' in best_params:
                best_params['min_samples_split'] = int(best_params['min_samples_split'])

        elif model_type == 'K近邻回归':
            if 'n_neighbors' in best_params:
                best_params['n_neighbors'] = int(best_params['n_neighbors'])
            if 'weights' in best_params:
                best_params['weights'] = weights_options[int(best_params['weights'])]

        elif model_type == '多层感知器回归':
            if 'hidden_layer_sizes' in best_params:
                # 确保hidden_layer_sizes是元组形式
                sizes = best_params['hidden_layer_sizes']
                if isinstance(sizes, str) and ',' in sizes:
                    sizes = tuple(map(int, sizes.replace('(', '').replace(')', '').split(',')))
                elif isinstance(sizes, str):
                    sizes = (int(sizes.replace('(', '').replace(')', '')),)
                best_params['hidden_layer_sizes'] = sizes
            if 'alpha' in best_params:
                best_params['alpha'] = float(best_params['alpha'])
            if 'activation' in best_params:
                best_params['activation'] = activation_options[int(best_params['activation'])]

        best_model = model_class(**best_params)
        best_model.fit(X_train, y_train)

        joblib.dump(best_model, './models/' + formatted_time + '_' + dependent_var + model_type + '_' + optimization_algorithm + '_' + os.path.basename(data_file_path).replace(data_file_path.split('.')[-1].lower(),'pkl'))
        # To load the model later
        # loaded_model = joblib.load(model_filename)
        # print(X_test)
        best_predictions = best_model.predict(X_test)

        if process_Method in ['L2', '对数', '不处理']:
            best_predictions = best_predictions
            y_test = y_test
        else:
            best_predictions = denormalize_data(best_predictions, process_Method, ydataparams)
            y_test = denormalize_data(y_test, process_Method, ydataparams)
            print(best_predictions,y_test)

        # 打开文件用于写入
        # np.savetxt('./result/' + formatted_time + '_' + dependent_var +  model_type +'process_Method'+ '_预处理参数.txt', ydataparams, fmt='%.6f')

        mse = mean_squared_error(y_test, best_predictions)
        mae = mean_absolute_error(y_test, best_predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, best_predictions)

    except Exception as e:
        logging.error(f"Error during final model training or evaluation: {e}")
        return jsonify({'error': 'Error during final model training or evaluation'}), 500

    best_predictions = convert_np_types(best_predictions)
    best_params = convert_np_types(best_params)

    # X_test = convert_np_types(X_test)  # Convert X_test to list
    y_test = convert_np_types(y_test)  # Convert y_test to list

    # Create a new DataFrame with independent variables, true values, and predictions
    result_df = pd.DataFrame(X_test, columns=independent_vars)
    result_df['True_' + dependent_var] = y_test
    result_df['Predicted_' + dependent_var] = best_predictions

    # Save the DataFrame to a new Excel file
    result_filename = './result/' + formatted_time + '_' + dependent_var + model_type + '_predictions.xlsx'
    result_df.to_excel(result_filename, index=False)

    plt.figure(figsize=(14, 7))
    plt.plot(y_test, label='真实值')
    plt.plot(best_predictions, label='预测值')
    plt.xlabel('样本序号')
    plt.ylabel(dependent_var)
    plt.title(f'测试集{dependent_var}真实值与预测值折线图')
    plt.legend()

    # Display metrics on the plot
    metrics_text = f'MSE: {mse:.2f}\nRMSE: {rmse:.2f}\nMAE: {mae:.2f}\nR²: {r2:.2f}'
    plt.text(0.95, 0.01, metrics_text, verticalalignment='bottom', horizontalalignment='right',
             transform=plt.gca().transAxes, color='black', fontsize=12,
             bbox=dict(facecolor='white', alpha=0.5))

    plot_filename = './result/' + formatted_time + '_' + dependent_var + model_type + '_test.png'
    plt.savefig(plot_filename)

    return jsonify({
        'params': best_params,
        'mse': mse,
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'ture_data': y_test,
        'predictions': best_predictions
    }), 200

if __name__ == '__main__':
    app.run(host='192.168.1.8', port=50001, debug=True)
