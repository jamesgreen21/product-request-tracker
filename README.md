# Product Request Tracker

The Product Request Tracker is a Python Flask application used to track all new product requests and change product requests within a Supply Chain. This particular version is for Martin Brower UK Ltd, but can be adapted for other companies.

The wireframes are available within the "wireframe" folder of the code.

There is a user guide under Testing within this README that will walk you through the App and demonstrate the tests carried out.

#### Process Flow

Create New/Change Product Request >>> Create Actions >>> Action Approval >>> Completion and Output Form

### Actions

The Tracker is broken down into 4 Action Stages:

#### Health & Safety Impact

Used to evaluate H&S based on a Manual Handling Form that can be uploaded along with any comments. This can then be approved, rejected or more information requested by the H&S Officer/User along with their feedback.

#### Quality Impact

Used to evaluate Quality Assurance based on Pallet Visuals that can be uploaded along with comments. This looks at how the product will impact warehouse storage. The user will also need to input the current (if applicable) and proposed Pallet Configuration details.

This can then be approved, rejected or more information requested by the QA Team along with their feedback.

#### Scheduling Impact

Used to evaluate Scheduling Impact based on Cage Visuals that can be uploaded along with comments. This looks at how the product will impact deliveries in accordance with cage storage. The user will also need to input the current (if applicable) and proposed Cage Configuration details.

This can then be approved, rejected or more information requested by the Scheduling Team along with their feedback.

#### Restaurant Shelving Impact

Used to evaluate Restaurant Impact based on Shelf Visuals that can be uploaded along with comments. This looks at how the product will impact the restaurant storage. The user will also need to input the current (if applicable) and proposed Shelf Configuration details.

This can then be approved, rejected or more information requested by the Restaurant Team along with their feedback.

### Completion & Output Form

This is the final part of the process in completing the Request. The user can complete a Request only when all Actions have been signed off by approval or rejection. The Request can then be Approved or Rejected.

The App will carry out a check on the Actions when the user attempts to complete the Request, and prompt the user if the Outcome chose (e.g. Approved/Rejected) goes against the Actions, with the ability to force approve/reject the Request.

E.g. Request Approved, but Quality stage has been rejected.

The Output Form can be viewed at any point during the process, and will show the content of the Request for what has been completed, and show "No Detail" where sections are still outstanding.

Finally, the Request can be Archived once it has been completed.

## Installation

Use the requirements.txt file to install the App within a virtual environment (assumed "env"):

```bash
source env/bin/activate
pip install requirements.txt
```
Once the App has been set up, create the tables within the Tracker:

```bash
cd tracker
flask create_tables
```
## Deployment

In order to deploy on Heroku, ensure all installation requirements are in-place, create a  GitHub repo and a Heroku app. Connect the Heorku app to the GitHub repo and set to automatically deploy. 

Within Heroku-Resources, create a Heroku Postgres DB. In Settings, Config Vars, set the following:

```
DATABASE_URL = "The Postgres DB created in Heroku"
SECRET_KEY = "A desire secret key"
```
Finally, go into the Heroku Console and enter the following to create the DB tables:

```
flask create_tables
```

#### File Uploads

Please be aware that the App does not currently allow for file uploads. This will be made avaialble in a later release as AWS S3 is required in order to store said files.

## Compatibility

The following browsers have been tested for compatibility with this app:

- Google Chrome
- Firefox


## Testing

There are no automated tests for the Project currently, but the App has been tested using a number of scenarios

I have included an example below of how to use the tool and test for functionality:

The Navbar contains 6 links:

 - HOME – takes you to the HOME page which holds all live requests
 - NEW – Creates a new request and is only available to the Product Request Team users, unavailable for the other user types
 - ACTIONS – Shows all actions for Product Request Team users and related actions for the other user types
 - SUPPLIERS – Adding, Editing and Hiding Suppliers
 - ARCHIVE – takes you to the ARCHIVE page which holds all completed requests
 - AUTHENTICATION – Log-in, log-out and register users

### How to Guide

1.	Welcome to the PRODUCT REQUEST APP. Let’s start by creating a new user. Click LOGIN/REGISTER on the Navbar and select LOGIN
2.	Whoops, we need a user, so at the bottom, select to SIGN UP NOW
3.	Now create a new user, giving a username of your choice and select to be a member of the PRODUCT REQUEST TEAM
4.	You will be redirected to the LOGIN PAGE. Re-enter your details 
5.	Right, let’s add a new Request. Go to NEW on the Navbar
6.	Enter the following information: 

| INPUT FIELDS | VALUES |
|  ---  |  ---  |
| GENERAL INFORMATION SECTION|
|Request Title|McCain Fries Proposal|
|Details|A change request to the case size to improve efficiency|
|Contact|Joe Bloggs|
|Supplier|McCain|
|PRODUCT INFORMATION SECTION|
|Number	|20011|
|Name	|Fries|
|Product Type	|Frz Side|
|New Product?	|No|
|EXISTING DETAILS|
|Length	|391|
|Width	|280|
|Height	|390|
|Weight	|15|
|Units Per Case	|15|
|Inners Per Case	|1|
|Can the case orientate?	|No|
|PROPOSED DETAILS|
|Length	|391|
|Width	|280|
|Height	|330|
|Weight	|15|
|Units Per Case	|15|
|Inners Per Case	|1|
|Can the case orientate?	|No|

7.	New Request added with confirmation message. Now we can add some ACTIONS for the other Teams to review.
Click ACTION on the request you just added and click ADD ACTION
8.	Use the following example: 

| INPUT FIELDS | VALUES |
|  ---  |  ---  |
| Stage | Health & Safety |
|Comments	|Change to pallet configuration to allow an addition case|
|File	|mccain_fries_pallet_visual.PNG|

Note: The "mccain_fries_pallet_visual.PNG" can be found in the repo within "tracker/static/testing/"

9.	Action added with confirmation message. Now let’s edit the action by clicking ACTION on the request and selecting ALL ACTIONS. This will take you to the ACTIONS PAGE and display all related actions on that Request. 
10.	Click the action created. This will take you to the edit screen. Now append “Test” to the COMMENTS and SUBMIT
11.	Now let’s see all actions; go to the ACTION PAGE directly using the Navbar
12.	Select an action with either an APPROVED or REJECTED status and click FEEDBACK. This will bring up a window displaying the feedback for its status.
13.	You will see all actions held in the App. Use the TOGGLE BUTTON top right of the screen to filter complete actions
14.	Now let’s go to the SUPPLIER PAGE using the Navbar
15.	Here you will see all Suppliers available, along with the ability to HIDE or EDIT each. You can add a new supplier using the ADD SUPPLIER button, top right of the screen
16.	Let’s add a new Supplier called “McCain”
17.	Then let’s hide the Supplier “Arla”
18.	Finally, let’s change the name of “Cargil” to read “Cargil-Test”
19.	All changes will gain a confirmation message. Now go back to the HOME PAGE
20.	Click ACTION on the request you created and click MANAGE. This will allow the Product Request Team users to edit the Request
21.	Now change the Supplier dropdown to “McCain”. Notice that the changes made in the SUPPLIER PAGE are visible here. 
22.	Submit the change and now LOGOUT so we can LOGIN as a Health & Safety Team user*
23.	Use the credentials:

 - Username: HS_User
 - Password: Qwerty123

24.	Now you are logged in as a Health & Safety Team user, you will notice the Navbar has less options (no NEW link)
25.	Click on the ACTION button for the Request you created. Here you will also see a difference as this user has limited access.
26.	Now let’s approve the action we raised earlier – select GO TO ACTION. Alternatively, you can go to ACTIONS on the Navbar and filter the completed 
27.	Now select APPROVE and type in comments “Test”. Then SUBMIT
28.	You will be taken back to the ACTIONS PAGE with a confirmation message. Go to the HOME PAGE and you will see the Request action traffic light has changed to Green
29.	Now let’s change the action to REJECTED, using the same process and check the traffic light changes to Red.
30.	Now that’s done, let’s LOGOUT and LOGIN as your original user
31.	Click the ACTION button of your Request and select COMPLETE followed by APPROVE
32.	Whoops, the Request is not ready to complete as there are still outstanding actions
33.	So let’s try and complete another Request. Try the same steps on the “Cargil Chicken Nugget” Request and APPROVE
34.	You will receive a confirmation message and the Request image will change to a TICK to confirm it’s approved.
35.	Finally, let’s move it into Archives by clicking the ACTION button followed by ARCHIVE
36.	Another confirmation message, then go to the ARCHIVES PAGE using the Navbar to check.
37.	You can choose to move it back into the HOME PAGE if required
38.	Lastly, let’s check the OUTPUT FORM for the “Cargil Chicken Nugget” Request. This can be done if in the HOME PAGE or ARCHIVE PAGE
39.	This will take you into the OUTPUT FORM used to send to the Supplier once the process is complete, giving the feedback of everything that occurd
40.	Hope you enjoyed the example!

* Other users for testing all stages:

 - Username: QA_User
 - Password: Qwerty123
 - Username: CF_User
 - Password: Qwerty123
 - Username: RI_User
 - Password: Qwerty123
  
 ## Acknowledgments

Along with the Flask framework, the following:

* [Materialize CSS](https://https://materializecss.com/) - The web framework used
* [jQuery](https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js) - Used to handle JS functions
* [Flask](http://flask.palletsprojects.com/en/1.1.x/) - The backend framework used
* [Heroku Postgres](https://dashboard.heroku.com/) - The database used

## License

There are currently no licensing on this application
