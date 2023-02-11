# FIA Technical Branch Test [Web]
#### Platform: TryHackMe (Private Room)
#### Category: Web
#### Rate: Medium
#### Time: 7AM 05/02/2022 - 9PM 07/02/20223
---
## Table of Contents
- [Overview](https://github.com/kahang3000/CTF-WriteUp/tree/main/FIA%20Technical%20Branch%20Test%20(Web)#overview)  
- [Task 15 - [Web] Be_Admin](https://github.com/kahang3000/CTF-WriteUp/tree/main/FIA%20Technical%20Branch%20Test%20(Web)#task-15---web-be_admin)  
- [Task 16 - [Web] Lets_Roll_Back](https://github.com/kahang3000/CTF-WriteUp/tree/main/FIA%20Technical%20Branch%20Test%20(Web)#task-16---web-lets_roll_back)  
- [Task 17 - [Web] U_Got_Me](https://github.com/kahang3000/CTF-WriteUp/tree/main/FIA%20Technical%20Branch%20Test%20(Web)#task-17---web-u_got_me)  
- [Conclusion](https://github.com/kahang3000/CTF-WriteUp/tree/main/FIA%20Technical%20Branch%20Test%20(Web)#conclusion)    
- [Other Category](https://github.com/kahang3000/CTF-WriteUp/tree/main/FIA%20Technical%20Branch%20Test%20(Web)#other-category)    

---
## Overview
<p align="center">
    <img src="https://user-images.githubusercontent.com/38382423/218241707-f3863a8d-bf1f-4c43-829b-11c2025f207d.png" alt="Logo">
</p>

This write-up will cover the **Web** category of a mini CTF created that test the skills of club members before we can join the Technical Branch.
LET'S GOOOO!!!


---
## Task 15 - [Web] Be_Admin
### Challenge Description
The task name is called "Be Admin", which hints that there might be a broken authentication vulnerability and we need to get access through it.
<div style="text-align: center;">
  <img src="https://user-images.githubusercontent.com/38382423/218241855-3036d6cb-47a0-4ece-90d0-d516845ac58a.png" alt="1">
</p>

### Web Source Code
First thing we see when accessing the IP is the source code of the website, so this is a form of white-box testing.
<p align="center">
  <img src="https://user-images.githubusercontent.com/38382423/218241900-b002d500-8ac0-431d-8804-697797558cc7.png" alt="2">
</p>

This code checks for the password passed as GET parameter in the URL and returns the flag from "$k4it0z11" if the password is "Or3Ap0_5AikoU!!" and the length is **not equal** to **15**. This is impossible when that string actually equal to 15.
`?password=Or3Ap0_5AikoU!!`
<p align="center">
  <img src="https://user-images.githubusercontent.com/38382423/218241902-7985388f-00c1-4d92-b1d0-532812dcee8d.png" alt="3">
</p>

### Research PHP Vulnerability
PHP is a "cancer" programming language :skull: that still has a lot dumb bugs that existed. First, I started by analyzing this line of code:
```php
if(!strcmp($_GET['password'],"Or3Ap0_5AikoU!!")&&strlen($_GET['password'])!=15)
```
Then I research Google for "*php strcmp()*" and looking at [PHP documentation](https://www.php.net/manual/en/function.strcmp.php) then realized this function has only 3 possible return values: 
- -1 if string1 is less than string2.
- 1 if string1 is greater than string2.
- 0 if they are equal.

So we need to manipulate the return value of `strcmp` equal to `0` or `NULL`. When `!strcmp()` is evaluated, it will return `1` which is `TRUE` and allowing us to bypass the authentication step.
### Bypass authentication
According to the [PHP documentation](https://www.php.net/manual/en/function.strcmp.php), there is a note that say if we compare a *string* with an *array* it will return **NULL** and **Warning**. So I tried to pass the password parameter in the URL as an array: `?password[]=test`
<p align="center">
  <img src="https://user-images.githubusercontent.com/38382423/218241916-9ba28090-97a4-46ef-9720-89016c9d520c.png" alt="4">
</p>

...:boom: BOOoOoMOM!!! And then we got the flag. :)

---
## Task 16 - [Web] Lets_Roll_Back
### Challenge Description
In this challenge, we know that the website is still maintaining and the interesting thing that is the developer forgot to remove the debugging feature somewhere on the website.
<p align="center">
  <img src="https://user-images.githubusercontent.com/38382423/218241917-ca8d6715-c7e3-466a-b083-d45ff401f9ca.png" alt="5">
</p>

### Enumerate The Web
First, I accessed the home page then navigated to the "about" page, where I saw a message that hinted maybe there is a file disclosure vulnerability, also known as LFI (Local File Inclusion).
<p align="center">
  <img src="https://user-images.githubusercontent.com/38382423/218241906-be506b90-e791-4da8-b698-88785bef8d74.png" alt="6">
</p>

Then i viewed the source of the page and found the hidden link which was in the comment `<!-- <a href="index.php?debug=1">debug</a> -->` same as with the "about" page and that lead me to another source code page.
<p align="center">
  <img src="https://user-images.githubusercontent.com/38382423/218241918-739b049f-bcf4-4631-ac94-6830a00c34ed.png" alt="7">
</p>

### Path Traversal Vulnerability
Access to the debug page we can see it is vulnerable to path traversal because it directly includes a file based on user input from the `$_GET['give_me']` parameter.
```php
<?php
    include('contents/'.$page);
?>
```
<p align="center">
  <img src="https://user-images.githubusercontent.com/38382423/218241925-2c05897a-1760-4c4c-8451-55fc5d796ba8.png" alt="8">
</p>

Imagine that if we inject a malicious value for `give_me` parameter such as ` ../../../../etc/passwd` the code would include a file at the path `contents/../../../../etc/passwd` and reveal us the sensitive `/etc/passwd` file 

### Bypass Restriction
However, life is not always that easy, the page checks the value regex "Regular Expression" if the parameter `give_me` has been passed, and  filter/replace the string value if it matches `../`, `etc`, or `passwd` with an empty string.
<p align="center">
  <img src="https://user-images.githubusercontent.com/38382423/218241928-b6eb4393-01a5-48f7-9322-1d7689f33afa.png" alt="9">
</p>

So, I've been thinking, what if I double the value or give it a "mask"? That's right! If we double the string, the `preg_replace()` function will replace it and leave us with the remaining characters, which we can then combine back into a valid value. For example the string "**e**~~etc~~**t**~~etc~~**c**" will be come "**etc**".
Let's put a mask on it with the string `....//....//....//....//....//eetctetcc/ppasswdapasswdspasswdspasswdwpasswdd`
<p align="center">
  <img src="https://user-images.githubusercontent.com/38382423/218241929-fff3f47d-6c2a-4165-aa7c-4ddd601f1bfa.png" alt="10">
</p>

...:boom: BOOoOoM!!! What an EXPERT in defending :penguin:. 

---
## Task 17 - [Web] U_Got_Me
### Challenge Description
This time the challenge's description didn't give me any good information so I have moved straight forward to the web page.
<p align="center">
  <img src="https://user-images.githubusercontent.com/38382423/218241932-349fdff1-2fc2-4a16-b30a-a3d1f18fdfb2.png" alt="11">
</p>

### IDOR 
When I accessed the web, it displayed only one character on the screen, nothing more. However, I noticed that the URL contained a directory `/id/0`.
<p align="center">
  <img src="https://user-images.githubusercontent.com/38382423/218241933-ab926671-c47c-4b96-a751-b7476b426dd9.png" alt="12">
</p>

I found out that I could increase the number from `0` to `n` so that leading to an IDOR vulnerability. 
> IDOR stands for Insecure Direct Object Reference, a vulnerability in which an attacker can manipulate a parameter in a URL to gain access to sensitive information or unauthorized actions.

<p align="center">
  <img src="https://user-images.githubusercontent.com/38382423/218241934-a9910dc7-d53a-40fd-a447-d9abff864ed8.png" alt="13">
</p>

But it seems like each page only contains one letter. I had the idea of trying to increase the number in the `/id/NUMBER` and combine the letters I obtained. After the first `10` numbers, put it all together and the words is '**Hello World**'. So if we keep increasing and combining the letters so we can get a meaning word or even flag. The problem here is that we don't know the limit of the `id` number and when it will stop. I have even tried `999`, but there are still more letters.
<p align="center">
  <img src="https://user-images.githubusercontent.com/38382423/218241935-35c38574-4027-42a5-a2de-74284e819af0.png" alt="14">
</p>

### Retrieve Letters Script
Imagine manually visiting each page by hand and don't even know its limit, you would waste your life time. I decided to make a small script that would automatically access the website within a certain range of `id` number and get those letters, then put them together:
```python
import requests

for i in range(0, 1000):
    url = f"http://10.10.217.246/id/{i}"
    response = requests.get(url)
    if response.status_code == 200:
        print(response.content.decode("utf-8"))
```
The script is working, but it's taking a long time to make each request. So I decided to optimize the code with the help of ChatGPT. Using the keywords "*send simultaneous requests*", "*asyncio*", and "*aiohttp*".
```python
# Generated By ChatGPT
import asyncio
import aiohttp

async def send_request(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.text()
            return content

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(0, 1000):
            url = f"http://10.10.217.246/id/{i}"
            task = asyncio.ensure_future(send_request(session, url))
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)

        with open("flag.txt", "w") as f:
            for content in responses:
                if content:
                    f.write(content + "")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```
Thank you, ChatGPT :heart:. The script has successfully retrieved all 1000 letters in just a second. We can observe that the flag is present among the text.
<p align="center">
  <img src="https://user-images.githubusercontent.com/38382423/218241937-904a1541-7ec3-4f4a-9321-23b0dfa1b6b6.png" alt="15">
</p>

---
## Conclusion
This mini CTF was a great experience. It was fun with interesting stories for each task and provided me with an opportunity to review my knowledge and I have learned a lot of new skill from many new challenge in this CTF. It was a good game, and the players were highly skilled and talented. Many thanks to leadership of FIA club for creating this contest for new members to experience amazing CTF challenges :heart:.

---
## Other Category
- [OSINT & Miscellaneous](https://github.com/P5ySm1th/CTF/blob/main/FIA/Technical%20Test/MISC%2BOSINT/README.md) 
- [Reverse Engineer]()
- [Cryptography]() 
- [Digital Forensic]()   