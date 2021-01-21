from my_parser import parse_dir
from my_util import for_training_dir, for_competition_dir, print_picture
from my_net import HopfieldNeuroNet


def main():
    feed = parse_dir(for_training_dir)

    print('>> Pictures for training')
    for picture in feed:
        print_picture(picture)

    print('>> Teaching...')
    neuronet = HopfieldNeuroNet()
    for picture in feed:
        neuronet.teach(picture)

    enemies = parse_dir(for_competition_dir)


    print('>> Pictures recognizing...')
    for picture in enemies:
        print('>> Modified picture:')
        print_picture(picture)
        recognized, recshape, iters = neuronet.recognize(picture)

        if recognized:
            print(f'>> Success. Picture recognized in {iters} iterations:')
        else:
            print(f'>> Fail. Picture not recognized in {iters} iterations...')
        print('>> Recognized picture:')
        print_picture(recshape)


if __name__ == '__main__':
    main()

