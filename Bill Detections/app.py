from flask import Flask, request, redirect, send_file,render_template
import pytesseract as tess
from PIL import Image
import re
import pandas as pd
from fuzzywuzzy import process
tess. pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import numpy as np
import cv2


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def extract(files):
    text_list = []
    tax_id_list = []  
    shop_name_list =[]
    tax_no_list = []
    dateo_list = []
    table_list = []
    n = len(files)

    for i in range(len(files)):
        img = Image.open(files[i])
        
        text = preprocess(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
        #text = tess.image_to_string(img,lang= 'tha+eng')
        print(text)
        text_list.append(text)
        
        tax_id = extract_tax_id(text)
        tax_id_list.append(tax_id)
        
        shop_name = extract_shop_name(text)
        shop_name_list.append(shop_name)

        tax_no = extract_tax_no(text)
        tax_no_list.append(tax_no)

        dateo = extract_date(text)
        dateo_list.append(dateo)

        table = extract_table(text)
        table_list.append(table)
        


        

        '''with open(f'text{i + 1}.txt', 'w' ,encoding='utf-8') as text_file:
            text_file.write(text_list[i])'''

    return [(index + 1, text, tax_id,shop_name,tax_no,dateo,table) for index, (text, tax_id,shop_name,tax_no,dateo,table) 
            in enumerate(zip(text_list, tax_id_list,shop_name_list,tax_no_list,dateo_list,table_list))]


#อัปโหลดไฟล์
@app.route('/upload', methods=['POST'])
def upload():
    if 'files[]' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('files[]')
    text_listmain = extract(files)
    text_list_all = []

    # Initialize an empty list to store data for each row
    data_list = []
    
    # Initialize a global row counter
    row_counter = 1

    for file in files:
        text_list = extract([file])
        Index, Text, Tax_ID, shopname, tax_no, date, table = text_list[0]
        text_list_all.append((shopname, table))

        # Split the 'table' column into separate items and lines and append to data_list
        for i, item in enumerate(table.split(', ')):
            lines = item.split('\n')
            for j, line in enumerate(lines):
                if j == 0 and line.strip():   # Append only non-empty lines
                    data_list.append([row_counter,shopname, Tax_ID, tax_no, date, line])
                    row_counter += 1
                elif line.strip():
                    data_list.append([row_counter,"", "", "", "", line])
                    row_counter += 1

    # Create a DataFrame using the data_list
    df = pd.DataFrame(data_list, columns=['row', 'ชื่อร้านค้า', 'เลขประจำตัวผู้เสียภาษี', 'หมายเลขใบกำกับภาษี', 'วันที่', 'ตารางสินค้าเเละบริการ'])

    # Reorder columns for the final DataFrame
    df = df[['row', 'ชื่อร้านค้า', 'เลขประจำตัวผู้เสียภาษี', 'หมายเลขใบกำกับภาษี', 'วันที่', 'ตารางสินค้าเเละบริการ']]

    excel_filename = 'result.xlsx'
    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        worksheet = writer.sheets['Sheet1']
        cell_format = writer.book.add_format()
        cell_format.set_align('center')
        cell_format.set_align('vcenter')
        # set column
        worksheet.set_column('A:F', 20, cell_format)  # Adjust the range based on your needs
        worksheet.set_column('B:B', 50, cell_format)  # Adjust the range based on your needs
        worksheet.set_column('F:F', 55, cell_format)  # Adjust the range based on your needs
        # set row
        for i in range(len(df) + 1):
            worksheet.set_row(i, 40)  # Adjust the row height based on your needs

    return render_template('index.html', text_list=text_listmain, excel_filename=excel_filename)






@app.route('/download_excel/<excel_filename>')
def download_excel(excel_filename):
    return send_file(excel_filename, as_attachment=True)

@app.route('/download/<int:index>')
def download(index):
    filename = f'text{index}.txt'
    return send_file(filename, as_attachment=True)



def extract_shop_name(ocr_result, seven=("CP ALL", "7-Eleven"), amazon="Cafe Amazon", lotus="เอก-ชัย"):
    lines = ocr_result.strip().split("\n")

    seven_match, seven_confidence = process.extractOne("\n".join(lines[0:4]), seven)
    amazon_match, amazon_confidence = process.extractOne("\n".join(lines[0:6]), [amazon])
    lotus_match, lotus_confidence = process.extractOne("\n".join(lines[0:4]), lotus)


    #Seven-Eleven
    if seven_confidence >= 60:
        similar_line, _ = process.extractOne(seven_match, lines)
        
        return similar_line

    #Cafe Amazon
    if amazon_confidence >= 60:
        similar_line, _ = process.extractOne(amazon_match, lines)
        
        return similar_line

    #Lotus
    if lotus_confidence >= 60:
        similar_line, _ = process.extractOne(lotus_match, lines)
        
        return similar_line

    return "ไม่พบข้อมูล"


def extract_tax_id(ocr_result):
    tax_id_pattern = r'TAX#(\d{13})'
    tax_id_match = re.search(tax_id_pattern, ocr_result)

    if tax_id_match:
        return tax_id_match.group(1)

    general_pattern = r'\d{13}'
    general_matches = re.findall(general_pattern, ocr_result)

    for match in general_matches:
        return match

    return "ไม่พบข้อมูล"
def extract_date(ocr_result):
    date_patterns = [
        r'\b\d{2}/\d{2}/\d{2}\b',
        r'\b\d{2}/\d{2}/\d{4}\b',
        r'\b\d{2}-\d{2}-\d{2}\b',
        r'\b\d{2}-\d{2}-\d{4}\b',
        r'\b\d{2}\s*[-/]\s*\d{2}\s*[-/]\s*\d{2}\b',
        r'\b\d{2}\s*[-/]\s*\d{2}\s*[-/]\s*\d{4}\b',
    ]
    date_cafe = [
        r'DATE(\d{2}/\d{2}/\d{2})',
    ]


    for pattern in date_patterns:
        match = re.search(pattern, ocr_result)
        if match:
            date = match.group(0)
            return date


    for pattern in date_cafe:
        match = re.search(pattern, ocr_result)
        if match:
            date = match.group(1)  
            return date

    return "ไม่พบข้อมูล"

def extract_tax_no(ocr_result, seven=("R#"), amazon="Tax Invoice No.", lotus=("RID.")):
    lines = ocr_result.strip()
    seven_match, seven_confidence = process.extractOne(lines, [seven])
    amazon_match, amazon_confidence = process.extractOne(lines,[amazon])
    lotus_match, lotus_confidence = process.extractOne(lines,[lotus])


    #Seven-Eleven
    if seven_confidence >= 60 and seven_confidence > amazon_confidence and seven_confidence > lotus_confidence:
        tax_no_group_0 = "ไม่พบข้อมูล"
        tax_no_patterns = [
        r'R#\d{10}P\d{1}',  # Pattern 1
        r'Tax Invoice No\.(\d+RC\d+/\d+)',  # Pattern 2
        r'No\.(\d+RC\d+/\d+)',  # Pattern 3
        r'Reg\. No\.([\w/]+)',  # Pattern 4
        r'No\.(\d+)',  # Pattern 5
        r'RID(\d{14})',
    ]

        for pattern in tax_no_patterns:
            match = re.search(pattern, ocr_result)

            if match:
                tax_no_group_0 = match.group(0)
    
            return tax_no_group_0

    #Cafe Amazon
    if amazon_confidence >= 60 and amazon_confidence > seven_confidence and amazon_confidence > lotus_confidence:
        tax_no_group_0 = "ไม่พบข้อมูล"
        tax_no_patterns = [
        r'Tax Invoice No\.(\d+RC\d+/\d+)',  # Pattern 2
    ]

        for pattern in tax_no_patterns:
            match = re.search(pattern, ocr_result)

            if match:
                tax_no_group_0 = match.group(0)
    
            return tax_no_group_0

    #Lotus
    if lotus_confidence >= 60:
        tax_no_group_0 = "ไม่พบข้อมูล"
        tax_no_patterns = [
            r'RID(\d{14})',
            r'RID. B(\d{14})',
            r'B(\d{14})',
            r'(\d{14})',

        ]

        for pattern in tax_no_patterns:
            match = re.search(pattern, ocr_result)

            if match:
                tax_no_group_0 = match.group(0)  

        return tax_no_group_0


def extract_table(ocr_result, seven='ใบเสร็จรับเงิน/ใบกํากับภาษีอย่างย่อ', seven_end='ยอดสุทธิ์',cafe="No Customer",cafe_end ="VAT 7.00%",lotus="RID. ",lotus_end="ยอดรวม"):
    lines = ocr_result.split('\n')
    seven_match, seven_score = process.extractOne(seven, lines)
    seven_end_match, seven_end_score = process.extractOne(seven_end, lines)
    cafe_match, cafe_score = process.extractOne(cafe, lines)
    cafe_end_match, cafe_end_score = process.extractOne(cafe_end, lines)
    lotus_match, lotus_score = process.extractOne(lotus, lines)
    lotus_end_match, lotus_end_score = process.extractOne(lotus_end, lines)

    extracted_data = []
    start_extraction = False

    if seven_score >= 60 and seven_end_score >=60 or ((seven_score > cafe_score)and (seven_score>lotus_score))and ((seven_end_score > cafe_end_score)and (seven_end_score>lotus_end_score)) :
        for line in lines:
            line = line.strip()

            if not line and not extracted_data:
                continue

            if not start_extraction and line == seven_match:
                extracted_data.append("ใบเสร็จรับเงิน/ใบกํากับภาษีอย่างย่อ")
                start_extraction = True
            if seven_end_match in line:
                extracted_data.append(line)
                break

            if start_extraction and not line.startswith(seven_match):
                extracted_data.append(line)

        formatted_data = '\n'.join(extracted_data)
        return formatted_data

    if cafe_score >= 50 and cafe_end_score >=50 and cafe_end_score > lotus_score:
        for line in lines:
            line = line.strip()

            if not line and not extracted_data:
                continue

            if not start_extraction and line == cafe_match:
                extracted_data.append("ใบเสร็จรับเงิน/ใบกํากับภาษีอย่างย่อ")
                start_extraction = True
            if cafe_end_match in line:
                extracted_data.append(line)
                break

            if start_extraction and not line.startswith(cafe_match):
                extracted_data.append(line)
                

        formatted_data = '\n'.join(extracted_data)
        return formatted_data
    
    if lotus_score >= 50 and lotus_end_score >= 50:
        start_extraction = False
        extracted_data = []

        for line in lines:
            line = line.strip()

            if not start_extraction and line == lotus_match:
                extracted_data.append("TAX INVOICE (ABB)/RECEIPT (VAT INCLUDE)")
                start_extraction = True

            if start_extraction and not line.startswith(lotus_match):
                extracted_data.append(line)

            if lotus_end_match in line:
                break

        formatted_data = '\n'.join(extracted_data)
        return formatted_data

    return "ไม่พบข้อมูล"

def preprocess(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    erosion_kernel = np.ones((1, 1), np.uint8)
    eroded = cv2.erode(gray , erosion_kernel, iterations=1)
    dilation_kernel = np.ones((1, 1), np.uint8)
    dilated = cv2.dilate(eroded, dilation_kernel, iterations=1)

    text = tess.image_to_string(dilated, lang='tha+eng', config='--psm 6 --oem 3 --dpi 2400')
    return text

if __name__ == "__main__":
    app.run(debug=True)





