# Envoke Distribution
My current workplace uses Envoke to send out e-mails to interested parties. We recently decided to use Envoke to send out surveys for a newly launched tool. I was taksed with writing a script using the Envoke API to do so. 

## Business Need 
- Retrieval of emails belonging to individuals who have used said tool in the past week.
- De-duplication of the list of e-mails, as one person can make multiple submissions.
- Sending customized e-mail to each user.
- Logging the users who received an e-mail.

## Deployment 
This script is part of an Azure Synapse pipeline set to run weekly, on Mondays. 

## Sendout Logic 
The form data goes directly into our Data Warehouse, and can be queried using Spark notebooks that connect directly to the SQL pool. Every monday, a short procedure is run, collecting the e-mails of all form users from the past Monday - Sunday. 
This procedure produces the output file used by my script.

The envoke script contains the functions used in this procedure: 
- `create_contact_dicts`: turn a dataframe of contacts into a dict for API interactions.
- `upsert_contact`: Upserting checks if an email is registered in our database. If True, it returns the contact information. If false, the email is used to create a new contact, based on contact information. 
- `send_survey`: Sending out the survey for the registered contact, using customized html content created by a UX designer.


The sendout script simply compiles the functions + fetches the email content.

## Output 
Success message for each e-mail sent. 
