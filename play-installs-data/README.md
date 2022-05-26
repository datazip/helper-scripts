# play-installs-data-extractor
Purpose of this script is to extract installs data from Google play to a GCS bucket concatinating into a single csv (for each type eg. overview.csv, os_version.csv, ...)

We first download all the files from private play store bucket which stores all the files in month wise format & then convert them to utf-8 format & combine and push it to our owned bucket in gcs


**Script requires three parameters :**

1. -b, --bucket_name

    --> Bucket name from where we have to fetch apps data

    --> Get this from Play-console > Download reports > Statistics > Copy Cloud Storage URI. (Only copy the gcs bucket name)


2. -t, --target_bucket_name

    --> Target bucket name where we have to store the combined files

    --> you can name any existing bucket or create a new one in GCS


3. -g, --gc_service_json_path


    --> Path of google service credential json file obtained from service account which has google cloud storage admin permission

    --> Go to Google cloud console > IAM & Admin > Service Account > Create service account > (grant cloud storage admin permission) > Click that service account > Keys > ADD KEY > JSON.




**IMPORTANT -- Granting permission for service account to access play data :**

1. After creating service account mentioned in point 3 above, copy email (details of service account has it)

2. Go to play console > Users & permissions > Invite new users > paste mail id

3. Add relevant app & give default permission (View app information (read-only))

4. Go to account permissions tab on the same page (View app information and download bulk reports (read-only)) & Give this permission.

5. Save the invite request & wait for 24 hours at least for this request to get accepted.




**How to run above script & get data imported in Datazip :**

1. Add the command to cron job and set period to 1 day.

2. Add source as File in Jitsu with type as CSV & source as GCS.

3. Use the same service account json as security credential.

4. This will import updated data everyday.
