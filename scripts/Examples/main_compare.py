import sys
sys.path.append('../')

from Service.compare_image_v2 import CompareImageV2

if __name__ == '__main__':
    id = '2454100925'

    result = CompareImageV2().get_similares(id)

    print(result)
