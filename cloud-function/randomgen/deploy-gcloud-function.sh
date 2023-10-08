gcloud functions deploy randomgen-function \
--gen2 \
--runtime python39 \
--region=us-central1 \
--entry-point=randomgen \
--trigger-http \
--allow-unauthenticated
