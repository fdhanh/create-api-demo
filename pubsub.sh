#create a topic
gcloud pubsub topics create api-gatekeeper

#create a subscription
gcloud pubsub subscriptions create sub-1 --topic=api-gatekeeper

#create a dataset to load the data
bq --location=US mk dataset WEEK4