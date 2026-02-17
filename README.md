# Reasoning-lab
## A application that allows local models to talk to each other
### this allows weaker gpus to achieve bigger results by distributing the weight of each task
A big project of mine, made for the community, uses ollama locally and makes agents talk to each other, then a larger model judges/corrects them, then another model synthesizes it, creating a curated answer, with variable number of models, updating with ollama/alpaca automatically (select port, see readme below)


a idea i put into practice: "huh, i dont have a powerful gpu, what if i layered smaller models?" then i made 3 models generate answers to the same prompt, but it still didn't generate answers, just 3 different texts.
then i added a judge, which contracted the reasoning models' opinions into one, curated "form".
it was a working idea, but it was still missing the actual chatbot vibe, so i added a final bot, in my tests i principally used mistral 7b, which is relativelly small, but worked great with qwen2.5 3b.
it gets the judges "form" and "translates" it to a actuall chatbot response, and this was the base program.
but right after the gui started as a plan
<img width="272" height="161" alt="image" src="https://github.com/user-attachments/assets/f3e6be62-4f83-45eb-b0c1-de8fce7f5230" />
then a selector
<img width="1095" height="694" alt="image" src="https://github.com/user-attachments/assets/1694e5c4-7f69-4098-896a-9e165f0f6164" />
<img width="1095" height="694" alt="image" src="https://github.com/user-attachments/assets/aa0ab6ef-fbfd-4f8a-9dfc-7ad525aa1c23" />
then themes
<img width="472" height="352" alt="image" src="https://github.com/user-attachments/assets/e8bb2027-39ae-4836-b9a2-36bc78eeca3a" />
and finally, the chat!
<img width="1095" height="694" alt="image" src="https://github.com/user-attachments/assets/95279efb-decc-4d88-9fb7-e37e2aebad5a" />
<img width="1095" height="694" alt="image" src="https://github.com/user-attachments/assets/20803849-eb22-43c5-ba51-9000765ec567" />
<img width="1095" height="694" alt="image" src="https://github.com/user-attachments/assets/2ff999ca-79f1-4ce8-b94e-5c5141ae4f30" />
<img width="1095" height="694" alt="image" src="https://github.com/user-attachments/assets/eb72036f-1182-44cb-99a3-29881bcc990b" />
i'm very proud of this, and i think it turned out really well, but there's always room for improvement, i gladly accept requests or bug fixes for it.

## License

This project is licensed under the **PolyForm Noncommercial 1.0.0 License**.

- You may fork, modify, and contribute to this project.
- You may **not use this project for commercial purposes**.
- See the [LICENSE](LICENSE) file for full details.
