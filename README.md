# Cold Calling Agent 

#### (this was done before the latest update of OpenAI API with Assistant API)

## Overview

The Cold Calling Agent is a Flask-based application designed to streamline and enhance the process of making cold calls. Utilizing the power of OpenAI's advanced language models and Twilio's robust communication API, this application aims to automate and personalize cold calling tasks. It's tailored for businesses seeking to improve their outreach efficiency and quality. Deployed on Heroku, it ensures ease of access and reliability.

## Features

- **Automated Calling**: Leverage Twilio's API for seamless call handling.
- **AI-Driven Interactions**: Utilize OpenAI's API for intelligent and dynamic conversation flow.
- **Heroku Deployment**: Easy and reliable hosting on Heroku platform.
- **Customizable Scripts**: Tailor conversation scripts based on business needs.
- **Real-time Analytics**: Track call performance and outcomes for continuous improvement.
- **User-Friendly Interface**: Simple and intuitive design for effortless navigation and usage.

## Prerequisites

- An account and API key from OpenAI.
- A Twilio account with an authenticated phone number.
- Heroku account for deployment.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Binbasri-in/cold-calling-agent.git
   cd cold-calling-agent
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**

   Set the following environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key.
   - `TWILIO_ACCOUNT_SID`: Your Twilio Account SID.
   - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token.
   - `TWILIO_PHONE_NUMBER`: Your Twilio phone number.

5. **Local Deployment:**

   ```bash
   flask run
   ```

## Deployment to Heroku

1. Create a new app on Heroku.
2. Set the same environment variables in the Heroku app settings.
3. Deploy the application using Heroku Git or connect your GitHub repository for automatic deployments.

## Usage

Describe how to use the application, including how to make calls, customize scripts, and view analytics.

## Contributing

Contributions to the Cold Calling Agent are welcome. Please read our contribution guidelines for more information.

## License

Include license information here.

## Contact

For support or queries, please contact [mohammed.binbasri@gmail.com](mailto:mohammed.binbasri@gmail.com).
