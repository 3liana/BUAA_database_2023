import base64

def changePicPath(path):
    with open(path, "rb") as image_file:
        # 读取文件
        image_data = image_file.read()
        # 对数据进行Base64编码
        base64_encoded_data = base64.b64encode(image_data)
        # 将Base64编码的数据转换为字符串
        base64_message = base64_encoded_data.decode('utf-8')
        return base64_message


