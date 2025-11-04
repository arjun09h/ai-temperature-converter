from word2number import w2n
import spacy

nlp = spacy.load("en_core_web_sm")

# --------------------------------------------------
#  Main Class
# --------------------------------------------------

class TemperatureConverter:

    # --------------------------------------------------
    #  Static Conversion Functions
    # --------------------------------------------------

    @staticmethod
    def c_to_k(c=28):
        return c + 273.15

    @staticmethod
    def c_to_f(c=28):
        return (c * (9 / 5)) + 32

    @staticmethod
    def k_to_c(k=230):
        return k - 273.15

    @staticmethod
    def k_to_f(k=230):
        return ((k - 273.15) * (9 / 5)) + 32

    @staticmethod
    def f_to_c(f=37):
        return (f - 32) * (5 / 9)

    @staticmethod
    def f_to_k(f=37):
        return ((f - 32) * (5 / 9)) + 273.15

    # --------------------------------------------------
    #  Class Methods
    # --------------------------------------------------

    def __init__(self):
        self.value = None
        self.from_temperature = None
        self.to_temperature = None
        self.words = []
        
        self.conversion_map = {
            ('celsius', 'kelvin'): self.c_to_k,
            ('celsius', 'fahrenheit'): self.c_to_f,
            ('kelvin', 'celsius'): self.k_to_c,
            ('kelvin', 'fahrenheit'): self.k_to_f,
            ('fahrenheit', 'celsius'): self.f_to_c,
            ('fahrenheit', 'kelvin'): self.f_to_k,
        }

    def input_finding(self, text):
        """
        Main function to parse text and trigger conversion.
        """
        text = text.replace("°", " ")
        self.words = text.lower().split()
        
        self.value = self.value_finding()
        # Handle case where value_finding returns None
        if self.value is None:
            print("Sorry, I couldn't find the temperature value in your request.🤖 ")
            return

        self.from_temperature, self.to_temperature = self.unit_finding()

        if self.from_temperature is None or self.to_temperature is None:
            print("⚠️ Error Finding Units. Please rephrase your request. ")
            return

        # Normalize for consistency before calling decision_making
        self.from_temperature = self.from_temperature.lower()
        self.to_temperature = self.to_temperature.lower()

        result = self.decision_making(self.value, self.from_temperature, self.to_temperature)
        
        if isinstance(result, str):
            print(result) # Print error messages
        else:
            # Format output for clarity
            from_temp_str = self.from_temperature.capitalize()
            to_temp_str = self.to_temperature.capitalize()
            print(f"Sure! {self.value:.2f}°{from_temp_str} is {result:.2f}°{to_temp_str} 🤖")

    def value_finding(self):
        """
        Finds the numerical value in the user's input.
        (Logic unchanged from original)
        """
        temp_value_container = []
        temp_value = None
        numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                   "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
                   "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty",
                   "ninety", "hundred", "thousand", "million", "and", "point"]
        
        for word in self.words:
            if word.isdigit():
                self.value = float(word)
                break
            else:
                try:
                    # Check if word is a float (e.g., "20.5")
                    val = float(word)
                    self.value = val
                    break
                except ValueError:
                    # If not a digit or float, check if it's a number word
                    if word in numbers:
                        temp_value_container.append(word)

        if self.value is None and temp_value_container:
            temp_value = " ".join(temp_value_container)
            try:
                self.value = (w2n.word_to_num(temp_value))
            except ValueError:
                self.value = None

        if self.value is None:
            return None
            
        return float(self.value)

    def unit_finding(self):
        """
        Finds the 'from' and 'to' units using spaCy.
        (Logic unchanged from original)
        """
        units = {"c": "celsius", "celsius": "celsius",
                 "k": "kelvin", "kelvin": "kelvin",
                 "f": "fahrenheit", "fahrenheit": "fahrenheit"}

        from_unit = None
        to_unit = None

        text = " ".join(self.words)
        doc = nlp(text)

        # finding from temperature
        temp_value = None
        for token in doc:
            try:
                if float(token.text) == float(self.value):
                    temp_value = token
            except ValueError:
                continue
        if temp_value:
            for child in temp_value.children:
                if child.text in units:
                    from_unit = units[child.text]
            if from_unit is None and temp_value.head.text in units:
                from_unit = units[temp_value.head.text]
            
            if from_unit is None:
                for ancestor in temp_value.ancestors:
                    if ancestor.text in units:
                        from_unit = units[ancestor.text]
                        break

        # finding to temperature
        to_token_found = False
        for token in doc:
            if token.lemma_ == "to":
                to_token_found = True
                continue
            if to_token_found and token.text in units:
                if units[token.text] != from_unit:
                    to_unit = units[token.text]
                    break

        if to_unit is None:
            for word in self.words:
                if word in units and from_unit != units[word]:
                    to_unit = units[word]
                    break
        
        # Handle cases where units are the same
        if from_unit is not None and from_unit == to_unit:
             to_unit = None # Force a search for a different unit

        return from_unit, to_unit

    def decision_making(self, value, from_temperature, to_temperature):
        # Create the key tuple from the normalized inputs
        conversion_key = (from_temperature, to_temperature)
        
        # Find the correct function in the map
        conversion_function = self.conversion_map.get(conversion_key)

        if conversion_function:
            return conversion_function(value)
        else:
            return "Invalid Conversion Unit -------------------------------------------------- 🤖"


# --------------------------------------------------
#  User Input Loop
# --------------------------------------------------

print("hi! i am your personal temperature converting AI 🤖. How can i help you ? (Type,'exit' to quit) ")
bot = TemperatureConverter()
while True:
    user_input = input("Enter the request here (eg. what is the conversion of 55 degree celsius to kelvin ? ) 🤖 : ")
    if (user_input).lower() == 'exit':
        print("GoodBye ✌️")
        break
    bot.input_finding(user_input)

