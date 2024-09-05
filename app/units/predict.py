import os
os.environ['PROJ_LIB'] = r'C:\Users\Admin\.conda\envs\PaddleRS\Library\share\proj'

import joblib
import numpy as np
from tqdm import tqdm
from osgeo import gdal
import psutil
import pandas as pd


def memory_usage():
    """计算可用内存"""
    mem_available = psutil.virtual_memory().available >> 20  # 可用内存
    mem_process = psutil.Process(os.getpid()).memory_info().rss >> 20  # 进程内存
    return mem_process, mem_available

def predict_block(model, arr):
    """对数据块进行预测"""
    flat_block = arr.reshape((arr.shape[0], -1)).T
    prediction_block = model.predict(flat_block)
    return prediction_block


def predict_excel(model_path, excel_path, output_path, columns_to_use):
    # 加载模型
    loaded_model = joblib.load(model_path)

    # Load the Excel file
    data = pd.read_excel(excel_path)

    features = data[columns_to_use]

    # Predict using the model
    predictions = loaded_model.predict(features)

    # Add predictions to the DataFrame
    data['Predicted'] = predictions

    # Save the updated DataFrame to a new Excel file
    data.to_excel(output_path, index=False)


def predict_image(model, block_size, img_path, num_bands, save_path):
    """预测图像并保存结果"""

    ds = gdal.Open(img_path)
    width, height, bands = ds.RasterXSize, ds.RasterYSize, ds.RasterCount

    # 设置输出数据集
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(save_path, width, height, 1, gdal.GDT_Float32)
    print(ds.GetGeoTransform(), ds.GetProjection())
    out_ds.SetGeoTransform(ds.GetGeoTransform())
    out_ds.SetProjection(ds.GetProjection())

    # 按块处理图像
    for y in tqdm(range(0, height, block_size)):
        for x in range(0, width, block_size):
            # 计算每块的实际大小
            x_end = min(x + block_size, width)
            y_end = min(y + block_size, height)
            block_width = x_end - x
            block_height = y_end - y

            # 读取块数据
            arr_tmp = ds.ReadAsArray(x, y, block_width, block_height)
            arr_tmp = np.nan_to_num(arr_tmp)
            # arr= np.array([arr_tmp[num_bands[0]],arr_tmp[num_bands[1]],arr_tmp[num_bands[2]],arr_tmp[num_bands[3]],
            #                arr_tmp[num_bands[4]],arr_tmp[num_bands[5]],arr_tmp[num_bands[6]],arr_tmp[num_bands[7]],
            #                arr_tmp[num_bands[8]],arr_tmp[num_bands[9]],arr_tmp[num_bands[10]],arr_tmp[num_bands[11]],
            #                arr_tmp[num_bands[12]],arr_tmp[num_bands[13]],arr_tmp[num_bands[14]],arr_tmp[num_bands[15]],
            #                arr_tmp[num_bands[16]],arr_tmp[num_bands[17]],arr_tmp[num_bands[18]],arr_tmp[num_bands[19]],
            #                arr_tmp[num_bands[20]],arr_tmp[num_bands[21]],arr_tmp[num_bands[22]]])
            arr = np.array([arr_tmp[num_bands[0]], arr_tmp[num_bands[1]], arr_tmp[num_bands[2]], arr_tmp[num_bands[3]],
                            #arr_tmp[num_bands[4]], arr_tmp[num_bands[5]],arr_tmp[num_bands[6]],# arr_tmp[num_bands[6]], arr_tmp[num_bands[7]],

                            ])
            # arr = np.array([arr_tmp[num_bands[0]], arr_tmp[num_bands[1]], arr_tmp[num_bands[2]], arr_tmp[num_bands[3]],
            #                 ])

            # 预测
            pred = predict_block(model, arr).reshape((block_height, block_width))

            arr_tmp = None
            # CO
            # pred = min_max_denormalization(pred, 1.416667, 59.956522)

            # 写入结果
            out_ds.GetRasterBand(1).WriteArray(pred, x, y)

    out_ds.FlushCache()
    out_ds = None
    print('Prediction complete and results saved to', save_path)


# 示例调用
if __name__ == '__main__':
    model_path = r'../models/20240816_183507_PM2.5随机森林_tpe_202407_mean_train.pkl'
    block_size = 512  # 每块的行数和列数
    img_path = r"F:\lvbotao\ATLAS\项目资料\20240708-海南岛Modis数据验证\大气反演\20240816\01PM2.5\04待反演栅格"
    save_path = r"F:\lvbotao\ATLAS\项目资料\20240708-海南岛Modis数据验证\大气反演\20240816\test\test"
    num_bands = [3,4,5,6]
    # 以二进制方式读取模型文件
    loaded_model = joblib.load(model_path)

    for filename in os.listdir(img_path):
        print(f'处理数据{filename}')
        processFile = os.path.join(img_path, filename)
        saveFile = os.path.join(save_path, filename)
        predict_image(loaded_model, block_size, processFile, num_bands, saveFile)


    # ###################################################################################################
    # # Example usage
    # columns_to_use = ['AOD_047', 'AOD_055', 'LST', 'DEM']
    # model_path = r"F:\lvbotao\ATLAS\02技术汇报\在线水质反演系统\app\models\随机森林_tpe_20240522_海南训练数据.pkl"
    # excel_path = r'F:\lvbotao\ATLAS\海南岛\20240522_海南训练数据.xlsx'  # Update with the path to your Excel file
    # output_path = r'F:\lvbotao\ATLAS\海南岛\20240522_海南训练数据预测.xlsx'  # Specify where you want to save the output
    #
    # predict_excel(model_path, excel_path, output_path, columns_to_use)
