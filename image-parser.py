from python_anticaptcha import AnticaptchaClient, ImageToTextTask

api_key = 'f12634370974461a767a103936917e6c'
captcha_fp = open('./img/2.jpeg', 'rb')
client = AnticaptchaClient(api_key)
task = ImageToTextTask(captcha_fp)
job = client.createTask(task)
job.join()
print(job.get_captcha_text())

