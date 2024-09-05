import numpy as np
from sklearn.preprocessing import normalize


def min_max_normalization(data):
    """
    将数据进行Min-Max归一化，使其缩放到[0, 1]的范围。
    """
    min_val = np.min(data, axis=0)
    max_val = np.max(data, axis=0)
    normalized_data = (data - min_val) / (max_val - min_val)
    return normalized_data, min_val, max_val


def min_max_denormalization(normalized_data, min_val, max_val):
    """
    反归一化Min-Max归一化后的数据。
    """
    denormalized_data = normalized_data * (max_val - min_val) + min_val
    return denormalized_data


def z_score_standardization(data):
    """
    将数据进行Z-score标准化，使其均值为0，标准差为1。
    """
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    standardized_data = (data - mean) / std
    return standardized_data, mean, std


def z_score_denormalization(standardized_data, mean, std):
    """
    反标准化Z-score标准化后的数据。
    """
    denormalized_data = standardized_data * std + mean
    return denormalized_data


def max_abs_scaler(data):
    """
    使用MaxAbsScaler将数据归一化到[-1, 1]的范围。
    """
    max_abs = np.max(np.abs(data), axis=0)
    normalized_data = data / max_abs
    return normalized_data, max_abs


def max_abs_denormalization(normalized_data, max_abs):
    """
    反归一化MaxAbsScaler归一化后的数据。
    """
    denormalized_data = normalized_data * max_abs
    return denormalized_data


def robust_scaler(data):
    """
    使用RobustScaler进行归一化，基于中位数和四分位数。
    """
    median = np.median(data, axis=0)
    q75, q25 = np.percentile(data, [75, 25], axis=0)
    iqr = q75 - q25
    normalized_data = (data - median) / iqr
    return normalized_data, median, iqr


def robust_denormalization(normalized_data, median, iqr):
    """
    反归一化RobustScaler归一化后的数据。
    """
    denormalized_data = normalized_data * iqr + median
    return denormalized_data


def l2_normalization(data):
    """
    使用L2范数进行归一化，使每个样本的L2范数为1。
    """
    normalized_data = normalize(data, norm='l2')
    return normalized_data


def log_normalization(data):
    """
    对数据进行对数归一化，处理非负数据。
    """
    normalized_data = np.log1p(data)  # log1p是log(1+x)，防止x为0时log(x)无效
    return normalized_data


def no_process(data):
    """
    不处理数据。
    """
    return data


def normalize_data(data, method='最小最大'):
    """
    根据指定的方法对数据进行归一化或标准化。

    参数:
    data (np.ndarray): 输入的原始数据。
    method (str): 选择的归一化或标准化方法。可选值为 '最小最大', 'z-score', '最大绝对值', '鲁棒', 'L2', '对数'。

    返回:
    np.ndarray: 处理后的数据。
    """
    if method == '最小最大':
        return min_max_normalization(data)
    elif method == 'z-score':
        return z_score_standardization(data)
    elif method == '最大绝对值':
        return max_abs_scaler(data)
    elif method == '鲁棒':
        return robust_scaler(data)
    elif method == 'L2':
        return l2_normalization(data), None, None
    elif method == '对数':
        return log_normalization(data), None, None
    elif method == '不处理':
        return no_process(data), None, None
    else:
        raise ValueError(f"未知的归一化方法: {method}")


def denormalize_data(normalized_data, method, params):
    """
    根据指定的方法和参数对数据进行反归一化。

    参数:
    normalized_data (np.ndarray): 归一化后的数据。
    method (str): 归一化的方法名称。
    params (tuple): 反归一化所需的参数。

    返回:
    np.ndarray: 反归一化后的数据。
    """
    if method == '最小最大':
        min_val, max_val = params
        return min_max_denormalization(normalized_data, min_val, max_val)
    elif method == 'z-score':
        mean, std = params
        return z_score_denormalization(normalized_data, mean, std)
    elif method == '最大绝对值':
        max_abs = params
        return max_abs_denormalization(normalized_data, max_abs)
    elif method == '鲁棒':
        median, iqr = params
        return robust_denormalization(normalized_data, median, iqr)
    elif method == 'L2' or method == '对数':
        return normalized_data
    elif method == '不处理':
        return normalized_data
    else:
        raise ValueError(f"未知的归一化方法: {method}")


# 使用示例
if __name__ == "__main__":
    data = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])

    # 选择不同的处理方法
    methods = ['最小最大', 'z-score', '最大绝对值', '鲁棒', 'L2', '对数', '不处理']

    for method in methods:
        if method in ['L2', '对数', '不处理']:
            processed_data, _, _ = normalize_data(data, method=method)
            denormalized_data = processed_data
        else:
            processed_data, *params = normalize_data(data, method=method)
            denormalized_data = denormalize_data(processed_data, method, params)

        print(f"\n{method} 处理后的数据:")
        print(processed_data)
        print(f"{method} 反归一化后的数据:")
        print(denormalized_data)
