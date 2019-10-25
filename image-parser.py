# try:
#     from PIL import Image
# except ImportError:
#     import Image
# import pytesseract
# import cv2
#
# # print("result:" + pytesseract.image_to_string('./img/2.jpeg', timeout=10))
# img = cv2.imread('./img/2.jpeg')
# print(pytesseract.image_to_string(img))

from python_anticaptcha import AnticaptchaClient, ImageToTextTask

api_key = 'f12634370974461a767a103936917e6c'
captcha_fp = open('./img/2.jpeg', 'rb')
client = AnticaptchaClient(api_key)
task = ImageToTextTask(captcha_fp)
job = client.createTask(task)
job.join()
print(job.get_captcha_text())

