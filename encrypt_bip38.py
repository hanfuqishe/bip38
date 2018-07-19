#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys, getopt, getpass
import bip38
import qrcode

def main(argv):
    inputfile = '-'
    outputfile = '-'
    passphrase = ''

    try:
        opts, args = getopt.getopt(argv,"hp:i:o:",["passphrase=","ifile=","ofile="])
    except getopt.GetoptError:
        print 'encrypt_bip38.py -p <passphrase> -i <inputfile> -o <outputfile>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'encrypt_bip38.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-p", "--passphrase"):
            passphrase = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if passphrase == '':
         passphrase   = getpass.getpass('Please input passphrase      :')
         temp         = getpass.getpass('Please input passphrase again:')
         if passphrase != temp:
              print "Verify failed!"
              sys.exit()


    if inputfile == '-':
         fin = sys.stdin
    else:
         fin = open(inputfile, "r")

    if outputfile == '-':
        fout = sys.stdout
        qrcodefoldername = 'privkey.bip38.qrcode'
    elif outputfile.endswith('.csv'):
        strlen=len(outputfile)
        qrcodefoldername=outputfile[0:strlen-4] + '.bip38.qrcode'
    else:
        qrcodefoldername = outputfile + '.bip38.qrcode'
        outputfile=outputfile+'.csv'

    fout = open(outputfile, "w")
    qrcodefolder = os.path.exists(qrcodefoldername)
    if not qrcodefolder:
        os.makedirs(qrcodefoldername)
         
    fout.write("Address, BIP38 Encrypted Private Key\n")

    while True:
        line = fin.readline()
        if not line:
            break

        items = line.split()

        if items[0]=='Address:':
            address = items[1]
            sys.stdout.write(address+'\t... ')
        elif items[0] == 'Privkey:':
            #print "Encrypt:" + items[1]+"  "+passphrase
            privkey_bip38 = bip38.bip38_encrypt(items[1], passphrase)
            fout.write(address+','+privkey_bip38+'\n')
            fout.flush()
            sys.stdout.write('bip38 encrypted: '+ privkey_bip38 +'\t... ')

            img=qrcode.make(privkey_bip38)
            img.get_image()
            img.save(qrcodefoldername+ '/' + address +'.png')
            sys.stdout.write('QRcode done. \n')

    fin.close()
    fout.close()


if __name__ == "__main__":
    main(sys.argv[1:])
