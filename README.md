# MiRA
A multi-agent model for homelessness assessments. 

## Purpose
In Canada, the primary tool for governments to assess homelessness is the Homeless Individuals and Families Information System (HIFIS). HIFIS is a database aiming to pinpoint the root cause(s) of homelessness in Canada. It does this by using individual homelessness assessments; commonly known as V-SPDAT assessments. V-SPDAT assessments are built for two reasons: to assess the degree of homelessness an individual is experiencing, and to feed more data into HIFIS. Currently, HIFIS is facing both inaccurate and outdated data, which is preventing policy makers from making more informed choices to tackle homelessness. This is because the V-SPDAT assessment is outdated. The demographic of the homeless population has changed significantly since the initial data collection period of 2005-2014, which primarily included white males (Liyanage et al., 2023). The current homeless population includes more women, refugees, and children; however, the assessment methodologies have not adapted to these changes (Liyanage et al., 2023). Language barriers, sociological biases, and lack of trust make it difficult for these groups to respond to the V-SPDAT questions effectively. In fact, only  about 50% of those assessed respond to the questions, with the rest either not understanding due to language barriers or feeling threatened by the style of questioning (Canada, 2024).
There is a need for a new assessment tool that is able to confront language barriers and biases, thus building trust amongst users. 

## Main Features
Multilingual in Resource Assessment (MiRA) is a tool that can solve the problems with the current V-SPDAT assessment. While MiRA is an automated tool, meaning that it can handle multiple assessments simultaneously, MiRA’s main strength is that it is a multi-agent system. A multi-agent system is where several functions or intelligent systems–grouped into agents–come together in one program. This makes MiRA easy to update and add more functionalities to. The agents in MiRA are the audio to text agent, the translation agent, the generative agent (made with support from Google ADK), and the empathy agent. The audio to text agent enables verbal communication with MiRA, meaning individuals who are illiterate can finish their assessment successfully. Additionally, if an individual begins speaking in another language out of confusion, MiRA can detect what this language is, repeat the current question in this language, and conduct the rest of the assessment in this language. To make the assessment more personable, MiRA leverages both a generative agent and an empathy agent. The generative agent focuses on generating a response to the user using Gemini 2.0, while the empathy agent is focused on making this response seem more empathetic given the user’s situation. This will encourage users to trust MiRA, and share more information that will be useful to both themselves and HIFIS.

## Building Information
- Language – Python
- MiRA Main Libraries – pygame, sounddevice, numpy, threading, time, collections, sys, os, pyttsx3, traceback, math, pyaudio, wave
- Audio-to-Text Agent Libraries: speech_recognition
- Translation Agent Libraries – googletrans, typing, langdetect
- Generative Agent Libraries  – google.adk.agents, os
- Empathy Libraries – google.adk.agents, os

## References
Canada, I. (2024, March 19). Infrastructure Canada - HIFIS version 4.0.60.2 Release Notes. https://www.infrastructure.gc.ca/homelessness-sans-abri/hifis-sisa/notes-4-0-60-2-eng.html
Liyanage, C. R., Mago, V., Schiff, R., Ranta, K., Park, A., Lovato-Day, K., Agnor, E., & Gokani, R. (2023). Understanding Why Many People Experiencing Homelessness Reported Migrating to a Small Canadian City: Machine Learning Approach With Augmented Data. JMIR Formative Research, 7, e43511. https://doi.org/10.2196/43511



