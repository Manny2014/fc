terraform {
  backend "gcs" {
    bucket                      = "bootstrap-us-central1"
    prefix                      = "tf/state/dev-gke"
    impersonate_service_account = "bootstrap-object-admin@bootstrap-9196.iam.gserviceaccount.com"
  }
}