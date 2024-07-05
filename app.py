import openai
from datetime import datetime

# set up OpenAI API credentials
openai.api_key = ""

def generate_personas_func(keyword):

    num_personas = 3

    
    # Use GPT3 to predict the intent of the keyword search
    prompt = f"What is the most likely intent of searching for {keyword}?"
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=60,
    n=1,
    stop=None,
    temperature=0.5
    )
    intent = response.choices[0].text.strip()

    # Generate 3 personas for the keyword/intent
    prompt = (f"You are an expert at marketing and consumer behavior, specifically persona generation. Given the searcher is using the keyword: \n {keyword} with the intent: \n {intent}, please generate 3 different but unique personas with the following format. Each persona should be seperated by ######## : \n\n"
            "1. Demographics\n"
            "- Name:\n"
            "- Age Range:\n"
            "- Gender:\n"
            "- Marital Status:\n"
            "- Income:\n"
            "- Education Level:\n\n"
            "2. Psychographics\n"
            "- Personality Traits:\n"
            "- Values and Beliefs:\n"
            "- Interests and Hobbies:\n"
            "- Lifestyle Factors:\n\n"
            "4. Behavior and Decision-Making\n"
            "- Information Sources:\n"
            "- Influences on Purchase Decisions:\n"
            "- Key Behaviors and Habits:\n\n"
            )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.8
    )
    personas_text = response.choices[0].text.strip()

    try:
        personas = personas_text.split('##########')
        personas = [persona.strip() for persona in personas if persona.strip()]

        json = []

        persona = personas[0]
        tasks = []
        questions_prompt = [
                f"For the following question please answer with a list. What are the most important features or benefits that a given persona is looking for when searching for {keyword}, given a persona of: \n Persona:\n {persona} ?",
                f"For the following question please answer with a list. What are the most common questions or concerns before making a purchase related to {keyword}, given a persona of: \n Persona:\n {persona} ?",
                f"For the following question please answer with a list. What are the biggest challenges that someone faces when searching for the right product or service related to {keyword}, given a persona of: \n Persona: \n {persona} ?",
                f"For the following question please answer with a list. How does the given persona typically research their options related to {keyword}, and where do they go to find information, given a persona of: \n Persona: \n {persona}?",
                f"For the following question please answer with a list. What are the most effective ways to convince the following persona to make a purchase related to {keyword}, given a persona of: \n Persona: \n {persona} ?"]

        questions = [f"What are the most important features or benefits that a given persona is looking for when searching for {keyword}",
                f"What are the most common questions or concerns before making a purchase related to {keyword}",
                f"What are the biggest challenges that someone faces when searching for the right product or service related to {keyword}",
                f"How does the given persona typically research their options related to {keyword}, and where do they go to find information",
                f"What are the most effective ways to convince the following persona to make a purchase related to {keyword}"]
        
        for index in range (len(questions_prompt)):
            prompt = questions_prompt[index]
            task =openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.5
                )
            
            tasks.append({f"question_{index+1}": questions[index],
                        f"answer_{index+1}": task['choices'][0]['text'].strip()})
            
        persona_result = persona.split("Demographics")[0].replace("\n", "")
        
        demographics_result = persona.split("Demographics")[1]
        name = demographics_result.split("Name:")[1].split("Age Range:")[0].replace("-","").strip()
        age_range = demographics_result.split("Name:")[1].split("Age Range:")[1].split("Gender:")[0][0:7].strip()
        gender = demographics_result.split("Name:")[1].split("Age Range:")[1].split("Gender:")[1].split("Marital Status:")[0].replace("-","").strip()
        marital_status = demographics_result.split("Name:")[1].split("Age Range:")[1].split("Gender:")[1].split("Marital Status:")[1].split("Income:")[0].replace("-","").strip()
        income = demographics_result.split("Name:")[1].split("Age Range:")[1].split("Gender:")[1].split("Marital Status:")[1].split("Income:")[1].split("Education Level:")[0][0:18].strip()
        education_level = demographics_result.split("Name:")[1].split("Age Range:")[1].split("Gender:")[1].split("Marital Status:")[1].split("Income:")[1].split("Education Level:")[1].split("Psychographics")[0].strip().replace("2.","")
        
        
        psychograpics_result = persona.split("Demographics")[1].split("Psychographics")[1].split("Behavior and Decision-Making")[0]
        Behavior_result = persona.split("Demographics")[1].split("Psychographics")[1].split("Behavior and Decision-Making")[1]
        
        json.append({
            "persona": {
                "Demographics": {
                    "Name": name,
                    "age_range": age_range,
                    "gender": gender,
                    "marital_status": marital_status,
                    "income": income,
                    "education_level": education_level},
                "Psychographics": psychograpics_result,
                "Behavior_result": Behavior_result,
                "tasks": tasks
            }
        })
            
        return json
    
    except Exception as e:
        
        with open("log_personas.log", "a") as log:
            log.write(f"{e}, Running on: {datetime.now()}")
            
        return "something went wrong, please try again"
