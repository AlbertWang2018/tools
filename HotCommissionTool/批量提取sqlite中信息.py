import os,sqlite3
import pandas as pd

# 指定文件夹路径
folder_path = r'D:\Download\00-CATL\KBESS\PG3'

# 指定输出Excel文件路径
output_excel_path = 'output.xlsx'

# 创建一个空的DataFrame来存储结果
results = pd.DataFrame(columns=['File', 'Date','Sys_Udc','Sys_I','I1','I2','I3','I4','I5','Sys_DSOC','Sys_U_Max','Sys_U_Min','Sys_T_Max'])

# 遍历文件夹中的所有文件
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if 'StartDate' in file:
            file_path = os.path.join(root, file)
            try:
                # 连接到SQLite数据库
                conn = sqlite3.connect(file_path)
                cursor = conn.cursor()
                
                # 查询表abc的最小值和最大值
                cursor.execute("SELECT Date,Sys_Udc,Sys_I,Sys_DSOC,Sys_U_Max,Sys_U_Min,Sys_T_Max FROM BMSMBMUData where abs(Sys_I)>100 limit 0,1")
                if cursor is None:continue
                Date,Sys_Udc,Sys_I,Sys_DSOC,Sys_U_Max,Sys_U_Min,Sys_T_Max = cursor.fetchone()
                cursor.execute("SELECT I_HVS from BMSSBMUData where date='"+Date+"'")
                I_HVS = cursor.fetchall()
                I=[I_HVS[0] for I_HVS in I_HVS]                
                # 将结果添加到DataFrame中
                results = results._append({'File': file, 'Date': Date, 'Sys_Udc': Sys_Udc, 'Sys_I': Sys_I,'I1':I[0],'I2':I[0],'I3':I[0],'I4':I[0],'I5':I[0],
                                        'Sys_DSOC': Sys_DSOC,'Sys_U_Max': Sys_U_Max, 'Sys_U_Min': Sys_U_Min, 'Sys_T_Max': Sys_T_Max}, ignore_index=True)
                
                cursor.execute("SELECT Date,Sys_Udc,Sys_I,Sys_DSOC,Sys_U_Max,Sys_U_Min,Sys_T_Max FROM BMSMBMUData where abs(Sys_I)>100 order by date desc limit 0,1")
                Date,Sys_Udc,Sys_I,Sys_DSOC,Sys_U_Max,Sys_U_Min,Sys_T_Max = cursor.fetchone()                
                cursor.execute("SELECT I_HVS from BMSSBMUData where date='"+Date+"'")
                I_HVS = cursor.fetchall()
                I=[I_HVS[0] for I_HVS in I_HVS]                
                # 将结果添加到DataFrame中
                results = results._append({'File': file, 'Date': Date, 'Sys_Udc': Sys_Udc, 'Sys_I': Sys_I,'I1':I[0],'I2':I[0],'I3':I[0],'I4':I[0],'I5':I[0],
                                        'Sys_DSOC': Sys_DSOC,'Sys_U_Max': Sys_U_Max, 'Sys_U_Min': Sys_U_Min, 'Sys_T_Max': Sys_T_Max}, ignore_index=True)
                
                # 关闭数据库连接
                conn.close()
            except Exception as e:
                print(f"Error processing {file}: {e}")

# 将结果写入Excel文件
results.to_excel(output_excel_path, index=False)

print(f"Results have been written to {output_excel_path}")