import pandas as pd

from Levenshtein import distance


ocr_result = "บริษัท เอก-ชัยฯ ขอนแก่น-บ้านศิลา (5098) 0105536092641 10400000200078 20/07/23 TAX INVOICE (ABB)/RECEIPT (VAT INCLUDE) เลย์เมี่ยงคําครบรส 69         31.00 โออิธิต้นตํารับ380 มล          20.00ป โค้กซีโร่กระบ๋อง 325        15.00ป ยอดรวม                   66.00"
actual_result = "บริษัท เอก-ชัยฯ ขอนแก่น-บ้านศิลา (5098) 0105536092641 10400000200078 20/07/23 TAX INVOICE (ABB)/RECEIPT (VAT INCLUDE) เลย์เมี่ยงคําครบรส 69         31.00 โออิชิต้นตํารับ380 มล          20.00v โค้กซีโร่กระป๋อง 325        15.00v ยอดรวม                   66.00"
# Calculate Levenshtein distance
levenshtein_distance = distance(ocr_result, actual_result)

# Calculate accuracy 
max_length = max(len(ocr_result), len(actual_result))
accuracy = 1 - (levenshtein_distance / max_length)

print(f"Levenshtein Distance: {levenshtein_distance}")
print(f"จำนวนอักขระทั้งหมด: {max_length}")
print(f"ความแม่นยำ: {accuracy:.2%}")

