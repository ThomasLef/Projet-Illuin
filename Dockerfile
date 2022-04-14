FROM ubuntu:latest
ENV DEBIAN_FRONTEND="noninteractive" TZ="Europe/London"
RUN apt-get update && apt-get install -y git wget libgconf-2-4 libnss3 libxss1 fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcairo2 libcups2 libdrm2 libgbm1 libgtk-3-0 libpango-1.0-0 libxcomposite1 libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils python3-pip
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN git clone https://github.com/ThomasLef/Projet-Illuin
WORKDIR /Projet-Illuin
RUN git checkout dockerBranch
RUN pip3 install -r requirements.txt
RUN pip install -U click==8
RUN mkdir html_maps
RUN mkdir model
RUN wget 'https://download.wetransfer.com/eugv/ebb6b7ba604c9d86e877aff3f31ab1ac20220406130151/d1d4cde6902d51277e8db53cfb699ffb1abf9f05/longformer_finetuned?token=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDk2Nzk3OTMsImV4cCI6MTY0OTY4MDM5MywidW5pcXVlIjoiZWJiNmI3YmE2MDRjOWQ4NmU4NzdhZmYzZjMxYWIxYWMyMDIyMDQwNjEzMDE1MSIsImZpbGVuYW1lIjoibG9uZ2Zvcm1lcl9maW5ldHVuZWQiLCJ3YXliaWxsX3VybCI6Imh0dHA6Ly9zdG9ybS1pbnRlcm5hbC5zZXJ2aWNlLmV1LXdlc3QtMS53ZXRyYW5zZmVyLm5ldC9hcGkvd2F5YmlsbHM_c2lnbmVkX3dheWJpbGxfaWQ9ZXlKZmNtRnBiSE1pT25zaWJXVnpjMkZuWlNJNklrSkJhSE5MZDJsT0t6QTBha0ZSUVQwaUxDSmxlSEFpT2lJeU1ESXlMVEEwTFRFeFZERXlPak16T2pFekxqQXdNRm9pTENKd2RYSWlPaUozWVhsaWFXeHNYMmxrSW4xOS0tMWViMTYzZjE5N2Y4ZjI0ZjY0YjQ3NWFjYjYwZDJlNzRjNjczM2RmZWRlODA3MjQxN2I5ODZlNDAwNjk4ZGI0NSIsImZpbmdlcnByaW50IjoiZDFkNGNkZTY5MDJkNTEyNzdlOGRiNTNjZmI2OTlmZmIxYWJmOWYwNSIsImNhbGxiYWNrIjoie1wiZm9ybWRhdGFcIjp7XCJhY3Rpb25cIjpcImh0dHA6Ly9mcm9udGVuZC5zZXJ2aWNlLmV1LXdlc3QtMS53ZXRyYW5zZmVyLm5ldC93ZWJob29rcy9iYWNrZW5kXCJ9LFwiZm9ybVwiOntcInRyYW5zZmVyX2lkXCI6XCJlYmI2YjdiYTYwNGM5ZDg2ZTg3N2FmZjNmMzFhYjFhYzIwMjIwNDA2MTMwMTUxXCIsXCJkb3dubG9hZF9pZFwiOjE0OTI0MTkxNjI5fX0ifQ.oLMeBvpszFE0HdeWdy2JF0TFK6vX6oE6RNacpVRvkj4&cf=y'
RUN mv longformer_finetuned?token=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDk2Nzk3OTMsImV4cCI6MTY0OTY4MDM5MywidW5pcXVlIjoiZWJiNmI3YmE2MDRjOWQ4NmU4NzdhZmYzZjMxYWIxYWMyMDIyMDQwNjEzMDE1MSIsImZpbGVuYW1lIjoibG9uZ2Zvcm1lcl9maW5ldHVuZWQiLCJ3YXliaWxsX3VybCI6 model/longformer_finetuned
RUN streamlit run streamlit_demo.py