import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

image_data = pytesseract.image_to_string('C:\sockshopping\MW_Collection_list1_01.jpg',
                                         lang='kor', config='-c preserve_interword_spaces=1 --psm 4')

print(image_data)

with open('./crawling/image/sock01.txt', 'w', encoding='utf-8') as tx:
    tx.write(image_data)