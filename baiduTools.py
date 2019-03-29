from aip import AipFace
import base64

#创建百度AI人脸识别的账号
APP_ID = '15788230'
API_KEY = 'G7vYGBDQT9ZkpbfNOesG9H2Y'
SECRET_KEY = 'f12oOtm7kFCFFvTaMK4hCOqjo024dwWC'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

#将图片传给百度AI，并解析饭回来的图片信息
def get_info(dir):
    data = img_encode(dir)      #编码图片得到图片信息
    #以下是需要上传的数据
    image = str(data, 'utf-8')      #将字节格式转化为字符串的格式
    imageType = 'BASE64'
    options = {}
    options["face_field"] = "age,beauty,expression,faceshape,gender,glasses,race,facetype"      #需要检测的人脸信息
    options["max_face_num"] = 5
    # 获得百度AI给的人脸信息，将信息解析之后，放入msg中返回
    result = client.detect(image, imageType, options)
    if result['error_msg'] == "SUCCESS":        #SUCCESS表示成功获取人脸信息
        info_dict = {'smiles': "微笑", 'nones': "不笑", 'laughs': "大笑", 'square': '正方形', 'triangle': '三角形', 'oval': '椭圆行',    #该字典将返回信息中的英文转换成中文
                     'heart': '心形', 'round': '圆形', 'male': '男性', 'female': '女性', 'noneg': '无眼镜', 'commong': '普通眼镜',
                     'sung': '墨镜', 'yellow': '黄种人', 'white': '白种人', 'black': '黑种人', 'arabs': '阿拉伯人',
                     'human': '真实人脸', 'cartoon': '卡通人脸'}
        face_num = result['result']['face_num']
        text = "人脸个数为：" + str(face_num)
        msg = text
        for i in range(face_num):
            info = result['result']['face_list'][i]
            text = "\n\n第" + str(i + 1) + "个人脸：\n" + \
                   "年龄：" + str(info['age']) + \
                   "\n颜值：" + str(info['beauty']) + \
                   "\n表情:" + info_dict[info['expression']['type'] + 's'] + "；可信度：" + str(
                info['expression']['probability']) + \
                   "\n脸型：" + info_dict[info['face_shape']['type']] + "；可信度：" + str(info['face_shape']['probability']) + \
                   "\n性别：" + info_dict[info['gender']['type']] + "；可信度：" + str(info['gender']['probability']) + \
                   "\n眼镜：" + info_dict[info['glasses']['type'] + 'g'] + "；可信度：" + str(info['glasses']['probability']) + \
                   "\n种族：" + info_dict[info['race']['type']] + "；可信度：" + str(info['race']['probability']) + \
                   "\n人脸类型：" + info_dict[info['face_type']['type']] + "；可信度：" + str(info['face_type']['probability'])
            msg = msg + text
        return msg      #返回解析得到的人脸信息
    else:
        return "识别失败，再试一次吧"

#将图片使用BASE64编码方式编码
def img_encode(dir):
    with open(dir, 'rb') as img:
        data = base64.b64encode(img.read())
        return data


def compare(dir1,dir2):
    data1 = str(img_encode(dir1), 'utf-8')      #将两张图片的信息进行编码
    data2 = str(img_encode(dir2), 'utf-8')
    result = client.match([                     #图片对比所需要上传的信息
        {
            'image': data1,
            'image_type': 'BASE64'
        },
        {
            'image': data2,
            'image_type': 'BASE64'
        }
    ])
    score = str('%.2f' % result['result']['score'])     #获得两张图片的相似度，并转换成字符串格式返回
    return score