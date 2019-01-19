from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '15453333'
API_KEY = 'ydtZuR5KAG5ao5fV5NuNsm8d'
SECRET_KEY = 'Ga1Rl8QoSkLw6k80LzcGodCCjUkgBzIl'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


class BaiduAI:
    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def find(self, img_name):
        image = self.get_file_content(img_name)
        idCardSide = "front"
        options = {}
        options["detect_direction"] = "true"
        options["detect_risk"] = "false"

        response = client.idcard(image, idCardSide, options)
        return response

if __name__ == '__main__':
    ai = BaiduAI()
    image = ai.get_file_content('testimages/61ba72c09fd847e5bc836e5c759b3e03.jpg')
    idCardSide = "front"
    options = {}
    options["detect_direction"] = "true"
    options["detect_risk"] = "false"

    response = client.idcard(image, idCardSide, options)
    print(response)