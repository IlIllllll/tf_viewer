import numpy as np
import h5py


def read_hdf5_data(file_path):
    """
    读取HDF5文件数据
    
    Args:
        file_path (str): HDF5文件路径
        
    Returns:
        dict: 包含读取数据的字典
    """
    try:
        with h5py.File(file_path, 'r') as indata:
            # 读取动作数据
            data = {}
            
            # 读取右手相关数据
            if 'action/rightHand/pose' in indata:
                data['rightHand_pose'] = np.array(indata['action/rightHand/pose'])
            if 'action/rightHand/quaternion' in indata:
                data['rightHand_quaternion'] = np.array(indata['action/rightHand/quaternion'])
                
            # 读取手指末端位置数据
            finger_tips = ['rightIndexTip', 'rightLittleTip', 'rightMiddleTip', 
                          'rightRingTip', 'rightThumbTip']
            
            for finger in finger_tips:
                pose_key = f'action/{finger}/pose'
                quat_key = f'action/{finger}/quaternion'
                
                if pose_key in indata:
                    data[f'{finger}_pose'] = np.array(indata[pose_key])
                if quat_key in indata:
                    data[f'{finger}_quaternion'] = np.array(indata[quat_key])
            
            # 打印数据信息
            print(f"成功读取HDF5文件: {file_path}")
            print(f"数据键值: {list(data.keys())}")
            for key, value in data.items():
                if hasattr(value, 'shape'):
                    print(f"{key}: shape={value.shape}")
            
            return data
            
    except Exception as e:
        print(f"读取HDF5文件时出错: {e}")
        return None


def display_data_info(file_path):
    """
    显示HDF5文件结构信息
    
    Args:
        file_path (str): HDF5文件路径
    """
    try:
        with h5py.File(file_path, 'r') as f:
            print(f"\nHDF5文件结构 ({file_path}):")
            
            def print_attrs(name, obj):
                print(name)
                if hasattr(obj, 'shape'):
                    print(f"  - 形状: {obj.shape}")
                    print(f"  - 数据类型: {obj.dtype}")
            
            f.visititems(print_attrs)
            
    except Exception as e:
        print(f"读取文件结构时出错: {e}")


def main():
    """主函数"""
    # HDF5文件路径
    indata_path = "/home/ls/Desktop/tf_test/base_action_data3/Data/Data.hdf5"
    
    # 显示文件结构信息
    display_data_info(indata_path)
    
    # 读取数据
    data = read_hdf5_data(indata_path)
    
    if data:
        print("\n数据读取成功!")
        # 可以在这里添加对读取数据的进一步处理
    else:
        print("数据读取失败!")


if __name__ == "__main__":
    main()