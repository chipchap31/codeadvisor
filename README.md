# Code Advisor 

Code advisor is the third milestone I have designed and developed at Code Institue. It is a platform where students can showcase thier projects by sharing their Github repositories. The codes will be reviewed by fellow students and each reviews will receive either a like or a dislike.

The goal of this project is to provide new coders a platform where they can gain more confidence developing projects by seeing what they need to work on.

![Mockup](https://github.com/chipchap31/codeadvisor/blob/student-dash/static/images/mockup.jpg?raw=true "Mockup")


## UX DESIGN


Sometimes looking for code feedbacks may seem to be too much to ask. The reason for this is because it just takes too much time and effort to read someone's codes. Code advisor is created to make reviewing projects fun and simple. 

During the research phase I found out that:

- The target audience are students and amateur coders both genders. Therefore the color must suit both genders.
- The target audience's age are between 18 - 30 years old, so the fonts don't have to 16px and over.
- The project has several pages including the register and login page. Therefore, a clear and easy to navigate is essential. 



### User stories 

- As a student, I want to be able to login to my account securely, so I can browse all of the projects and start giving feeedbacks.
- As a student, I want to be able to see all of my public repositories, so I can easily choose what want to share.
- As a student, I want to be able like or dislike a feedback, so I can rate a good or bad feedback.
- As a student, I want to be able to delete a post because I don't like the feedback I received.
- As a student, I want to be able to remove feedback, so that I can create a better one.

### Wireframing

To create a beatiful wireframe, I used a software called [Balsamiq](https://balsamiq.com/). To view the pdf format of the wireframe please click here. I have changed some parts of this wireframe depending on the Github API data received. 

## Features 

### Existing features
- __Authentication__ - Allows students to have access to their account securely by registering and logging in. 
- __Navigation__ - Allows students to navigate the project easily. For the landing page, the navigation items are located at the very top with the logo. When each of them are clicked, the window smoothly move towards that particular element with the right ID.

    When the user is authenticated, the navigation items are located at the very right side.
- __Document Sorting__ - Users have the ability to sort the list of projects depending on the amount of views, feedbacks and the posted date.
- __Github API__ - Student's repositories are fetched using the github username provided by the user. Example data extracted are repositorie's most dominant language, date last updated, and the url for the codes.
- __Contact Section__ - Using the SendGrid API I was able to implement simple code to send custom email to an email entered in the form. 
- __Like and Dislike__ - students have the ability to like or dislike a feedback. If they feel that the feedback have not given enough thought or effort they can dislike and if they think that it is good enough, they can give it a like.

### In the future
- I want to allow students to see the code straight away from the project itself, rathen than being redirected to Github.
- I want to give the students the ability to save a certain projects.
- I want to give the students to add online resources as a list or when they typed a link it would be highlighted and clickable.    

## Technologies used

### Language stack

- Python
- HTML
- JavaScript
- CSS (SASS)

### Libraries used
- __[SASS](https://sass-lang.com/)__ - It is my favourite library as it allows me to split my CSS as much as I want. It allows me to create multiple files to locate codes easily. 
- __[Feather Icons](https://feathericons.com/)__ - It is a free icon library that you can instantly implement by using few codes. I use feather because the icons are really simple but has an elegant look.
- __[Pymongo](https://api.mongodb.com/python/current/)__ - Allows me to use Mongo with Python.
- __[Jinja](https://jinja.palletsprojects.com/en/2.11.x/)__ - It is a HTML templating language used with Flask. I use this library for me to loop through lists and reuse too much codes such as the header and the footer.

### Framework
- __[Flask](https://flask.palletsprojects.com/en/1.1.x/)__ - It is a micro framework to provide web service with Python. I used this framework because my application is really small and this allows me to create a development environment start coding instantly.
### Other tools
- __[Github](https://github.com/)__ - It is one of the top version control sytems available. I mainly use it in order or me to have a full control of my codes.

## Database structure
User model
```javascript
{
    _id: ObjectID(String),
    user_name: String,
    email: String,
    first_name: String,
    last_name: String,   
    password: Binary(String), // hashed using bcrypt
    git_username: String,
    registered: Date
}
```
Post model
```javascript
{
    _id: Number, // Id of repository
    name: String, // Name of the repository
    _user: String, // refers to the unique user_name
    stack_labels: [String] // languages used
    stack_value: [Number] // percentage of each language
    description: String,
    updated_at: Date
    homepage: String // site url    
    html_url: String // repository url
    language: String // most dominant language
    feedbacks: [String] // Feedback IDs
    views: [String] // User IDs
    posted_at: Date
}
```
Feedback model
```javascript
{
    _id: ObjectID(String)
    feedback: [Object] // Advice for each language
    post_name: String // reference to the posts / name of the repository
    post_id: Number // Post ID
    _user: String, // // feedback owner
    _username: String, // post owner,
    posted_at: Date,
    like: [String], // IDs array
    dislike: [String], // IDs array
}

```
## Testing


