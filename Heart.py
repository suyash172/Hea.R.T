import os
import speech_recognition as sr
import win32com.client
import webbrowser

import google.generativeai as genai
from config2 import apikey
from PIL import Image
import random

os.environ["API_KEY"] = "AIzaSyDW-oUtLpVpB63ZoaNBrgKZazY2CXLpLjM"
genai.configure(api_key=os.environ["API_KEY"])
speaker = win32com.client.Dispatch("SAPI.SpVoice")



total_symptoms_matched = 0
query = ""
chatStr = ""
symtoms_list = []
actual_disease_list = []
disease_priority_list = []

# D1 - D10:
Thyroid_disease_Symptoms_01 = ["unintensional weight gain or weightloss", "Fatigue", "poor concentration", "palpitations", "constipation", "dry skin", "tremors"]
Dengue_Symptoms_02 = ["high fever", "Severe headache" , "muscles and joints pain","development of skin rashes", "fatigue","vomiting", "mild bleeding"]
Malaria_Symptoms_03 =["profuse sweating" , "headache" , "abdominal pain" , "muscle pain" , "nausea" , "vomiting" ,"diarrhoea" ,"anaemia","deep breathing and respiratory distress" ,"clinical jaundice andevidence of vital organ dysfunction" ,"impaired consciousness" ,"bloodystool" ,"convulsions" ,"coma"]
Hypothyroidism_Symptoms_04 = ["weight gain" ,"increased blood", "cholesterol level" ,"increased sensitivity to cold" ,"constipation" ,"dry skin" ,"puffy face" ,"hoarseness" ,"muscle weakness", "aches", "tenderness and stiffness" ,"joint pain", "stiffness", "swelling" ,"irregular menstrual periods or amenorrhea" ,"dry hair or hair loss"]
Typhoid_Symptoms_05 = [ "low to high fever" ,"headache and body pain" ,"loss of appetite and weight Loss" ,"dry cough ","sweating","abdominal pain" ,"swelling in abdomen" ,"diarrhoea or constipation", "itching or rashes" ]
Kidney_Symptoms_06 = ["pain in the abdomen or lower back","pain worsens during movement" ,"blood in urine" ,"pusin urine" ,"fever" ,"difficulty in urination", "feeling of urgency", "frequent,painful", "burning urination" ,"Nausea", "vomiting"]
Heart_attack_symptoms_07 = ["discomfort in the chest region","pressure or tightness in the chest" ,"pain or discomfort in the arm","back or neck region- usually on the left side" ,"Excessive sweating","Shortness of breath", "either on exertion or at rest" ,"Nausea","Vomiting" ,"Dizziness"]
Depression_symptoms_08 = ["hopeless outlook", "loss of interest", "increased fatigue and sleep problems", "anxiety" , "irritability" ,"changes in appetite and weight "]
Appendicitis_symptoms_09 = ["nausea", "vomiting", "fever", "fast heartbeats", "foul breath" ,"constipation" ,"frequent urination"]
Braintumor_symptoms_10=[ "Headache" ,"Weakness in the limbs, face, or one side of the body" ,"Impaired coordination" , "Difficulty while walking" ,"Difficulty reading and talking","taste and smell" ,"Bladder control problems" ,"Changes in mood, personality, or behavior" ,"Nausea or vomiting" ,"Memory loss"]

# D11 - D20
lung_cancer_symptoms_11 = ["persistent coughing", "chest pain that worsens with deep breathing, coughing or laughing", "hoarseness", "loss of appetite and weight loss", "shortness of breath", "fatigue", "wheezing", "coughing up blood"]
migraine_symptoms_12 = ["intense headache, often on one side of the head", "throbbing or pulsing pain", "sensitivity to light, noise and smells", "nausea and vomiting", "blurred vision", "lightheadedness", "fainting"]
hyperthyroidism_symptoms_13 = ["rapid or irregular heartbeat", "anxiety and irritability", "weight loss", "difficulty sleeping", "tremors in hands and fingers", "increased sweating", "heat sensitivity", "changes in menstrual patterns"]
throat_cancer_symptoms_14 = ["sore throat", "pain in swallowing", "hoarseness", "swelling or lumps in the neck or throat", "ear pain or trouble hearing", "constant coughing", "bad breath"]
kidney_failure_symptoms_15 = ["decreased urination or no urination", "swelling in legs, ankles, and feet", "fatigue and weakness", "shortness of breath", "confusion or difficulty concentrating", "nausea and vomiting", "seizures or coma (in severe cases)"]
chicken_pox_symptoms_16 = ["rash that begins as small red bumps and then turns into blisters", "itching", "fever", "headache", "fatigue", "loss of appetite", "nausea"]
tuberculosis_symptoms_17 = ["persistent coughing that lasts for more than three weeks", "blood in coughed-up phlegm", "chest pain", "weakness and fatigue", "weight loss", "loss of appetite", "fever and chills", "night sweats"]
urine_infection_symptoms_18 = ["frequent urges to urinate", "pain or burning sensation while urinating", "cloudy or strong-smelling urine", "lower abdominal pain or pressure", "fever or chills (in more severe cases)"]
blood_cancer_symptoms_19 = ["fatigue and weakness", "shortness of breath", "unexplained weight loss", "easy bruising or bleeding", "recurrent infections", "swollen lymph nodes, especially in the neck, armpit or groin", "bone pain or tenderness"]
piles_symptoms_20 = ["Pain or discomfort during bowel movements", "Itching or swelling around the anus", "Bright red blood on toilet tissue, stool or in the toilet bowl", "Painful swelling or lumps near the anus", "Leakage of feces", "Mucus discharge after a bowel movement"]

# D21 - D30
Viral_Fever_Symptoms_21 = ["chills", "tiredness", "fever", "fatigue", "nausea", "running nose", "blocked nose", "cough", "muscle pain", "vomiting", "diarrhoea"]
Pneumonia_Symptoms_22 = ["headache", "confusion", "dry cough", "musle pain", "clammy skin", "shaking chills", "loss of appetite", "shortness of breath", "high fever", "high respiratoy", "incresed pulsed rate", "low energy", "chest pain", "cough", "changing colour of lips"]

# D31-D40:
Vitamin_D_Deficiency_Symptoms_31 = ["fatigue", "hair loss", "back pain", "weakness in muscles", "mood swings", "frequent infection", "slow healing", "cramps"]
Hernia_Symptoms_33 = ["dull pain in affected area", "swelling in the affected area", "burning sensation", "bulging", "buildup of pressure"]
Skin_Cancer_Symtoms_32 = ["firm lump", "brownish scar", "Waxy translucent bump", "tender and itchy moles", "open sores on skin", "changes in sensation", "new change in an existing mole", "bleeding or oozing out moles", "changes appearance of the skin", "ppearance of new spot-on skin", "red and scaly patches on the skin", "red sore inside the mouth or ears", "unusual growth of patches or sores on the skin"]
Uric_Acide_Symptoms_34 = ["fatigue", "dry skin", "constipation", "swollen joints", "muscle stiffness", "kidney disorders", "muscle weakness", "pain and stiffness in joints", "aches and tenderness of muscles", "sudden and server pain in a particular joint"]
Asthama_Symptoms_35 = ["shortness of breath", "chest pain", "wheezing and coughing"]
Acidity_Symtomps_36 = ["nausea", "heartburn", "bad breath", "indigestion", "constipation", "restlessness", "regurgitation", "inflammation", "stomachulcers", "excessive vomiting", "sour taste in mouth", "difficulty swallowing", "burning sensation in mouth and throat", "server pain in chest or abdomen"]
Food_Poisoning_Symptoms_37 = ["abdominal pain and cramps", "diarrhoea", "headache", "vomiting", "fever and chills"]
Fatty_Liver_Symptoms_38 = ["abdominal pain or discomfort", "pain in upper right abdomen", "fatigue", "weight loss", "loss of appetite", "mental confusion", "abdominal swelling", "reddish palms"]
Anxiety_Symptoms_39 = ["nausea", "fatigue", "sweating", "dizziness", "headaches", "being irritable", "stomach upsets", "inability to rest", "rapid breathing", "rapid heartbeat", "shortness of breath", "electric shock feeling", "trouble in concentration", "shooting pains in the face"]
Vitamin_B12_Deficiency_Symptoms_40= ["loss of appetite", "weight loss", "constipation", "anaemia", "dementia", "dementia", "depression", "increase the risk of psychosis"]

# D41 - D50:
Stomach_Ulcer_41=["Abdominal pain","Bloatin","Pain that recedes after eating","Nausea","Feeling of fullness after a small meal","Vomit streaked with blood","Very dark stools","Tiredness","Pale skin","Loss of weight"]
Gerd_42=["Hoarseness of voice","Difficulty breathing","Shortness of breath", "tooth decay", "Persistent cough", "Burning sensation in the chest"]
Hypertension_43=["Dizziness","Chest Pain","Heart attack","Headaches","Bleeding Nose","Visual Changes","Shortness of Breath","Flushing or Blushing","Narrowing of blood vessels","Formation of plagues in the blood vessels"]
Psoriasis_44=["Fever","Chills","Diarrhoea","Itching","Pus-Filled Blisters","Small scaling spots","Discolouration of nails","Abnormal nail growth","Swollen and stiff joints","Red patches on the skin","Severe Itchy and burning skin","Dry, cracked and bleeding skin","Thickened, pitted or ridged nails","Skin covered with thick and silvery scales"]
Liver_Problem_45=["Jaundice","Weakness","Weight loss","Vomiting","Fatigue","Swelling of the limbs","Itches and rashes","Dark urine","Bloody stool, or dark stools","Pain in the abdominal region","Swelling in the abdominal region","Slower blood clotting"]
Flu_46=["Cough","Fever accompanied by chills","Blocked or running nose","Sore throat","Body pain","Headaches","Fatigue and tiredness","Loss of appetite","Secondary bacterial infections","Nausea and Vomiting"]
Calcium_Deficiency_47=["Fainting","Anxiety","Depression","Tooth Erosion","Loss of appetite","Muscle spasms","Muscle cramps","Difficulties in swallowing","Confusion or Memory loss","Weak and brittle fingernails","Easy fracturing of the bones","Numbness and tingling effect in fingers, hands, feet, and face"]
Gastric_48=["Nausea","Hiccups","Bloating","Indigestion","Upset stomach","Abdominal pain","Vomiting blood","Loss of appetite","Black, tarry stools","Gnawing or burning in the upper abdomen"]
Fever_49=["Chills","Fatigue","Paleness","Confusions","Shivering","Seizures", "Vomiting","Diarrhoea","Headache","Sore eyes","Flushed skin","Dehydration","Loss of appetite","Warm forehead","Excessive sleepiness","Difficulty in swallowing","A general feeling of weakness","Greater irritability than usual in infants or young children"]
Blood_Pressure_50=["Dizziness","Chest pain","Heart disease","Nose Bleeding","Kidney failure","Breathlessness","Severe headaches","Heart or Brain Stroke in the most severe cases"]

Covid_19_Symptoms_57 = ["cough", "fever", "sore throat", "shortness of breath", "headache", "diarrhoea", "loss of taste or smell", "aches and pains"]

# Desiase names dictionary
Disease_names = {"""Thyroid :Here's a detailed overview of the thyroid gland and thyroid-related disorders:

What is the Thyroid Gland?

The thyroid gland is a small, butterfly-shaped gland located in the neck, just below the Adam's apple. It plays a crucial role in regulating various bodily functions, including metabolism, growth, and development.

Functions of the Thyroid Gland

The thyroid gland produces two main hormones:

Triiodothyronine (T3): This hormone is responsible for regulating metabolism, energy production, and growth.
Thyroxine (T4): This hormone is converted to T3 in the body and also plays a role in regulating metabolism and energy production.
The thyroid gland also produces a third hormone, calcitonin, which helps regulate calcium levels in the blood.

Thyroid Disorders

There are several thyroid disorders that can affect the gland's function and hormone production. Some of the most common thyroid disorders include:

Hypothyroidism: This is a condition where the thyroid gland does not produce enough thyroid hormones, leading to symptoms such as fatigue, weight gain, and dry skin.
Hyperthyroidism: This is a condition where the thyroid gland produces too many thyroid hormones, leading to symptoms such as weight loss, anxiety, and rapid heartbeat.
Thyroid Nodules: These are abnormal growths on the thyroid gland that can be benign or cancerous.
Thyroid Cancer: This is a type of cancer that affects the thyroid gland.
Thyroiditis: This is inflammation of the thyroid gland, which can be caused by a variety of factors, including autoimmune disorders and infections.
Causes of Thyroid Disorders

Thyroid disorders can be caused by a variety of factors, including:

Genetics: Some thyroid disorders can be inherited.
Autoimmune Disorders: Conditions such as Hashimoto's thyroiditis and Graves' disease can cause thyroid disorders.
Radiation Exposure: Exposure to radiation can increase the risk of thyroid cancer.
Iodine Deficiency: Iodine is essential for thyroid hormone production, and a deficiency can lead to hypothyroidism.
Thyroid Surgery: Surgery to remove part or all of the thyroid gland can lead to hypothyroidism.
Symptoms of Thyroid Disorders

The symptoms of thyroid disorders can vary depending on the specific condition. Some common symptoms include:

Fatigue: Feeling tired or sluggish.
Weight Changes: Weight gain or loss.
Mood Changes: Depression, anxiety, or mood swings.
Hair Loss: Hair loss or brittle hair.
Skin Changes: Dry skin, thinning skin, or skin lesions.
Cold Intolerance: Feeling cold even in mild temperatures.
Heat Intolerance: Feeling hot even in mild temperatures.
Changes in Menstruation: Changes in menstrual cycle or fertility.
Diagnosis of Thyroid Disorders

Thyroid disorders can be diagnosed using a variety of tests, including:

Thyroid Function Tests (TFTs): Blood tests that measure thyroid hormone levels.
Thyroid-Stimulating Hormone (TSH) Test: A blood test that measures TSH levels.
Thyroid Ultrasound: An imaging test that uses sound waves to create images of the thyroid gland.
Thyroid Biopsy: A procedure that involves removing a sample of thyroid tissue for examination.
Treatment of Thyroid Disorders

The treatment of thyroid disorders depends on the specific condition and may include:

Medications: Medications such as levothyroxine (T4) and liothyronine (T3) can be used to treat hypothyroidism.
Radioactive Iodine: This treatment can be used to treat hyperthyroidism and thyroid cancer.
Surgery: Surgery may be necessary to remove part or all of the thyroid gland.
Lifestyle Changes: Lifestyle changes such as a healthy diet and regular exercise can help manage thyroid disorders. """:1,
                 "Dengue ":2,
                 "Malaria":3 ,
                 "Hypothyroidism : ":4,
                 "Typhoid":5,
                 "kidney":6,
                 "Heart attack":7,
                 "Depression":8,
                 "Appendicitis":9,
                 "Brain Tumor":10,
                "lung cancer":11,
                 "migraine":12,
                 """hyperthyroidism : What is Hyperthyroidism?

Hyperthyroidism is a medical condition in which the thyroid gland produces too many thyroid hormones, leading to an overactive thyroid gland. This can cause a range of symptoms, including weight loss, anxiety, and rapid heartbeat.

Causes of Hyperthyroidism

There are several causes of hyperthyroidism, including:

Graves' Disease: This is an autoimmune disorder that causes the thyroid gland to produce too many thyroid hormones.
Thyroid Nodules: These are abnormal growths on the thyroid gland that can produce excess thyroid hormones.
Thyroiditis: This is inflammation of the thyroid gland, which can cause the gland to produce too many thyroid hormones.
Thyroid Cancer: In some cases, thyroid cancer can cause the thyroid gland to produce too many thyroid hormones.
Excessive Iodine Intake: Taking too much iodine can cause the thyroid gland to produce too many thyroid hormones.
Thyroid Hormone Overmedication: Taking too much thyroid hormone medication can cause hyperthyroidism.
Symptoms of Hyperthyroidism

The symptoms of hyperthyroidism can vary from person to person, but common symptoms include:

Weight Loss: Unintentional weight loss, even if you eat more than usual.
Rapid Heartbeat: A rapid or irregular heartbeat, which can be a sign of hyperthyroidism.
Anxiety: Feeling anxious or nervous, which can be a symptom of hyperthyroidism.
Fatigue: Feeling tired or weak, even after getting enough rest.
Heat Intolerance: Feeling hot even in mild temperatures.
Changes in Menstruation: Changes in menstrual cycle or fertility.
Hair Loss: Hair loss or brittle hair.
Skin Changes: Dry skin, thinning skin, or skin lesions.
Muscle Weakness: Muscle weakness or tremors.
Changes in Bowel Movements: Changes in bowel movements, such as diarrhea or constipation.
Diagnosis of Hyperthyroidism

Hyperthyroidism can be diagnosed using a range of tests, including:

Thyroid Function Tests (TFTs): Blood tests that measure thyroid hormone levels.
Thyroid-Stimulating Hormone (TSH) Test: A blood test that measures TSH levels.
Thyroid Ultrasound: An imaging test that uses sound waves to create images of the thyroid gland.
Thyroid Biopsy: A procedure that involves removing a sample of thyroid tissue for examination.
Treatment of Hyperthyroidism

The treatment of hyperthyroidism depends on the underlying cause and may include:

Medications: Medications such as methimazole or propylthiouracil can be used to reduce thyroid hormone production.
Radioactive Iodine: This treatment can be used to destroy part or all of the thyroid gland.
Surgery: Surgery may be necessary to remove part or all of the thyroid gland.
Beta Blockers: Beta blockers can be used to reduce symptoms such as rapid heartbeat and anxiety.
Lifestyle Changes: Lifestyle changes such as a healthy diet and regular exercise can help manage hyperthyroidism.
Complications of Hyperthyroidism

If left untreated, hyperthyroidism can lead to a range of complications, including:

Osteoporosis: Weakened bones, which can increase the risk of fractures.
Heart Problems: Heart problems, such as atrial fibrillation or heart failure.
Thyroid Storm: A life-threatening condition that requires immediate medical attention.
Pregnancy Complications: Hyperthyroidism can increase the risk of pregnancy complications, such as miscarriage or premature birth.
Prevention of Hyperthyroidism

While it's not possible to prevent hyperthyroidism, there are some steps you can take to reduce your risk:

Get Enough Iodine: Iodine is essential for thyroid hormone production, so make sure you get enough iodine in your diet.
Avoid Excessive Iodine Intake: Taking too much iodine can cause hyperthyroidism, so avoid excessive iodine intake.
Get Regular Check-Ups: Regular check-ups with your doctor can help detect hyperthyroidism early, when it's easier to treat.
Maintain a Healthy Lifestyle: Maintaining a healthy lifestyle, including a healthy diet and regular exercise, can help reduce your risk of hyperthyroidism.""":13,
                 "throat cancer":14,
                 "kidney failure":15,
                 "chicken pox":16,
                 "tuberculosis":17,
                 "urine infection":18,
                 "blood cancer":19,
                 "piles":20,
                "Viral fever":21,
                 "Pneumonia":22,
                 "Diabetes":23,
                 "Menopause":24,
                 "Sinusitis":25,
                 "Colon Cancer":26,
                 "Low Bp":27,
                 "Anemia":28,
                 "High Bp":29,
                 "Ulcer":30,
                "Vitamin D Deficiency":31,
                 "Skin Cancer":32,
                 "Hernia":33,
                 "Uric Acid":34,
                 "Asthama":35,
                 "Acidity":36,
                 "Food Poising":37,
                 "Fatty Liver":38,
                 "Anxiety":39,
                 "Vitamin B12 Deficiency":40,
                "Stomach Ulcer":41,
                 "Gerd":42,
                 "Hypertension":43,
                 "Psoriasis":44,
                 "Liver Problem":45,
                 "Flu":46,
                 "Calcium deficiency":47,
                 "Gastric":48,
                 "Fever":49,
                 "Blood Pressure":50 }

prescription_list = {1:"1.Avoid smoking or drinking alcohol. 2.Say no to macronutrients. Fats, protein and carbohydrates are the big macronutrients.",
    2:"1.Use insect repellent, wear long-sleeved shirts and long pants, and control mosquitoes inside and outside your home. 2.Avoid dark clothes",
    3:"Drape mosquito netting over beds.2.Put screens on windows and doors.",
    4:"People with hypothyroidism should avoid consuming large amounts of goitrogenic foods and limit ultra-processed foods in order to promote overall 2.Iodine-rich foods,High-fiber foods should be avoided",
    5:"1.Avoid raw fruits, vegetables, oats, barley, seeds, whole grains, nuts, and legumes.2.Cooked vegetables: potatoes, carrots, green beans, beets, squash should be eaten",
    6:"1.Make healthy food choices.2.Stop Smoking",
    7:"1.Eat healthy,balanced diet. 2.Do not Smoke",
    8:"1.cut back on Social Media time. 2.Reduce stress",
    9:"1.Avoid fatty foods and fatty meats. 2.Support your abdomen when you cough",
    10:"1.Avoiding enviromental hazards such as smoking and excessive radiation exposure",
    11:"1.Avoid carcinogens at work. 2. Exercise most days of the week",
    12:"1.Turn off lights,Lights & sound make migraine pain worse. 2. Try temerature therapy",
    13:"1.Limiting your intake. 2.Make sure you get enough calcium",
    14:"1.Protect yourself from HPV. 2.Choose healthy diet",
    15:"1.Manage alcohol intake. 2.Becareful with painkillers",
    16:"1.Keep fingernails trimmed short. 2.Avoid hard crunchy food",
    17:"1.Avoid tobacco consumption. 2.Reduce exposure by eliminating",
    18:"1.Stay well hydrated. 2.Take showers instead of baths.",
    19:"1.Dont use tobacco. 2. Get vaccinated",
    20:"1.Drinking a lot of fluid. 2.Warm bath to soothe itching and pain",
    21:"Prevent mosquito bites. 2. Cover your nose and mouth",
    22:"1.Keep your immune system strong. 2. Wash your hands with soap and water.",
    23:"1.Keep your weight under control. 2.Eating healthy diet.",
    24:"1.Maintain a moderate weight. 2.Eat lots of fruits and vegetables.",
    25:"1.Clean your hands. 2. Receive recommended vaccines.",
    26:"1.Get regular exercise. 2.Take control of your weight.",
    27:"1.Eat small,low-carb meals. 2. Exercise regularly.",
    28:"1.Eating iron-rich foods. 2.treatment of anemic cases.",
    29:"1.Get enough sleep. 2. Be physically active.",
    30:"1.Maintain healthy lifestyle. 2.Quit smoking.",
    31:"1.Ensure you are getting enough Vitamin D in your diet. 2.Be careful about being in the sun for too long without sunscreem",
    32:"1.Stay in the shade. 2.Wear sunglasses that wrap around and block both UVA and UVB.",
    33:"1.Increase core strength. 2.Control diabetes.",
    34:"1.Drink more water. 2.Avoid alcohol.",
    35:"1.Follow your asthama action plan. 2. Monitor your breathing.",
    36:"1.Eat a light dinner. 2.Don't lie down for at least 2-3 hours after eating.",
    37:"1.Cook food to safe internal temperature to kill harmful bacteria. 2. Wash your hands before food preparing and eating.",
    38:"1.Avoid alcohol. 2. Increase your physical activity.",
    39:"1.Keep an anxiety journal. 2. Take timeout for yourself every day.",
    40:"1.Don't eat any animal products,including eggs. 2.Consume foods and drinks that have vitamin B12.",
    41:"1.Wash your hands frequently to avoid infections. 2.Not mixing alcohol with medication.",
    42:"1.Maintain a healthy weight. 2.Don't lie down after a meal.",
    43:"1.Be physically active. 2. Get enough sleep.",
    44:"1.Avoid Dry,Cold weather. 2.Use a humidifier.",
    45:"1.Drink alcohol in moderation.",
    46:"1.Get the flu vaccine. 2.Stay home if you have the flu.",
    47:"1.Include calcium in your diet every day. 2.Take calcium pills.",
    48:"1.Drink water and tea. 2. Take medicines.",
    49:"1.Drink plenty of fluids to stay hydrated. 2. Dress in lightweight clothing.",
    50:"1.Be physically active. 2. Do not smoke."}


# Function to return Disease name base on disease number
def get_key(val):
    for key, value in Disease_names.items():
        if val == value:
            return key
    return "Matches not found with system built disease, sorry try again"


# function to chat using ai
# Function to chat using ai
def chat(query):
    global chatStr
    genai.api_key = os.getenv("API_KEY")
    chatStr = f"Patient: {query}\n Heart : "

    # Use Gemini model to generate response
    response = genai.generate_text(chatStr, max_tokens=256)

    print(response)
    say(response)
    chatStr += f"{response}\n"
    return response

    with open(f"ai_responses/{query[0:30]}.txt", "w") as f:
        f.write(response)

    
    try:
        print(response["choices"][0]["text"])
        say(response["choices"][0]["text"])
        chatStr += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]

        with open(f"ai_responses/{query[0:30]}.txt", "w") as f:
            f.write(text)
    except Exception as e:
        print(e)


# Function for doctors voice
def say(text):
    speaker.Speak(text)


# function to search query using ai
def ai(prompt):
    genai.api_key = os.getenv("API_KEY")
    text = " "

    # Use Gemini model to generate response
    response = genai.generate_text(prompt, max_tokens=256)

    print(response)
    say(response)
    if not os.path.exists("ai_responses"):
        os.mkdir("ai_responses")

    with open(f"ai_responses/{prompt[0:30]}.txt", "w") as f:
        f.write(response)
    try:
        # print(response.choices[0].text)
        text += response.choices[0].text
        print(text)
        say(text)
        if not os.path.exists("ai_responses"):
            os.mkdir("ai_responses")

        with open(f"ai_responses/{prompt[0:30]}.txt", "w") as f:
            f.write(text)
    except Exception as e:
        print(e)


# function to take user voice as input and save as string
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print("User:  ", query)
            return query
        except Exception as e:
            return "sorry unable to hear your voice please be clear and loud"


# Function to check symptoms of user
def checkSymtoms():
    global symtoms_list
    global query

    symtoms_list = []
    query = " "
    say("Let me check for your symptoms")
    print("Are you male or female")
    say("Are you male or female")
    print("checking your past report...")
    query = takeCommand()
    say("Please tell me your major symptom")
    print("checking your past report...")
    
    for i in range(4):
        query = takeCommand()
        symtoms_list.append(query)
        say("Please tell me your next symptom")
        print("checking your past report...")

    while True:
        say("Do you have any more symptoms?")
        print("checking your past report...")
        query = takeCommand()
        if "yes".lower() in query.lower():
            symtoms_list.append(query)
            say("Please tell me your next symptom")
            print("checking your past report...")
        else:
            break
    say("your symptoms are ")
    i = 0
    while i < len(symtoms_list):
        say(symtoms_list[i])
        i = i + 1

    compareSymptom()


# Function to compare user symptomps with all the diseases
def compareSymptom():
    global total_symptoms_matched
    global actual_disease_list
    global disease_priority_list

    # Viral fever :
    global Viral_Fever_Symptoms_21
    viral_fever_matched = 0
    # print("Comparing with viral symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Viral_Fever_Symptoms_21:
            viral_fever_matched = viral_fever_matched + 1
        i = i + 1
    # print(f"total matches with viral are {viral_fever_matched}")
    # if viral_fever_matched > 0:
    actual_disease_list.append(21)
    disease_priority_list.append(viral_fever_matched)
        #say("you have viral fever")

    # Comparing with Thyroid :
    global Thyroid_disease_Symptoms_01
    Thyroid_matched = 0
    # print("Comparing with Thyroid symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Thyroid_disease_Symptoms_01:
            Thyroid_matched = Thyroid_matched + 1
        i = i + 1
    # print(f"total matches with Thyroid are {Thyroid_matched}")
    # if Thyroid_matched != 0:
    actual_disease_list.append(1)
    disease_priority_list.append(Thyroid_matched)
        #say("you have Thyroid")

    # Comparing with Dengue :
    global Dengue_Symptoms_02
    Dengue_matched = 0
    # print("Comparing with Dengue symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Dengue_Symptoms_02:
            Dengue_matched = Dengue_matched + 1
        i = i + 1
    # print(f"total matches with Dengue are {Dengue_matched}")
    # if Dengue_matched != 0:
    actual_disease_list.append(2)
    disease_priority_list.append(Dengue_matched)
        #say("you have Dengue")

    # Comparing with malaria :
    global Malaria_Symptoms_03
    malaria_matched = 0
    # print("Comparing with malaria symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Malaria_Symptoms_03:
            malaria_matched = malaria_matched + 1
        i = i + 1
    # print(f"total matches with malaria are {malaria_matched}")
    # if malaria_matched != 0:
    actual_disease_list.append(3)
    disease_priority_list.append(malaria_matched)
        #say("you have malaria")

    # Comparing with Hypothyroidism :
    global Hypothyroidism_Symptoms_04
    Hypothyroidism_matched = 0
    # print("Comparing with Hypothyroidism symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Hypothyroidism_Symptoms_04:
             Hypothyroidism_matched = Hypothyroidism_matched + 1
        i = i + 1
    # print(f"total matches with Hypothyroidism are {Hypothyroidism_matched}")
    # if Hypothyroidism_matched != 0:
    actual_disease_list.append(4)
    disease_priority_list.append(Hypothyroidism_matched)
        #say("you have Hypothyroidism")

    # Comparing with Typhoid :
    global Typhoid_Symptoms_05
    Typhoid_matched = 0
    # print("Comparing with Typhoid symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Typhoid_Symptoms_05:
            Typhoid_matched = Typhoid_matched + 1
        i = i + 1
    # print(f"total matches with Typhoid are {Typhoid_matched}")
    # if Typhoid_matched != 0:
    actual_disease_list.append(5)
    disease_priority_list.append(Typhoid_matched)
        #say("you have Typhoid")

    # Comparing with kidney_stone :
    global Kidney_Symptoms_06
    kidney_stone_matched = 0
    # print("Comparing with kidney_stone symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Kidney_Symptoms_06:
            kidney_stone_matched = kidney_stone_matched + 1
        i = i + 1
    # print(f"total matches with kidney_stone are {kidney_stone_matched}")
    # if kidney_stone_matched != 0:
    actual_disease_list.append(6)
    disease_priority_list.append(kidney_stone_matched)
        #say("you have kidney_stone")

    # Comparing with Heart_attack :
    global Heart_attack_symptoms_07
    Heart_attack_matched = 0
    # print("Comparing with Heart_attack symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Heart_attack_symptoms_07:
            Heart_attack_matched = Heart_attack_matched + 1
        i = i + 1
    # print(f"total matches with Heart_attack are {Heart_attack_matched}")
    # if Heart_attack_matched != 0:
    actual_disease_list.append(7)
    disease_priority_list.append(Heart_attack_matched)
        #say("you have Heart_attack")

    # Comparing with Depression :
    global Depression_symptoms_08
    Depression_matched = 0
    # print("Comparing with Depression symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Depression_symptoms_08:
            Depression_matched = Depression_matched + 1
        i = i + 1
    # print(f"total matches with Depression are {Depression_matched}")
    # if Depression_matched != 0:
    actual_disease_list.append(8)
    disease_priority_list.append(Depression_matched)
        #say("you have Depression")

    # Comparing with Appendicitis :
    global Appendicitis_symptoms_09
    Appendicitis_matched = 0
    # print("Comparing with Appendicitis symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Appendicitis_symptoms_09:
            Appendicitis_matched = Appendicitis_matched + 1
        i = i + 1
    # print(f"total matches with Appendicitis are {Appendicitis_matched}")
    # if Appendicitis_matched != 0:
    actual_disease_list.append(9)
    disease_priority_list.append(Appendicitis_matched)
        #say("you have Appendicitis")

    # Comparing with Brain_tumor
    global Braintumor_symptoms_10
    Brain_tumor_matched = 0
    # print("Comparing with Brain_tumor symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Braintumor_symptoms_10:
            Brain_tumor_matched = Brain_tumor_matched + 1
        i = i + 1
    # print(f"total matches with Brain_tumor are {Brain_tumor_matched}")
    # if Brain_tumor_matched != 0:
    actual_disease_list.append(10)
    disease_priority_list.append(Brain_tumor_matched)

    # Comparing with lung cancer
    global lung_cancer_symptoms_11
    lung_cancer_matched = 0
    # print("Comparing with lung cancer symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in lung_cancer_symptoms_11:
            lung_cancer_matched = lung_cancer_matched + 1
        i = i + 1
    # print(f"total matches with lung cancer are {lung_cancer_matched}")
    # if lung_cancer_matched != 0:
    actual_disease_list.append(11)
    disease_priority_list.append(lung_cancer_matched)
        #say("you have lung cancer if it matched maximum")

    # Comparing with migraine
    global migraine_symptoms_12
    migraine_matched = 0
    # print("Comparing with migraine symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in migraine_symptoms_12:
            migraine_matched = migraine_matched + 1
        i = i + 1
    # print(f"total matches with migraine are {migraine_matched}")
    # if migraine_matched != 0:
    actual_disease_list.append(12)
    disease_priority_list.append(migraine_matched)
        #say("you have migraine if it matched maximum")

    # Comparing with hyperthyroidism
    hyperthyroidism_matched = 0
    # print("Comparing with hyperthyroidism symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in hyperthyroidism_symptoms_13:
            hyperthyroidism_matched = hyperthyroidism_matched + 1
        i = i + 1
    # print(f"total matches with hyperthyroidism are {hyperthyroidism_matched}")
    # if hyperthyroidism_matched != 0:
    actual_disease_list.append(13)
    disease_priority_list.append(hyperthyroidism_matched)
        #say("you have hyperthyroidism if it matched maximum")

    # Comparing with throat cancer
    throat_cancer_matched = 0
    # print("Comparing with throat cancer symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in throat_cancer_symptoms_14:
            throat_cancer_matched = throat_cancer_matched + 1
        i = i + 1
    # print(f"total matches with throat cancer are {throat_cancer_matched}")
    # if throat_cancer_matched != 0:
    actual_disease_list.append(14)
    disease_priority_list.append(throat_cancer_matched)
        #say("you have throat cancer if it matched maximum")

    # Comparing with kidney failure
    kidney_failure_matched = 0
    # print("Comparing with kidney failure symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in kidney_failure_symptoms_15:
            kidney_failure_matched = kidney_failure_matched + 1
        i = i + 1
    # print(f"total matches with kidney failure are {kidney_failure_matched}")
    # if kidney_failure_matched != 0:
    actual_disease_list.append(15)
    disease_priority_list.append(kidney_failure_matched)
        #say("you have kidney failure if it matched maximum")

    # comparing with tuberculosis
    tuberculosis_matched = 0
    # print("Comparing with tuberculosis symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in tuberculosis_symptoms_17:
            tuberculosis_matched = tuberculosis_matched + 1
        i = i + 1
    # print(f"total matches with tuberculosis are {tuberculosis_matched}")
    # if tuberculosis_matched != 0:
    actual_disease_list.append(17)
    disease_priority_list.append(tuberculosis_matched)
        #say("you have tuberculosis if it matched maximum")

    # comparing with urinary tract infection
    urine_infection_matched = 0
    # print("Comparing with urinary tract infection symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in urine_infection_symptoms_18:
            urine_infection_matched = urine_infection_matched + 1
        i = i + 1
    # print(f"total matches with urinary tract infection are {urine_infection_matched}")
    # if urine_infection_matched != 0:
    actual_disease_list.append(18)
    disease_priority_list.append(urine_infection_matched)
        #say("you have urinary tract infection if it matched maximum")

    # Compering with blood cancer
    blood_cancer_matched = 0
    # print("Comparing with blood cancer symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in blood_cancer_symptoms_19:
            blood_cancer_matched = blood_cancer_matched + 1
        i = i + 1
    # print(f"total matches with blood cancer are {blood_cancer_matched}")
    # if blood_cancer_matched != 0:
    actual_disease_list.append(19)
    disease_priority_list.append(blood_cancer_matched)
        #say("you have blood cancer if it matched maximum")

    # comparing with piles
    global piles_symptoms_20
    piles_matched = 0
    # print("Comparing with piles symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in piles_symptoms_20:
            piles_matched = piles_matched + 1
        i = i + 1
    # print(f"total matches with piles are {piles_matched}")
    # if piles_matched != 0:
    actual_disease_list.append(20)
    disease_priority_list.append(piles_matched)

    # Comparing with vd
    global Vitamin_D_Deficiency_Symptoms_31
    vitamin_D_deficiency_matched = 0
    # print("Comparing with Vitamin D Deficiency Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Vitamin_D_Deficiency_Symptoms_31:
            vitamin_D_deficiency_matched = vitamin_D_deficiency_matched + 1
        i = i + 1
    # print(f"total matches with vitamin D Deficiency are {vitamin_D_deficiency_matched}")
    # if vitamin_D_deficiency_matched != 0:
    actual_disease_list.append(31)
    disease_priority_list.append(vitamin_D_deficiency_matched)

    # Comparing with skin cancer
    global Skin_Cancer_Symtoms_32
    skin_cancer_matched = 0
    # print("Comparing with Skin Cancer Symtoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Skin_Cancer_Symtoms_32:
            skin_cancer_matched = skin_cancer_matched + 1
        i = i + 1
    # print(f"total matches with skin cancer are {skin_cancer_matched}")
    # if skin_cancer_matched != 0:
    actual_disease_list.append(32)
    disease_priority_list.append(skin_cancer_matched)

    # comparing with Hernia
    global Hernia_Symptoms_33
    hernia_matched = 0
    # print("Comparing with Hernia Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Hernia_Symptoms_33:
            hernia_matched = hernia_matched + 1
        i = i + 1
    # print(f"total matches with hernia are {hernia_matched}")
    # if hernia_matched != 0:
    actual_disease_list.append(33)
    disease_priority_list.append(hernia_matched)

    # comparing with Uric Acid
    global Uric_Acide_Symptoms_34
    uric_acid_matched = 0
    # print("Comparing with Uric Acide Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Uric_Acide_Symptoms_34:
            uric_acid_matched = uric_acid_matched + 1
        i = i + 1
    # print(f"total matches with uric acide are {uric_acid_matched}")
    # if uric_acid_matched != 0:
    actual_disease_list.append(34)
    disease_priority_list.append(uric_acid_matched)

    # comparing with asthma
    global Asthama_Symptoms_35
    asthama_matched = 0
    # print("Comparing with Asthama Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Asthama_Symptoms_35:
            asthama_matched = asthama_matched + 1
        i = i + 1
    # print(f"total matches with asthama are {asthama_matched}")
    # if asthama_matched != 0:
    actual_disease_list.append(35)
    disease_priority_list.append(asthama_matched)

    #comparing with Acidity
    global Acidity_Symtomps_36
    acidity_matched = 0
    # print("Comparing with Acidity symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Acidity_Symtomps_36:
            acidity_matched = acidity_matched + 1
        i = i + 1
    # print(f"total matches with acidity are {acidity_matched}")
    # if acidity_matched != 0:
    actual_disease_list.append(36)
    disease_priority_list.append(acidity_matched)

    # comparing with Food poisning
    global Food_Poisoning_Symptoms_37
    food_poisoning_matched = 0
    # print("Comparing with Food Poisoning Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Food_Poisoning_Symptoms_37:
            food_poisoning_matched = food_poisoning_matched + 1
        i = i + 1
    # print(f"total matches with food poisoning are {food_poisoning_matched}")
    # if food_poisoning_matched != 0:
    actual_disease_list.append(37)
    disease_priority_list.append(food_poisoning_matched)

    # comparing with Fatty liver
    global Fatty_Liver_Symptoms_38
    fatty_liver_matched = 0
    # print("Comparing with Fatty Liver Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Fatty_Liver_Symptoms_38:
            fatty_liver_matched = fatty_liver_matched + 1
        i = i + 1
    # print(f"total matches with fatty liver are {fatty_liver_matched}")
    # if fatty_liver_matched != 0:
    actual_disease_list.append(38)
    disease_priority_list.append(fatty_liver_matched)

    # comparing with anxiety
    global Anxiety_Symptoms_39
    anxiety_matched = 0
    # print("Comparing with Anxiety Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Anxiety_Symptoms_39:
            anxiety_matched = anxiety_matched + 1
        i = i + 1
    # print(f"total matches with anxiety are {anxiety_matched}")
    # if anxiety_matched != 0:
    actual_disease_list.append(39)
    disease_priority_list.append(anxiety_matched)

    # comparing with vitamine b
    global Vitamin_B12_Deficiency_Symptoms_40
    vitamin_B12_deficiency_matched = 0
    # print("Comparing with Vitamin B12 Deficiency Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Vitamin_B12_Deficiency_Symptoms_40:
            vitamin_B12_deficiency_matched = vitamin_B12_deficiency_matched + 1
        i = i + 1
    # print(f"total matches with vitamin-B12 deficiency are {vitamin_B12_deficiency_matched}")
    # if vitamin_B12_deficiency_matched != 0:
    actual_disease_list.append(40)
    disease_priority_list.append(vitamin_B12_deficiency_matched)

    # comparing with stomach ulcer
    global Stomach_Ulcer_41
    Stomach_Ulcer_matched = 0
    # print("Comparing with  Stomach Ulcer Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Stomach_Ulcer_41:
            Stomach_Ulcer_matched = Stomach_Ulcer_matched + 1
        i = i + 1
    # print(f"total matches with Stomach Ulcer are{Stomach_Ulcer_matched}")
    # if Stomach_Ulcer_matched != 0:
    actual_disease_list.append(41)
    disease_priority_list.append(Stomach_Ulcer_matched)

    #Comparing with gerd
    global Gerd_42
    Gerd_matched = 0
    # print("Comparing with  Gerd Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Gerd_42:
            Gerd_matched = Gerd_matched + 1
        i = i + 1
    # print(f"total matches with Gerd are{Gerd_matched}")
    # if Gerd_matched != 0:
    actual_disease_list.append(42)
    disease_priority_list.append(Gerd_matched)

    # Cmoparing with hypertension
    global Hypertension_43
    Hypertension_matched = 0
    # print("Comparing with Hypertension  Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Hypertension_43:
            Hypertension_matched = Hypertension_matched + 1
        i = i + 1
    # print(f"total matches with Hypertension are{Hypertension_matched}")
    # if Hypertension_matched != 0:
    actual_disease_list.append(43)
    disease_priority_list.append(Hypertension_matched)

    # comparing with psoriasis
    global Psoriasis_44
    Psoriasis_matched = 0
    # print("Comparing with Psoriasis Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Psoriasis_44:
            Psoriasis_matched = Psoriasis_matched + 1
        i = i + 1
    # print(f"total matches with Psoriasis are{Psoriasis_matched}")
    # if Psoriasis_matched != 0:
    actual_disease_list.append(44)
    disease_priority_list.append(Psoriasis_matched)

    # Comparing with liver
    global Liver_Problem_45
    Liver_Problem_matched = 0
    # print("Comparing with Liver Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Liver_Problem_45:
            Liver_Problem_matched = Liver_Problem_matched + 1
        i = i + 1
    # print(f"total matches with Liver Problem are{Liver_Problem_matched}")
    # if Liver_Problem_matched != 0:
    actual_disease_list.append(45)
    disease_priority_list.append(Liver_Problem_matched)

    # comparing with flue
    global Flu_46
    Flu_matched = 0
    # print("Comparing with Flu Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Flu_46:
            Flu_matched = Flu_matched + 1
        i = i + 1
    # print(f"total matches with flu are{Flu_matched}")
    # if Flu_matched != 0:
    actual_disease_list.append(46)
    disease_priority_list.append(Flu_matched)

    # comparing with calciium dificiency
    global Calcium_Deficiency_47
    Calcium_Deficiency_matched = 0
    # print("Comparing with Calcium_Deficiency  Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Calcium_Deficiency_47:
            Calcium_Deficiency_matched = Calcium_Deficiency_matched + 1
        i = i + 1
    # print(f"total matches with Calcium Deficiency are{Calcium_Deficiency_matched}")
    # if Calcium_Deficiency_matched != 0:
    actual_disease_list.append(47)
    disease_priority_list.append(Calcium_Deficiency_matched)

    # comparing with gastric
    global Gastric_48
    Gastric_matched = 0
    # print("Comparing with Gastric  Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Gastric_48:
            Gastric_matched = Gastric_matched + 1
        i = i + 1
    # print(f"total matches with Gastric are{Gastric_matched}")
    # if Gastric_matched != 0:
    actual_disease_list.append(48)
    disease_priority_list.append(Gastric_matched)

    # comparing with blood presure
    global Blood_Pressure_50
    Blood_Pressure_matched = 0
    # print("Comparing with Blood_Pressure Symptoms...")
    i = 0
    while i < len(symtoms_list):
        if symtoms_list[i] in Blood_Pressure_50:
            Blood_Pressure_matched = Blood_Pressure_matched + 1
        i = i + 1
    # print(f"total matches with Blood_Pressure are{Blood_Pressure_matched}")
    # if Blood_Pressure_matched != 0:
    actual_disease_list.append(50)
    disease_priority_list.append(Blood_Pressure_matched)

    # Find largest priority disease
    global Disease_names
    largest_priority_disease = 0
    for i in disease_priority_list:
        if largest_priority_disease < i:
            largest_priority_disease = i

    dindex = disease_priority_list.index(largest_priority_disease)
    dnum = actual_disease_list[dindex]
    # print(disease_priority_list)
    # print(actual_disease_list)
    # print(dnum)
    confirmed_disease = get_key(dnum)
    say(f"Based on the observations i made you may have {confirmed_disease}")
    print(f"You may have {confirmed_disease}")
    say("please consult your nearest doctor for more help")

    say(f"would you like for some suggestion to over come {confirmed_disease}")
    print("waiting for answer")
    query = takeCommand()
    if "yes" in query.lower():
        give_prescription(dnum-1)
    else:
        say("owhkay is their anything i can help you with")
        query = takeCommand()
        if "no" in query.lower():
            say("Nice to meet you")
            say("i hope you never see me again    because i hope to see you fit and fine")
            say("still whenever you need me i am always here ")
            say("take care")
            say("bye")
            exit()
        else:
            say("How can i help you")


# Mental Health Function is yet pending # todo
def mentalHealth():
    say("Sometimes its okay to not to feel okay")
    say("but we should controll our feelings and and stand strong")
    say("Is their any particular reason thats making you feel sad ")
    query = takeCommand()
    if "yes" in query.lower():
        say("What is it")
        query = takeCommand()
        say("I am sorry to here that. share your report")
        say("just remember one thing ")
        say("dark nights are the indicator for happy sunrise ")
        say("so till then have patience and courage")
        say(" be strong ")
    else:
        say("yeah that is totally normal ")
        say(" its a game of mind ")
        say(" instead of giving the controller to the mind take the controller in your own hands ")
        say(" and let your emotions and feeling be controlled")
        say("just remember one thing ")
        say("dark nights are the indicator for happy sunrise ")
        say("so till then have patience and courage")
        say(" be strong ")
    say("I recommend you to improve your daily schedule that will help you a lot ")
    say(" should i suggest you to some healthy schedule tips ")
    query = takeCommand()
    if "yes" in query.lower():
        say(" start your day with positive thought ")
        say(" wakeup early in the morning and meditate at least for a two minutes ")
        say(" Engage yourself in interesting activities or rather follow your hobbies")
        say("hit the gym ")
        say("Love yourself you matter you have to be better version of yourself")
    else:
        say("Okay but remember one thing")
        say("Love yourself you matter you have to be better version of yourself")
    say(" i admire you and i will always be with you ")
    say(" whenever you wanna have a talk i am here")
    say(" stay happy ")

def give_prescription(disease_number):
    global prescription_list
    say(prescription_list[disease_number])

# main
say(" Hello I am Heart ")
say(" How may I help you ")
while True:
    print("Listening...")
    query = takeCommand()
    sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wekipedia.com"], ["google", "https://www.google.com"]]
    for site in sites:
        if f"open {site[0]}".lower() in query.lower():
            say("Opening Site")
            webbrowser.open(site[1])

    if "prescription".lower() in query.lower():
        say("Here is the prescription")
        ai(prompt=query)

    elif "by doctor ".lower() in query.lower():
        say("Bye Bye")
        say("Wish you a good health")
        exit()

    elif "not well".lower() in query.lower():
        say("I am sorry to hear that")
        checkSymtoms()

    elif "ill" in query.lower():
        say("I am sorry to hear that")
        checkSymtoms()

    elif "sad" in query.lower():
        say("I am sorry to hear that")
        mentalHealth()

    elif "thank you" in query.lower():
        say("its my duty and responsibility to make sure you are well and guide for your better help")
        say("do you need any more help from me")
        print("listening...")
        query = takeCommand()
        if "no" in query.lower():
            say("Nice to meet you")
            say("i hope you never see me again    because i hope to see you fit and fine")
            say("still whenever you need me i am always here ")
            say("take care")
            say("bye")
            exit()

    elif "bye" in query.lower():
        say("i hope you never see me again    because i hope to see you fit and fine")
        say("still whenever you need me i am always here ")
        say("take care")
        say("bye")
        exit()

    else:
        
        chat(query)
        say('thank you and get well soon :) ')
        print('exiting')
        exit()