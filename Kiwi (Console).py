import openai
import sys
import time
history = []


def api_key():
    global api_key
    newapi = input("Type your API key (Enter to cancel)")
    if newapi.strip():
        openai.api_key = newapi.strip()
        try:
            _ = openai.models.list()
        except Exception as e:
            print("Error", e)
        else:
            print('Yes, it works!')
    else:
        sys.exit()


answer = input(
    "Enter key to continue\nTo set a key, type Y.\nCTRL+C to exit.\n:")
if answer.strip():
    if answer.upper().strip() == "Y":
        api_key()
    else:
        sys.exit()


def submitmsg():
    global time
    try:
        input_msg = input("Me: ")
        if "%exit" in input_msg:
            raise KeyboardInterrupt
        if not input_msg.strip() == "":
            try:
                global history
                history.append({"role": "user", "content": input_msg.strip()})
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=history,
                    max_tokens=150
                )
                answer = completion.choices[0].message["content"]
                history.append({"role": "assistant", "content": answer})
                multiline_array = answer.split("\n")
                print("ChatGPT: " + multiline_array[0])
                for element in multiline_array:
                    if element != multiline_array[0] and element.strip() != "```":
                        print("         " + element)
            except openai.error.RateLimitError:
                print(
                    "Please wait 10 seconds.\nYou have reached the limit or the server is under heavy load.\n")
                time.sleep(10)
            except Exception as e:
                print("[ERR] " + str(e))
    except KeyboardInterrupt:
        print("Exit.")
        time.sleep(0.5)
        sys.exit()


print('To exit type "%exit"')
while True:
    submitmsg()
