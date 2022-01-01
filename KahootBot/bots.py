from selenium import webdriver

import time
import usefull

class KahootBot:
    def __init__(self, name, driver, pin=None):
        """

            Arguments :
                name : the name the bot will have in the game
                driver : an instance of webdriver's driver (exemple : webdriver.Chrome())
                pin : optional, the game pin, recommand to give it while connecting

        """
        self.name = name
        self.pin = pin
        self.driver = driver
        self.connected = False
        self.score = 0
        self.currentQuestion = 0
        self.maxQuestion = 0
        self.currentlyPLaying = False
    
    def __repr__(self):
        return f'Kahoot Bot [{self.name}] on {self.pin} : Connection by {self.driver}'
    
    #GETTERS
    def getName(self): return self.name
    def getPin(self): return self.pin
    def getScore(self): return self.score

    #STATE GETTERS
    def isConnected(self): return self.connected
    def isCurrentlyPLaying(self): return self.currentlyPLaying

    #SETTERS
    def setName(self, name): self.name = name
    def setPin(self, pin): self.pin = pin

    def connect(self, pin=None):
        """

            Argsuments :
                pin : optional, the game pin
            
            Raise :
                Exception :
                    "Your game pin is not valid, try using another one" => Your game pin is incorect, verify it from the admin
                    "Can not connect without a game pin" => Neither when you created the bot or while conecting was a game pin gave

        """
        self.pin = pin if pin else self.pin
        if self.pin:
            #CONNECT TO KAHOOT
            print('open browser')
            self.driver.get('https://kahoot.it')

            #SEARCH FOR THE GAME PIN ENTRY, FILL IT UP AND CONNECT
            self.pin_entry = self.driver.find_element_by_id('game-input')
            self.pin_entry.send_keys(pin)
            self.validate_button = self.driver.find_element_by_class_name('button__Button-c6mvr2-0')
            self.validate_button.submit()
            time.sleep(1)

            try:
                self.driver.find_element_by_id('notification-bar__NotificationBar-uw7wkb-0')

            except Exception:
                #MEAN THAT THE ERROR PIN BAR DID NOT APPEARED, SO THE PIN IS OK, THEN GIVE A NAME
                self.name_entry = self.driver.find_element_by_id('nickname')
                self.name_entry.send_keys(self.name)
                self.validate_button = self.driver.find_element_by_class_name('button__Button-c6mvr2-0')
                self.validate_button.submit()

                self.connected = True

            else:
                raise Exception('Your game pin is not valid, try using another one')

        else:
            raise Exception('Can not connect without a game pin')

    def updateValues(self):
        try:
            self.score = int(self.driver.find_element_by_class_name('bottom-bar__Score-sc-1bibjvm-2').text())
        except Exception:
            self.currentlyPLaying = False