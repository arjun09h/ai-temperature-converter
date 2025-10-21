from word2number import w2n
#   --------------------------------------------------   Constants    ---------------------------------------------------------
CONVERSION_9_5 = 9/5
CONVERSION_5_9= 5/9
OFFSET_32 = 32
OFFSET_273 = 273.15

    #  --------------------------------------------------   Functions    ---------------------------------------------------------
        # Conversions of Celsius
def c_to_k(c = 28):return c + OFFSET_273
def c_to_f(c = 28):return (c * CONVERSION_9_5) + OFFSET_32
        #  Conversions of Kelvin
def k_to_c(k = 230):return k - OFFSET_273
def k_to_f(k = 230):return ((k - OFFSET_273) * CONVERSION_9_5) + OFFSET_32
        #  Conversions of Fahrenheit
def f_to_c(f = 37):return (f - OFFSET_32) * CONVERSION_5_9
def f_to_k(f = 37):return ((f - OFFSET_32) * CONVERSION_5_9) + OFFSET_273
         
        #  --------------------------------------------------   Main Class    ---------------------------------------------------------
          
class temperature_converter:
    def __init__(self):  
        self.value = None         
        self.from_temperature = None   
        self.to_temperature = None    
        self.words = []
        
    #  Input_Finding
    
    def input_finding(self,text):
        text = text.replace("°"," ")
        self.words = text.lower().split()
        self.value = self.value_finding()
        self.from_temperature , self.to_temperature = self.unit_finding()
        if self.value is None or self.from_temperature is None or self.to_temperature is None:
            print("⚠️ Error Finding Values. Please Enter The Value Again. ")
            return
        
        self.from_temperature = self.from_temperature.upper()
        self.to_temperature = self.to_temperature.upper()

        result = self.decision_making(self.value , self.from_temperature , self.to_temperature)
        if isinstance(result, str):
            print(result)
        else:
            print (f"Sure {self.value:.2f}°{self.from_temperature} to {self.to_temperature} is {result:.2f}°{self.to_temperature} 🤖 ")

        # Value Finding
    
    def value_finding(self):
        temp_value_container = []
        temp_value = None
        numbers =["one","two","three","four","five","six","seven","eight","nine","ten","eleven",
                  "twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen",
                  "nineteen","twenty","thirty","forty","fifty","sixty","seventy","eighty",
                  "ninety","hundred","thousand","million","and","point"]
        for word in self.words:
            if word.isdigit():
                self.value = float(word)
                break
            else:
                if word in numbers:
                    temp_value_container.append(word)
        if temp_value_container:
            temp_value = " ".join(temp_value_container)
            try:
                self.value = (w2n.word_to_num(temp_value))
            except ValueError:
                self.value = None
        if self.value is None:
            print("Sorry, I couldn't find the temperature value in your request.🤖 ")
            return None
        return float(self.value)

        # Unit Finding
    
    def unit_finding(self):

        units = {"c": "celsius" , "celsius": "celsius",
                 "k" : "kelvin" , "kelvin" : "kelvin",
                  "f" : "fahrenheit" , "fahrenheit" : "fahrenheit" }
        
        temp_units = []

            # finding temperature 
        
        for w in self.words :
            if w in units :
                temp_units.append(units[w])
        
        if len(temp_units) < 2:
            return None,None
    
        return(temp_units[0],temp_units[1])

    def decision_making(self,value,from_temperature,to_temperature):

            #  Unit Variable

        from_unit = from_temperature.lower() 
        to_unit = to_temperature.lower()
            #  Logic 
        if from_unit in ["celsius","c"] and to_unit in ["kelvin","k"]:
             return c_to_k(value)
        elif from_unit in["c","celsius"] and to_unit in ["fahrenheit","f"]:
             return c_to_f(value)
        elif from_unit in ["kelvin","k"] and to_unit in  ["c","celsius"]:
             return k_to_c(value)
        elif from_unit in ["kelvin","k"] and to_unit in ["fahrenheit","f"]:
             return k_to_f(value)
        elif from_unit in ["fahrenheit","f"] and to_unit in["c","celsius"]:
             return f_to_c(value)
        elif from_unit in ["fahrenheit","f"] and to_unit in ["kelvin","k"]:
             return f_to_k(value)
        else:
             return "Invalid Conversion Unit 🤖"
        

            

        
                  
# User Input

print("hi! i am your personal temperature converting AI 🤖. How can i help you ? (Type,'exit' to quit) ") 
bot = temperature_converter()
while True:
    user_input = input("Enter the request here (eg. what is the coversion of 55 degree celsius to kelvin is ? ) 🤖 : ")
    if (user_input).lower() == 'exit':
        print("GoodBye ✌️")
        break    
    bot.input_finding(user_input)
