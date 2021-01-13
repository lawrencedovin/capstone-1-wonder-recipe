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

### Database Schema  

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

- #### Login
  Every user that is logged in can log out of their account.

- #### Logout
  If a user enters incorrect credentials for logging in a password reset 
will be displayed. The user enters their email address and a password 
reset link will be sent to their email.

- #### Filtering
  Users can filter by diet, cuisine, likes or querying their search using a searchbar.

- #### Favorite
  Users can favorite a recipe which will store that recipe to the favorites list.

- #### Shoplist
  Users can store the recipes in a shoplist which allows the user to be sent the
recipe along with their ingredients to their phone.

- #### Likes
  Users can like or not like a particular recipe. The total likes will be displayed
next to a recipe item.

### User Flow

### Additional Features  
  The shopping list feature will temporarily store in recipes the user wants to use 
which the user can send to their phone to conveniently shop for the ingredients. 
There will be filtering options for different diet types and cuisines.

### Possible Future Features  
- Randomize Recipes feature will allow a user to swipe left or right for discovering and favoriting recipes.  
- User may further search of the Randomize Recipe by diet and or cuisine. 
- Different language support. 
- Users can add comments on the recipes.  
- Dark and light mode.  
- Social media share.

