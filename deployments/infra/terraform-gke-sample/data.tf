data "terraform_remote_state" "bootstrap" {
  backend = "local"
  config = {
    path = "../00-terrfrom-gcp-bootstrap/terraform.tfstate"
  }
}

data "terraform_remote_state" "org" {
  backend = "gcs"
  config = {
    bucket                      = "bootstrap-us-central1"
    prefix                      = "tf/state/gcp-org"
    impersonate_service_account = "${data.terraform_remote_state.bootstrap.outputs.bootstrap_bucket_object_viewer_sa.email}"
  }
}

data "terraform_remote_state" "host_project" {
  backend = "gcs"
  config = {
    bucket                      = "bootstrap-us-central1"
    prefix                      = "tf/state/gcp-host-project"
    impersonate_service_account = "${data.terraform_remote_state.bootstrap.outputs.bootstrap_bucket_object_viewer_sa.email}"
  }
}

data "terraform_remote_state" "dev_project" {
  backend = "gcs"
  config = {
    bucket                      = "bootstrap-us-central1"
    prefix                      = "tf/state/dev-project"
    impersonate_service_account = "${data.terraform_remote_state.bootstrap.outputs.bootstrap_bucket_object_viewer_sa.email}"
  }
}
