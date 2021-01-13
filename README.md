# **Capstone 1 Project Proposal**

## Goals

The goal is to allow the users who want to discover recipes to do  
so conveniently from the website all the way to the grocery store.  

## Demographic  
Anyone that wants to discover new recipes to cook.

## API
`food-api`  `twilio`  
The food-api will be used to display recipes along with their ingredients 
which also allows recipes to be filtered by different types of diets such
as vegetarian, vegan, pescetarian also the types of cuisine which comes from
various countries. The twilio API will be used to gather the user’s phone if
they want to text the ingredients of the recipes to their phone to conveniently
shop at the grocery store. In terms of user data: a username, password, 
favorite recipes, phone number, shopping list.

## Details  
### Potential API issues
The food-api has over 330,000 recipes but the application will only contain 
a few thousand, the potential issue is randomizing the data properly so that 
we can have sufficient data for each cuisine and diet type. Another potential 
issue is extracting the exact ingredients from the recipe according to how many 
people to serve for the shopping list. For the twilio API verifying a phone number 
after registering.

### Sensitive Information
password and phone number.

### Functionality

- #### Registration
  Users register with their username, password, phone number, and “email” for 
password reset.  

- #### Password Encryption
  Every user’s password will be encrypted by salting and then hashing the 
password storing it in the database through using `Flask-Bcrypt`.

- #### Password Reset
  If a user enters incorrect credentials for logging in a password reset 
will be displayed. The user enters their email address and a password 
reset link will be sent to their email.