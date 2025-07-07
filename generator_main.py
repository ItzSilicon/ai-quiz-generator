import generator

try:
    with open("apikey.txt", "r") as f:
        api_key = f.read()
        if api_key=="":
            api_key = input("Please enter your API key:\n You can also paste it into 'api_key.txt' in the same directory as this script.\n If you don't have an API key, please visit https://ai.google.dev/api for further infomation.\n")
            with open("apikey.txt", "w") as f_write:
                f_write.write(api_key)
except FileNotFoundError:
    raise FileNotFoundError("API key file not found. Please create 'apikey.txt' with your API key.")


    
try:
    while 1:
        quiz_name, resource, input_content ,prompt = generator.get_info()
        print(f"Quiz Name: {quiz_name}\nResource: {resource}\nInput Content: {input_content}\nPrompt: {prompt}")
        print("Are you sure you want to generate questions with these details? (yes/no)")
        if input().strip().lower() != 'yes':
            print("Exiting without generating questions.")
            continue
        else:
            generator.generate_questions(api_key, quiz_name, resource, input_content, prompt)
            print("Do you want to generate another quiz? (yes/no)")
            if input().strip().lower() != 'no':
                continue
            else:
                break
except Exception as e:
    print(f"An error occurred: {e}")