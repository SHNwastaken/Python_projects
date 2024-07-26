import cv2
from PIL import Image
from ultralytics import YOLO
model=YOLO('D:\\project1\\best (1).pt')
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
service=Service(executable_path='chromedriver.exe')
from io import BytesIO
target_class_id=3

while 1:
    a=0
    driver= webdriver.Chrome(service=service)
    driver.get("https://demo.defectdojo.org/login?next=/")
    ss_asbytes=driver.get_screenshot_as_png()
    driver.quit()
    image=Image.open(BytesIO(ss_asbytes))
    image=image.resize((1024,576))
    results=model.predict(image,conf=0.3,imgsz=640,show=True)
    for result in results:
        boxes = result.boxes.xyxy.cpu()
        class_ids = result.boxes.cls.cpu() 
        for box, class_id in zip(boxes, class_ids):
            if class_id == target_class_id: 
                a+=1 
                x1, y1, x2, y2 = map(int, box[:4])
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                print(f'Centre of input box {a} : {center_x},{center_y}')
    k=cv2.waitKey(0)
    if k==109:
        cv2.destroyAllWindows()
        continue
    elif k==112:
        break
