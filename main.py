import re
from sympy import factorint, isprime
from math import gcd
from PyPDF2 import PdfReader
from get_variant_number import get_variant_number


def parse_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
    
    text_clean = re.sub(r"\s+", "", full_text)
    
    pattern = r"a\[([0-9]+)\]=([0-9]+).*?b\[\1\]=([0-9]+)"
    
    matches = re.findall(pattern, text_clean, re.DOTALL)
    pairs = [(int(a), int(b)) for _, a, b in matches]
    return pairs

def main():
    pdf_path = "Лабораторная 2.pdf"
    full_name = "Кочкожаров Иван Вячеславович"
    variant_number = get_variant_number(full_name)
    print(f"ФИО: {full_name}")
    print(f"Вариант: {variant_number}")
    pairs = parse_pdf(pdf_path)
    a = pairs[variant_number][0]
    b = pairs[variant_number][1]
    print(f"a = {a}")
    print(f"b = {b}")

    bs = [b for _, b in pairs]
    bs.pop(variant_number)
    factors_b=[]
    for other_b in bs:
        divisor1 = gcd(b, other_b)
        if (isprime(divisor1)):
            divisor2 = b // divisor1
            if (isprime(divisor2)):
                factors_b.append(divisor1)
                factors_b.append(divisor2)
                break
    print("Разложение b:")
    print(*factors_b, sep=' * ')

    print("Разложение a: ")
    factors_a_dict = factorint(a)
    factors_a = [key for key, count in factors_a_dict.items() for _ in range(count)]
    print(*factors_a, sep=' * ')

if __name__ == "__main__":
    main()