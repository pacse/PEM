'''
=== Put it all together into an Enigma class for the final machine ===
                              [VERIFIED]                              
'''

import KeyLampboard as kl
import plugboard as pb
import reflector as rf
import rotor as rtr

# flag to show/hide debug messages
DEBUG = False

class Enigma:
  def __init__(self, reflector: str | rf.Reflector, rotors: list[str] | list[rtr.Rotor], notches: list[str], start_positions: str, plugs: list[str]) -> None:
    '''
    Initialize an Enigma machine
    Parameters:
    reflector - Reflector wiring
    rotors - List of rotor wirings
    notches - List of strings of rotor notches for each rotor
    start_positions - List of rotor start positions
    plugs - List of plugboard 'plugs'
    '''

    # === Initialize Reflector ===
    if isinstance(reflector, str): # if reflector is a string, create a new Reflector object
        self.rf = rf.Reflector(reflector)
    else: # if reflector is a Reflector object, use it
        self.rf = reflector

    # === Initialize Rotors ===
    self.rtrs: list[rtr.Rotor] = [] # list for inited rotors
    
    # ensure rotors, notches, and start_positions are the same length
    assert len(rotors) == len(notches) == len(start_positions), f"Error in rotor initilization: Length of rotors ({len(rotors)}), notches ({len(notches)}), and start positions ({len(start_positions)}) must be equal"

    # append rotors to list
    for i, rotor in enumerate(rotors):
        if isinstance(rotor, str): # if rotor is a string, create a new Rotor object
            rotor = rtr.Rotor(rotor, [notch for notch in notches[i]])
        else: # if rotor is a Rotor object, use it
            rotor = rotor
        rotor.rotate_to_letter(start_positions[i]) # rotate to start pos
        self.rtrs.append(rotor) # append to list

    # === Initialize Plugboard ===
    self.pb = pb.Plugboard(plugs)

    # === Initialize Keyboard and Lampboard ===
    self.kb = kl.Keyboard()
    self.lb = kl.Lampboard()

  def pass_letter(self, letter: str) -> str:
    '''
    Passes a letter through the Enigma machine
    Parameters:
    letter - The letter to be passed through the Enigma machine
    '''

    # debug loop
    if DEBUG:
        signal = self.kb.forward(letter)  # convert letter to signal
        print(signal)

        signal = self.pb.forward(signal)  # pass through plugboard
        print(signal)

        # pass through rotors right to left
        for i, rotor in enumerate(reversed(self.rtrs)):
            print(f"Rotor {i+1} ({rotor.position})")
            signal = rotor.forward(signal)
            print(signal)

        signal = self.rf.reflect(signal)  # pass through reflector
        print(signal)

        # pass through rotors left to right
        for i, rotor in enumerate(self.rtrs):
            print(f"Rotor {i+1} ({rotor.position})")
            signal = rotor.backward(signal)
            print(signal)

        signal = self.pb.backward(signal) # pass through plugboard
        print(signal)

        letter = self.lb.forward(signal)  # finally, convert signal to letter
        return letter
      
    # normal loop
    else:
      signal = self.kb.forward(letter)  # convert letter to signal
      signal = self.pb.forward(signal)  # pass through plugboard
      
      # pass through rotors right to left
      for rotor in reversed(self.rtrs):
        signal = rotor.forward(signal)

      signal = self.rf.reflect(signal)  # pass through reflector

      # pass through rotors left to right
      for rotor in self.rtrs:
        signal = rotor.backward(signal)

      signal = self.pb.backward(signal) # pass through plugboard
      letter = self.lb.forward(signal)  # finally, convert signal to letter
      return letter

  def step(self) -> None:
    '''
    Steps rotors after a keypress
    '''
    to_rotate = [False] * len(self.rtrs)

    # rightmost always rotates
    to_rotate[-1] = True

    # check each rotor (right to left) for rotation, stopping
    # at the second to left rotor to prevent IndexErrors
    for i in range(len(self.rtrs)-1, 1, -1):
      # if current is rotating and at notch, cascade
      if to_rotate[i] and self.rtrs[i].position in self.rtrs[i].notch:
        to_rotate[i-1] = True

    # === double step ===
    middle_index = len(self.rtrs) // 2
    # all step if middle rotor at notch
    if self.rtrs[middle_index].position in self.rtrs[middle_index].notch:
      to_rotate = [True] * len(self.rtrs)

    # rotate rotors
    for i, rotate in enumerate(to_rotate):
      if rotate:
        self.rtrs[i].rotate()

  def set_key(self, key: str) -> None:
    '''
    Sets the key for the enigma machine
    Parameters:
    key - The key to set
    '''
    # ensure we have enough rotor positions
    assert len(self.rtrs) == len(key), f"Error in message passing (set_key): Length of rotors ({len(self.rtrs)}) and rotor positions ({len(key)}) must be equal"
  
    # set start positions
    for i, rotor in enumerate(self.rtrs):
      rotor.rotate_to_letter(key[i])
  
  def pass_message(self, message: str, key: str) -> str:
    '''
    Passes a provided message through the enigma machine
    Parameters:
    message - The message to be passed through the enigma machine
    rotor_positions - Rotor positions at the start of the message
    '''

    # screw ring settings, may implement later
    
    # set key
    self.set_key(key)

    # pass message
    result = ""
    for char in message: # pass each letter and rotate
      if DEBUG:
        print(f"Passing: {char}")
      self.step()
      result += self.pass_letter(char)

    return result