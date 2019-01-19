from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '15453333'
API_KEY = 'ydtZuR5KAG5ao5fV5NuNsm8d'
SECRET_KEY = 'Ga1Rl8QoSkLw6k80LzcGodCCjUkgBzIl'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


if __name__ == '__main__':
    image = get_file_content('testimages/未命名.png')

    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    """ 调用通用文字识别, 图片参数为本地图片 """
    response = client.basicGeneral(image, options)
    print(response)