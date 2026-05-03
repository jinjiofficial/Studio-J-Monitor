🖥️ Studio J PC Monitor
실시간 PC 상태 모니터링 및 원격 제어 시스템

Real-time PC Status Monitoring & Remote Control System

🇰🇷 한국어 (Korean)
📌 프로젝트 소개
Studio J PC Monitor는 파이썬(Python)과 파이어베이스(Firebase)를 활용하여 원격에서 내 컴퓨터의 상태를 확인하고 제어할 수 있는 대시보드 시스템입니다. 중학교 1학년 개발자가 직접 기획하고 구현하였습니다.

✨ 주요 기능
실시간 상태 확인: 컴퓨터가 켜져 있는지(Online/Offline) 실시간으로 확인 가능합니다.

사용 시간 측정: 오늘 총 사용 시간을 측정하며, 앱을 껐다 켜도 데이터가 유지됩니다. (매일 00:00 자동 초기화)

원격 제어: 웹 대시보드에서 원격으로 절전 모드 실행 및 시스템 종료가 가능합니다.

데이터 시각화: 주간 사용량을 막대그래프로 한눈에 파악할 수 있습니다.

보안: 시스템 종료와 같은 주요 명령은 설정된 비밀번호를 입력해야 실행됩니다.

🚀 기술 스택
언어: Python 3.12, HTML5, JavaScript

데이터베이스: Firebase Realtime Database

라이브러리: psutil, requests, python-dotenv (Python) / Chart.js (Web)

🇺🇸 English
📌 About the Project
Studio J PC Monitor is a dashboard system that allows you to monitor and control your computer's status remotely using Python and Firebase. It was planned and developed by a 7th-grade (Middle School 1st year) student developer.

✨ Key Features
Real-time Status: Check if the PC is Online or Offline in real-time.

Usage Tracking: Tracks total daily usage time. Data persists even after restarting the app. (Resets at 00:00 daily)

Remote Control: Execute Sleep Mode or System Shutdown remotely from the web dashboard.

Data Visualization: View weekly usage statistics through an intuitive bar chart.

Security: Critical commands like Shutdown require a pre-configured password.

🚀 Tech Stack
Languages: Python 3.12, HTML5, JavaScript

Database: Firebase Realtime Database

Libraries: psutil, requests, python-dotenv (Python) / Chart.js (Web)

🛠️ Installation & Setup
Clone the repository

Install dependencies: pip install psutil requests python-dotenv

Configure .env file:

코드 스니펫
DB_URL=your_firebase_url/usage.json
MY_PASSWORD=your_secure_password
Run the agent: python Pcchecker.py

Open index.html on your web browser or deploy via GitHub Pages.

Developed by Studio J (Jinji)

Contact: GitHub @jinjiofficial
