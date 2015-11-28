import crcmod


def crc32(string, make_crc32=crcmod.predefined.mkPredefinedCrcFun('crc-32')):
    crc = make_crc32(bytes(string, encoding='utf-8'))
    if crc > 2147483647:  # 2 ** 32 // 2 - 1
        crc = -(crc >> 1)
    return crc


def crc64(string, make_crc64=crcmod.predefined.mkPredefinedCrcFun('crc-64')):
    crc = make_crc64(bytes(string, encoding='utf-8'))
    if crc > 9223372036854775807:  # 2 ** 64 // 2 - 1
        crc = -(crc >> 1)
    return crc
