#!/usr/local/bin/python
#Author: Saira Montermoso
#Editor: Benjamin Strauss

import requests
import htmlement

def retrieveGOR1(sequence):
    """ Retrieves predications for input sequence
        GOR1 server appears to finish near instantneous so no sleep is implemented

        Param:
            sequence: str, primary protein sequence
        
        Returns:
            str, secondary structury prediction
        """
    if not isinstance(sequence, str):
        raise TypeError("GOR1 Error - Bad Sequence")
    
    r = requests.post('http://cib.cf.ocha.ac.jp/bitool/GOR/GOR.php', data={'aasequence':sequence, 'OK':'start prediction'})
    root = htmlement.fromstring(r.text)
    
    try:
        pred = root.findall("body/pre")[1]
        dummy = pred.text
        
        gor = []
        for lines in dummy.splitlines():
            line = lines.split()
            if (len(line) == 7):
                gor.append(line[6].upper())
        gorPred = "".join(gor);
        if len(gorPred) != len(sequence):
             print('GOR1 failure - Code 1')
        else:
            return gorPred;

    except (IndexError, LengthError):
        print('GOR1 failure - Code 2')
