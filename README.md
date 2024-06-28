# FinalProject
### การติดตั้งเว็บไซต์ดึงข้อมูลส่วนสำคัญของใบกำกับภาษีอย่างย่อ:

ก่อนที่จะทำการใช้งานเว็บไซต์ ควรที่จะทำตามขั้นตอนตามที่ระบุด้านล่างนี้ไว้

#### ขั้นตอนการติดตั้ง Visual Studio Code:

1. **Windows:**
   - ดาวน์โหลด Visual Studio Code ได้ที่ (https://code.visualstudio.com/Download)
   - ทำการติดตั้งโปรแกรม Visual Studio Code ตามคู่มือการใช้งาน

2. **MacOS:**
   - ดาวน์โหลดตัวติดตั้ง Visual Studio Code ได้ที่ (https://code.visualstudio.com/Download)
   - เปิดไฟล์ .dmg ที่ดาวน์โหลดและลาก Visual Studio Code เข้าไปในโฟลเดอร์ Applications

3. **Linux:**
   - ทำตามคำแนะนำสำหรับการติดตั้งสำหรับ Linux ได้ที่ (https://code.visualstudio.com/docs/setup/linux)

#### ขั้นตอนการติดตั้ง TesseractOCR:

1. **Windows:**
   - ดาวน์โหลด TesseractOCR ได้ที่ (https://github.com/UB-Mannheim/tesseract/wiki)
   - ทำการติดตั้ง TesseractOCR โดยปฏิบัติตามคู่มือการใช้งาน

2. **MacOS:**
   - ใช้ Homebrew เพื่อติดตั้ง TesseractOCR โดยใช้คำสั่ง `brew install tesseract`

3. **Linux:**
   - ใช้เครื่องมือการจัดการแพคเกจของระบบปฏิบัติการ Linux ที่ใช้ เช่น APT สำหรับ Ubuntu/Debian หรือ YUM สำหรับ Fedora เพื่อติดตั้ง TesseractOCR
     - สำหรับ Ubuntu/Debian: `sudo apt install tesseract-ocr`
     - สำหรับ Fedora: `sudo yum install tesseract-ocr`

#### การติดตั้งไลบารี่ที่จำเป็น

   - Python จำเป็นต้องถูกติดตั้ง ถ้ายังไม่ติดตั้งสามารถติดตั้งผ่านทาง installer จาก:
	-  สำหรับ window: (https://www.python.org/downloads/windows/)  
	-  สำหรับ Macos: (https://www.python.org/downloads/macos/)
      หรือตั้งตั้งผ่าน terminal ได้ที่:
	 - สำหรับ Macos: 'brew install python'  
	 - สำหรับ Linux: 'sudo apt install python3' 
   - ไลบารี่ที่จำเป็นอื่นๆสามารถติดตั้งได้ผ่านทาง 'pip install -r requirements.txt'

#### การตั้งค่าต่างๆใน Visual Studio Code:
        - หลังจากติดตั้ง Visual Studio Code และ TesseractOCR เรียบร้อยแล้ว
    1. ทำการเปิดไฟล์ app.py ที่อยู่ใน source code folder 
    2. ไปที่บรรทัดที่ 7 จะเจอการตั้งค่า TesseractOCR แบบนี้ tess.pytesseract.tesseract_cmd = r"ที่อยู่จัดเก็บของ Tesseract-OCR"  ให้ทำการเปลี่ยน "ที่อยู่จัดเก็บของ Tesseract-OCR" ให้ตรงกับที่อยู่ที่ติดตั้งโปรแกรม TesseractOCR
เมื่อเสร็จสิ้นทุกอย่าง สามารถใช้คำสั่ง 'flask run' ในคอนโซล เพื่อทำการรันเว็บไซต์ขึ้นมา

**การเปลี่ยนภาษา:**

โดยปกติแล้ว TesseractOCR จะถูกตั้งค่าไว้ที่ ภาษาอังกฤษ แต่ถ้าต้องการเปลี่ยนให้สามารถรองรับภาษาอื่นๆได้ให้ไปที่บรรทัด
'text = tess.image_to_string(dilated, lang='tha+eng', config='--psm 6 --oem 3 --dpi 2400')' ตรงที่ lang="ตามด้วยภาษาที่ต้องการ+ภาษาที่รองรับเพิ่ม"สามารถปรับเปลี่ยนหรือเพิ่มได้

**การเพิ่มภาษาใหม่:**

ถ้าต้องการเพิ่มภาษาใหม่ ที่ไม่ได้เพิ่มมาจากการติดตั้ง TesseractOCR ในตอนแรก สามารถไปดาวน์โหลดไฟล์ภาษาเพิ่มเติมได้ที่ TesseractOCR GitHub repository       (https://github.com/tesseract-ocr/tessdata)
หลังจากดาวน์โหลดไฟล์ภาษาเพิ่มเติมเรียบร้อยแล้ว ให้ไปที่โฟลเดอร์ที่จัดเก็บของ TesseractOCR จะมีโฟล์เดอร์ที่ชื่อว่า tessdata ให้ทำการวางไฟล์ภาษาเพิ่มเติมเข้าไป
หลังจากเสร็จสิ้นให้เรามาเปลี่ยนพารามิเตอร์ เพื่อให้สามารถรับภาษาใหม่ได้ ได้ที่บรรทัด
'text = tess.image_to_string(dilated, lang='tha+eng+fra', config='--psm 6 --oem 3 --dpi 2400')'  # ตัวอย่างเพิ่มภาษาฝรั่งเศษเข้ามา
