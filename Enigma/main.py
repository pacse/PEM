import KeyLampboard as kl
import plugboard as pb
import reflector as rf
import rotor as rtr
import enigma

if __name__ == "__main__":
    # Keyboard, Lampboard and Plugboard
    KB = kl.Keyboard()
    LB = kl.Lampboard()
    PB = pb.Plugboard(["AR", "GK", "OX"])

    # Reflectors
    A = rf.A
    B = rf.B
    C = rf.C

    # Rotors
    I = rtr.I
    II = rtr.II
    III = rtr.III
    IV = rtr.IV
    V = rtr.V

    # Enigma Machine
    Enigma = enigma.Enigma(B, [IV, II, III], ["J", "Q", "V"], "DOG", ["BQ", "CR", "DI", "EJ", "KW", "MT", "OS", "PX", "UZ", "GH",])

    message = "boot klar x bei j schnoor j etwa zwo siben x nov x sechs nul cbm x proviant bis zwo nul x dez x benoetige glaeser y noch vier klar x stehe marqu bruno bruno zwo funf x lage wie j schaefer j x nnn www funf y eins funf mb steigend y gute sicht vvv j rasch".upper()
    updated = ""
    for char in message:
        if char != " ":
            updated += char.upper()
    print(updated)
    result = Enigma.pass_message(updated, "AQL")
    print(result)
    correct= "qlxyx obhjh nggto wwduj lbxro ahmuv yxtiy rhhxk bwzgh myvhb lgzew hyarl xeizx ryyyx owfns yfabl nsese fjogg jzbon ejexc dhmem ooigl kesyz bffya utqti hffcg jsarh uzqef qxepp ivrzr cttpn fdvdu bqtxv rsbpp kvwvk okrwf idwwn obuyb kmilx jwbbf dqkyz xxeps nrpbr kbvku rkbmq ipyyb vacuz oruly dwrkf erryf jnrfk veksn lchyx vdtcm elyjf yhomp wzymk zrjwq fwmxp wwywk wbred gkjzz zpubl fvxdq hawrg vjarc jrlmi pvbbg npksr ulofx dapey ltnfw mfcwd gkgzw anqkp ldblj nbmqo szqsm lqllh wwddp zrivd eufeg pwllc lgvtp nouwa utsnq ktdci regut eihpd fvr".upper()
    updated = ""
    for char in correct:
        if char != " ":
            updated += char
    #print(updated)

    #print(Enigma.pass_message(result, "CAT"))


    '''
    I.show()
    I.rotate_to_letter("G")
    I.show()
    '''