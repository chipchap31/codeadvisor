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
- As a visitor, I want to be able to register so that I can become a student.
- As a student, I want to be able to login to my account securely, so I can browse all of the projects and start giving feeedbacks.
- As a student, I want to be able to see all of my public repositories, so I can easily choose what want to share.
- As a student, I want to be ables to add a post, so that I can get a feedback improve my coding skills.
- As a student, I want to be able to add a feedback, so that I can share some comments on each languages.
- As a student, I want to be able like or dislike a feedback, so I can rate a good or bad feedback.
- As a student, I want to be able to delete a post because I don't like the feedback I received.
- As a student, I want to be able to remove feedback, so that I can create a better one.
- As a student, I want to be able to edit my feedback so that I can improve it.

### Wireframing

To create a beatiful wireframe, I used a software called [Balsamiq](https://balsamiq.com/). To view the pdf format of the wireframe please click here. I have changed some parts of this wireframe depending on the Github API data received. 

In order to see the wireframes click [here](https://github.com/chipchap31/codeadvisor/blob/master/wireframes/ms3.pdf)
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
- I will get students to validate their email.
- I will give the students the ability to recover their password via random code, possibly a string of random letters or numbers.

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
- __[ChartJS](https://www.chartjs.org/)__ - Chart js is an open source library to create elegant charts. For this project, I used it to show the consistency of the repository in percentage.
### Framework
- __[Flask](https://flask.palletsprojects.com/en/1.1.x/)__ - It is a micro framework to provide web service with Python. I used this framework because my application is really small and this allows me to create a development environment start coding instantly.
### Other tools
- __[Github](https://github.com/)__ - It is one of the top version control sytems available. I mainly use it in order or me to have a full control of my codes.
- __[VS Code](https://code.visualstudio.com/)__ - It is open source code editor. I really like using VS code, because it is free and supports Git.


## Database structure
__User model__
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
__Post model__
```javascript
{
    _id: Number, // Id of repository
    name: String, // Name of the repository
    _user: String, // refers to the unique user_name
    stack_labels: [String], // languages used
    stack_value: [Number], // percentage of each language
    description: String,
    updated_at: Date,
    homepage: String, // site url    
    html_url: String, // repository url
    language: String, // most dominant language
    feedbacks: [String], // Feedback IDs
    views: [String], // User IDs
    posted_at: Date,
}
```
__Feedback model__
```javascript
{
    _id: ObjectID(String),
    feedback: [Object], // Advice for each language
    post_name: String, // reference to the posts / name of the repository
    post_id: Number, // Post ID
    _user: String, // // feedback owner
    _username: String, // post owner,
    posted_at: Date,
    like: [String], // IDs array
    dislike: [String], // IDs array
}

```
## Testing

For testin, the first thing that I do is make sure that there are no silly mistake like unclosed tags, missing attributes or syntax errors. This can be done using validators for each languages.

- __[WC3 validator ](https://validator.w3.org/)__ - I used this web application to validate my HTML files. During the process I came upon two major errors. The first one was in landing page, I made a mistake of placing the script tag outside the body tag. 

    The second major issue is a duplicate ID. When I copy the nav bar on my project, I didn't realize that I also made a copy of the drop-down content of the sticky nav. As a result the un-ordered list of main nav is the same as the sticky nav.

- __[jigsaw.w3.org/css-validator](https://jigsaw.w3.org/css-validator/)__ - For the CSS files, I didn't expect any errors because I used a library which is called [SASS](https://sass-lang.com/). The reason behind this is because SASS does not compile if there are any errors. This also one of the advantage of using SASS. 

- __[pep8online](http://pep8online.com/)__ - It is online validator for python codes. I checked every python codes and there were no major errors.

The second part of testing is to go over the user stories and to make sure that they actually work. 

> As a visitor, I want to be able to register so that I can become a student.

1. When the register link from the nav bar is clicked, the page is redirected from the landing page to register page.
1. The required fields shows a warning if the input is empty.
1. Shows an error if the email or username already exist in the database.
1. Password requires to match and contain more than 10 characters. Both requirements fine. During the testing session for this functionality, I see that the password field renders the string "False" when theres no error. The simple fix is to add a code that check if there is an error just for password.
1. After passing all of the requirements, the page is successfully renders a message that registration is completed.

> As a student, I want to be able to login to my account securely, so I can browse all of the projects and start giving feeedbacks.

1. The login link at the nav bar works perfectly.
1. Submiting an empty fields does not work as the page displays a warning.
1. When an unregistered username is entered an error message is rendered.
1. When a registered username is entered but the password is wrong, an error is also successfully rendered.

> As a student, I want to be able to see all of my public repositories, so I can easily choose what want to share.

1. When there is no project posted a link to the project is displayed so that the student can be swiftly redirected to project page and see the list of public repositories.
2. The Github api is properly set up and the request returns the user's repository data successfully.

> As a student, I want to be ables to add a post, so that I can get a feedback improve my coding skills.

1. The link for the project list is visible and the page loads the project list when clicked.
1. The repositories are shown.
1. When the post buttons are pressed on the projects page, the page is automatically redirected to posts page. The project posted is then added at the very top. 

> As a student, I want to be able to add a feedback, so that I can share some comments on each languages.

1. The input and textarea field are very clear and easy to find the students.
1. The expand button shows the rest of the fields .
1. If student tries to submit without choosing a rate for all languages, it does not work.
1. If the students picks a rate for each languages the feedback is submitted and the page redirects to itself.

> As a student, I want to be able like or dislike a feedback, so I can rate a good or bad feedback.

1. To be able to like or dislike, there should be a feedback that exist to that particular post. 
1. When the like button is pressed it turns green which means it is selected and when you refresh the page the like button is still green which means the user id of user is successfully added to like array.
1. The same testing process for disliking the feedback. Refer to step 2. 
1. If the like or dislike is already selected and it is click again the corresponding button is deselected.

> As a student, I want to be able to delete a post.

1. In order to delete a post, student must go to the post page to see their own posts.
1. When the more button in every post is click, the dropdown shows the delete option.
1. When the delete is click a modal shows right in the middle of the window.
1. The modal shows the option of delete or cancel clearly.
1. If the cancel button is clicked, the modal closes.
1. The page then refreshes when the delete button is pressed and the post is deleted.

> As a student, I want to be able to remove feedback, so that I can create a better one.

1. To be able to delete a feedback, the ID of user of created the feedback must be the same as the current user.
1. I created a feedback from two different accounts and it works as I can't delete the other feedback.
1. When I pressed the delete button it refreshes the same page and the feedback is gone.

    During this part I came accross a bug where the icon to delete a feedback renders even though the current ID of the user does not match the creator of the feedback.

> As a student, I want to be able to edit my feedback so that I can improve it.
1. The dropdown button the shows the edit button in feedback works when hovered.
1. The edit button works when clicked.
1. The page is redirected with the id of feedback.
1. The previous feedback are successfully shown and can be edited.
1. When the submit button is pressed, the page is redirected to the right page with the changes.

## Mobile responsiveness

To check for websites responsiveness I used a website called [responsinator](http://www.responsinator.com/). 

Below are the list of devices:
- iPhone X portrait · width: 375px
- iPhone X landscape · width: 734px 
- Android (Pixel 2) portrait · width: 412px
- Android (Pixel 2) landscape · width: 684px
- iPhone 6-8 portrait · width: 375px
- iPhone 6-8 landscape · width: 667px
- iPhone 6-8 Plump portrait · width: 414px
- iPhone 6-8 Plump landscape · width: 736px
- iPad portrait · width: 768px
- iPad landscape · width: 1024px

The project response very well to these list of devices.

## User testing
The feedback collected is all from the #peer-code-review channel.
- The project has the functionality to edit the feedback. The solution is to edit option with the delete option and redirect the user to a another page with the feedback id.

- The same person also pointed out that the footer is not fixed to the bottom when there are not much content. The fix would be to add a class with a fixed position and a set the the bottom style to zero.

- A student pointed out to me that the owner of the project should not be able to add a feedback. She is absolutely right but I this functionality is essential as there are not much users yet.

## Deployment

To run this project you must have the following: 

- [Git](https://git-scm.com/)
- A [MongoDB](https://www.mongodb.com/) account
- [python3](https://www.python.org/) 
- [PIP](https://pip.pypa.io/en/stable/)
- Sendgrid api key

### Local deployment
1. Clone the repository in Github
```
$ git clone https://github.com/chipchap31/codeadvisor.git
```
2. Open terminal and go to '/codeadvisor' directory and install dependencies.

```
$ pip3 install requirements.txt
```

3. Set up the environment variables on your .bash_profile.
```
$ sudo nano .bash_profile
```
4. Add the variables.
```
MONGO_URI="mongodb+srv://<USERNAME>:<PASSWORD>@cluster0-bxxlw.mongodb.n$
SENDGRID_KEY="<SENDGRID API KEY>"
GIT_TOKEN="<GIT TOKEN FROM GITHUB>"

export GIT_TOKEN
export SENDGRID_KEY
export MONGO_URI
```
5. Run the application.
```
$ python3 app.py
```

## Heroku deployment
1. Save all of the dependencies.
```

```
1. Create a procfile.
```
$ echo web: python3 > Procfile
```
1. Make sure that you have Heroku installed on your system. This can be simply done by checking the version.
```
$ heroku --version

-> heroku/7.39.0 darwin-x64 node-v12.13.0
```

1. Assuming you have it installed already, create a new app.
```
$ heroku create <name of app>
```
1. While in the root directory of the app. Commit the project.
```

$ git init 
$ git remote -a <name of app>
$ git add .
$ git commit -m "<commit message>"

```
1. Set the environment variables on your Heroku settings.

```
MONGO_URI="mongodb+srv://<USERNAME>:<PASSWORD>@cluster0-bxxlw.mongodb.n$
SENDGRID_KEY="<SENDGRID API KEY>"
GIT_TOKEN="<GIT TOKEN FROM GITHUB>"
IP="0.0.0.0"
PORT="5000"
```
## Credits

### Content

- Some of content of the reset.sass was taken from [Eric Meyer Reset 2.0 SASS](https://gist.github.com/joshvermaire/1102033)

### Media
- The image at the landing page was downloaded from [freepik.com](https://www.freepik.com/)