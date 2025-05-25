- DONE Create Virtual Environment and Install Django Package

- DONE Change Time Zone [IST]

- DONE Welcome Pages and Templates
    - DONE Create App for [accounts management; featured app]
    - DONE Views
        - DONE Create Base Template 
        - DONE Create Front Page
        - DONE Create About Page

- DONE User Authentication
    - DONE Register
    - DONE Login
    - DONE Logout
    - DONE Google Authentication

- User Profile
    - DONE View Page
        - DONE Display Information
    - Edit Info Form
    - Delete Account Form

- DONE Dashboard App
    - DONE Views page for Dashboard
    - DONE Show Number [total contacts; total documents; total tasks(pending && completed);]
    - DONE Search Input
    - DONE Upcomming Tasks
    - DONE Previous Activities

- REJECTED Leads App
    - DONE Database Model
    - Views pages for leads
        - List of leads
        - Detailed view page of leads
    - Form for creation of leads
    - Form for updation of leads
    - Deletion of leads 
    - Move to Trash for deleted Leads

- DONE Contacts App
    - Project (store client based on project)
        - DONE DataBase Model
        - DONE Create Signal to trigger and create a -> [default project]
        - DONE Creation From for Project
        - DONE A Pop-up window views for creating new project
        - REMOVED Edit Form for Project
        - DONE Deletion Form for Project

    - DONE Client (store the contact info)
        - DONE Database Model
        - DONE link with Project Model
        - DONE Views pages for [contact page]
            - DONE List of Client
            - DONE Detailed View of each Client (their details)
        - DONE Creation form for Client
        - DONE Detailed View for Client
        - DONE Edit form for Client
        - DONE Deletion form for Client

- DONE Documents App
    - DONE create model [document_name; file; related_to; description;]
    - DONE Views pages for documents
        - DONE List of documents
        - DONE Detailed View page for each Document
    - DONE Form for creation of documents
    - DONE Form for updation of documents
    - DONE Deletion for documents 
    - DONE Move to Trash for deleted Documents

- DONE Tasks App
    - DONE Create Database Model(   
        task_name; 
        description; 
        status[New; In-Progress; Completed]; 
        Priority[Normal; Urgent; Low; ]; 
        Owner[me; share_access; ]; 
        Type[Call; Whatsappp; Gmail; Other; ]; 
        related_to;
        Due_date;
        Due_time;
    )
    - DONE Views page
        - DONE List of Tasks
        - DONE Task Detail
    - DONE Form for creating new Tasks
    - DONE Deletion of Tasks
    - DONE Edit Tasks

- Implement Solution for Teams

- DONE Track Activities

- Seach Bar
    - DONE Main Page
    - Specific to Contacts
    - Specific to Docuements
    - Specific to Tasks

- Connecting Multiple User

    - DONE Roles Model [contact_read; contact_write; contact_edit; contact_delete; contact_delete_permanenet;]

    - DONE AccessPermission Model 
        - DONE Owner [who is sharing;]
        - DONE Shared_with [who is accessing;]
        - DONE role [from Role Model]

    - DONE Form for Roles
        - DONE Creating New Role
        - BYPASS Updating Existing Role

    - DONE Form for AccessPermission Model
        - DONE Creating New AccessPermission
        - BYPASS Update Exiting AccessPermission

    - DONE Deletion of Roles

    - DONE Deletion of AccessPermission

    - DONE Building User Management UI 
        - DONE Manage User Views
            - DONE Form to invite / grant access to another user
                - DONE INPUT: Email + Role
                - DONE ON SUBMIT: create AccessPermission record
    
    - DONE Switch Accounts
        - DONE DEFAULT: My Account
        - DONE OPTIONS: Other BusinessUser
        - DONE Update request.session (Add Session Key)
    
    - DONE Fallback to the logged-in usre's ID if session key is missing or invalid

    - DONE Update Contact Queries
        - DONE Load Contact owned by current user
        - DONE load shared contacts via AccessPermission [filter based on allowed access]

    - DONE Restrict Actions Based on Role
        - DONE check the permission before performing any action
    
    - Add Email Notification Flow
        - Send Email to other user
        - Accept / Reject the invitation
        - Only activate AccessPermission is accepted
    

- DONE Implement Trash
    - DONE Add BaseModel[is_deleted; deleted_at;]
        - DONE add [soft_delete; restore] method
    - DONE Inherit this BaseModel all Models
    - DONE Add querySet filter field to CustomManager
    - DONE add [objects; all_objects] to your models
    - DONE Update your Deletion Form for all objects
    - DONE Implement [Delete; Restore;] to your Trash View List

- Forget Password
    - INPUT: Email
    - Check if the email exist
    - Forward Email
    - ...

- Account SideBar
    - Includes: [Switch Account; Logout; Appearance; Settings; Help; Send Feedback]

    - Scrollable (part below account info section)

    - ONGOING Switch Account
        - Further clickable window
        - Back button send to Account Sidebar
        - List View 
            - My Account
            - Others
        - Sign Out button
     
    - DONE Logout

    - Appearance
        - DONE Layout For Theme Selector
            - DONE Clickable div
            - DONE Tick mark (for active theme)
        - DONE Back button to Account Sidebar
        - DONE Click outside to close everything
        - DONE Options
            - DONE Default: System
            - DONE Dark Theme
            - DONE Light Theme
        
        - DONE CSS Change
            - DONE Add class theme-dark
            - DONE Add Variables
        
        - DONE JS Theme Handler
            - DONE localStorage
            - DONE class = "theme-dark" (through variables)
    
    - Settings
        - Delete Account
        - Data Export* (optional)
    
    - Send Feedback
        - New Window
        - Includes: [Describe everything; Capture Screenshot; Send Button(apply after the valid information is entered)]
        - Connect to crm-mail author

- Deploy
    - Get PythonAnywhere Subscription
    - Follow Django Deployment Procedure
    - Add Docker if valid
    - Add Apache License
    - ...