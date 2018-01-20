# Installation

```
pip install -r requirements.txt
```

# Mailer configuration

Sample .env file:
```
EMAIL_USE_TLS = True
EMAIL_PORT = 587

EMAIL_HOST = smtp.gmail.com
EMAIL_HOST_USER = sample_email@gmail.com
EMAIL_HOST_PASSWORD = password

EMAIL_FROM = sample_email@gmail.com 
EMAIL_TO = example@extraordinarymedia.com
```

I included `EMAIL_FROM` because some smtp servers require it

# Notes

* Phone number validation was based on the rule agreed upon in the document (parentheses, +, space, - and 10 numbers) but with an added tolerance for numbers

* I normally use bower (or yarn) for front-end dependencies, but it seemed overkill for this mini-project

* I spent a lot of time looking for a way to generate front-end validators from the Model (or Form) validators to keep it DRY, but there doesn't seem to be one.