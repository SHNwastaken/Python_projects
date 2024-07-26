import cv2
import numpy as np
import torch
from PIL import Image
from pdf2image import convert_from_path
from transformers import AutoImageProcessor, TableTransformerForObjectDetection

image_processor = AutoImageProcessor.from_pretrained("microsoft/table-transformer-detection")
model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")

def detect_tables(image):
    
    inputs = image_processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]])
    results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]
    
    return results

def draw_boxes(image_np, boxes):
    for box in boxes:
        x1, y1, x2, y2 = box
        cv2.rectangle(image_np, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    return image_np

def main(pdf_path):
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        print(f"Processing page {i+1}")
        results = detect_tables(image)
        
        boxes = results["boxes"]
        image_np = np.array(image)
        image_with_boxes = draw_boxes(image_np, boxes)
        
        output_path = f'table_detection_page_{i+1}.png'
        cv2.imwrite(output_path, image_with_boxes)
        print(f"Saved detected tables to {output_path}")

if __name__ == "__main__":
    pdf_path = 'E:\\pythonvenv\\venv\\table.pdf'  
    main(pdf_path)
