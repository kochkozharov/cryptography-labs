from gostcrypto import gosthash

def get_variant_number(full_name: str):

    data_bytes = full_name.encode('utf-8')

    hash_256 = gosthash.new('streebog256', data=data_bytes)

    digest = hash_256.digest()

    return digest[-1]

def main():
    fio = input("Введите ФИО: ")
    variant = get_variant_number(fio)
    print(f"Вариант: {variant}")    

if __name__ == "__main__":
    main()